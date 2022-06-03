import os
import re
import glob
import json

def fix_json_files(inputdir:str):
    files = glob.glob(os.path.join(inputdir, "*.json"))
    for file in files:
        try:
            data = json.load(open(file))
        except:
            text = open(file).read()
            loc = text.rfind("}", 0, text.rfind("}"))
            text = text[:loc+1]
            with open(file, "w") as f:
                f.write(text)
            print(f"INFO: Fixed file \"{file}\"")

fix_json_files("outputs_HHH2022_20220520_*/likelihood/*/*/*/cache")
fix_json_files("outputs_HHH2022_20220520_*/xsection_scan/*/*/*/cache")
