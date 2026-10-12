import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

# configure the detector, showing where the file of the model downloaded is
# running_mode=VIDEO because it's processing a sequence of frames
options = vision.HandLandmarkerOptions(
	base_options=BaseOptions(model_asset_path="models/hand_landmarker.task"),
	num_hands=2,
	running_mode=vision.RunningMode.VIDEO
)
detector  = vision.HandLandmarker.create_from_options(options)

webcam = cv2.VideoCapture(0)

# the VIDEO mode requires an increasing "timestamp" for each frame, in miliseconds
frame_counter = 0

while True: 
	# read a message from the webcam
	got_it, image = webcam.read()
	
	if not got_it:
		break

	# opencv read the message as BGR, but mediapipe reads in RGB
	# convert the order of the colors before processing
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# the new api expects an object mp.Image, not an array directly from opencv
	image_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

	#calculates the timestamp assuming 30 frames per second
	timestamp_ms = int(frame_counter * (1000/30))
	result = detector.detect_for_video(image_mp, timestamp_ms)
	frame_counter += 1

	height, width, _ = image.shape

	# draws a green dot in each landmark found, in each hand found
	for hand in result.hand_landmarks:
		for dot in hand:
			x = int(dot.x * width)
			y = int(dot.y * height)
			cv2.circle(image, (x, y), 4, (0, 255, 0), -1)

	# shows the image in a window
	cv2.imshow("Camera", image)

	# if press ESC, exit the loop
	if cv2.waitKey(1) == 27:
		break

webcam.release()
cv2.destroyAllWindows()
