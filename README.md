# FaceSwap.AI

FaceSwap.AI is a Python-based AI application designed to perform face swapping not only between two images, but also from an image to a video, and even in real time via a live webcam feed.  
This repository provides two solutions:
- A **desktop GUI application** using **PyQt5**
- A **web application** using **Flask**

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Solution Overview](#solution-overview)
  - [1. PyQt5 Desktop App](#1-pyqt5-desktop-app)
  - [2. Flask Web App](#2-flask-web-app)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Running PyQt5 App](#running-pyqt5-app)
  - [Running Flask Web App](#running-flask-web-app)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- AI-powered face swapping:
  - **Between two images**
  - **From an image to a video**
  - **From an image to a live webcam feed (real-time)**
- User-friendly desktop GUI (PyQt5)
- Simple web interface (Flask)
- Drag-and-drop / file upload support
- Download or save swapped results (image/video/frames)

---

## Demo

<!-- Optionally add demo images, videos, or GIFs here -->

---

## Solution Overview

### 1. PyQt5 Desktop App

The PyQt5 desktop application provides an intuitive graphical interface for face swapping.

**Features:**
- Select source and target images, video files, or live webcam as input
- Swap faces:
  - Between two images
  - From an image onto a video
  - From an image onto live webcam frames (real-time)
- Preview original and swapped results side by side
- Save the swapped image or video locally

**Workflow:**
1. Launch the PyQt5 app.
2. Select the desired mode: Image, Video, or Webcam.
3. Provide the source image and the target (image, video, or webcam).
4. Click the "Swap Faces" button.
5. The swapped result appears in the app; save it if desired.

---

### 2. Flask Web App

The Flask web application allows users to perform face swapping directly from a web browser.

**Features:**
- Upload images or video, or use live webcam (if supported)
- Server-side processing for face swapping
- View and download the swapped image or video in-browser

**Workflow:**
1. Start the Flask server.
2. Visit `http://127.0.0.1:5000/` in your browser.
3. Upload your source image and the target (image, video, or choose webcam if available).
4. The swapped result is displayed and available for download.

---

## Installation

### Prerequisites

- Python 3.7+
- `pip` package manager

### Setup

Clone the repository:
```bash
git clone https://github.com/HarshMishra-Git/FaceSwap.AI.git
cd FaceSwap.AI
```

Install dependencies:
```bash
pip install -r requirements.txt
```
> **Note:** Ensure you have all necessary dependencies for both solutions (PyQt5, Flask, OpenCV, numpy, Pillow, etc.).

---

## Usage

### Running PyQt5 App

```bash
python main.py
```
- Opens the desktop GUI.
- Follow instructions to select images, videos, or webcam and swap faces.

### Running Flask Web App

```bash
python app.py
```
- Starts the web server.
- Open your browser and go to `http://127.0.0.1:5000/`
- Upload images, videos, or use webcam to perform face swapping online.

---

## Project Structure

```
FaceSwap.AI/
├── pyqt_faceswap.py        # PyQt5 desktop application
├── flask_app.py            # Flask web application
├── faceswap_core.py        # Core face swapping logic (shared)
├── static/                 # Static files for Flask (CSS, JS, images)
├── templates/              # HTML templates for Flask
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Contributing

Pull requests and suggestions are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT License](LICENSE)
