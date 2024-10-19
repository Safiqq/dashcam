import cv2
import mediapipe as mp
import numpy as np

class EyeTrackingMetrics:
    def __init__(self, fps):
        self.fps = fps
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.01,
            min_tracking_confidence=0.01
        )
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

    def preprocess_video(self, video_path, progress_callback):
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        blink_data = []
        saccade_data = []
        closed_times = []
        
        last_eye_state = "open"
        last_relative_iris_position = None
        blink_start_time = None
        closing_start_time = None
        
        for frame_num in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_num / fps
            results = self.process_frame(frame)

            if results.multi_face_landmarks:
                landmarks = np.array([(lm.x, lm.y) for lm in results.multi_face_landmarks[0].landmark])
                left_eye = landmarks[self.LEFT_EYE]
                right_eye = landmarks[self.RIGHT_EYE]
                left_iris = landmarks[self.LEFT_IRIS]
                right_iris = landmarks[self.RIGHT_IRIS]
                
                eyes_closed = self.is_eye_closed(left_eye) or self.is_eye_closed(right_eye)
                
                # Blink detection
                if eyes_closed and last_eye_state == "open":
                    closing_start_time = timestamp
                    blink_data.append(("closing", timestamp))
                    last_eye_state = "closing"
                elif eyes_closed and last_eye_state == "closing":
                    closing_duration = timestamp - closing_start_time
                    blink_data.append(("closed", timestamp, closing_duration))
                    last_eye_state = "closed"
                elif not eyes_closed and last_eye_state in ["closing", "closed"]:
                    closed_duration = timestamp - closing_start_time - closing_duration
                    blink_data.append(("reopening", timestamp, closed_duration))
                    last_eye_state = "reopening"
                elif not eyes_closed and last_eye_state == "reopening":
                    reopening_duration = timestamp - closing_start_time - closing_duration - closed_duration
                    blink_duration = timestamp - closing_start_time
                    blink_data.append(("complete", timestamp, blink_duration, reopening_duration))
                    last_eye_state = "open"
                
                # Closed time for PERCLOS
                closed_times.append((timestamp, 1 / fps) if eyes_closed else (timestamp, 0))
                
                # Saccade detection
                current_relative_iris_position = self.calculate_relative_iris_position(left_eye, left_iris, right_eye, right_iris)
                
                if last_relative_iris_position is not None:
                    movement = abs(current_relative_iris_position - last_relative_iris_position)
                    if movement > 0.01:
                        saccade_data.append(("saccade", timestamp))
                    else:
                        saccade_data.append(("no_saccade", timestamp))
                
                last_relative_iris_position = current_relative_iris_position
            
            progress_callback(int((frame_num + 1) / total_frames * 100))
        
        cap.release()
        return self.calculate_metrics(blink_data, saccade_data, closed_times, fps)

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.face_mesh.process(frame_rgb)

    def is_eye_closed(self, eye_landmarks, threshold=0.396):
        ear = self.calculate_eye_aspect_ratio(eye_landmarks)
        return ear < threshold

    def calculate_eye_aspect_ratio(self, eye_landmarks):
        vertical_1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        vertical_2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        horizontal = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        return (vertical_1 + vertical_2) / (2.0 * horizontal)

    def calculate_relative_iris_position(self, left_eye, left_iris, right_eye, right_iris):
        # Calculate the relative position of the iris for both eyes
        left_eye_center = np.mean(left_eye[:, 0])
        right_eye_center = np.mean(right_eye[:, 0])
        left_iris_center = np.mean(left_iris[:, 0])
        right_iris_center = np.mean(right_iris[:, 0])
        
        left_relative_position = (left_iris_center - left_eye_center) / (np.max(left_eye[:, 0]) - np.min(left_eye[:, 0]))
        right_relative_position = (right_iris_center - right_eye_center) / (np.max(right_eye[:, 0]) - np.min(right_eye[:, 0]))
        
        # Return the average relative position of both irises
        return (left_relative_position + right_relative_position) / 2

    def calculate_metrics(self, blink_data, saccade_data, closed_times, fps):
        metrics = []
        for minute in range(int(closed_times[-1][0] / 60) + 1):
            start_time = minute * 60
            end_time = (minute + 1) * 60
            
            recent_blinks = [b for b in blink_data if start_time <= b[1] < end_time]
            recent_saccades = [s for s in saccade_data if start_time <= s[1] < end_time]
            recent_closed_times = [c for c in closed_times if start_time <= c[0] < end_time]
            
            closing_frequency = sum(1 for b in recent_blinks if b[0] == "closed")
            if closing_frequency > 0: closing_duration = sum(b[2] for b in recent_blinks if b[0] == "closed") / closing_frequency
            else: closing_duration = 0.00
            
            closed_frequency = sum(1 for b in recent_blinks if b[0] == "reopening")
            if closed_frequency > 0: closed_duration = sum(b[2] for b in recent_blinks if b[0] == "reopening") / closed_frequency
            else: closed_duration = 0.00
            
            reopening_frequency = sum(1 for b in recent_blinks if b[0] == "complete")
            if reopening_frequency > 0: reopening_duration = sum(b[3] for b in recent_blinks if b[0] == "complete") / reopening_frequency
            else: reopening_duration = 0.00

            blink_frequency = sum(1 for b in recent_blinks if b[0] == "complete")
            if blink_frequency > 0: blink_duration = sum(b[2] for b in recent_blinks if b[0] == "complete") / blink_frequency
            else: blink_duration = 0.00
                
            microsleep_frequency = sum(1 for b in recent_blinks if b[0] == "complete" and b[2] > 0.5)
            total_closed_time = sum(duration for _, duration in recent_closed_times)
            perclos = (total_closed_time / 60) * 100 if recent_closed_times else 0
            saccade_frequency = sum(1 for s in recent_saccades if s[0] == "saccade")
            saccade_mean = np.mean([1 if s[0] == "saccade" else 0 for s in recent_saccades]) if recent_saccades else 0
            
            metrics.append({
                "closing_duration": closing_duration,
                "closed_duration": closed_duration,
                "reopening_duration": reopening_duration,
                "blink_duration": blink_duration,
                "blink_frequency": blink_frequency,
                "microsleep_frequency": microsleep_frequency,
                "perclos": perclos,
                "saccade_frequency": saccade_frequency,
                "saccade_mean": saccade_mean,
                "timestamp": end_time
            })
        
        return metrics