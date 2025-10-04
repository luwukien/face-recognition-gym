from imutils import paths
import face_recognition
import pickle
import cv2
import os 
import shutil

DATASET_PATH = "data/cleaned_photos"
ENCODINGS_PATH = "encodings.pickle"
QUARANTINE_PATH = "data/quarantined_photos" 

DECTECTION_METHOD = "hog"

def is_blurry(image, threhold=100.0):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  variance = cv2.Laplacian(gray, cv2.CV_64F).var()

  return variance < threhold

imagePaths = list(paths.list_images(DATASET_PATH))

knowEncodings = []
knowNames = []

for (i, imagePath) in enumerate(imagePaths):
  print(f"[INFO] Đang xử lý ảnh thứ {i + 1}/{len(imagePaths)}")

  #Getting id member from image 
  name = os.path.basename(imagePath).split('_@')[0]
  image = cv2.imread(imagePath)

  #Rule 1: Filter blur image
  if is_blurry(image,threhold=100):
    print(f"The image moved the folder quarantined photos : {os.path.basename(imagePath)}")
    shutil.move(imagePath, os.path.join(QUARANTINE_PATH, os.path.basename(imagePath)))
    continue;

  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  #Finding face location in image
  boxes = face_recognition.face_locations(rgb, model=DECTECTION_METHOD)
  
  #Rule 2: Filter a image which only a face
  if len(boxes) != 1:
    print(f"Find {len(boxes)} face : {os.path.basename(imagePath)}")
    shutil.move(imagePath, os.path.join(QUARANTINE_PATH, os.path.basename(imagePath)))
    continue;

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

