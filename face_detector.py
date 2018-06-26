import dlib
import cv2

class FaceDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.maxWidth = 250
    
    # required info["gray"]
    def workon(self, frame, info):
        h, w = info["gray"].shape
        f = float(self.maxWidth) / max(h,w)
        gray = cv2.resize(info["gray"], None, None, f, f)
        rects = self.detector(gray, 0)
        info["faces"] = [self.dlibrect(r.left()/f, r.top()/f, r.right()/f, r.bottom()/f) for r in rects]

    def dlibrect(self, left, top, right, bottom):
        return dlib.rectangle(int(left), int(top), int(right), int(bottom))
