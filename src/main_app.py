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
#Loading file font
font_path = "/home/luwukien/Mics/Font/Roboto/static/Roboto-Regular.ttf" 
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
time.sleep(3.0)

try:
  font = ImageFont.truetype(font_path, 20)
except IOError:
  print(f"Error: Cannot find file font at '{font_path}'. Using default font")
  font = ImageFont.load_default()

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
  persons_info = []

  for encoding in encodings:
    #Compare this encoding with encoding in file encodings.pkl
    face_distances = face_recognition.face_distance(data["encodings"], encoding)
    best_match_index =  np.argmin(face_distances)
    best_match_distance = face_distances[best_match_index]

    register_date = "" 

    #Default name is Unknown
    name = "Unknown"

    if best_match_distance < 0.45:
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

      member_id = data["names"][best_match_index]
      try:
        member_info = df_members.loc[member_id]

        full_name = member_info['Tên Hội viên']
        date_from_csv = member_info['Ngày đăng ký']

        name = str(full_name).title()
        register_date = str(date_from_csv).split(' ')[0]
      except KeyError:
        name = f"{member_id} (No info)"
    persons_info.append({"name": name, "date": register_date})

    # Convert frame OpenCV (BGR) to Pillow (RGB)
  pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
  
  # Initalize a object to draw
  draw = ImageDraw.Draw(pil_img)

  #Draw box into the screen
  for ((top, right, bottom, left), person)in zip(boxes, persons_info):

    name_to_draw = person["name"]
    date_to_draw = person["date"]

    #Draw the rectangle around face
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0), width=2)

    #Location to draw text
    y = top - 50 if top - 50 > 0 else top + 10

    draw.text((left, y), name_to_draw , font=font, fill=(0, 255, 0))

    draw.text((left, y + 25), date_to_draw , font=font, fill=(225, 255, 0))

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




