import os
import platform
import setuptools
import subprocess
import re

# Print out our uname for debugging purposes
uname = platform.uname()
print(uname)

# Install OSX Golang if needed
if uname.system == "Darwin":
    os.system("./scripts/setup-macos.sh")

# Install Linux Golang if needed
elif uname.system == "Linux":
    if uname.machine == "aarch64":
        os.system("./scripts/setup-arm64.sh")
    elif uname.machine in ("armv7l", "armv6l"):
        os.system("./scripts/setup-arm6vl.sh")
    elif uname.machine == "x86_64":
        os.system("./scripts/setup-linux-64.sh")
    elif uname.machine == "i686":
        os.system("./scripts/setup-linux-32.sh")

# Add in our downloaded Go compiler to PATH
old_path = os.environ["PATH"]
new_path = os.path.join(os.getcwd(), "go", "bin")
env = {"PATH": f"{old_path}:{new_path}"}
env = dict(os.environ, **env)
os.environ["PATH"] = f"{old_path}:{new_path}"

# Clean out any existing files
subprocess.call(["make", "clean"], env=env)

# Build the Go shared module for whatever OS we're on
subprocess.call(["make", "so"], env=env)

# Build the CFFI headers
subprocess.call(["pip", "install", "cffi~=1.1"], env=env)
subprocess.call(["make", "ffi"], env=env)

with open("pybluemonday/__init__.py", "r", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybluemonday",
    version=version,
    author="Kevin Chung",
    author_email="kchung@nyu.edu",
    description="Python bindings for the bluemonday HTML sanitizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ColdHeat/pybluemonday",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # I'm not sure what this value is supposed to be
    build_golang={"root": "github.com/ColdHeat/pybluemonday"},
    ext_modules=[setuptools.Extension("pybluemonday/bluemonday", ["bluemonday.go"])],
    setup_requires=["setuptools-golang==2.3.0", "cffi~=1.1"],
    install_requires=["cffi~=1.1"],
)
