import os
import shutil
import subprocess
import sys

import minify_html

from scripts.check import check_dependencies
from scripts.utils import err, info

# check all dependencies
if not check_dependencies():
    err("Dependencies not met")
    exit(1)

print()

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
            command = [
                "typst",
                "compile",
                "--features",
                "html",
                "--format",
                "html",
                compile_file,
                output_file,
            ]
            info(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command)
            if result.returncode != 0:
                err(f"Compilation failed for {compile_file}")
                sys.exit(1)
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

# compress html files
for root, dirs, files in os.walk("out"):
    for file in files:
        if file.endswith(".html"):
            html_file = os.path.join(root, file)
            minified_html = minify_html.minify(open(html_file).read())
            open(html_file, "w").write(minified_html)
            info(f"Minified {html_file}")

# compress js files by terser
for root, dirs, files in os.walk("out"):
    for file in files:
        if file.endswith(".js"):
            js_file = os.path.join(root, file)
            result = subprocess.run(["terser", js_file, "-o", js_file])
            if result.returncode != 0:
                err(f"Minification failed for {js_file}")
                sys.exit(1)
            info(f"Minified {js_file}")
