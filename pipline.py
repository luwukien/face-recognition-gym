import os
import shutil
import importlib

SCRIPT_ORDER = [
  "step1_find_similar_images",
  "step2_change_format_img",
  "step3_filter_member_id",
  "step4_encode_faces",
]

PATHS_TO_CLEAN = [
  "data/cleaned_photos",
  "data/redudant_photos",
  "data/quarantined_photos",
  "encodings.pickle",
  "data/members.csv"
]

def cleanup():
  print("Start cleaning ...")
  for path in PATHS_TO_CLEAN:
    try:
      if os.path.isfile(path):
        os.remove(path)
      elif os.path.isdir(path):
        shutil.rmtree(path)
      else:
        print(f"Not exist {path}")
    except Exception as e:
      print(f"Error - cannot delete {path}: {e}")
  print("Cleaned successfull")

def run_pipline():
  cleanup()

  for script_name in SCRIPT_ORDER:
    try:
      print(f"\n Running file {script_name}")
      script_module = importlib.import_module(f"scripts.{script_name}")

      importlib.reload(script_module)

      print(f"Finished file {script_name}")
    except Exception as e:
      print(f"Error:{e}")
      return
    
if __name__ == "__main__":
  run_pipline()
  print("Finished pipline")