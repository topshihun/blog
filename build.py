import os
import shutil

from scripts.utils import err, info

# clean out directory
if os.path.exists("out"):
    shutil.rmtree("out")
    info("Removed existing out directory")
os.makedirs("out")

# compile all typst files in posts to html and correct output file path(out/posts)
for root, dirs, files in os.walk("posts"):
    for file in files:
        if file.endswith(".typ"):
            compile_file = os.path.join(root, file)
            output_file = os.path.join(
                root.replace("posts", "out/posts"), file.replace(".typ", ".html")
            )
            # create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            info(f"Compiling {compile_file}")
            command = f"typst compile --features html --format html {compile_file} {output_file}"
            info(f"Executing command: {command}")
            os.system(command)
info("Compiled posts")


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
copyFile("index.html")
copyFile("favicon.ico")
copyFile("robots.txt")
