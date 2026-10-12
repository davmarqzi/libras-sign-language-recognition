import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

# configures the holistic detector, pointing to the file of the downloaded model
options = vision.HolisticLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="models/holistic_landmarker.task"),
    running_mode=vision.RunningMode.VIDEO
)
detector = vision.HolisticLandmarker.create_from_options(options)

webcam = cv2.VideoCapture(0)
frame_counter = 0

while True:
    got_it, image = webcam.read()
    if not got_it:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    timestamp_ms = int(frame_counter * (1000 / 30))
    result = detector.detect_for_video(image_mp, timestamp_ms)
    frame_counter += 1

    height, width, _ = image.shape

    # Debug fallback: if nothing gets drawn, or you get an AttributeError,
    # uncomment the line below to inspect the real shape of "result"
    # print(dir(result))

    # face, blue dots, really tiny because they're many (478 dots)
    if result.face_landmarks:
        for dot in result.face_landmarks:
            x = int(dot.x * width)
            y = int(dot.y * height)
            cv2.circle(image, (x, y), 1, (255, 0, 0), -1)  # blue

    # body, yellow dots
    if result.pose_landmarks:
        for dot in result.pose_landmarks:
            x = int(dot.x * width)
            y = int(dot.y * height)
            cv2.circle(image, (x, y), 3, (0, 255, 255), -1)  # yellow

    # left hand, green dots  
    if result.left_hand_landmarks:
        for dot in result.left_hand_landmarks:
            x = int(dot.x * width)
            y = int(dot.y * height)
            cv2.circle(image, (x, y), 4, (0, 255, 0), -1)  # green

    # right hand, red dots   
    if result.right_hand_landmarks:
        for dot in result.right_hand_landmarks:
            x = int(dot.x * width)
            y = int(dot.y * height)
            cv2.circle(image, (x, y), 4, (0, 0, 255), -1)  # red

    cv2.imshow("Camera", image)
    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
