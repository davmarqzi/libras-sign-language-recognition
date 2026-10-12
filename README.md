# Brazilian Sign Language Recognition

> An experimental machine learning project exploring computer vision and temporal modeling for real-time Brazilian Sign Language (Libras) recognition.

## Overview

This project explores the development of a real-time Brazilian Sign Language (Libras) recognition system using computer vision and machine learning.

The long-term goal is to build a system capable of analyzing visual information from a webcam, extracting relevant features from the hands, face, and body, and recognizing signs in real time.

The project is being developed progressively, starting with fundamental machine learning experiments and moving toward computer vision, landmark extraction, temporal modeling, and eventually a real-time recognition system.

## Motivation

Communication is a fundamental part of human interaction, yet language barriers can make communication difficult between people who use different languages or communication systems.

This project was created as an independent learning and research project to explore how machine learning and computer vision can be applied to Brazilian Sign Language.

Beyond building a final application, the project is also an opportunity to study the complete process of developing a machine learning system: understanding the problem, collecting and processing data, selecting appropriate representations, training models, evaluating their performance, analyzing errors, and integrating the model into a real-time application.

## Project Status

**Early development**

The project is currently in the learning and experimentation stage. The first experiments focus on understanding the fundamental machine learning workflow before applying it to sign language recognition.

### Completed

- [x] Learned the basic machine learning workflow
- [x] Loaded and explored the MNIST dataset
- [x] Created training, validation, and test sets
- [x] Built a simple neural network classifier
- [x] Compiled the model using Adam and sparse categorical cross-entropy
- [x] Trained the model
- [x] Evaluated the model on unseen test data
- [x] Generated predictions
- [x] Compared predictions with ground-truth labels
- [x] Performed basic error analysis
- [x] Visualized incorrect predictions
- [x] Learned MediaPipe
- [x] Captured hand landmarks from a webcam
- [x] Understood the 21 hand landmarks
- [x] Explored landmark coordinates
- [x] Experimented with MediaPipe Holistic

### In Progress

- [ ] Study CNN-based image classification
- [ ] Study RNN/LSTM-based sequence classification
- [ ] Explore combined spatial and temporal modeling

### Planned

- [ ] Build a landmark-based dataset
- [ ] Collect Brazilian Sign Language examples
- [ ] Design the first sign classification model
- [ ] Train and evaluate the model
- [ ] Analyze classification errors
- [ ] Build a real-time recognition pipeline
- [ ] Integrate the model into a usable application
- [ ] Document the final system and results

## Learning Path

```
Machine Learning Fundamentals
            ↓
       MNIST Experiment
            ↓
      Computer Vision
            ↓
         MediaPipe
            ↓
    Hand Landmark Data
            ↓
            CNN
            ↓
        RNN / LSTM
            ↓
 Spatial + Temporal Modeling
            ↓
  Libras Dataset Collection
            ↓
    Sign Classification
            ↓
   Real-Time Recognition
```

The initial MNIST experiment is intentionally separate from the final Libras system. Its purpose is to understand the complete machine learning workflow before working with more complex real-world data.

## Preliminary Experiment: MNIST

Before working directly with Brazilian Sign Language data, a simple neural network was trained on the MNIST handwritten-digit dataset, to practice the complete machine learning pipeline (training, validation, testing, prediction, and error analysis) on a controlled, well-understood problem.

The model reached approximately 97.74% test accuracy. Full details, architecture, and error analysis are documented in [`notebooks/01-mnist-classifier.md`](notebooks/01-mnist-classifier.md).

MNIST is not part of the final Libras recognition system; it was a first experiment to learn the fundamental workflow before introducing the additional complexity of real-time video and human movement.

## Hand and Holistic Landmark Detection

The next step after MNIST was extracting structured information from live video instead of static images:

```
Webcam
   ↓
Video Frames
   ↓
MediaPipe
   ↓
Hand / Face / Pose Landmarks
   ↓
Structured Numerical Data
   ↓
Machine Learning Model
```

Two scripts were built using the current MediaPipe Tasks API: `scripts/hands_demo.py`, which detects up to two hands per frame and draws their 21 landmarks each (x, y, z coordinates), and `scripts/holistic_demo.py`, which detects face, body pose, and both hands at the same time.

Building these also meant dealing with a real compatibility problem: the `mp.solutions` API used in most MediaPipe tutorials has been removed from current MediaPipe releases, and the scripts were written against the newer Tasks API instead of pinning to an older version. Full details, including that debugging process and an open question about the exact shape of the Holistic model's output, are documented in [`scripts/02-mediapipe-hands-and-holistic.md`](scripts/02-mediapipe-hands-and-holistic.md).

MediaPipe provides 21 landmarks for each detected hand, each with spatial coordinates (x, y, z). This representation allows the project to work with structured information about hand position and movement rather than directly processing raw video frames.

## Spatial and Temporal Modeling

A major challenge of sign language recognition is that a sign is not always defined by a single static hand position; movement over time can contain important information. This motivates studying two types of models: CNNs for spatial patterns in a single frame, and RNNs/LSTMs for sequences where the order of observations over time matters. The project will investigate how these two forms of information can be combined for sign recognition.

## Roadmap

**Phase 1 — Machine Learning Fundamentals**
- Train a basic MNIST classifier
- Understand training, validation, and testing
- Understand model evaluation, generate predictions, analyze errors

**Phase 2 — Computer Vision**
- Install OpenCV and MediaPipe
- Capture webcam video, detect hands, visualize landmarks
- Explore MediaPipe Holistic

**Phase 3 — Machine Learning for Movement**
- Study CNNs, RNNs, LSTMs
- Understand spatial vs. temporal information
- Explore spatial + temporal architectures

**Phase 4 — Dataset**
- Define initial sign vocabulary
- Design data collection process, collect and label landmark sequences
- Split data into training, validation, and test sets

**Phase 5 — Sign Recognition Model**
- Build, train, and evaluate the first classifier
- Analyze errors, iterate on architecture and dataset

**Phase 6 — Real-Time System**
- Connect webcam input to the trained model
- Real-time landmark extraction and prediction
- Improve robustness and latency

**Phase 7 — Final Application**
- Build the final interface
- Document the system, evaluate real-world performance, record limitations

## Technologies

- Python
- TensorFlow / Keras
- NumPy
- Matplotlib
- OpenCV
- MediaPipe

## Repository Structure

```
libras-sign-language-recognition/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── notebooks/
│   ├── 01-mnist-classifier.ipynb
│   └── 01-mnist-classifier.md
│
└── scripts/
    ├── hands_demo.py
    ├── holistic_demo.py
    └── 02-mediapipe-hands-and-holistic.md
```

The `models/` folder (where the downloaded MediaPipe model bundles live) is intentionally not committed to the repository; see `scripts/02-mediapipe-hands-and-holistic.md` for the download commands.

The repository structure will evolve as new experiments and components are developed.

## Limitations

This project is currently an experimental and educational project. The current implementation does not yet provide Brazilian Sign Language translation or recognition. The project is still in development, and future stages will determine how accurately signs can be recognized under different conditions.

## Author

Davi, independent student researcher and developer. This project is being developed as an independent passion project focused on machine learning, computer vision, and Brazilian Sign Language recognition.
