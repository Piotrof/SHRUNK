#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class ScreensaverWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Hardcoded path to your custom video
        self.video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animated_image.gif")
        self.initUI()

    def initUI(self):
        # Set window to fullscreen and frameless
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showFullScreen()

        # Create a QVBoxLayout to hold the video widget
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.setLayout(layout)

        # Initialize QVideoWidget
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        # Initialize QMediaPlayer
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # Check if the video file exists
        if not os.path.exists(self.video_path):
            print(f"Video file not found: {self.video_path}")
            self.close()
            return

        # Set the media content
        media = QMediaContent(QUrl.fromLocalFile(self.video_path))
        self.media_player.setMedia(media)

        # Play the video
        self.media_player.play()

        # Loop the video
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def keyPressEvent(self, event):
        # Close screensaver on any key press
        self.close()

    def mouseMoveEvent(self, event):
        # Close screensaver on mouse movement
        self.close()

    def mousePressEvent(self, event):
        # Close screensaver on mouse click
        self.close()

    def mouseReleaseEvent(self, event):
        # Close screensaver on mouse release
        self.close()

    def wheelEvent(self, event):
        # Close screensaver on mouse wheel
        self.close()

    def closeEvent(self, event):
        # Stop the media player when closing
        self.media_player.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    screensaver = ScreensaverWindow()
    screensaver.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
