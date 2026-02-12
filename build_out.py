import os
import shutil

from scripts.utils import err, info

# clean out directory
if os.path.exists("out"):
    shutil.rmtree("out")
    info("Removed existing out directory")
os.makedirs("out")


def copyDir(file):
    if os.path.exists(file):
        shutil.copytree(file, f"out/{file}")
        info(f"{file} copied.")
    else:
        err(f"{file} not found.")


def copyFile(file):
    if os.path.exists(file):
        shutil.copy(file, f"out/{file}")
        info(f"{file} copied.")
    else:
        err(f"{file} not found.")


copyDir("assets")
copyDir("posts")
copyFile("index.html")
copyFile("favicon.ico")
copyFile("robots.txt")
