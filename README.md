SpeechCam
=========

Welcome to SpeechCam! A python based speech operated selfie capture program

The user specifies a quadrant of an image frame to appear in, and SpeechCam will direct a subject to the correct positioning. When positioning is achieved, an image of the subject will be captured and saved as 'selfie.jpg'.

To operate SpeechCam, a camera and microphone must be accesible to the program.

## Dependencies
PyAudio is a requirement for this project to capture microphone input from user. Installation of this dependency can be difficult at times. PyAudio can be pip installed. However this can often fail due to problems with particular architectures. If that is the case, please downloand and install PyAudio from [this](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) source for the architecture and python version SpeechCam will be executed by.

# Installing and Running
To install and run SpeechCam, after installing PyAudio for the same python being used to run SpeechCam, clone this repo into a desired directory, navigate to the root of this directory, and run:

```$ python -m pip install -e .```

Upon a sucessful installation, SpeechCam can be executed by executing command

```$ SpeechCam```

or by

```$ python -m SpeechCam```

It is recommended to use a Python virtual environment to install and run SpeechCam


### Contributors

John Parent

Owen Talmage