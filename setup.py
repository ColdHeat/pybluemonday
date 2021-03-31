import os
import setuptools
import re

uname = os.uname()
print(uname)
if uname.machine == "Darwin":
    os.system("./scripts/setup-macos.sh")
elif uname.machine == "Linux":
    if uname.machine.startswith("arm"):
        if uname.machine == "armv8l":
            os.system("./scripts/setup-arm64.sh")
        elif uname.machine in ("armv7l", "armv6l"):
            os.system("./scripts/setup-armv6l.sh")
    else:
        os.system("./scripts/setup-linux.sh")

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
