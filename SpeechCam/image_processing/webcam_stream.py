import cv2
import sys, os

def capture_webcam_image()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Webcam not available")

    ret, frame = cap.read()
    if not ret:
        raise IOError("No Capture on attempt, try restarting webcam or this program")
    cap.release()
    return frame

def load_cascades():
    cur_dir = os.getcwd()
    casc_dir = cur_dir+"/haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(casc_dir)


def imtogray(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

def detect_face(gray_im):
    detector = load_cascades()
    faces = detector.detectMultiScale(
        gray_im,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize = (10,10),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    return faces

def display_bbox(bbox, im):
    (x, y, width, height) = bbox
    cv2.rectangle(im,(x,y), (x+w, y+h), (255, 0, 0), thickness=4)
    return im

def image_quadrant(im, bbox):
    h, w, _ = im.shape
    quadrants = {}
    quadrants["ul"] = ((0,0),(w/2,h/2))
    quadrants["ur"] = ((w/2,h/2),(w,0))
    quadrants["ll"] = ((0,h/2),(w/2,h))
    quadrants["lr"] = ((w/2,h/2),(w,h))

    def find_nearest_quadrant():
        (x,y,w,h) = bbox
        return quadrant["ul"]
    return find_nearest_quadrant()


