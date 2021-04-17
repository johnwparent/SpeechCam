import sys, os, time
import argparse
from .speech import stt
from .speech import tts
from .image_processing import webcam_stream as ws

directions_to_abbr = {"upper right":"ur", "upper left":"ul", "bottom left":"ll", "bottom right":"lr"}

def detect_speech():
    language_processor = stt.get_interpreter()
    default_mic = stt.get_mic()
    with default_mic as audio_src:
        language_processor.adjust_for_ambient_noise(audio_src, duration=0.3)
        audio_capture = language_processor.listen(audio_src)

    google = stt.get_google_interp(language_processor)
    try:
        text_from_speech = google(audio_capture)
    except stt.RequestError:
        raise RuntimeError("Unable to access speech recognition runtime, please connect to network.")
    except stt.UnknownValueError:
        raise RuntimeWarning("Sorry, we're having trouble understanding you, please try to say that again, this time waiting for just a moment before speaking")
    return text_from_speech



def request_move(speaker,direction):
    def left():
        speaker.speak("Please Move left")
    def right():
        speaker.speak("Please Move right")
    def up():
        speaker.speak("Please Move up")
    def down():
        speaker.speak("Please Move down")
    return locals()[direction]


def query_user(speaker):
    speaker.speak("Please state desired location in image you want your face to appear")
    speaker.speak("Options are:")
    speaker.speak("Upper left")
    speaker.speak("Bottom left")
    speaker.speak("Bottom right")
    speaker.speak("Upper right")

def capture_user_option(speaker):
    query_user(speaker)
    user_input = detect_speech()
    while True:
        if user_input not in set(["upper right", "upper left", "bottom right", "bottom left"]):
            speaker.speak("Invalid quadrant option, please state a valid option or speak more clearly")
        else:
            break
        query_user(speaker)
        user_input = detect_speech()
    return user_input

def find_frame(speech_out):
    faces = ()
    while not len(faces) :
        for opt in ("left","right","up","down"):
            for _ in range(2):
                direc = request_move(speech_out, opt)
                direc()
            time.sleep(1)
            faces, im = ws.im_cap_driver()
            if len(faces):
                break
            speech_out.speak("User still not in frame")
        if not len(faces):
            speech_out.speak("Face was unable to be detected.")
            speech_out.speak("For best results, please remove any object obscuring the face and orient against a neutral backdrop")
            speech_out.speak("Please indicate if you wish to continue. State yes or no")
            opt = detect_speech()
            if opt.lower() != "yes":
                break
            else:
                speech_out.speak("Continuing!")
                time.sleep(0.25)
    return faces

directions = {"ul": "up.left","ur":"up.right","lr":"down.right","ll":"down.left"}


def direct_user(speech_out, desired_quad, face, im):
    is_in, direc = ws.image_quadrant(im,face,desired_quad)
    while not is_in:
        move_in = ws.determine_direction_to_move(direc)
        move_eng_dirs = directions[move_in].split(".")
        for move in move_eng_dirs:
            speech_out.speak("To position face in desired frame, please move %s" % move)
            time.sleep(0.5)
        faces, im = ws.im_cap_driver()
        if not len(faces):
            speech_out.speak("Out of frame, please move to previous position and try again")
        else:
            face = faces[0]
        is_in, direc = ws.image_quadrant(im,face,desired_quad)
    return im


def main(argv=None):
    # initialize main loop
    speech_out = tts.TTS()
    speech_out.set_voice(1)
    u_loc = capture_user_option(speech_out)
    desired_quad = directions_to_abbr[u_loc]
    faces, im = ws.im_cap_driver()
    if not len(faces):
        speech_out.speak("User not in frame, image not captured")
        speech_out.speak("Please make sure face is oriented ")
        # no face detected scenario
        faces = find_frame(speech_out)

    if not len(faces):
        speech_out.speak("Camera exiting. No image captured")
        return(0)
    new_im = direct_user(speech_out,desired_quad,faces[0],im)
    ws.save(new_im)
    speech_out.speak("Image captured and saved. Thank you for using SpeechCam! The program will now exit")
    # face detected, determine if in selected quadrant
    # if not, prompt user to move in appropriate direction


if __name__ == '__main__':
    main()