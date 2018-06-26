import datetime as dt
import cv2
import numpy as np

allEAR = []

class FaceDecorator:
    def __init__(self):
        self.count = 0
        self.start = dt.datetime.now()
        self.fps = 0
    
    def workon(self, frame, info):
        #print(frame, info)
        self.count += 1
        if self.count == 30:
            elapsed = (dt.datetime.now() - self.start).total_seconds()
            self.fps = self.count / elapsed
            self.start = dt.datetime.now()
            self.count = 0

        output = frame.copy()
        #for r in info["faces"]:
        #    cv2.rectangle(output, (r.left(), r.top()), (r.right(), r.bottom()), (0,255,0), 2)

        # for l in info["leftEye"]: cv2.polylines(output, [l], True, (255,255,0))
        # for r in info["rightEye"]: cv2.polylines(output, [r], True, (0,255,255))

        # cv2.putText(output, "FPS: {:.2f}".format(self.fps), (30, frame.shape[0]-20),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # if len(info["EAR"]) > 0:
        #     ear = info["EAR"][0]
        #     cv2.putText(output, "EAR: {:.2f}".format(ear), (frame.shape[1]-150, 30),
        #         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # cv2.putText(output, "BLINKS: {:2d}".format(info["BLINKS"]), (30, 30),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        overlay = output.copy()
        color = (0,0,0) if info["BLINKS"] % 2 == 0 else (0,0,255)
        alpha = 0.0 if info["BLINKS"] % 2 == 0 else 0.6
        cv2.rectangle(overlay, (0,0),(frame.shape[1], frame.shape[0]), color, -1)
        cv2.addWeighted(overlay, alpha, output, 1-alpha, 0, output)
        
        info["output"] = output

        global allEAR
        val = allEAR[-100:]
        f = 3
        height = 200
        width = len(val)*f
        minY = 0.2
        maxY = 0.4
        thres = 0.3
        graph = np.zeros((height,width,3), np.uint8)
        yt = height-int( (thres-minY)/(maxY-minY) * height)
        cv2.line(graph, (0,yt), (width, yt), (0,0,255), 1)
        for x1, v1, v2 in zip( np.arange(len(val)-1), val[:-1], val[1:] ):
            x2 = x1+1
            y1 = height-int( (v1-minY)/(maxY-minY) * height)
            y2 = height-int( (v2-minY)/(maxY-minY) * height)
            color = (255,200,0) if v1 < thres or v2 < thres else (0,200,255)
            cv2.line(graph, (x1*f,y1), (x2*f, y2), color, 1)
            cv2.circle(graph, (x1*f,y1), 2, (0,255,255))
        info["graph"] = graph
        #  print(graph.shape)
