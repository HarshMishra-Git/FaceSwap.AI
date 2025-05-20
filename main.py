
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from face_swap import face_swap


class FaceSwapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Face Swap - High Accuracy')
        self.setFixedSize(1280, 720)

        main_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        self.video_label = QtWidgets.QLabel()
        self.video_label.setFixedSize(960, 540)
        self.video_label.setStyleSheet("background-color: black;")

        self.btn_load_face = QtWidgets.QPushButton("Load Source Face")
        self.btn_load_video = QtWidgets.QPushButton("Load Video")
        self.btn_start_webcam = QtWidgets.QPushButton("Start Webcam")
        self.btn_stop_webcam = QtWidgets.QPushButton("Stop Webcam")
        self.btn_toggle_anonymize = QtWidgets.QPushButton("Toggle Anonymize: OFF")
        self.btn_toggle_theme = QtWidgets.QPushButton("Toggle Theme: Light")
        self.btn_toggle_save = QtWidgets.QPushButton("Save Frames: OFF")
        self.btn_stop_webcam.setEnabled(False)

        button_layout.addWidget(self.btn_load_face)
        button_layout.addWidget(self.btn_load_video)
        button_layout.addWidget(self.btn_start_webcam)
        button_layout.addWidget(self.btn_stop_webcam)
        button_layout.addWidget(self.btn_toggle_anonymize)
        button_layout.addWidget(self.btn_toggle_theme)
        button_layout.addWidget(self.btn_toggle_save)

        main_layout.addWidget(self.video_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.source_face = None
        self.capture = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_webcam = False
        self.anonymize = False
        self.save_faces = False
        self.output_writer = None
        self.video_path = None
        self.frame_count = 0
        self.dark_mode = False

        self.btn_load_face.clicked.connect(self.load_source_face)
        self.btn_load_video.clicked.connect(self.load_video)
        self.btn_start_webcam.clicked.connect(self.start_webcam)
        self.btn_stop_webcam.clicked.connect(self.stop_webcam)
        self.btn_toggle_anonymize.clicked.connect(self.toggle_anonymize)
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)
        self.btn_toggle_save.clicked.connect(self.toggle_save_faces)

    def load_source_face(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Source Face Image', '', 'Image Files (*.jpg *.jpeg *.png)')
        if fname:
            img = cv2.imread(fname)
            if img is None:
                QMessageBox.warning(self, "Error", "Failed to load image.")
                return
            self.source_face = img
            QMessageBox.information(self, "Source Face Loaded", "Source face image loaded successfully.")

    def load_video(self):
        if self.capture:
            self.capture.release()
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '', 'Video Files (*.mp4 *.avi *.mov)')
        if fname:
            self.capture = cv2.VideoCapture(fname)
            if not self.capture.isOpened():
                QMessageBox.warning(self, "Error", "Could not open video file.")
                return

            self.video_path = fname
            self.is_webcam = False

            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.capture.get(cv2.CAP_PROP_FPS) or 20.0

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.output_writer = cv2.VideoWriter('output_face_swapped.avi', fourcc, fps, (width, height))

            self.btn_stop_webcam.setEnabled(True)
            self.btn_start_webcam.setEnabled(False)
            self.timer.start(int(1000 // fps))

    def start_webcam(self):
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            QMessageBox.warning(self, "Error", "Cannot access webcam.")
            return
        self.is_webcam = True
        self.output_writer = cv2.VideoWriter('output_webcam.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (960, 540))
        self.btn_stop_webcam.setEnabled(True)
        self.btn_start_webcam.setEnabled(False)
        self.timer.start(30)

    def stop_webcam(self):
        self.timer.stop()
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.output_writer:
            self.output_writer.release()
            self.output_writer = None
        self.btn_start_webcam.setEnabled(True)
        self.btn_stop_webcam.setEnabled(False)
        self.video_label.clear()

    def toggle_anonymize(self):
        self.anonymize = not self.anonymize
        status = "ON" if self.anonymize else "OFF"
        self.btn_toggle_anonymize.setText(f"Toggle Anonymize: {status}")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("background-color: #1e1e1e; color: white;")
            self.btn_toggle_theme.setText("Toggle Theme: Dark")
        else:
            self.setStyleSheet("")
            self.btn_toggle_theme.setText("Toggle Theme: Light")

    def toggle_save_faces(self):
        self.save_faces = not self.save_faces
        status = "ON" if self.save_faces else "OFF"
        self.btn_toggle_save.setText(f"Save Frames: {status}")

    def update_frame(self):
        if not self.capture:
            return

        if self.is_webcam:
            ret, frame = self.capture.read()
        else:
            ret, frame = self.capture.read()
            if not ret:
                self.timer.stop()
                if self.capture:
                    self.capture.release()
                if self.output_writer:
                    self.output_writer.release()
                    self.output_writer = None

                if not self.is_webcam and self.video_path:
                    try:
                        from moviepy.editor import VideoFileClip
                        orig = VideoFileClip(self.video_path)
                        edited = VideoFileClip("output_face_swapped.avi")
                        final = edited.set_audio(orig.audio)
                        final.write_videofile("output_with_audio.mp4", codec='libx264', audio_codec='aac')
                        print("✅ Audio merged into final output.")
                    except Exception as e:
                        print("Audio merge error:", e)
                return

        if frame is None:
            return

        height, width = frame.shape[:2]

        if self.source_face is not None and self.source_face.shape[:2] != (height, width):
            resized_face = cv2.resize(self.source_face, (width, height))
        else:
            resized_face = self.source_face

        try:
            if resized_face is not None or self.anonymize:
                swapped = face_swap(resized_face, frame, anonymize=self.anonymize, save_faces=self.save_faces)
            else:
                swapped = frame
        except Exception as e:
            print(f"Face swap error: {e}")
            swapped = frame

        if self.output_writer:
            self.output_writer.write(cv2.resize(swapped, (960, 540)))

        frame_rgb = cv2.cvtColor(cv2.resize(swapped, (960, 540)), cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0],
                           frame_rgb.strides[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_label.setPixmap(pix.scaled(self.video_label.size(), QtCore.Qt.KeepAspectRatio))


    def closeEvent(self, event):
        self.stop_webcam()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FaceSwapApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
