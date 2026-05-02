import cv2
import mediapipe as mp
import os

def validate_face_presence(video_path: str) -> dict:
    if not os.path.exists(video_path):
        return {"passed": False, "face_presence_ratio": 0.0, "error": "Video file not found"}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"passed": False, "face_presence_ratio": 0.0, "error": "Could not open video file"}

    # Get FPS and compute frame step to sample at ~2 fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0  # fallback
    
    frame_step = max(1, int(fps / 2))
    
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    total_frames_checked = 0
    frames_with_face = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_step == 0:
            total_frames_checked += 1
            
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)
            
            if results.detections:
                frames_with_face += 1
                
        frame_count += 1

    cap.release()
    face_detection.close()

    if total_frames_checked == 0:
        return {"passed": False, "face_presence_ratio": 0.0, "error": "No frames to process"}

    ratio = frames_with_face / total_frames_checked
    return {
        "passed": ratio >= 0.6,
        "face_presence_ratio": round(ratio, 2),
        "total_frames_checked": total_frames_checked,
        "frames_with_face": frames_with_face
    }
