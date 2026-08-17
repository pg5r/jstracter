import os
from colorama import init, Fore

init(autoreset=True)

def make_file(path: str, txt: str):
    if not os.path.isdir("temp_js"):
        print(Fore.RED + "\n[JSDEBUG] FATAL ERROR: temp_js/ not found.")
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    return True
    
def del_file(path: str):
    if not os.path.isdir("temp_js"):
        print(Fore.RED + "\n[JSDEBUG] FATAL ERROR: temp_js/ not found.")
        return False

    os.remove(path)
    return True

def clear_temp_js():
    temp_dir = "temp_js"

    if not os.path.isdir(temp_dir):
        print(Fore.RED + "\n[JSDEBUG] FATAL ERROR: temp_js/ not found.")
        return False

    for name in os.listdir(temp_dir):
        path = os.path.join(temp_dir, name)

        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            import shutil
            shutil.rmtree(path)

    return True