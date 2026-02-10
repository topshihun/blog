import os

# remove posts files
for root, dirs, files in os.walk("posts"):
    for file in files:
        if os.path.isfile(os.path.join(root, file)):
            remove_file = os.path.join(root, file)
            print(f"Removing {remove_file}")
            os.remove(remove_file)
# remove posts directory if it exists
for root, dirs, files in os.walk("posts"):
    for dir in dirs:
        remove_dir = os.path.join(root, dir)
        print(f"Removing {remove_dir}")
        os.rmdir(remove_dir)
print("Cleaned posts")

# compile all typst files in posts_typst to html and correct output file path(posts)
for root, dirs, files in os.walk("posts_typst"):
    for file in files:
        if file.endswith(".typ"):
            compile_file = os.path.join(root, file)
            output_file = os.path.join(
                root.replace("posts_typst", "posts"), file.replace(".typ", ".html")
            )
            # create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            print(f"Compiling {compile_file}")
            command = f"typst compile --features html --format html {compile_file} {output_file}"
            print(f"Executing command: {command}")
            os.system(command)
print("Compiled posts")
