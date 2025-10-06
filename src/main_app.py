import face_recognition
import pickle
import cv2
import pandas as pd
import numpy as np
import threading
import time 
from PIL import ImageFont, ImageDraw, Image

#Class camera using multithreading 
class WebcamStream:
  def __init__(self, src=0):
    #Initialize webcamcvtColor
    self.stream = cv2.VideoCapture(src, cv2.CAP_V4L2)
    # Reading first frame
    (self.ret, self.frame) = self.stream.read()
    #Variable to stop thread
    self.stopped = False

  def start(self):
    threading.Thread(target=self.update, args=(), daemon=True).start()
    return self
  
  def update(self):
    if not self.ret:
      return
    while True:
      if self.stopped:
        return
      (self.ret, self.frame) = self.stream.read()
  
  def read(self):
    return self.frame 
  
  def stop(self):
    self.stopped = True
    self.stream.release()

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

print("Start thread camera")
vs = WebcamStream(src=0).start()
time.sleep(2.0)

while True:
  #Read a frame from webcam thread
  frame = vs.read()
  
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

    if best_match_distance < 0.5:
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

  font_path = "/home/luwukien/Mics/Font/Roboto/static/Roboto-Regular.ttf" 
  font = ImageFont.truetype(font_path, 20)

    # Convert frame OpenCV (BGR) to Pillow (RGB)
  pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
  
  # Initalize a object to draw
  draw = ImageDraw.Draw(pil_img)

  #Draw box into the screen
  for ((top, right, bottom, left), name)in zip(boxes, names):
    #Draw the rectangle around face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    y = top - 25 if top - 25 > 0 else top + 10
    draw.text((left, y), name, font=font, fill=(0, 255, 0))

    # Convert Pillow to frame OpenCV to display
    frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    #Display frame
    cv2.imshow("The system check-in face in gym", frame)

  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
      break

print("Cleaning and exit.....")
vs.stop()
cv2.destroyAllWindows()




