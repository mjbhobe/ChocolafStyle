#!/usr/bin/env python
import glob
import os
import pathlib

this_dir = "/home/mjbhobe/code/git-projects/learning_Qt/bogo2bogo/ChocolafStyle/examples"
print(f"You are in {this_dir} directory")
all_files = glob.glob(f"{this_dir}/*.py", recursive=True)
for i, file_name in enumerate(all_files):
    print(file_name)
    if (i >= 20):
        break

