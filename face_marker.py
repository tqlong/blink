import numpy as np
import dlib

class FaceMarker:
    def __init__(self, path):
        self.predictor = dlib.shape_predictor(path)
        self.lStart, self.lEnd = 36, 42
        self.rStart, self.rEnd = 42, 48
    
    def workon(self, frame, info):
        info["leftEye"] = []
        info["rightEye"] = []
        for r in info["faces"]:
            shape = self.predictor(info["gray"], r)
            info["leftEye"].append( np.array( [ [p.x, p.y] for p in shape.parts()[self.lStart:self.lEnd]] ) )
            info["rightEye"].append( np.array( [ [p.x, p.y] for p in shape.parts()[self.rStart:self.rEnd]] ) )
