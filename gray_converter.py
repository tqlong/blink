import cv2

class GrayConverter:
    def __init__(self):
        pass

    def workon(self, frame, info):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        info["gray"] = gray
