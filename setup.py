from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jiwer',
    version='1.3',
    description='Approximate the WER of an ASR transcript',
    url='https://github.com/jitsi/asr-wer/',
    author='Nik Vaessen',
    author_email='nikvaes@gmail.com',
    license='Apache 2',
    packages=['jiwer'],
    install_requires=["numpy"],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown'
)