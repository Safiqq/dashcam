import math

def check_non_conflict(event):
    # TODO
    # v.vehicle speed 80 <= x <= 100
    # accel.y < 0.4
    # jarak = 65.54

    if (80 <= event['v_subject'] <= 100) and (event['accel_y'] < 0.1) and (event['distance'] == 65.54):
        return True

    return False

def check_proximity_conflict(event):
    # v.vehicle speed 80 <= x <= 140
    # accel.y > 0.4
    # jarak = 65.54
    
    if (80 <= event['v_subject'] <= 100) and (0.1 <= event['accel_y'] <= 0.2) and (event['distance'] == 65.54):
        return True

    return False

def check_crash_relevant_conflict(event):
    # v.vehicle speed 80 <= x <= 100
    # accel.y > 0.4
    # jarak 30 < x < 65.54

    if (80 <= event['v_subject'] <= 100) and (0.2 < event['accel_y'] <= 0.4) and (30 < event['distance'] < 65.54):
        return True

    return False

def check_near_crash(event):
    # v.vehicle speed 80 <= x <= 140
    # accel.y > 0.4
    # jarak <= 30
    # gyro.x >= 2
    
    if (80 <= event['v_subject'] <= 140) and (event['accel_y'] > 0.4) and (event['distance'] <= 30) and (event['gyro_x'] >= 2):
        return True

    return False

def check_crash(event):
    # jarak <= 0
    
    if (event['distance'] <= 0):
        return True

    return False

def check_exists(check, events):
    for event in events:
        for i in check:
            if i in event:
                return True

    return False

def time_to_collision(event):
    # TTC (detik) = Jarak (m)/ kecepatan relatif (km/jam)
    # Kecepatan relatif = kecepatan leading vehicle- kecepatan subject vehicle
    
    if (event['distance'] >= 65.54):
        return math.nan
    
    v_relative = event['v_leading'] - event['v_subject']
    
    if (v_relative <= 0 or v_relative == math.nan):
        return math.nan
    
    return event['distance'] * 3.6 / v_relative

def distance_category(speed):
    # Jarak Minimal saja, karena Jarak Aman = Kecepatan
    if speed <= 60:
        return speed / 2
    else:
        return speed - 20
    
def speed_category(speed):
    if speed < 60:
        return "Under Speed"
    elif 60 <= speed <= 100:
        return "Medium Speed"
    else:
        return "Over Speed"
    