from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("cnnlstm-gru-i3d-others-onego.h5")

# Classes from training
classes = ["Jumping", "Running", "Sitting", "Standing", "Walking"]  # Modify as per your dataset

def preprocess_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))  # Resize to match model input
        frames.append(frame)

    cap.release()
    
    if len(frames) == 0:
        return None

    frames = np.array(frames) / 255.0  # Normalize
    frames = np.expand_dims(frames, axis=0)  # Model expects batch dimension
    return frames

@app.route('/predict', methods=['POST'])
def predict():
    if 'video' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['video']
    file_path = "temp_video.mp4"
    file.save(file_path)

    video_data = preprocess_video(file_path)
    
    if video_data is None:
        return jsonify({"error": "Invalid video"}), 400

    prediction = model.predict(video_data)
    predicted_class = np.argmax(prediction)

    if prediction.max() < 0.5:  # Confidence threshold
        return jsonify({"action": "Action doesn't match trained classes"})
    
    return jsonify({"action": classes[predicted_class]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render automatically sets PORT
    app.run(host="0.0.0.0", port=port, debug=True)
