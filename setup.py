from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="SpeechCam",
     version="0.1A",
     author="Parent, Talmage",
     author_email="parent@clarkson.edu",
     description="Speech operated selfie cam",
     long_description=long_description,
     long_description_content_type="text/markdown",
     license="BSD 3 Clause",
     packages=find_packages(),
     py_modules=["SpeechCam","image_processing","speech"],
     url="https://github.com/johnwparent/SpeechCam",
     entry_points={"console_scripts":['SpeechCam = SpeechCam.__main__:main']},
     install_requires=["opencv-python",
                      "SpeechRecognition",
                      "numpy",
                      "pyttsx3",
                      ],
    )