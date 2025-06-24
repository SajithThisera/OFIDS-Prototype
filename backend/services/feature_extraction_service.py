import os
import numpy as np
from transformers import VideoMAEFeatureExtractor, VideoMAEForVideoClassification
import cv2
import torch

def load_video_clips_with_videomae_features(video_path, max_frames=16):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    frame_rate = 1  # You may adjust for your FPS

    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_rate == 0:
            resized_frame = cv2.resize(frame, (224, 224))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb_frame)
        frame_count += 1
    cap.release()
    if len(frames) < max_frames and frames:
        frames += [frames[-1]] * (max_frames - len(frames))
    if not frames:
        return np.zeros((1, 2))
    # Load model/feature extractor ONCE per request
    extractor = VideoMAEFeatureExtractor()
    model = VideoMAEForVideoClassification.from_pretrained("MCG-NJU/videomae-base").to("cpu")
    inputs = extractor(frames, return_tensors="pt").to("cpu")
    with torch.no_grad():
        outputs = model(**inputs)
    features = outputs.logits.cpu().numpy()
    return features

def extract_features_from_uploads(upload_dir):
    features = []
    labels = []
    for fname in os.listdir(upload_dir):
        if fname.lower().endswith('.avi'):
            video_path = os.path.join(upload_dir, fname)
            video_features = load_video_clips_with_videomae_features(video_path)
            # Option 1: Use logits as feature (e.g. shape (1,2)), flatten for stacking
            features.append(video_features.flatten())
            label = 0 if fname.startswith('N') else 1
            labels.append(label)
    features = np.array(features)
    labels = np.array(labels)
    return features, labels
