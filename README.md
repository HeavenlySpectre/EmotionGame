
# ReactiFace: The Emotion-Meter Game

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-OpenCV_&_DeepFace-orange.svg)

ReactiFace is an interactive Python-based game that uses your webcam to analyze your facial expressions in real-time. The game challenges you to match a randomly selected emotion, turning cutting-edge computer vision technology into a fun and engaging experience.


*(This is a placeholder GIF. You can create one of your own gameplay using a screen recorder like ScreenToGif or Kap.)*

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [How to Run the Game](#how-to-run-the-game)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Code Walkthrough](#code-walkthrough)
- [Troubleshooting](#troubleshooting)

---

## Features

-   **Real-time Face Detection**: Utilizes OpenCV's Haar Cascade classifier to detect faces from a live webcam feed.
-   **Deep Learning Emotion Analysis**: Leverages the `deepface` library to accurately identify the dominant emotion (happy, sad, surprise, angry, etc.).
-   **Interactive Gamification**: Challenges players with a target emotion and a "hold meter" that must be filled to score points.
-   **Live Feedback System**: Provides on-screen instructions, a dynamic score, and a progress bar.
-   **Dynamic Emoticon Overlay**: Overlays a fun emoticon corresponding to the detected emotion onto the user's face for instant visual feedback.
-   **Performance Metrics**: Displays the current Frames Per Second (FPS) to monitor performance.

---

## Technologies Used

-   **Python 3.8+**
-   **OpenCV (`opencv-python`)**: For all computer vision tasks, including video capture, face detection, and image manipulation.
-   **DeepFace**: A powerful, lightweight facial recognition and analysis library for Python. It acts as a wrapper for state-of-the-art models like VGG-Face, Google FaceNet, and Facebook DeepFace.
-   **TensorFlow (`tf_keras`)**: The primary backend used by `deepface` for running the deep learning models.

---

## Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Prerequisites

-   Python 3.8 or newer
-   `pip` package installer
-   A webcam connected to your computer

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/reactiface-game.git
cd reactiface-game
```

### 3. Create a Virtual Environment (Recommended)

It's best practice to create a virtual environment to manage project-specific dependencies.

-   **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
-   **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 4. Install Dependencies

Install all the required libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**Note:** The `deepface` library will download pre-trained model weights on its first run. This may take some time and requires an internet connection.

### 5. Add Emoticon Assets

The application requires `.png` image files for the emoticons. Make sure the following files are present in the root directory of the project:
- `happy.png`
- `sad.png`
- `fear.png`
- `angry.png`
- `surprised.png`
- `neutral_emoji.png`
- `disgust_emoji.png`
- `middle_finger.png` (or any other default image)

---

## How to Run the Game

Once the setup is complete, you can run the application with a single command:

```bash
python emotion.py
```

A window will open showing your webcam feed.

---

## How to Play

1.  **Start the Game**: Press the **`s`** key to begin.
2.  **Check the Target**: Look at the top-left corner of the screen to see the `Target` emotion (e.g., `HAPPY`).
3.  **Make the Face**: Try to make the facial expression corresponding to the target emotion.
4.  **Hold the Expression**: If you're showing the correct emotion, a green progress bar will start to fill. Keep holding the expression until the bar is full.
5.  **Score Points**: Once the bar is full, you'll earn 10 points, and a new round will begin with a new target emotion.
6.  **Quit**: Press the **`q`** key at any time to close the game.

---

## Project Structure

```
.
├── emotion.py              # Main application script
├── requirements.txt        # Python dependencies
├── happy.png               # Emoticon assets
├── sad.png
├── fear.png
├── angry.png
├── surprised.png
├── neutral_emoji.png
├── disgust_emoji.png
└── middle_finger.png       # Default emoticon asset
```

---

## Code Walkthrough

The `emotion.py` script is organized as follows:

1.  **Imports and Initializations**:
    -   Libraries like `cv2`, `deepface`, `time`, and `random` are imported.
    -   The Haar Cascade classifier for face detection is loaded.
    -   Emoticon images are loaded into a dictionary. A default is set for unhandled cases.

2.  **`overlay_emoticon()` Function**:
    -   This function handles placing the emoticon image on top of the detected face.
    -   It supports transparency (alpha channel) in `.png` files to blend the emoticon smoothly with the video frame.

3.  **Game Variables**:
    -   Constants and variables for game state management are defined here (`GAME_EMOTIONS`, `score`, `target_emotion`, etc.).

4.  **Main Game Loop (`while True`)**:
    -   **Frame Capture**: Reads a new frame from the webcam.
    -   **Game State Management**: Checks for keyboard input (`s` to start, `q` to quit) and manages the start/end of rounds.
    -   **Face Detection**: Converts the frame to grayscale (for performance) and uses the Haar Cascade classifier to find faces.
    -   **Emotion Analysis**:
        -   For each detected face, a Region of Interest (ROI) is cropped from the **original color frame**.
        -   The color ROI is passed to `DeepFace.analyze()`. `enforce_detection=False` is used because we've already detected a face.
    -   **Game Logic**:
        -   Compares the `dominant_emotion` with the `target_emotion`.
        -   Updates the `current_emotion_duration` counter and the `feedback_message`.
        -   Awards points and resets the round if the expression is held long enough.
    -   **UI Rendering**:
        -   The emoticon overlay is applied.
        -   Text for the score, target emotion, feedback messages, and the progress bar are drawn onto the frame using `cv2.putText()` and `cv2.rectangle()`.
    -   **Display**: The final, annotated frame is shown to the user.

---

## Troubleshooting

-   **"IOError: Cannot open webcam"**: Ensure your webcam is connected properly and not being used by another application. You might need to change the `cv2.VideoCapture(0)` index to `1` or higher if you have multiple cameras.
-   **Slow Performance / Low FPS**: Emotion analysis is computationally expensive. Running on a machine with a less powerful CPU will result in lower FPS. Try reducing the webcam resolution or closing other demanding applications.
-   **`deepface` Installation Issues**: The library has many dependencies, including specific versions of TensorFlow. If `pip install -r requirements.txt` fails, try installing the libraries one by one to identify the problematic package.
-   **"Warning: ... not found"**: This message appears if the emoticon `.png` files are missing from the project's root directory. Make sure all required images are present.

---
