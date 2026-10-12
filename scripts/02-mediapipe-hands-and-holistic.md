# Experiment 02 — MediaPipe Hand and Holistic Landmarks

After the MNIST classifier, the next step was moving from a static image dataset to real video: extracting structured landmark data from a live webcam feed using MediaPipe.

## Objective

Capture hand, face, and body landmarks from webcam video in real time. This landmark data, not raw pixels, is the representation the final Libras recognition model will eventually be trained on.

## Environment

These scripts run locally (not in Colab), since Colab cannot access a local webcam. A virtual environment was created on the local machine, and the dependencies were installed with:

```
python3 -m venv venv
source venv/bin/activate
pip install opencv-python mediapipe
```

## Hitting a wall: the removed `mp.solutions` API

Most existing MediaPipe tutorials use an API like `mp.solutions.hands.Hands()`. Trying that raised:

```
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

Investigating this error showed that MediaPipe removed the old `mp.solutions` API in its current releases. It was replaced by a new interface called the MediaPipe Tasks API.

Two options were considered: install an older version of MediaPipe (`mediapipe==0.10.21`) to match the old tutorials, or rewrite the code using the current Tasks API. The second option was chosen, since the goal of this project is to be built with actively maintained tools rather than a pinned, outdated dependency.

## The MediaPipe Tasks API

The new API works differently from the old one:

- A model is loaded from a `.task` file (a pretrained model bundle) using `BaseOptions(model_asset_path=...)`.
- Detection runs in `VIDEO` mode, which requires passing an increasing timestamp (in milliseconds) for every frame via `detect_for_video(image, timestamp_ms)`.
- Each frame has to be converted into a `mp.Image` object (`mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)`) instead of being passed as a raw OpenCV array.

The two required model files were downloaded directly from Google's official MediaPipe model storage:

```
curl -L -o models/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

curl -L -o models/holistic_landmarker.task https://storage.googleapis.com/mediapipe-models/holistic_landmarker/holistic_landmarker/float16/latest/holistic_landmarker.task
```

These `.task` files are not committed to this repository (see `.gitignore`), since they are large pretrained binaries that anyone can redownload with the commands above.

## Hand landmarks (`hands_demo.py`)

This script opens the webcam, detects up to two hands per frame, and draws all 21 landmarks per hand as green dots.

Each hand is represented by 21 points, each with `x`, `y` (normalized image coordinates, from 0 to 1) and `z` (relative depth). These 21 points describe the position of each knuckle and fingertip.

## Holistic landmarks (`holistic_demo.py`)

This script uses `HolisticLandmarker`, which detects face, body pose, and both hands at the same time, in a single pass:

- Face landmarks are drawn in blue
- Body pose landmarks are drawn in yellow
- Left hand landmarks are drawn in green
- Right hand landmarks are drawn in red

Holistic detection is closer to what the final system will likely need, since a sign is not only a hand shape: body posture and facial expression can also carry meaning in Libras.

## Open question

The official documentation describes `HolisticLandmarkerResult` as having `face_landmarks`, `pose_landmarks`, `left_hand_landmarks`, and `right_hand_landmarks`, but it was not confirmed from a code example whether each of these is a flat list of points or a nested list (similar to how `hand_landmarks` in the Hands model is a list of hands, each containing a list of points). The code above assumes a flat list. If it throws an error or draws nothing when actually run, the debug line left commented in `holistic_demo.py` (`print(dir(result))`) can be uncommented to inspect the real structure and adjust the loop.

This is documented here on purpose, instead of hidden: figuring out a library's real data shape by inspecting it directly is a normal and expected part of working with any API, not just a mistake to avoid.

## Next steps

With landmark extraction working for both hands and the full body, the next phase of the project is studying CNNs and RNNs/LSTMs, to understand how to go from a sequence of landmark frames to a sign classification.
