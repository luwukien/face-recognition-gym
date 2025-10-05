from imutils import paths
import face_recognition
import pickle
import cv2
import os 
import shutil

#cleaned_photos
DATASET_PATH = "/home/luwukien/Project/Personal/VisionGym/data/cleaned_photos"
ENCODINGS_PATH = "/home/luwukien/Project/Personal/VisionGym/encodings.pickle"
QUARANTINE_PATH = "/home/luwukien/Project/Personal/VisionGym/data/quarantined_photos" 
os.makedirs(QUARANTINE_PATH, exist_ok=True)

DECTECTION_METHOD = "hog"

def is_blurry(image, threhold=60.0):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  variance = cv2.Laplacian(gray, cv2.CV_64F).var()
  print(f"--> Image sharpness: {variance}") 
  return variance < threhold

imagePaths = list(paths.list_images(DATASET_PATH))

knowEncodings = []
knowNames = []

for (i, imagePath) in enumerate(imagePaths):
  print(f"[INFO] Đang xử lý ảnh thứ {i + 1}/{len(imagePaths)}: {os.path.basename(imagePath)}")

  #Getting id member from image 
  name = os.path.basename(imagePath).split('_@')[0]
  image = cv2.imread(imagePath)

  #Need to change from BGR to RGB because cv2 uses 3 channels B G R, but face_recognition uses 3 channels R G B
  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  #Finding face location in image
  boxes = face_recognition.face_locations(rgb, model=DECTECTION_METHOD)
  
  #Rule 1: Filter a image which only a face
  if len(boxes) != 1:
    print(f"Find {len(boxes)} face, moving image: {os.path.basename(imagePath)}")
    shutil.move(imagePath, os.path.join(QUARANTINE_PATH, os.path.basename(imagePath)))
    continue;

  (top, right, bottom, left) = boxes[0]
  face_roi = image[top:bottom, left:right]

  #Rule 2: Filter blurry images
  if is_blurry(face_roi,threhold=40.0):
    print(f"The image moved the folder quarantined photos, moving image : {os.path.basename(imagePath)}")
    shutil.move(imagePath, os.path.join(QUARANTINE_PATH, os.path.basename(imagePath)))
    continue;
  print(f"The valid image: {os.path.basename(imagePath)}")

  #If image overcome 2 rules, it will be embedded
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

