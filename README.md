# FaceSwap.AI

FaceSwap.AI is a Python-based AI application designed to perform face swapping between two images. This repository provides two solutions:
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

- AI-powered face swapping between two images
- User-friendly desktop GUI (PyQt5)
- Simple web interface (Flask)
- Drag and drop / file upload support
- Download or save the swapped image

---

## Demo

---

## Solution Overview

### 1. PyQt5 Desktop App

The PyQt5 desktop application provides an intuitive graphical interface for face swapping.

**Features:**
- Select source and target images from your computer
- Preview original and swapped images side by side
- Swap faces with a single click
- Save the swapped image locally

**Workflow:**
1. Launch the PyQt5 app.
2. Select the source and target images.
3. Click the "Swap Faces" button.
4. The swapped image appears in the app. Save it if desired.

---

### 2. Flask Web App

The Flask web application allows users to perform face swapping directly from a web browser.

**Features:**
- Upload two images via a web form
- Server-side processing for face swapping
- View and download the swapped image in-browser

**Workflow:**
1. Start the Flask server.
2. Visit `http://127.0.0.1:5000/` in your browser.
3. Upload the two images.
4. The swapped image is displayed for download.

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
- This opens the desktop GUI.
- Follow instructions to select images and swap faces.

### Running Flask Web App

```bash
python app.py
```
- This starts the web server.
- Open your browser and go to `http://127.0.0.1:5000/`
- Upload images and perform face swapping online.

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

---
