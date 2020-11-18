from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# setup library
setup(
    name="jiwer",
    version="2.2.0",
    description="Evaluate your speech-to-text system with similarity measures such as word error rate (WER)",
    url="https://github.com/jitsi/jiwer/",
    author="Nik Vaessen",
    author_email="nikvaes@gmail.com",
    license="Apache 2",
    packages=["jiwer"],
    setup_requires=["wheel", "twine"],
    install_requires=["numpy", "python-Levenshtein"],
    zip_safe=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    test_suite="tests",
    python_requires=">3",
)
