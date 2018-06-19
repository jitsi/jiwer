from setuptools import setup

setup(name='jiwer',
      version='1.0',
      description='Approximate the WER of an ASR transcript',
      url='https://github.com/jitsi/asr-wer/',
      author='Nik Vaessen',
      author_email='nikvaes@gmail.com',
      license='Apache 2',
      packages=['jiwer'],
      install_requires=["numpy"],
      zip_safe=False)