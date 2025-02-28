import depthai as dai
import cv2
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
import threading
import time

# Known faces dictionary with names and corresponding image paths
known_faces = {
    "Noah": "/home/pi/assets/Noah.jpg"
}

# Dictionary to store precomputed face encodings
known_encodings = {}

# Load known face encodings during startup
for name, img_path in known_faces.items():
    try:
        embedding = DeepFace.represent(img_path, enforce_detection=False)[0]["embedding"]
        known_encodings[name] = np.array(embedding)
        print(f"Successfully loaded reference image for {name}")
    except Exception as e:
        print(f"Error loading reference image: {e}")

# Create DepthAI pipeline
pipeline = dai.Pipeline()

# Create and configure the color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(320, 240)  # Lower resolution for faster processing
cam_rgb.setInterleaved(False)

# Create output stream
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

# Function to process face recognition in a separate thread
def process_face_recognition(frame, known_encodings):
    try:
        # Detect faces using DeepFace's face detection only
        faces = DeepFace.extract_faces(frame, detector_backend="opencv", enforce_detection=False)
        
        # Process each detected face
        for face in faces:
            x = face["facial_area"]["x"]
            y = face["facial_area"]["y"]
            w = face["facial_area"]["w"]
            h = face["facial_area"]["h"]
            
            # Ensure the face region is within the frame boundaries
            if x >= 0 and y >= 0 and x + w <= frame.shape[1] and y + h <= frame.shape[0]:
                face_img = frame[y:y+h, x:x+w]
                
                try:
                    # Get the embedding for the detected face
                    embedding = DeepFace.represent(face_img, enforce_detection=False)[0]["embedding"]
                    
                    # Initialize variables for face matching
                    matched_name = "Unknown"
                    max_similarity = -1  # Cosine similarity ranges from -1 to 1
                    
                    # Compare the detected face with known faces using cosine similarity
                    for name, known_emb in known_encodings.items():
                        similarity = cosine_similarity([embedding], [known_emb])[0][0]
                        if similarity > max_similarity and similarity > 0.6:  # Threshold for matching
                            max_similarity = similarity
                            matched_name = name
                    
                    # Set the color and text based on whether a match was found
                    if matched_name != "Unknown":
                        color = (0, 255, 0)  # Green
                        text = matched_name
                    else:
                        color = (0, 0, 255)  # Red
                        text = "Unknown"
                    
                    # Draw rectangle and text on the frame
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, text, (x, y - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                except Exception as e:
                    print(f"Recognition error: {e}")
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                
    except Exception as e:
        print(f"Detection error: {e}")

# Start the pipeline and connect to the device
with dai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb", 4, False)
    
    frame_counter = 0
    skip_frames = 2  # Process every Nth frame
    
    # Allow camera to warm up
    print("Warming up camera...")
    time.sleep(2)
    
    while True:
        # Get the frame from the camera
        frame = q_rgb.get().getCvFrame()
        
        # Process every Nth frame
        if frame_counter % skip_frames == 0:
            # Use threading to offload face recognition
            threading.Thread(target=process_face_recognition, args=(frame, known_encodings)).start()
        
        # Display the frame
        cv2.imshow("Face Recognition", frame)
        
        # Increment frame counter
        frame_counter += 1
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Release resources
cv2.destroyAllWindows()
