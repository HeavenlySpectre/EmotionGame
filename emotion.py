import cv2
from deepface import DeepFace
import random # For randomly selecting target emotions
import time # For a brief pause/message display

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- Emoticon Loading ---
emoticons = {}
emoticon_files = {
    "happy": "happy.png",
    "sad": "sad.png",
    "fear": "fear.png",
    "angry": "angry.png",
    "surprise": "surprised.png",
    "neutral": "neutral_emoji.png",
    "disgust": "disgust_emoji.png"
}
default_emoticon_file = "middle_finger.png" # Or a more neutral default like "question_mark.png"

for emotion_name, filename in emoticon_files.items():
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    if img is not None:
        emoticons[emotion_name] = img
    else:
        print(f"Warning: {filename} for emotion '{emotion_name}' not found. Will use default if this emotion is detected.")

default_emoticon_img = cv2.imread(default_emoticon_file, cv2.IMREAD_UNCHANGED)
if default_emoticon_img is None:
    print(f"Warning: {default_emoticon_file} not found. No default emoticon will be shown if an unknown emotion is detected.")


# --- Emoticon Overlay Function ---
def overlay_emoticon(frame, emoticon_img, x, y, w, h):
    if emoticon_img is None:
        return

    try:
        emoticon_resized = cv2.resize(emoticon_img, (w, h))

        if emoticon_resized.shape[2] == 4:  # Image has an alpha channel
            alpha_s = emoticon_resized[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                frame_roi = frame[y:y+h, x:x+w, c]
                emoticon_channel = emoticon_resized[:, :, c]
                frame[y:y+h, x:x+w, c] = (alpha_s * emoticon_channel +
                                          alpha_l * frame_roi)
        elif emoticon_resized.shape[2] == 3: # Image is BGR (no alpha)
            frame[y:y+h, x:x+w] = emoticon_resized
        # else:
            # print(f"Warning: Emoticon image has an unexpected number of channels: {emoticon_resized.shape[2]}")

    except Exception as e:
        print(f"Error during emoticon overlay: {e} (ROI: x={x},y={y},w={w},h={h}, Frame Shape: {frame.shape}, Emoticon Shape: {emoticon_img.shape if emoticon_img is not None else 'None'})")


# --- Game Variables ---
GAME_EMOTIONS = ["happy", "sad", "surprise"]
target_emotion = None
score = 0
current_emotion_duration = 0
TARGET_HOLD_FRAMES = 10
game_round_active = False
feedback_message = "Press 's' to start the game!"
message_display_time = 0
game_started_ever = False

# Start capturing video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# FPS calculation variables
fps_start_time = time.time()
fps_frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS calculation
    fps_frame_count += 1
    if (time.time() - fps_start_time) > 1: # every second
        fps = fps_frame_count / (time.time() - fps_start_time)
        cv2.putText(frame, f"FPS: {fps:.2f}", (frame.shape[1] - 150, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        fps_start_time = time.time()
        fps_frame_count = 0


    # --- Game Round Management ---
    key = cv2.waitKey(1) & 0xFF

    if not game_started_ever and not game_round_active:
        if key == ord('s'):
            game_started_ever = True
            game_round_active = False
            feedback_message = ""
        cv2.putText(frame, "Press 's' to start the game!", (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if game_started_ever and not game_round_active and (target_emotion is None or time.time() > message_display_time):
        target_emotion = random.choice(GAME_EMOTIONS)
        current_emotion_duration = 0
        feedback_message = f"Show a {target_emotion.upper()} face!"
        game_round_active = True

    # Convert frame to grayscale FOR HAAR CASCADE FACE DETECTION ONLY
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    detected_emotion_this_frame = None

    for (x, y, w, h) in faces:
        # Ensure ROI coordinates are valid and within frame boundaries
        if x < 0 or y < 0 or x + w > frame.shape[1] or y + h > frame.shape[0]:
            continue # Skip this face if ROI is out of bounds

        # Extract the face ROI (Region of Interest) FROM THE ORIGINAL COLOR FRAME
        face_roi_color = frame[y:y + h, x:x + w]

        # Check if ROI is valid (not empty)
        if face_roi_color.size == 0:
            continue

        try:
            # Perform emotion analysis on the COLOR face ROI
            result = DeepFace.analyze(face_roi_color, actions=['emotion'], enforce_detection=False, silent=True)
            
            if isinstance(result, list) and len(result) > 0:
                emotion_data = result[0]
                dominant_emotion = emotion_data['dominant_emotion']
                detected_emotion_this_frame = dominant_emotion

                # --- Game Logic ---
                if game_round_active:
                    if dominant_emotion == target_emotion:
                        current_emotion_duration += 1
                        if current_emotion_duration < TARGET_HOLD_FRAMES:
                             feedback_message = f"Keep holding {target_emotion.upper()}! ({current_emotion_duration}/{TARGET_HOLD_FRAMES})"
                        
                        if current_emotion_duration >= TARGET_HOLD_FRAMES:
                            score += 10
                            feedback_message = f"GREAT! +10 Points for {target_emotion.upper()}!"
                            game_round_active = False
                            message_display_time = time.time() + 2
                    else:
                        current_emotion_duration = 0
                        feedback_message = f"Not {dominant_emotion}. Show: {target_emotion.upper()}"
            # else:
                # print("DeepFace result format unexpected or empty.")


        except Exception as e:
            # print(f"Error in DeepFace analysis for face at ({x},{y},{w},{h}): {e}")
            detected_emotion_this_frame = None

        # --- Emoji Overlay ---
        if detected_emotion_this_frame:
            emoticon_to_show = emoticons.get(detected_emotion_this_frame, default_emoticon_img)
            if emoticon_to_show is not None:
                 overlay_emoticon(frame, emoticon_to_show, x, y, w, h)


    if game_started_ever and game_round_active and len(faces) == 0:
        current_emotion_duration = 0
        feedback_message = f"Face not found. Show: {target_emotion.upper()}"

    # --- UI Display for Game ---
    if game_started_ever:
        if target_emotion:
            cv2.putText(frame, f"Target: {target_emotion.upper()}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.putText(frame, f"Score: {score}", (frame.shape[1] - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        meter_width = 200
        meter_height = 25
        meter_x = 10
        meter_y = 50
        
        fill_percentage = max(0, min(1, current_emotion_duration / TARGET_HOLD_FRAMES if TARGET_HOLD_FRAMES > 0 else 0))
        fill_width = int(fill_percentage * meter_width)

        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + meter_width, meter_y + meter_height), (50, 50, 50), -1)
        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + fill_width, meter_y + meter_height), (0, 255, 0), -1)
        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + meter_width, meter_y + meter_height), (255, 255, 255), 2)

        if feedback_message:
            text_color = (0, 255, 0) if "GREAT" in feedback_message else (0, 255, 255) if "Keep" in feedback_message else (0, 0, 255)
            cv2.putText(frame, feedback_message, (10, frame.shape[0] - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2, cv2.LINE_AA)

    cv2.imshow('Emotion-Meter Game (Press "s" to start, "q" to quit)', frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()