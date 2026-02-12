def greenPrint(msg):
    print(f"\033[92m{msg}\033[0m")


def redPrint(msg):
    print(f"\033[91m{msg}\033[0m")


def info(msg):
    greenPrint(msg)


def err(msg):
    redPrint(f"Error: {msg}")
