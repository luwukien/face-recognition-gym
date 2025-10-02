from imutils import paths
import face_recognition
import pickle
import cv2
import os 

DATASET_PATH = "data/cleaned_photos"

ENCODINGS_PATH = "encodings.pickle"

DECTECTION_METHOD = "hog"

imagePaths = list(paths.list_images(DATASET_PATH))

knowEncodings = []
knowNames = []

for (i, imagePath) in enumerate(imagePaths):
  print(f"[INFO] Đang xử lý ảnh thứ {i + 1}/{len(imagePaths)}")

  #Getting id member from image 
  name = os.path.basename(imagePath).split('_@')[0]
  image = cv2.imread(imagePath)
  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  #Finding face location in image
  boxes = face_recognition.face_locations(rgb, model=DECTECTION_METHOD)
  
  #Face embedding 
  encodings = face_recognition.face_encodings(rgb, boxes)

  #Save result 
  for encoding in encodings:
    knowEncodings.append(encoding)
    knowNames.append(name)

print("Loading image to encoding file....")
data = {"encodings": knowEncodings, "names": knowNames}
with open(ENCODINGS_PATH, "wb") as f: 
  f.write(pickle.dumps(data))

print("Finished!")

