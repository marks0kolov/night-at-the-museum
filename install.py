#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import platform

print("Starting setup...")

OS = platform.system()

# ============ helpers ============
def _run(cmd, check=True):
    try:
        subprocess.run(cmd, check=check, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        if check:
            sys.exit(1)

def _cmd_exists(cmd):
    return shutil.which(cmd) is not None

# ============ ensure git ============
def ensure_git():
    # check git
    if _cmd_exists("git"):
        print("Git present")
    else: 
        # install git
        print("Installing Git...")
        if OS == "Darwin": # install git for mac
            _run(["xcode-select", "--install"], check=False)
        
        elif OS == "Linux": # install git for linux
            if _cmd_exists("apt"):
                _run(["sudo", "apt", "update", "-y"])
                _run(["sudo", "apt", "install", "-y", "git"])
            elif _cmd_exists("dnf"):
                _run(["sudo", "dnf", "install", "-y", "git"])
            elif _cmd_exists("yum"):
                _run(["sudo", "yum", "install", "-y", "git"])
            else:
                print("An error occured. Please install git manually at https://git-scm.com")
                sys.exit(1)
        
        elif OS == "Windows": # install git for the microslop os
            if _cmd_exists("winget"):
                _run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"])
            else:
                print("Please innstall Git manually at https://git-scm.com")
                sys.exit(1)

        else:
            print("Unsupported OS. Please install git manually at https://git-scm.com")
            sys.exit(1)

# ============ clone repo ============
def clone_repo():
    base_name = "night-at-the-museum"
    repo_dir = base_name

    i = 1
    while os.path.isdir(repo_dir):
        repo_dir = f"{base_name}-{i}"
        i += 1

    print(f"Cloning repo into '{repo_dir}'...")
    _run(["git", "clone", "--quiet", "https://github.com/marks0kolov/night-at-the-museum.git", repo_dir])

    return repo_dir

# ============ ensure python ============
def detect_python():
    global PYTHON
    PYTHON = sys.executable

# ============ ensure pip ============
def ensure_pip():
    # check pip
    try:
        subprocess.run([PYTHON, "-m", "pip", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("pip detected")
    except subprocess.CalledProcessError:
        # install pip
        print("Installing pip...")
        _run([PYTHON, "-m", "ensurepip", "--upgrade"])

# ============ create venv ============
def setup_venv():
    print("Creating venv...")
    _run([PYTHON, "-m", "venv", ".venv"])

# ============ install requirements ============
def install_requirements():
    print("Installing required packages...")
    if OS == "Windows": # special microslop version
        VENV_PYTHON = os.path.join(".venv", "Scripts", "python.exe")
    else:
        VENV_PYTHON = os.path.join(".venv", "bin", "python")

    _run([VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip"])
    _run([VENV_PYTHON, "-m", "pip", "install", "-r", "requirements.txt"])

# ============ provide run command ============
def print_run_command():
    print("Setup complete")
    if OS == "Windows": # special microslop version
        print(f"cd {repo_dir} && .venv\\Scripts\\python.exe -m app.main")
    else:
        print(f"cd {repo_dir} && .venv/bin/python -m app.main")

# ============ run ============
ensure_git()
repo_dir = clone_repo()
os.chdir(repo_dir)
detect_python()
ensure_pip()
setup_venv()
install_requirements()
print_run_command()