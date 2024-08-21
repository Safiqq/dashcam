from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys, io, folium, cv2
from scipy.spatial import distance
import dlib
import cv2
import numpy as np
from datetime import datetime, timedelta
import IO
import locale
import algorithm

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.setStyleSheet('''
                            * {
                                font-size: 18px;
                            }
                            ''')
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setStyleSheet('''
                                        #centralwidget {
                                            background-color: #BDBBBE;
                                        }
                                        ''')
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_left = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_left.setMaximumSize(QtCore.QSize(360, 16777215))
        self.frame_left.setStyleSheet('''
                                        #frame_left {
                                            background-color: #f9f9f9;
                                            border-radius: 4px;
                                        }
                                        ''')
        self.frame_left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_left.setObjectName("frame_left")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_left)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_data = QtWidgets.QFrame(parent=self.frame_left)
        self.frame_data.setMaximumSize(QtCore.QSize(16777215, 240))
        self.frame_data.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_data.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_data.setObjectName("frame_data")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_data)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_data_1 = QtWidgets.QFrame(parent=self.frame_data)
        self.frame_data_1.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_data_1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_data_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_data_1.setObjectName("frame_data_1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_data_1)
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textbox_data = QtWidgets.QPlainTextEdit(parent=self.frame_data_1)
        self.textbox_data.setReadOnly(True)
        self.textbox_data.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.textbox_data.setStyleSheet('''
                                        #textbox_data {
                                            padding: 8px 10px;
                                            border-radius: 4px;
                                            background: transparent;
                                            border: 1px solid #BDBBBE;
                                        }
                                        ''')
        self.textbox_data.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textbox_data.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textbox_data.setObjectName("textbox_data")
        self.textbox_data.setPlaceholderText("Choose Data (.csv)")
        
        self.horizontalLayout_2.addWidget(self.textbox_data)
        self.btn_data = QtWidgets.QPushButton(parent=self.frame_data_1)
        self.btn_data.setMinimumSize(QtCore.QSize(45, 45))
        self.btn_data.setStyleSheet('''
                                    #btn_data {
                                        border-radius:4px;
                                        border: 0.5px solid #BDBBBE;
                                    }
                                    
                                    #btn_data:hover{
                                        background-color: #D7D5D8;
                                    }
                                    ''')
        self.btn_data.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/folder_open.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_data.setIcon(icon)
        self.btn_data.setIconSize(QtCore.QSize(24, 24))
        self.btn_data.setObjectName("btn_data")
        self.btn_data.clicked.connect(self.open_data)
        
        self.horizontalLayout_2.addWidget(self.btn_data)
        self.verticalLayout_2.addWidget(self.frame_data_1)
        self.frame_data_2 = QtWidgets.QFrame(parent=self.frame_data)
        self.frame_data_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_data_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_data_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_data_2.setObjectName("frame_data_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_data_2)
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textbox_vid = QtWidgets.QPlainTextEdit(parent=self.frame_data_2)
        self.textbox_vid.setReadOnly(True)
        self.textbox_vid.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.textbox_vid.setStyleSheet('''
                                        #textbox_vid {
                                            padding: 8px 10px;
                                            border-radius: 4px;
                                            background: transparent;
                                            border: 1px solid #BDBBBE;
                                        }
                                        ''')
        self.textbox_vid.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textbox_vid.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textbox_vid.setObjectName("textbox_vid")
        self.textbox_vid.setPlaceholderText("Choose Front Video")
        
        self.horizontalLayout_3.addWidget(self.textbox_vid)
        self.btn_vid = QtWidgets.QPushButton(parent=self.frame_data_2)
        self.btn_vid.setMinimumSize(QtCore.QSize(45, 45))
        self.btn_vid.setStyleSheet('''
                                    #btn_vid {
                                        border-radius:4px;
                                        border: 0.5px solid #BDBBBE;
                                    }
                                    
                                    #btn_vid:hover{
                                        background-color: #D7D5D8;
                                    }
                                    ''')
        self.btn_vid.setText("")
        self.btn_vid.setIcon(icon)
        self.btn_vid.setIconSize(QtCore.QSize(24, 24))
        self.btn_vid.setObjectName("btn_vid")
        self.btn_vid.clicked.connect(self.open_vid)
        
        self.horizontalLayout_3.addWidget(self.btn_vid)
        self.verticalLayout_2.addWidget(self.frame_data_2)
        
        self.frame_data_3 = QtWidgets.QFrame(parent=self.frame_data)
        self.frame_data_3.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_data_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_data_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_data_3.setObjectName("frame_data_3")
        self.horizontalLayout_extend = QtWidgets.QHBoxLayout(self.frame_data_3)
        self.horizontalLayout_extend.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_extend.setObjectName("horizontalLayout_extend")
        self.textbox_vid_2 = QtWidgets.QPlainTextEdit(parent=self.frame_data_3)
        self.textbox_vid_2.setReadOnly(True)
        self.textbox_vid_2.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.textbox_vid_2.setStyleSheet('''
                                        #textbox_vid_2 {
                                            padding: 8px 10px;
                                            border-radius: 4px;
                                            background: transparent;
                                            border: 1px solid #BDBBBE;
                                        }
                                        ''')
        self.textbox_vid_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textbox_vid_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textbox_vid_2.setObjectName("textbox_vid_2")
        self.textbox_vid_2.setPlaceholderText("Choose Rear Video")
        
        self.horizontalLayout_extend.addWidget(self.textbox_vid_2)
        self.btn_vid_2 = QtWidgets.QPushButton(parent=self.frame_data_3)
        self.btn_vid_2.setMinimumSize(QtCore.QSize(45, 45))
        self.btn_vid_2.setStyleSheet('''
                                    #btn_vid_2 {
                                        border-radius:4px;
                                        border: 0.5px solid #BDBBBE;
                                    }
                                    
                                    #btn_vid_2:hover{
                                        background-color: #D7D5D8;
                                    }
                                    ''')
        self.btn_vid_2.setText("")
        self.btn_vid_2.setIcon(icon)
        self.btn_vid_2.setIconSize(QtCore.QSize(24, 24))
        self.btn_vid_2.setObjectName("btn_vid_2")
        self.btn_vid_2.clicked.connect(self.open_vid_2)
        
        self.horizontalLayout_extend.addWidget(self.btn_vid_2)
        self.verticalLayout_2.addWidget(self.frame_data_3)
        
        self.frame_data_4 = QtWidgets.QFrame(parent=self.frame_data)
        self.frame_data_4.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_data_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_data_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_data_4.setObjectName("frame_data_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_data_4)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_submit = QtWidgets.QPushButton(parent=self.frame_data_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_submit.sizePolicy().hasHeightForWidth())
        self.btn_submit.setSizePolicy(sizePolicy)
        self.btn_submit.setStyleSheet('''
                                    #btn_submit {
                                        padding: 12px 0px;
                                        border-radius: 6px;
                                        background-color: #6A676E;
                                        color: #f9f9f9;
                                        font-weight: 600;
                                    }
                                    
                                    #btn_submit:hover {
                                        background-color: #514E55;
                                    }
                                    ''')
        self.btn_submit.setDefault(False)
        self.btn_submit.setFlat(False)
        self.btn_submit.setObjectName("btn_submit")
        self.btn_submit.setText("Submit")
        self.btn_submit.clicked.connect(self.submit)
        
        self.horizontalLayout_4.addWidget(self.btn_submit)
        self.verticalLayout_2.addWidget(self.frame_data_4)
        self.verticalLayout.addWidget(self.frame_data)
        self.frame_list = QtWidgets.QFrame(parent=self.frame_left)
        self.frame_list.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_list.setStyleSheet('''
                                    #frame_list {
                                        border-top: 2px solid #BDBBBE;
                                    }
                                    ''')
        self.frame_list.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_list.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_list.setObjectName("frame_list")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_list)
        self.verticalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.frame_list)
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet('''
                                    #scrollArea {
                                        border: 0px;
                                    }
                                    ''')
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 332, 846))
        self.scrollAreaWidgetContents.setStyleSheet('''
                                                    #scrollAreaWidgetContents {
                                                        background-color: #f9f9f9;
                                                        border: 0px;
                                                    }
                                                    ''')
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_data = QtWidgets.QVBoxLayout()
        self.verticalLayout_data.setObjectName("verticalLayout_data")
        
        self.verticalLayout_7.addLayout(self.verticalLayout_data)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.frame_list)
        self.horizontalLayout.addWidget(self.frame_left)
        self.frame_mid = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_mid.setStyleSheet("")
        self.frame_mid.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mid.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_mid.setObjectName("frame_mid")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_mid)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_media = QtWidgets.QFrame(parent=self.frame_mid)
        self.frame_media.setMinimumSize(QtCore.QSize(0, 750))
        self.frame_media.setStyleSheet('''
                                        #frame_media {
                                            background-color: #f9f9f9;
                                            border-radius: 4px;
                                        }
                                        ''')
        self.frame_media.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_media.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_media.setObjectName("frame_media")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_media)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_vid = QtWidgets.QFrame(parent=self.frame_media)
        self.frame_vid.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_vid.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_vid.setObjectName("frame_vid")
        self.verticalLayout_9.addWidget(self.frame_vid)
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        btnSize = QtCore.QSize(16, 16)
        videoWidget = QVideoWidget()
        videoWidget2 = QVideoWidget()

        self.playButton = QtWidgets.QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(videoWidget2)

        self.frame_vid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        # self.mediaPlayer.durationChanged.connect(self.durationChanged)
        
        self.mediaPlayer2.setVideoOutput(videoWidget2)
        self.mediaPlayer2.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer2.positionChanged.connect(self.positionChanged)
        # self.mediaPlayer2.durationChanged.connect(self.durationChanged)
        
        self.frame_player = QtWidgets.QFrame(parent=self.frame_media)
        self.frame_player.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_player.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_player.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_player.setObjectName("frame_player")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_player)
        self.horizontalLayout_10.setContentsMargins(12, 0, 30, 0)
        self.horizontalLayout_10.setSpacing(18)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.btn_play = QtWidgets.QPushButton(parent=self.frame_player)
        self.btn_play.setEnabled(False)
        self.btn_play.setMaximumSize(QtCore.QSize(45, 45))
        self.btn_play.setStyleSheet("")
        self.btn_play.setText("")

        self.btn_play.setIcon(self.frame_player.style().standardIcon(
            QtWidgets.QStyle.StandardPixmap.SP_MediaPlay))
        self.btn_play.setIconSize(QtCore.QSize(40, 40))
        self.btn_play.setObjectName("btn_play")
        self.btn_play.clicked.connect(self.play)

        self.horizontalLayout_10.addWidget(self.btn_play)
        self.horizontalSlider = QtWidgets.QSlider(parent=self.frame_player)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(0, 36))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.sliderMoved.connect(self.setPosition)
        self.horizontalSlider.setEnabled(False)
        
        self.horizontalLayout_10.addWidget(self.horizontalSlider)
        self.verticalLayout_9.addWidget(self.frame_player)
        self.verticalLayout_6.addWidget(self.frame_media)
        self.frame_res = QtWidgets.QFrame(parent=self.frame_mid)
        self.frame_res.setStyleSheet('''
                                    #frame_res {
                                        background-color: #f9f9f9;
                                        border-radius: 4px;
                                    }
                                    ''')
        self.frame_res.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res.setObjectName("frame_res")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_res)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.frame_res_top = QtWidgets.QFrame(parent=self.frame_res)
        self.frame_res_top.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame_res_top.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_top.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_top.setObjectName("frame_res_top")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_res_top)
        self.horizontalLayout_13.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_res = QtWidgets.QLabel(parent=self.frame_res_top)
        self.label_res.setStyleSheet('''
                                    #label_res {
                                        font-weight: 600;
                                        font-size: 20px;
                                    }
                                    ''')
        self.label_res.setObjectName("label_res")
        self.label_res.setText("Result")
        
        self.horizontalLayout_13.addWidget(self.label_res)
        self.verticalLayout_13.addWidget(self.frame_res_top)
        self.frame_res_bot = QtWidgets.QFrame(parent=self.frame_res)
        self.frame_res_bot.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_bot.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_bot.setObjectName("frame_res_bot")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_res_bot)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.frame_res_1 = QtWidgets.QFrame(parent=self.frame_res_bot)
        self.frame_res_1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_1.setObjectName("frame_res_1")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_res_1)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.frame_res_total = QtWidgets.QFrame(parent=self.frame_res_1)
        self.frame_res_total.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_total.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_total.setObjectName("frame_res_total")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_res_total)
        self.horizontalLayout_15.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_total_1 = QtWidgets.QLabel(parent=self.frame_res_total)
        self.label_total_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_total_1.setObjectName("label_total_1")
        self.label_total_1.setText("Total Events")
        
        self.horizontalLayout_15.addWidget(self.label_total_1)
        self.label_total_2 = QtWidgets.QLabel(parent=self.frame_res_total)
        self.label_total_2.setStyleSheet('''
                                        #label_total_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_total_2.setObjectName("label_total_2")
        self.label_total_2.setText("0")
        
        self.horizontalLayout_15.addWidget(self.label_total_2)
        self.horizontalLayout_14.addWidget(self.frame_res_total)
        self.frame_res_speed = QtWidgets.QFrame(parent=self.frame_res_1)
        self.frame_res_speed.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_speed.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_speed.setObjectName("frame_res_speed")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_res_speed)
        self.horizontalLayout_16.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_crash_relevant_conflict_1 = QtWidgets.QLabel(parent=self.frame_res_speed)
        self.label_crash_relevant_conflict_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_crash_relevant_conflict_1.setObjectName("label_crash_relevant_conflict_1")
        self.label_crash_relevant_conflict_1.setText("Crash Relevant Conflict")
        
        self.horizontalLayout_16.addWidget(self.label_crash_relevant_conflict_1)
        self.label_crash_relevant_conflict_2 = QtWidgets.QLabel(parent=self.frame_res_speed)
        self.label_crash_relevant_conflict_2.setStyleSheet('''
                                            #label_crash_relevant_conflict_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_crash_relevant_conflict_2.setObjectName("label_crash_relevant_conflict_2")
        self.label_crash_relevant_conflict_2.setText("0")
        
        self.horizontalLayout_16.addWidget(self.label_crash_relevant_conflict_2)
        self.horizontalLayout_14.addWidget(self.frame_res_speed)
        self.verticalLayout_14.addWidget(self.frame_res_1)
        self.frame_res_2 = QtWidgets.QFrame(parent=self.frame_res_bot)
        self.frame_res_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_2.setObjectName("frame_res_2")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_res_2)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.frame = QtWidgets.QFrame(parent=self.frame_res_2)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_18.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_non_conflict_1 = QtWidgets.QLabel(parent=self.frame)
        self.label_non_conflict_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_non_conflict_1.setObjectName("label_non_conflict_1")
        self.label_non_conflict_1.setText("Non Concflict")
        
        self.horizontalLayout_18.addWidget(self.label_non_conflict_1)
        self.label_non_conflict_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_non_conflict_2.setStyleSheet('''
                                        #label_non_conflict_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_non_conflict_2.setObjectName("label_non_conflict_2")
        self.label_non_conflict_2.setText("0")
        
        self.horizontalLayout_18.addWidget(self.label_non_conflict_2)
        self.horizontalLayout_17.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(parent=self.frame_res_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_19.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_near_crash_1 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_near_crash_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_near_crash_1.setObjectName("label_near_crash_1")
        self.label_near_crash_1.setText("Near Crash")
        
        self.horizontalLayout_19.addWidget(self.label_near_crash_1)
        self.label_near_crash_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_near_crash_2.setStyleSheet('''
                                            #label_near_crash_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_near_crash_2.setObjectName("label_near_crash_2")
        self.label_near_crash_2.setText("0")

        self.horizontalLayout_19.addWidget(self.label_near_crash_2)
        self.horizontalLayout_17.addWidget(self.frame_2)
        self.verticalLayout_14.addWidget(self.frame_res_2)
        self.frame_res_3 = QtWidgets.QFrame(parent=self.frame_res_bot)
        self.frame_res_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_3.setObjectName("frame_res_3")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_res_3)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_res_3)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_21.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_proximity_conflict_1 = QtWidgets.QLabel(parent=self.frame_7)
        self.label_proximity_conflict_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_proximity_conflict_1.setObjectName("label_proximity_conflict_1")
        self.label_proximity_conflict_1.setText("Proximity Conflict")

        self.horizontalLayout_21.addWidget(self.label_proximity_conflict_1)
        self.label_proximity_conflict_2 = QtWidgets.QLabel(parent=self.frame_7)
        self.label_proximity_conflict_2.setStyleSheet('''
                                        #label_proximity_conflict_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_proximity_conflict_2.setObjectName("label_proximity_conflict_2")
        self.label_proximity_conflict_2.setText("0")

        self.horizontalLayout_21.addWidget(self.label_proximity_conflict_2)
        self.horizontalLayout_20.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_res_3)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_222 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_222.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_222.setObjectName("horizontalLayout_222")
        self.label_crash_1 = QtWidgets.QLabel(parent=self.frame_8)
        self.label_crash_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_crash_1.setObjectName("label_crash_1")
        self.label_crash_1.setText("Crash")

        self.horizontalLayout_222.addWidget(self.label_crash_1)
        self.label_crash_2 = QtWidgets.QLabel(parent=self.frame_7)
        self.label_crash_2.setStyleSheet('''
                                        #label_crash_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_crash_2.setObjectName("label_crash_2")
        self.label_crash_2.setText("0")

        self.horizontalLayout_222.addWidget(self.label_crash_2)
        
        self.horizontalLayout_20.addWidget(self.frame_8)
        self.verticalLayout_14.addWidget(self.frame_res_3)
        self.frame_res_4 = QtWidgets.QFrame(parent=self.frame_res_bot)
        self.frame_res_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_res_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_res_4.setObjectName("frame_res_4")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_res_4)
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.frame_9 = QtWidgets.QFrame(parent=self.frame_res_4)
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        # self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_9)
        # self.horizontalLayout_23.setContentsMargins(3, 0, 3, 0)
        # self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        # self.label_crash_1 = QtWidgets.QLabel(parent=self.frame_9)
        # self.label_crash_1.setMaximumSize(QtCore.QSize(200, 16777215))
        # self.label_crash_1.setObjectName("label_crash_1")
        # self.label_crash_1.setText("Crash")
        
        # self.horizontalLayout_23.addWidget(self.label_crash_1)
        # self.label_crash_2 = QtWidgets.QLabel(parent=self.frame_9)
        # self.label_crash_2.setStyleSheet('''
        #                                 #label_crash_2 {
        #                                     font-weight: 600;
        #                                 }
        #                                 ''')
        # self.label_crash_2.setObjectName("label_crash_2")
        # self.label_crash_2.setText("0")
        
        # self.horizontalLayout_23.addWidget(self.label_crash_2)
        self.horizontalLayout_22.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(parent=self.frame_res_4)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_22.addWidget(self.frame_10)
        self.verticalLayout_14.addWidget(self.frame_res_4)
        self.verticalLayout_13.addWidget(self.frame_res_bot)
        self.verticalLayout_6.addWidget(self.frame_res)
        self.horizontalLayout.addWidget(self.frame_mid)
        self.frame_right = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_right.setMinimumSize(QtCore.QSize(480, 0))
        self.frame_right.setMaximumSize(QtCore.QSize(480, 16777215))
        self.frame_right.setStyleSheet("")
        self.frame_right.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_right.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_right.setObjectName("frame_right")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_right)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_legends = QtWidgets.QFrame(parent=self.frame_right)
        self.frame_legends.setMinimumSize(QtCore.QSize(0, 535))
        self.frame_legends.setMaximumSize(QtCore.QSize(16777215, 535))
        self.frame_legends.setStyleSheet('''
                                        #frame_legends {
                                            background-color: #f9f9f9;
                                            border-radius: 4px;
                                        }
                                        ''')
        self.frame_legends.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_legends.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_legends.setObjectName("frame_legends")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_legends)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_speed = QtWidgets.QFrame(parent=self.frame_legends)
        self.frame_speed.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_speed.setStyleSheet("")
        self.frame_speed.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_speed.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_speed.setObjectName("frame_speed")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_speed)
        self.horizontalLayout_8.setContentsMargins(4, -1, 4, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_speed = QtWidgets.QLabel(parent=self.frame_speed)
        self.label_speed.setObjectName("label_speed")
        self.label_speed.setText("Driving Speed")

        self.horizontalLayout_8.addWidget(self.label_speed)
        self.label_speed_2 = QtWidgets.QLabel(parent=self.frame_speed)
        self.label_speed_2.setStyleSheet('''
                                        #label_speed_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_speed_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_speed_2.setObjectName("label_speed_2")
        self.label_speed_2.setText("000 km/h")

        self.horizontalLayout_8.addWidget(self.label_speed_2)
        self.verticalLayout_11.addWidget(self.frame_speed)
        self.frame_coordinates = QtWidgets.QFrame(parent=self.frame_legends)
        self.frame_coordinates.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_coordinates.setStyleSheet('''
                                            #frame_coordinates {
                                                border-top: 2px solid #BDBBBE;
                                            }
                                            ''')
        self.frame_coordinates.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_coordinates.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_coordinates.setObjectName("frame_coordinates")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_coordinates)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.frame_coordinates_left = QtWidgets.QFrame(parent=self.frame_coordinates)
        self.frame_coordinates_left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_coordinates_left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_coordinates_left.setObjectName("frame_coordinates_left")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_coordinates_left)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.frame_top_2 = QtWidgets.QFrame(parent=self.frame_coordinates_left)
        self.frame_top_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_top_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_top_2.setObjectName("frame_top_2")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.frame_top_2)
        self.horizontalLayout_24.setContentsMargins(4, 0, 4, 0)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_coordinates = QtWidgets.QLabel(parent=self.frame_top_2)
        self.label_coordinates.setObjectName("label_coordinates")
        self.label_coordinates.setText("Coordinates")
        
        self.horizontalLayout_24.addWidget(self.label_coordinates)
        self.verticalLayout_12.addWidget(self.frame_top_2)
        self.frame_temp = QtWidgets.QFrame(parent=self.frame_coordinates_left)
        self.frame_temp.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_temp.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_temp.setObjectName("frame_temp")
        self.verticalLayout_12.addWidget(self.frame_temp)
        self.horizontalLayout_9.addWidget(self.frame_coordinates_left)
        self.frame_coordinates_right = QtWidgets.QFrame(parent=self.frame_coordinates)
        self.frame_coordinates_right.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_coordinates_right.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_coordinates_right.setObjectName("frame_coordinates_right")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_coordinates_right)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_top = QtWidgets.QFrame(parent=self.frame_coordinates_right)
        self.frame_top.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_lat_1 = QtWidgets.QLabel(parent=self.frame_top)
        self.label_lat_1.setStyleSheet('''
                                        #label_lat_1 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_lat_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_lat_1.setObjectName("label_lat_1")
        self.label_lat_1.setText("lat")

        self.horizontalLayout_11.addWidget(self.label_lat_1)
        self.label_lat_2 = QtWidgets.QLabel(parent=self.frame_top)
        self.label_lat_2.setStyleSheet('''
                                        #label_lat_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_lat_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_lat_2.setObjectName("label_lat_2")
        self.label_lat_2.setText("0.0")

        self.horizontalLayout_11.addWidget(self.label_lat_2)
        self.verticalLayout_3.addWidget(self.frame_top)
        self.frame_bot = QtWidgets.QFrame(parent=self.frame_coordinates_right)
        self.frame_bot.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_bot.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_bot.setObjectName("frame_bot")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_bot)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_long_1 = QtWidgets.QLabel(parent=self.frame_bot)
        self.label_long_1.setStyleSheet('''
                                        #label_long_1 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_long_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_long_1.setObjectName("label_long_1")
        self.label_long_1.setText("long")

        self.horizontalLayout_12.addWidget(self.label_long_1)
        self.label_long_2 = QtWidgets.QLabel(parent=self.frame_bot)
        self.label_long_2.setStyleSheet('''
                                        #label_long_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_long_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_long_2.setObjectName("label_long_2")
        self.label_long_2.setText("0.0")
                                  
        self.horizontalLayout_12.addWidget(self.label_long_2)
        self.verticalLayout_3.addWidget(self.frame_bot)
        self.horizontalLayout_9.addWidget(self.frame_coordinates_right)
        
        self.verticalLayout_11.addWidget(self.frame_coordinates)
        
        self.frame_phase = QtWidgets.QFrame(parent=self.frame_legends)
        self.frame_phase.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frame_phase.setStyleSheet('''
                                        #frame_phase {
                                            border-top: 2px solid #BDBBBE;
                                        }
                                        ''')
        self.frame_phase.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_phase.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_phase.setObjectName("frame_phase")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.frame_phase)
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.frame_phase_left = QtWidgets.QFrame(parent=self.frame_phase)
        self.frame_phase_left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_phase_left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_phase_left.setObjectName("frame_phase_left")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frame_phase_left)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.frame_top_3 = QtWidgets.QFrame(parent=self.frame_phase_left)
        self.frame_top_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_top_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_top_3.setObjectName("frame_top_3")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.frame_top_3)
        self.horizontalLayout_26.setContentsMargins(4, 0, 4, 0)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_4 = QtWidgets.QLabel(parent=self.frame_top_3)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Phases")
        
        self.horizontalLayout_26.addWidget(self.label_4)
        self.verticalLayout_15.addWidget(self.frame_top_3)
        self.frame_temp_3 = QtWidgets.QFrame(parent=self.frame_phase_left)
        self.frame_temp_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_temp_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_temp_3.setObjectName("frame_temp_3")
        self.verticalLayout_15.addWidget(self.frame_temp_3)
        self.frame_temp_2 = QtWidgets.QFrame(parent=self.frame_phase_left)
        self.frame_temp_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_temp_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_temp_2.setObjectName("frame_temp_2")
        self.verticalLayout_15.addWidget(self.frame_temp_2)
        self.horizontalLayout_25.addWidget(self.frame_phase_left)
        self.frame_phase_right = QtWidgets.QFrame(parent=self.frame_phase)
        self.frame_phase_right.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_phase_right.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_phase_right.setObjectName("frame_phase_right")
        self.verticalLayout_110 = QtWidgets.QVBoxLayout(self.frame_phase_right)
        self.verticalLayout_110.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_110.setSpacing(0)
        self.verticalLayout_110.setObjectName("verticalLayout_110")
        self.frame_top_4 = QtWidgets.QFrame(parent=self.frame_phase_right)
        self.frame_top_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_top_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_top_4.setObjectName("frame_top_4")
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout(self.frame_top_4)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_27.setSpacing(6)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_closing_1 = QtWidgets.QLabel(parent=self.frame_top_4)
        self.label_closing_1.setStyleSheet('''
                                            #label_closing_1 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_closing_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_closing_1.setObjectName("label_closing_1")
        self.label_closing_1.setText("closing")
        
        self.horizontalLayout_27.addWidget(self.label_closing_1)
        self.label_closing_2 = QtWidgets.QLabel(parent=self.frame_top_4)
        self.label_closing_2.setStyleSheet('''
                                            #label_closing_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_closing_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_closing_2.setObjectName("label_closing_2")
        self.label_closing_2.setText("0.0 s")
        
        self.horizontalLayout_27.addWidget(self.label_closing_2)
        self.verticalLayout_110.addWidget(self.frame_top_4)
        self.frame_mid_2 = QtWidgets.QFrame(parent=self.frame_phase_right)
        self.frame_mid_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mid_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_mid_2.setObjectName("frame_mid_2")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout(self.frame_mid_2)
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_28.setSpacing(6)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_closed_1 = QtWidgets.QLabel(parent=self.frame_mid_2)
        self.label_closed_1.setStyleSheet('''
                                            #label_closed_1 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_closed_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_closed_1.setObjectName("label_closed_1")
        self.label_closed_1.setText("closed")
        
        self.horizontalLayout_28.addWidget(self.label_closed_1)
        self.label_closed_2 = QtWidgets.QLabel(parent=self.frame_mid_2)
        self.label_closed_2.setStyleSheet('''
                                            #label_closed_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_closed_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_closed_2.setObjectName("label_closed_2")
        self.label_closed_2.setText("0.0 s")
        
        self.horizontalLayout_28.addWidget(self.label_closed_2)
        self.verticalLayout_110.addWidget(self.frame_mid_2)
        self.frame_bot_3 = QtWidgets.QFrame(parent=self.frame_phase_right)
        self.frame_bot_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_bot_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_bot_3.setObjectName("frame_bot_3")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.frame_bot_3)
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_29.setSpacing(6)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_reopening_1 = QtWidgets.QLabel(parent=self.frame_bot_3)
        self.label_reopening_1.setStyleSheet('''
                                            #label_reopening_1 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_reopening_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_reopening_1.setObjectName("label_reopening_1")
        self.label_reopening_1.setText("reopening")
        
        self.horizontalLayout_29.addWidget(self.label_reopening_1)
        self.label_reopening_2 = QtWidgets.QLabel(parent=self.frame_bot_3)
        self.label_reopening_2.setStyleSheet('''
                                            #label_reopening_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_reopening_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_reopening_2.setObjectName("label_reopening_2")
        self.label_reopening_2.setText("0.0 s")
        
        self.horizontalLayout_29.addWidget(self.label_reopening_2)
        self.verticalLayout_110.addWidget(self.frame_bot_3)
        self.horizontalLayout_25.addWidget(self.frame_phase_right)
        self.verticalLayout_11.addWidget(self.frame_phase)
        
        # atas
        self.frame_collection = QtWidgets.QFrame(parent=self.frame_legends)
        self.frame_collection.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_collection.setStyleSheet('''
                                            #frame_collection {
                                                border-top: 2px solid #BDBBBE;
                                            }
                                            ''')
        self.frame_collection.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_collection.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_collection.setObjectName("frame_collection")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.frame_collection)
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.frame_collection_left = QtWidgets.QFrame(parent=self.frame_collection)
        self.frame_collection_left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_collection_left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_collection_left.setObjectName("frame_collection_left")
        self.frame_collection_left.setMaximumWidth(200)
        
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_collection_left)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.frame_top_5 = QtWidgets.QFrame(parent=self.frame_collection_left)
        self.frame_top_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_top_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_top_5.setObjectName("frame_top_5")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout(self.frame_top_5)
        self.horizontalLayout_31.setContentsMargins(4, 0, 4, 0)
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_5 = QtWidgets.QLabel(parent=self.frame_top_5)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Collection")
        
        self.horizontalLayout_31.addWidget(self.label_5)
        self.verticalLayout_16.addWidget(self.frame_top_5)
        self.frame_temp_4 = QtWidgets.QFrame(parent=self.frame_collection_left)
        self.frame_temp_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_temp_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_temp_4.setObjectName("frame_temp_4")
        self.verticalLayout_16.addWidget(self.frame_temp_4)
        self.frame_temp_5 = QtWidgets.QFrame(parent=self.frame_collection_left)
        self.frame_temp_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_temp_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_temp_5.setObjectName("frame_temp_5")
        self.verticalLayout_16.addWidget(self.frame_temp_5)
        self.frame_temp_6 = QtWidgets.QFrame(parent=self.frame_collection_left)
        self.frame_temp_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_temp_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_temp_6.setObjectName("frame_temp_6")
        self.verticalLayout_16.addWidget(self.frame_temp_6)
        self.horizontalLayout_30.addWidget(self.frame_collection_left)
        self.frame_collection_right = QtWidgets.QFrame(parent=self.frame_collection)
        self.frame_collection_right.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_collection_right.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_collection_right.setObjectName("frame_collection_right")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.frame_collection_right)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.frame_top_6 = QtWidgets.QFrame(parent=self.frame_collection_right)
        self.frame_top_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_top_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_top_6.setObjectName("frame_top_6")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout(self.frame_top_6)
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_32.setSpacing(6)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_blink_duration_1 = QtWidgets.QLabel(parent=self.frame_top_6)
        self.label_blink_duration_1.setStyleSheet('''
                                                #label_blink_duration_1 {
                                                    font-weight: 600;
                                                }
                                                ''')
        self.label_blink_duration_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_blink_duration_1.setObjectName("label_blink_duration_1")
        self.label_blink_duration_1.setText("blink duration")
        self.label_blink_duration_1.setMinimumWidth(133)
        
        self.horizontalLayout_32.addWidget(self.label_blink_duration_1)
        self.label_blink_duration_2 = QtWidgets.QLabel(parent=self.frame_top_6)
        self.label_blink_duration_2.setStyleSheet('''
                                                #label_blink_duration_2 {
                                                    font-weight: 600;
                                                }
                                                ''')
        self.label_blink_duration_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_blink_duration_2.setObjectName("label_blink_duration_2")
        self.label_blink_duration_2.setText("0.0 s")
        
        self.horizontalLayout_32.addWidget(self.label_blink_duration_2)
        self.verticalLayout_17.addWidget(self.frame_top_6)
        self.frame_mid_3 = QtWidgets.QFrame(parent=self.frame_collection_right)
        self.frame_mid_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mid_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_mid_3.setObjectName("frame_mid_3")
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.frame_mid_3)
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_33.setSpacing(6)
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.label_blink_freq_1 = QtWidgets.QLabel(parent=self.frame_mid_3)
        self.label_blink_freq_1.setStyleSheet('''
                                            #label_blink_freq_1 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_blink_freq_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_blink_freq_1.setObjectName("label_blink_freq_1")
        self.label_blink_freq_1.setText("blink freq")
        self.label_blink_freq_1.setMinimumWidth(133)

        self.horizontalLayout_33.addWidget(self.label_blink_freq_1)
        self.label_blink_freq_2 = QtWidgets.QLabel(parent=self.frame_mid_3)
        self.label_blink_freq_2.setStyleSheet('''
                                            #label_blink_freq_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_blink_freq_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_blink_freq_2.setObjectName("label_blink_freq_2")
        self.label_blink_freq_2.setText("0.0 s")
        
        self.horizontalLayout_33.addWidget(self.label_blink_freq_2)
        self.verticalLayout_17.addWidget(self.frame_mid_3)
        self.frame_mid_4 = QtWidgets.QFrame(parent=self.frame_collection_right)
        self.frame_mid_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mid_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_mid_4.setObjectName("frame_mid_4")
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout(self.frame_mid_4)
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_35.setSpacing(6)
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.label_microsleep_1 = QtWidgets.QLabel(parent=self.frame_mid_4)
        self.label_microsleep_1.setStyleSheet('''
                                            #label_microsleep_1 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_microsleep_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_microsleep_1.setObjectName("label_microsleep_1")
        self.label_microsleep_1.setText("microsleep")
        self.label_microsleep_1.setMinimumWidth(133)
        
        self.horizontalLayout_35.addWidget(self.label_microsleep_1)
        self.label_microsleep_2 = QtWidgets.QLabel(parent=self.frame_mid_4)
        self.label_microsleep_2.setStyleSheet('''
                                            #label_microsleep_2 {
                                                font-weight: 600;
                                            }
                                            ''')
        self.label_microsleep_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_microsleep_2.setObjectName("label_microsleep_2")
        self.label_microsleep_2.setText("0.0 s")
        
        self.horizontalLayout_35.addWidget(self.label_microsleep_2)
        self.verticalLayout_17.addWidget(self.frame_mid_4)
        self.frame_bot_4 = QtWidgets.QFrame(parent=self.frame_collection_right)
        self.frame_bot_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_bot_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_bot_4.setObjectName("frame_bot_4")
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout(self.frame_bot_4)
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_34.setSpacing(6)
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.label_perclos_1 = QtWidgets.QLabel(parent=self.frame_bot_4)
        self.label_perclos_1.setStyleSheet('''
                                        #label_perclos_1 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_perclos_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_perclos_1.setObjectName("label_perclos_1")
        self.label_perclos_1.setText("perclos")
        self.label_perclos_1.setMinimumWidth(133)
        
        self.horizontalLayout_34.addWidget(self.label_perclos_1)
        self.label_perclos_2 = QtWidgets.QLabel(parent=self.frame_bot_4)
        self.label_perclos_2.setStyleSheet('''
                                        #label_perclos_2 {
                                            font-weight: 600;
                                        }
                                        ''')
        self.label_perclos_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_perclos_2.setObjectName("label_perclos_2")
        self.label_perclos_2.setText("0.0 s")
        
        self.horizontalLayout_34.addWidget(self.label_perclos_2)
        self.verticalLayout_17.addWidget(self.frame_bot_4)
        self.horizontalLayout_30.addWidget(self.frame_collection_right)
        self.verticalLayout_11.addWidget(self.frame_collection)
        # bawah
        
        self.verticalLayout_11.addWidget(self.frame_collection)
        self.verticalLayout_10.addWidget(self.frame_legends)
        self.frame_maps = QtWidgets.QFrame(parent=self.frame_right)
        self.frame_maps.setStyleSheet('''
                                    #frame_maps {
                                        background-color: #f9f9f9;
                                        border-radius: 4px;
                                    }
                                    ''')
        self.frame_maps.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_maps.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_maps.setObjectName("frame_maps")
        
        self.layout = QtWidgets.QVBoxLayout()
        self.frame_maps.setLayout(self.layout)

        coordinate = (-6.891355706290874, 107.6106683270131)
        
        self.m = folium.Map(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Maps',
            overlay=True,
            control=True,
            zoom_start=16,
            location=coordinate
        )
        folium.Marker(location=coordinate).add_to(self.m)

        # save map data to data object
        data = io.BytesIO()
        self.m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.webView)
        
        self.verticalLayout_10.addWidget(self.frame_maps)
        self.horizontalLayout.addWidget(self.frame_right)
        self.setCentralWidget(self.centralwidget)
        
    def process_data(self):
        file_path = self.textbox_data.toPlainText().strip()
        
        rows = IO.read_csv(file_path)
                
        start = rows[0][1] + " " + rows[0][2]
        end = rows[-1][1] + " " + rows[0][2]
                
        locale.setlocale(locale.LC_TIME, "id_ID")

        self.start_time = datetime.strptime(start, "%d %B %Y %H:%M:%S")
        self.end_time = datetime.strptime(end, "%d %B %Y %H:%M:%S")
        
        events = []
        
        # Csv 2
        dateTimeNow = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = f"result/result2_{dateTimeNow}.csv"
        IO.write_header2(csv_file)
        
        for col in rows:            
            timestamp = col[1] + " " + col[2]
            
            event = {
                "day": col[0],
                "event_time": datetime.strptime(timestamp, "%d %B %Y %H:%M:%S"),
                "distance": float(col[3]),
                "v_subject": float(col[4]),
                "v_leading": float(col[5]),
                "latitude": float(col[6]),
                "longitude": float(col[7]),
                "accel_x": float(col[8]),
                "accel_y": float(col[9]),
                "accel_z": float(col[10]),
                "gyro_x": float(col[11]),
                "gyro_y": float(col[12]),
                "gyro_z": float(col[13]),
                "degrees": float(col[14])
            }
                        
            events.append(event)
            
            event_category = "-"
            if algorithm.check_non_conflict(event):
                event_category = "Non-Conflict"
            elif algorithm.check_proximity_conflict(event):
                event_category = "Proximity Conflict"
            elif algorithm.check_crash_relevant_conflict(event):
                event_category = "Crash Relevant Conflict"
            elif algorithm.check_near_crash(event):
                event_category = "Near Crash"
            elif algorithm.check_crash(event):
                event_category = "Crash"
                
            IO.write_data_to_csv([col[0], col[1], col[2], algorithm.time_to_collision(event), event_category], csv_file)
                
        self.raw_events = events
        
        self.all_events = {"non_conflict": [], "proximity_conflict": [], "crash_relevant_conflict": [], "near_crash": [], "crash": []}

        for i in range(len(events)):
            current_event = events[i]
            
            if algorithm.check_non_conflict(current_event):
                if i == 0 and i != len(events) - 1: # at the beginning
                    self.all_events["non_conflict"].append([current_event, events[i + 1], "Non Conflict"])
                elif i == len(events) - 1 and i != 0: # at the end
                    # check if events[i - 1], current_event are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["non_conflict"]):
                        self.all_events["non_conflict"].append([events[i - 1], current_event, "Non Conflict"])
                else:
                    # check if events[i - 1], current_event, events[i + 1] are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["non_conflict"]):
                        self.all_events["non_conflict"].append([events[i - 1], current_event, events[i + 1], "Non Conflict"])
                    else:
                        self.all_events["non_conflict"].append([events[i + 1], "Non Conflict"])
            
            elif algorithm.check_proximity_conflict(current_event):
                if i == 0 and i != len(events) - 1: # at the beginning
                    self.all_events["proximity_conflict"].append([current_event, events[i + 1], "Proximity Conflict"])
                elif i == len(events) - 1 and i != 0: # at the end
                    # check if events[i - 1], current_event are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["proximity_conflict"]):
                        self.all_events["proximity_conflict"].append([events[i - 1], current_event, "Proximity Conflict"])
                else:
                    # check if events[i - 1], current_event, events[i + 1] are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["proximity_conflict"]):
                        self.all_events["proximity_conflict"].append([events[i - 1], current_event, events[i + 1], "Proximity Conflict"])    
                    else:
                        self.all_events["proximity_conflict"].append([events[i + 1], "Proximity Conflict"])
            
            elif algorithm.check_crash_relevant_conflict(current_event):
                if i == 0 and i != len(events) - 1: # at the beginning
                    self.all_events["crash_relevant_conflict"].append([current_event, events[i + 1], "Crash Relevant Conflict"])
                elif i == len(events) - 1 and i != 0: # at the end
                    # check if events[i - 1], current_event are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["crash_relevant_conflict"]):
                        self.all_events["crash_relevant_conflict"].append([events[i - 1], current_event, "Crash Relevant Conflict"])
                else:
                    # check if events[i - 1], current_event, events[i + 1] are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["crash_relevant_conflict"]):
                        self.all_events["crash_relevant_conflict"].append([events[i - 1], current_event, events[i + 1], "Crash Relevant Conflict"])   
                    else:
                        self.all_events["crash_relevant_conflict"].append([events[i + 1], "Crash Relevant Conflict"])
            
            elif algorithm.check_near_crash(current_event):
                if i == 0 and i != len(events) - 1: # at the beginning
                    self.all_events["near_crash"].append([current_event, events[i + 1], "Near Crash"])
                elif i == len(events) - 1 and i != 0: # at the end
                    # check if events[i - 1], current_event are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["near_crash"]):
                        self.all_events["near_crash"].append([events[i - 1], current_event, "Near Crash"])
                else:
                    # check if events[i - 1], current_event, events[i + 1] are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["near_crash"]):
                        self.all_events["near_crash"].append([events[i - 1], current_event, events[i + 1], "Near Crash"])
                    else:
                        self.all_events["near_crash"].append([events[i + 1], "Near Crash"])
            
            elif algorithm.check_crash(current_event):
                if i == 0 and i != len(events) - 1:  # at the beginning
                    self.all_events["crash"].append([current_event, events[i + 1], "Crash"])
                elif i == len(events) - 1 and i != 0: # at the end
                    # check if events[i - 1], current_event are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["crash"]):
                        self.all_events["crash"].append([events[i - 1], current_event, "Crash"])
                else:
                    # check if events[i - 1], current_event, events[i + 1] are there in the list, if not append
                    if not algorithm.check_exists([events[i - 1], current_event], self.all_events["crash"]):
                        self.all_events["crash"].append([events[i - 1], current_event, events[i + 1], "Crash"])
                    else:
                        self.all_events["crash"][-1].insert(-1, events[i + 1])
    
    def display_data(self):
        data = self.all_events
                        
        length = len(data["non_conflict"]) + len(data["proximity_conflict"]) + len(data["crash_relevant_conflict"]) + len(data["near_crash"]) + len(data["crash"])
        self.label_non_conflict_2.setText(str(len(data["non_conflict"])))
        self.label_proximity_conflict_2.setText(str(len(data["proximity_conflict"])))
        self.label_crash_relevant_conflict_2.setText(str(len(data["crash_relevant_conflict"])))
        self.label_total_2.setText(str(length))
        self.label_near_crash_2.setText(str(len(data["near_crash"])))
        self.label_crash_2.setText(str(len(data["crash"])))
        
        combined_events = data["non_conflict"] + data["proximity_conflict"] + data["crash_relevant_conflict"] + data["near_crash"] + data["crash"]
        sorted_events = sorted(combined_events, key=lambda event: event[0]["event_time"])

        self.events = sorted_events
        video_file = self.fileName_1
        
        for i in range(length):
            self.data = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
            self.data.setMinimumSize(QtCore.QSize(0, 90))
            self.data.setMaximumSize(QtCore.QSize(16777215, 90))
            self.data.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.data.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.data.setObjectName(f"data_{i}")
            self.data.mousePressEvent = lambda event, index=i: self.data_clicked(event, f"data_{index}")
            
            self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.data)
            self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
            self.horizontalLayout_5.setSpacing(0)
            self.horizontalLayout_5.setObjectName("horizontalLayout_5")
            self.data_left = QtWidgets.QFrame(parent=self.data)
            self.data_left.setMaximumSize(QtCore.QSize(120, 16777215))
            self.data_left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.data_left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.data_left.setObjectName("data_left")
            self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.data_left)
            self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_6.setSpacing(0)
            self.horizontalLayout_6.setObjectName("horizontalLayout_6")
            self.img_vid = QtWidgets.QLabel(parent=self.data_left)
            
            # Create a new video capture object for each video file
            cap = cv2.VideoCapture(video_file)

            desired_time = sorted_events[i][0]["event_time"] - self.start_time

            # Set the video capture position to the desired time
            cap.set(cv2.CAP_PROP_POS_MSEC, int(desired_time.total_seconds()) * 1000)
            
            # Read a frame from the video at the desired time
            ret, frame = cap.read()
            
            # Convert the frame to QImage
            image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            
            # Convert QImage to QPixmap
            pixmap = QtGui.QPixmap.fromImage(image)

            # Set the pixmap as the background of the QLabel
            self.img_vid.setPixmap(pixmap)
            self.img_vid.setScaledContents(True)  # Scale the pixmap to fit the QLabel
            
            # Release the video capture object
            cap.release()
            
            self.img_vid.setStyleSheet('''
                                        #img_vid {
                                            background-color: transparent;
                                        }
                                        ''')
            self.img_vid.setObjectName("img_vid")
            self.horizontalLayout_6.addWidget(self.img_vid)
            self.horizontalLayout_5.addWidget(self.data_left)
            self.data_right = QtWidgets.QFrame(parent=self.data)
            self.data_right.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.data_right.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.data_right.setObjectName("data_right")
            self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.data_right)
            self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_4.setSpacing(0)
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.frame_4 = QtWidgets.QFrame(parent=self.data_right)
            self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_4.setObjectName("frame_4")
            self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_4)
            self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_7.setSpacing(0)
            self.horizontalLayout_7.setObjectName("horizontalLayout_7")
            self.label_time = QtWidgets.QLabel(parent=self.frame_4)
            self.label_time.setStyleSheet('''
                                        #label_time {
                                            font-size: 16px;
                                            font-weight: 600;
                                        }
                                        ''')
            self.label_time.setScaledContents(False)
            self.label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label_time.setObjectName("label_time")
            self.label_time.setText(sorted_events[i][0]["event_time"].strftime("%H:%M:%S"))

            self.horizontalLayout_7.addWidget(self.label_time)
            self.label_date = QtWidgets.QLabel(parent=self.frame_4)
            self.label_date.setStyleSheet('''
                                        #label_date {
                                            font-size: 16px;
                                            font-weight: 600;
                                        }
                                        ''')
            self.label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label_date.setObjectName("label_date")
            self.label_date.setText(sorted_events[i][0]["event_time"].strftime("%Y-%m-%d"))

            self.horizontalLayout_7.addWidget(self.label_date)
            self.verticalLayout_4.addWidget(self.frame_4)
            self.frame_5 = QtWidgets.QFrame(parent=self.data_right)
            self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.frame_5.setObjectName("frame_5")
            self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_5)
            self.verticalLayout_8.setContentsMargins(18, 0, 0, 0)
            self.verticalLayout_8.setSpacing(0)
            self.verticalLayout_8.setObjectName("verticalLayout_8")
            self.label_category = QtWidgets.QLabel(parent=self.frame_5)
            self.label_category.setStyleSheet('''
                                            #label_category {
                                                padding: 2px 16px;
                                                font-size: 16px;
                                                font-weight: 600;
                                                border-radius: 18px;
                                                border: 1px solid black;
                                                background-color: #f9f9f9;
                                            }
                                            ''')
            self.label_category.setObjectName("label_category")
            self.label_category.setText(sorted_events[i][-1])

            self.verticalLayout_8.addWidget(self.label_category)
            self.verticalLayout_4.addWidget(
                self.frame_5, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
            self.horizontalLayout_5.addWidget(self.data_right)
            self.verticalLayout_data.addWidget(self.data)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        
        self.verticalLayout_data.addItem(spacerItem)
    
    def data_clicked(self, event, data_name):
        # Find the object with the matching data_name
        obj_list = self.scrollAreaWidgetContents.findChildren(QtWidgets.QFrame, data_name)
        
        if obj_list:
            self.btn_play.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            clicked_data = obj_list[0]  # Get the first matching object
            clicked_data.setStyleSheet("background-color: #D3EBF9;")  # Change the background color of the clicked data frame
            
            x = int(data_name.split("_")[1])
            data = self.events[x]
            self.data_state = data

            start_time = data[0]["event_time"] - self.start_time - timedelta(seconds=1)
            end_time = data[-2]["event_time"] - self.end_time
                        
            self.start_time_processed = int(start_time.total_seconds()) * 1000
            self.end_time_processed = int(end_time.total_seconds()) * 1000            

            if (self.start_time_processed < 0):
                self.start_time_processed = 0
            for time in reversed(self.time_list):
                if time != 0:
                    if (self.end_time_processed > int(time) * 1000):
                        self.end_time_processed = int(time) * 1000
                    break

            self.mediaPlayer.setMedia(
                QMediaContent(QtCore.QUrl.fromLocalFile(self.fileName_1)))
            self.mediaPlayer2.setMedia(
                QMediaContent(QtCore.QUrl.fromLocalFile(self.fileName_2)))
            
            # self.setPosition(self.start_time_processed)
            
            self.horizontalSlider.setRange(self.start_time_processed, self.end_time_processed)
            self.mediaPlayer.setPosition(self.start_time_processed)
            self.mediaPlayer2.setPosition(self.start_time_processed)
            
            # display data
            self.label_speed_2.setText(f"{data[0]['v_subject']:6.6} km/h")
            self.label_lat_2.setText(f"{data[0]['latitude']:7.7}")
            self.label_long_2.setText(f"{data[0]['longitude']:7.7}")
            
            closing_time_avg, closing_time = self.calculate_average_duration(start_time.total_seconds(), self.closing_list)
            closed_time_avg, closed_time = self.calculate_average_duration(start_time.total_seconds(), self.closed_list)
            reopening_time_avg, reopening_time = self.calculate_average_duration(start_time.total_seconds(), self.reopening_list)
            
            self.label_closing_2.setText(f"{closing_time_avg:4.4} s")
            self.label_closed_2.setText(f"{closed_time_avg:4.4} s")
            self.label_reopening_2.setText(f"{reopening_time_avg:4.4} s")

            blink_duration = closing_time_avg + reopening_time_avg + closed_time_avg
            blink_frequency, microsleep = self.blink_count(start_time.total_seconds(), self.blink_list)
            perclos = closed_time
                        
            self.label_blink_duration_2.setText(f"{blink_duration:4.4} s")
            self.label_blink_freq_2.setText(f"{blink_frequency}")
            self.label_microsleep_2.setText(f"{microsleep}")
            self.label_perclos_2.setText(f"{perclos:4.4} s")
            
            self.update_map(data[0]['latitude'], data[0]['longitude'])
            
            # Reset the background color of other data frames
            for obj in self.scrollAreaWidgetContents.children():
                if isinstance(obj, QtWidgets.QFrame) and obj is not clicked_data:
                    obj.setStyleSheet("background-color: transparent;")
    
    def update_map(self, lat, long):
        coordinate = (lat, long)
        
        self.m = folium.Map(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Maps',
            overlay=True,
            control=True,
            zoom_start=16,
            location=coordinate
        )

        folium.Marker(location=coordinate).add_to(self.m)

        # save map data to data object
        data = io.BytesIO()
        self.m.save(data, close_file=False)

        self.webView.setHtml(data.getvalue().decode())
    
    def updateState(self, position):
        print("updateState")
        range_size = 1000
        index = (position - self.start_time_processed) // range_size
        print(index, len(self.data_state))
        if (0 <= index < len(self.data_state)):
            start_time = self.data_state[index]['event_time'] - self.start_time - timedelta(seconds=1)
            
            self.label_speed_2.setText(f"{self.data_state[index]['v_subject']:6.6} km/h")
            self.label_lat_2.setText(f"{self.data_state[index]['latitude']:7.7}")
            self.label_long_2.setText(f"{self.data_state[index]['longitude']:7.7}")
            
            closing_time_avg, closing_time = self.calculate_average_duration(start_time.total_seconds(), self.closing_list)
            closed_time_avg, closed_time = self.calculate_average_duration(start_time.total_seconds(), self.closed_list)
            reopening_time_avg, reopening_time = self.calculate_average_duration(start_time.total_seconds(), self.reopening_list)
            
            self.label_closing_2.setText(f"{closing_time_avg:4.4} s")
            self.label_closed_2.setText(f"{closed_time_avg:4.4} s")
            self.label_reopening_2.setText(f"{reopening_time_avg:4.4} s")
            
            blink_duration = closing_time_avg + reopening_time_avg + closed_time_avg
            blink_frequency, microsleep = self.blink_count(start_time.total_seconds(), self.blink_list)
            perclos = closed_time
            
            self.label_blink_duration_2.setText(f"{blink_duration:4.4} s")
            self.label_blink_freq_2.setText(f"{blink_frequency}")
            self.label_microsleep_2.setText(f"{microsleep}")
            self.label_perclos_2.setText(f"{perclos:4.4} s")
            
            self.update_map(self.data_state[index]['latitude'], self.data_state[index]['longitude'])
    
    def reset(self):
        self.label_total_2.setText("0")
        self.label_near_crash_2.setText("0")
        self.label_crash_2.setText("0")
        
        # Remove data widgets
        while self.verticalLayout_data.count():
            item = self.verticalLayout_data.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Remove spacerItem
        spacerItem = self.verticalLayout_data.takeAt(self.verticalLayout_data.count() - 1)
        if spacerItem is not None:
            self.verticalLayout_data.removeItem(spacerItem)
            
    def submit(self):
        if self.textbox_data.toPlainText().strip() == "":
            QtWidgets.QMessageBox.warning(self, "Error", "Data cannot be empty!")
            return
        
        if self.textbox_vid.toPlainText().strip() == "":
            QtWidgets.QMessageBox.warning(self, "Error", "Video cannot be empty!")
            return
           
        if self.textbox_vid_2.toPlainText().strip() == "":
            QtWidgets.QMessageBox.warning(self, "Error", "Video cannot be empty!")
            return
        
        self.reset()
        
        self.process_data()
                
        fileName = self.fileName_2
        
        cap = cv2.VideoCapture(fileName)
        # cap = cv2.VideoCapture(0)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("dataset/shape_predictor_68_face_landmarks.dat")

        # Set the desired display resolution
        display_width = 800
        display_height = 600

        def midpoint(p1, p2):
            return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

        def euclidean_distance(p1, p2):
            distance = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
            return distance

        def get_blinking_ratio(eye_points, facial_landmarks):
            print("a")
            left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
            right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
            center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
            center_bot = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

            print("b")
            hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
            ver_line = cv2.line(frame, center_top, center_bot, (0, 255, 0), 2)

            print("c")
            hor_line_length = euclidean_distance(left_point, right_point)
            ver_line_length = euclidean_distance(center_top, center_bot)

            if (ver_line_length == 0):
                return hor_line_length
            print(hor_line_length, ver_line_length)
            ratio = hor_line_length/ver_line_length
            return ratio

        prev_ratio_left = 0
        prev_ratio_right = 0
        
        self.closing_list = []
        self.reopening_list = []
        self.closed_list = []
        self.time_list = []
        
        closing_list_csv = []
        reopening_list_csv = []
        closed_list_csv = []
        blink_list_csv = []
        
        self.time_list_processed = []
        self.blink_list = []

        count_minute = 0
        
        dateTimeNow = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = f"result/result1_{dateTimeNow}.csv"
        IO.write_header1(csv_file)
        flag = False
        
        while True:
            print("a")
            # Read a frame from the video
            ret, frame = cap.read()
            
            # Get the current position of the video in milliseconds
            current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

            # Convert milliseconds to seconds
            current_time_s = current_time_ms / 1000
            print(current_time_s)

            if current_time_s != 0.0:
                self.time_list.append(current_time_s)
                
            # Break the loop if the video is over or not successfully read
            if not ret:
                break
            
            frame_height, frame_width, _ = frame.shape
            
            # Resize the frame while maintaining the aspect ratio
            aspect_ratio = frame_width / frame_height
            if aspect_ratio > display_width / display_height:
                new_width = display_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = display_height
                new_width = int(new_height * aspect_ratio)
            
            frame = cv2.resize(frame, (new_width, new_height))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = detector(gray)
            print(faces)
            
            for face in faces:
                print("1")
                x, y = face.left(), face.top()
                x1, y1 = face.right(), face.bottom()    
                if x < frame.shape[1] // 2:
                    print("2")
                    cv2.rectangle(frame, (x, y), (x1, y1), (255, 0, 0), 2)
                    
                    print("landmarks")
                    landmarks = predictor(gray, face)
                    
                    print("landmarks2")
                    
                    # LEFT EYE
                    left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                    
                    # RIGHT EYE
                    right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                                            
                    print("2.5")
                    if left_eye_ratio > 6 and right_eye_ratio > 6 and current_time_s != 0.0:
                        # closed
                        print("closed")
                        flag = True
                        self.closed_list.append(current_time_s)
                        closed_list_csv.append(current_time_s)
                        self.time_list_processed.append(current_time_s)
                        print("done")

                        # if prev_ratio_left < 6 and prev_ratio_right < 6:
                        #     count += 1
                    elif left_eye_ratio > prev_ratio_left and right_eye_ratio > prev_ratio_right and left_eye_ratio > 4 and right_eye_ratio > 4 and current_time_s != 0.0:
                        # closing
                        print("closing")
                        flag = True
                        self.closing_list.append(current_time_s)
                        closing_list_csv.append(current_time_s)
                        self.time_list_processed.append(current_time_s)

                    elif left_eye_ratio <= prev_ratio_left and right_eye_ratio <= prev_ratio_right and left_eye_ratio > 4 and right_eye_ratio > 4 and current_time_s != 0.0:
                        # reopening
                        print("reopening")
                        flag = True
                        self.reopening_list.append(current_time_s)
                        reopening_list_csv.append(current_time_s)
                        self.time_list_processed.append(current_time_s)
                    else:
                        print("else")
                        if len(self.time_list_processed) > 5:
                            last_five_elements = self.time_list_processed[-5:]
                            all_negative_ones = all(num == -1 for num in last_five_elements)
                            if all_negative_ones and flag:
                                self.blink_list.append((self.time_list_processed[0], self.time_list_processed[-6] - self.time_list_processed[0]))
                                blink_list_csv.append((self.time_list_processed[0], self.time_list_processed[-6] - self.time_list_processed[0]))
                                self.time_list_processed = []
                                flag = False
                            else:
                                self.time_list_processed.append(-1)

                    print("2.7")
                    prev_ratio_left = left_eye_ratio
                    prev_ratio_right = right_eye_ratio
                    print("2.8")
            
            print("3")
            # Create a black background image with the desired display resolution
            display_frame = np.zeros((display_height, display_width, 3), dtype=np.uint8)
            x_offset = (display_width - new_width) // 2
            y_offset = (display_height - new_height) // 2
            
            # Overlay the resized frame onto the black background
            display_frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = frame
            
            cv2.imshow("Frame", display_frame)
            
            key = cv2.waitKey(1)
            if key == 27:
                break
                
            print("4")
                        
            if (current_time_s >= 60 + count_minute * 60) or (current_time_s == 0 and len(self.time_list) != 0):
                count_minute += 1

                # Write to CSV    
                seconds = self.time_list[-1] if current_time_s == 0 else current_time_s
                            
                tanggal = (self.start_time + timedelta(seconds=seconds)).strftime("%d %B %Y")
                
                hari = (self.start_time + timedelta(seconds=seconds)).strftime("%A")

                waktu = (self.start_time + timedelta(seconds=seconds)).strftime("%H:%M:%S")
                closing_time_avg, closing_time = self.calculate_average_duration(seconds, closing_list_csv, csv=True)
                reopening_time_avg, reopening_time = self.calculate_average_duration(seconds, reopening_list_csv, csv=True)
                closed_time_avg, closed_time = self.calculate_average_duration(seconds, closed_list_csv, csv=True)

                # pengolahan data
                blink_duration = closing_time_avg + reopening_time_avg + closed_time_avg
                blink_frequency, microsleep = self.blink_count(seconds, blink_list_csv, csv=True)
                perclos = closed_time
                
                avg_distance = self.average([item['distance'] for item in self.raw_events], count_minute)
                avg_speed = self.average([item['v_subject'] for item in self.raw_events], count_minute)
                category_distance = algorithm.distance_category(avg_speed)
                category_speed = algorithm.speed_category(avg_speed)
                                
                IO.write_data_to_csv([hari, tanggal, waktu, closing_time_avg, reopening_time_avg, closed_time_avg, blink_duration, blink_frequency, microsleep, perclos, avg_distance, category_distance, avg_speed, avg_speed, category_speed], csv_file)
                
                if current_time_s == 0:
                    break
        
        self.display_data()
                   
        cap.release()
        cv2.destroyAllWindows()
    
    def average(self, list, minutes):
        start = 60 * (minutes - 1)
        end = 60 * (minutes)
        
        if end > len(list):
            l = list[start:]
        else:
            l = list[start:end]
        
        return sum(l) / len(l)
    
    def blink_count(self, d, durations, csv=False):
        filtered_durations = []
        microsleep = []
        
        start = d - 60
        # Data yang dicalculate adalah 1 menit sebelumnya
        
        if csv:
            i = 0
            while i < len(durations):
                duration = durations[i][0]
                if start <= duration < d:
                    filtered_durations.append(duration)
                    durations.pop(i)
                elif duration >= d:
                    break
                elif duration < start:
                    durations.pop(i)
                else:
                    i += 1
        else:
            for duration, minus in durations:
                if start <= duration < d:
                    filtered_durations.append(duration)
                    if minus > 0.5:
                        microsleep.append(duration)
                elif duration >= d:
                    break
            
        return len(filtered_durations), len(microsleep)
        
    def group_sum(self, list):
        if (len(list) == 1):            
            average_gap = (self.time_list[-1] - self.time_list[0]) / len(self.time_list)
            return average_gap

        return list[-1] - list[0]
        
    def calculate_average_duration(self, d, durations, csv=False):
        filtered_durations = []
                
        start = d - 60
        # Data yang dicalculate adalah 1 menit sebelumnya
                
        if csv:
            i = 0
            while i < len(durations):
                duration = durations[i]
                if start <= duration < d:
                    filtered_durations.append(duration)
                    durations.pop(i)
                elif duration >= d:
                    break
                elif duration < start:
                    durations.pop(i)
                else:
                    i += 1
        else:
            for duration in durations:
                if start <= duration < d:
                    filtered_durations.append(duration)
                elif duration >= d:
                    break
        
        sum_all = 0.0
        count = 0

        current_group = []
        
        average_gap = (self.time_list[-1] - self.time_list[0]) / len(self.time_list)
        for duration in filtered_durations:
            if current_group and (duration - current_group[-1]) >= 0.1:
                sum_all += self.group_sum(current_group) + average_gap
                count += 1
                current_group = []

            current_group.append(duration)

        if len(current_group) == 1:
            sum_all += average_gap
            count += 1

        if count > 0:
            sum_all /= count

        return sum_all, sum_all * count
            
    def open_data(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                  ".", "Data Files (*.csv)")

        if fileName != '':
            self.textbox_data.setPlainText(fileName)
    
    def open_vid(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                  ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.m4v)")

        if fileName != '':
            self.mediaPlayer.setMuted(True)
            self.textbox_vid.setPlainText(fileName)
            self.fileName_1 = fileName
    
    def open_vid_2(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                            ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.m4v)")

        if fileName != '':
            self.mediaPlayer2.setMuted(True)
            self.textbox_vid_2.setPlainText(fileName)
            self.fileName_2 = fileName

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        self.mediaPlayer2.setPosition(position)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState and self.mediaPlayer2.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.mediaPlayer2.pause()
        else:
            self.mediaPlayer.play()
            self.mediaPlayer2.play()

    def positionChanged(self, position):
        if (position > self.end_time_processed):
            self.mediaPlayer.pause()
            self.mediaPlayer2.pause()
            self.setPosition(self.start_time_processed)
        else:     
            self.horizontalSlider.setValue(position)
            self.updateState(position)
            
    def durationChanged(self, duration):
        self.horizontalSlider.setRange(0, duration)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState and self.mediaPlayer2.state() == QMediaPlayer.PlayingState:
            self.btn_play.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.btn_play.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
    
    def eye_aspect_ratio(eye):
        # Calculate the Euclidean distances between the vertical eye landmarks
        vertical_dist1 = distance.euclidean(eye[1], eye[5])
        vertical_dist2 = distance.euclidean(eye[2], eye[4])

        # Calculate the Euclidean distance between the horizontal eye landmarks
        horizontal_dist = distance.euclidean(eye[0], eye[3])

        # Calculate the eye aspect ratio
        ear = (vertical_dist1 + vertical_dist2) / (2.0 * horizontal_dist)
        return ear

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
