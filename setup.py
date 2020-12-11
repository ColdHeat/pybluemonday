import setuptools
import re

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
    setup_requires=["setuptools-golang==2.3.0", "cffi==1.14.3"],
    install_requires=["cffi==1.14.3"],
)
