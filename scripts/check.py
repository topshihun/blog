import shutil

required_tools = ["terser"]


def check_dependencies():
    result = True
    for tool in required_tools:
        print(f"checking: {tool}", end="")
        if shutil.which(tool) is None:
            print(f"checking: {tool} ✗")
            result = False
        else:
            print(f"checking: {tool} ✓")
    return result
