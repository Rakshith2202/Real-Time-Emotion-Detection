import tensorflow
from tensorflow import keras
from keras.models import load_model
from time import sleep
from keras.preprocessing import image
from keras.utils import img_to_array
import cv2 
import numpy as np

face_classifier = cv2.CascadeClassifier(r'C:\Users\91886\Desktop\Machine Learning\ML and DL Projects\Real-time emotion recognition\haarcascade_frontalface_default.xml')
classifier =load_model(r'C:\Users\91886\Desktop\Machine Learning\ML and DL Projects\Real-time emotion recognition\main_model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in faces:
        #Here we are extracting the region of interest
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray])!=0: #This is done to take care if there is no face detected in the web cam.
            roi = roi_gray.astype('float')/255.0 #normalizing the pixels of the roi between 0 and 1
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()