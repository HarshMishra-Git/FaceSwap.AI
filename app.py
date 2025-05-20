import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from flask import Flask, render_template, request, jsonify, Response, send_file
import cv2
import uuid
import numpy as np
from face_swap import face_swap
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

source_face = None
anonymize = False
save_faces = False
webcam_active = False
cap = None


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/app')
def main_app():
    return render_template('app.html')


@app.route('/upload-face', methods=['POST'])
def upload_face():
    global source_face
    file = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], f"face_{uuid.uuid4().hex}.jpg")
    file.save(path)
    source_face = cv2.imread(path)
    return jsonify({'status': 'success'})


@app.route('/upload-video', methods=['POST'])
def upload_video():
    global source_face
    file = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], f"video_{uuid.uuid4().hex}.mp4")
    file.save(path)

    cap = cv2.VideoCapture(path)
    width, height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"output_{uuid.uuid4().hex}.mp4")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result = face_swap(source_face, frame)
        out.write(result)

    cap.release()
    out.release()

    try:
        original = VideoFileClip(path)
        edited = VideoFileClip(output_path)
        final = edited.set_audio(original.audio)
        final_path = output_path.replace(".mp4", "_with_audio.mp4")
        final.write_videofile(final_path, codec='libx264', audio_codec='aac')
        return send_file(final_path, as_attachment=True)
    except Exception as e:
        print("Audio merge error:", e)
        return send_file(output_path, as_attachment=True)


@app.route('/toggle-anonymize', methods=['POST'])
def toggle_anonymize():
    global anonymize
    anonymize = not anonymize
    return jsonify({'status': 'success', 'anonymize': anonymize})


@app.route('/toggle-save-faces', methods=['POST'])
def toggle_save_faces():
    global save_faces
    save_faces = not save_faces
    return jsonify({'status': 'success', 'save_faces': save_faces})


@app.route('/start-webcam')
def start_webcam():
    global webcam_active, cap
    if not webcam_active:
        cap = cv2.VideoCapture(0)
        webcam_active = True
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop-webcam')
def stop_webcam():
    global webcam_active, cap
    webcam_active = False
    if cap:
        cap.release()
    return jsonify({'status': 'stopped'})


def gen_frames():
    global cap, webcam_active, source_face
    while webcam_active and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = face_swap(source_face, frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    if cap:
        cap.release()


if __name__ == '__main__':
    app.run(debug=True)
