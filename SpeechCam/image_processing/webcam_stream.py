import cv2
import sys, os, math, numpy as np

def im_cap_driver():
    im = capture_webcam_image()
    im_gray = imtogray(im)
    faces = detect_face(im_gray)
    if len(faces) > 1:
        print("Too many faces detected in image, please have other people step away from camera frame")
        while True:
            im = capture_webcam_image()
            im_gray = imtogray(im)
            faces = detect_face(im_gray)
            if len(faces) < 2:
                break
    return faces, im

def capture_webcam_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Webcam not available")

    ret, frame = cap.read()
    if not ret:
        raise IOError("No Capture on attempt, try restarting webcam or this program")
    cap.release()
    return cv2.flip(frame, 1)

def load_cascades():
    cur_dir = os.getcwd()
    casc_dir = "/haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(cv2.data.haarcascades + casc_dir)

def imtogray(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

def detect_face(gray_im):
    detector = load_cascades()
    faces = detector.detectMultiScale(gray_im, 1.3, 5)
    return faces

def display_bbox(bbox, im):
    x, y, w, h = bbox
    cv2.rectangle(im,(x,y), (x+w, y+h), (255, 0, 0), thickness=4)
    return im

def image_quadrant(im, bbox, ideal_quad):
    im_h, im_w, _ = im.shape
    x,y,w,h = bbox

    quadrants = {}
    quadrants["ul"] = ((0,0),(im_w//2,im_h//2))
    quadrants["ur"] = ((im_w//2,0),(im_w,im_h//2))
    quadrants["ll"] = ((0,im_h//2),(im_w//2,im_h))
    quadrants["lr"] = ((im_w//2,im_h//2),(im_w,im_h))

    def is_inside(bbox_center):
        quad = quadrants[ideal_quad]
        x,y = bbox_center
        u_corner = quad[0]
        l_corner = quad[1]
        if x > u_corner[0] and x < l_corner[0] and y > u_corner[1] and y < l_corner[1]:
            return True
        return False

    def compute_bbox_center():
        xmid = (x+w+x)//2
        ymid = (y+h+y)//2
        return (xmid, ymid)

    def compute_quadrant_center(quad):
        pt1 = quadrants[quad][0]
        pt2 = quadrants[quad][1]
        x_mid = (pt1[0] + pt2[0])//2
        y_mid = (pt1[1] + pt2[1])//2
        return (x_mid, y_mid)

    def compute_angle(center1, center2):
        diff_x = center1[0] - center2[0]
        diff_y = center1[1] - center2[1]
        diff_y = -diff_y
        angle = np.arctan2(diff_y,diff_x)
        return angle

    center = compute_bbox_center()
    found = is_inside(center)
    angle = 0
    if not found:
        q_center = compute_quadrant_center(ideal_quad)
        angle = compute_angle(q_center, center)

    return found, angle


def determine_direction_to_move(angle):
    fst = (0, math.pi/2)
    snd = (math.pi/2, math.pi)
    trd = (-math.pi, -math.pi/2)
    fth = (-math.pi/2, 0)
    quads = [fst, snd, trd, fth]
    quad_names = {fst: "ur",snd:"ul",trd:"ll",fth:"lr"}
    for quad in quads:
        if quad[0] <= angle < quad[1]:
            return quad_names[quad]
    raise RuntimeError("Angle not found in unit circle, math has broken")

def save(image):
    cv2.imwrite("Selfie.jpg", image)
