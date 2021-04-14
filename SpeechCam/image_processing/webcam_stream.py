import cv2
import sys, os, operator, math

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

    def compare_tuples(t1, t2, oper):
        x = t1[0] oper t2[0]
        y = t1[1] oper t2[1]
        return x and y

    def compute_distance(pt1, pt2):
        dist_x = pt2[0] - pt1[0]
        dist_y = pt2[1] - pt1[1]
        return math.sqrt(dist_x**2 + dist_y**2)

    def find_nearest_quadrant():
        (x,y,w,h) = bbox
        corners = ((x,y),(x+w,y+h))
        closest = (2**64,2**64)
        closest_quad = ""
        is_inside = False
        for quadrant in quadrants:
            upper = compare_tuples(corners[0], quadrants[quadrant][0], operator.gt)
            lower = compare_tuples(corners[1], quadrants[quadrant][1], operator.lt)
            if upper and lower:
                is_inside = True
                closest = (0,0)
                closest_quad = quadrant
            else:
                dist_u = compute_distance(corner[0], quadrants[quadrant][0])
                dist_l = compute_distance(corner[1], quadrants[quadrant][1])
                if dist_u < closest[0] and dist_l < closest[1]:
                    closest = (dist_u, dist_l)
                    closest_quad = quadrant
        return closest_quad, is_inside

    return find_nearest_quadrant()

def determine_direction_to_move(im, bbox):
    closest, is_inside = image_quadrant(im, bbox)
    if not is_inside:
        # need to compute direction to move to aquire closest
        pass
    else:
        return None
