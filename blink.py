import cv2

from video_stream import VideoStream
from gray_converter import GrayConverter
from face_detector import FaceDetector
from face_marker import FaceMarker
from face_decorator import allEAR
from face_decorator import FaceDecorator
from eye_aspect_ratio import EyeAspectRatio
from config import args

vs = VideoStream(args["path"]).start()
workers = [ GrayConverter(), FaceDetector(), FaceMarker(args["landmark_model"]), EyeAspectRatio(), FaceDecorator() ]

winname = args["display"]
graphWin = "Graph"
cv2.namedWindow(winname)
cv2.moveWindow(winname, 200, 300)
cv2.namedWindow(graphWin)
cv2.moveWindow(graphWin, 900, 300)
while True:
    frame = vs.read()
    if frame is None: break

    info = {}
    for w in workers: w.workon(frame, info)
    
    cv2.imshow(winname, info["output"])
    cv2.imshow(graphWin, info["graph"])
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q') or key == 27:
        break
    elif key == ord(' '):
        cv2.waitKey(0)

cv2.destroyAllWindows()
vs.stop()
vs.t.join()