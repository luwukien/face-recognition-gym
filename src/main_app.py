import face_recognition
import pickle
import cv2
import pandas as pd
import numpy as np

#Loading file encodings.pickle
pickle_file_path = '/home/luwukien/Project/Personal/VisionGym/encodings.pickle'
try:  
  with open(pickle_file_path, "rb") as f:
    data = pickle.load(f)
except FileNotFoundError:
  print(f"Error: The file '{pickle_file_path}' was not found.")
except Exception as e:
  print(f"An error occurred while loading the pickle file: {e}")

#Loading members list from file .csv
df_members = pd.read_csv("/home/luwukien/Project/Personal/VisionGym/data/members.csv", index_col="Mã hội viên")

#Initialize webcamcvtColor
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
  ret, frame = cap.read()
  #Read a frame from webcam
  #ret is a boolean variable. If it read a frame, it could return true. 
  if not ret:
    print("[ERROR] Cannot read frame from webcam. End!")
    break
  
  #Detect faces and calc encodings
  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
  #boxes is including of top, right, bottom, left of each face
  boxes = face_recognition.face_locations(rgb_frame, model="hog")
  #encodings contains a list of 128-D corresponding to each face
  encodings = face_recognition.face_encodings(rgb_frame, boxes)

  #Create a empty list to save names who detected faces.
  names = []

  for encoding in encodings:
    #Compare this encoding with encoding in file encodings.pkl
    face_distances = face_recognition.face_distance(data["encodings"], encoding)

    best_match_index =  np.argmin(face_distances)
    best_match_distance = face_distances[best_match_index]

    best_match_id = data["names"][best_match_index]

    print(f"Best match is {best_match_id} with distance {best_match_distance:.4f}")

    #Default name is Unknown
    name = "Unknown"

    if best_match_distance < 0.4:
      #Finding location index which has True value
      # matchIdxs = [i for (i, b) in enumerate(matches) if b]

      # #Counting 
      # counts = {}
      # for i in matchIdxs:
      #   #Getting member id corresponded 
      #   member_id = data["names"][i]
      #   #Counting frequency the numbers of id member 
      #   counts[member_id] = counts.get(member_id, 0) + 1
      
      # #Choose a person who the highest count
      # name = max(counts, key=counts.get)

      name = best_match_id
      try:
        full_name = df_members.loc[name, 'Tên Hội viên']
        name = full_name
      except KeyError:
        name = f"{name} (No info)"
      
    names.append(name)

  #Draw box into the screen
  for ((top, right, bottom, left), name)in zip(boxes, names):
    #Draw the rectangle around face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    #Draw the background for name member
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
    
    #Display last frame which processed 
    cv2.imshow("The system check-in face in gym", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

print("Cleaning and exit.....")
cap.release()
cv2.destroyAllWindows()




