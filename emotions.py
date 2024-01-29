import cv2
from deepface import DeepFace

#Create model
model = DeepFace.build_model("Emotion")

#If error loading model...
if model is None:
    print("Error: Couldn't load emotion detection model.")
    break

emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#Start capturing
videocap = cv2.VideoCapture(0)

#If any camera error...
videocap = cv2.VideoCapture(0)
if not videocap.isOpened():
    print("Error: Couldn't open camera.")
    break

while True:
  ret, frame = videocap.read()
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


  for (x, y, w, h) in faces:
      # Extract the face ROI (Region of Interest)
      face_roi = gray_frame[y:y + h, x:x + w]

      # Resize the face ROI to match the input shape of the model
      resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)

      # Normalize the resized face image
      normalized_face = resized_face / 255.0

      # Reshape the image to match the input shape of the model
      reshaped_face = normalized_face.reshape(1, 48, 48, 1)
      
      # Predict emotions using the pre-trained model
      preds = model.predict(reshaped_face)[0]
      emotion_idx = preds.argmax()
      emotion = emotion_labels[emotion_idx]
      
      # Draw rectangle around face and label with predicted emotion
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
      cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

      # Display the resulting frame
      cv2.imshow('Real-time Emotion Detection', frame)

      #Press 'q' to quit
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break
      
      videocap.release()
      cv2.destroyAllWindows()
   