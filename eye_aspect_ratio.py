from scipy.spatial import distance
from face_decorator import allEAR

class EyeAspectRatio:
    def __init__(self):
        self.blinks = 0
        self.counter = 0
        self.thres = 0.3
        self.counter_thres = 3
    
    def workon(self, frame, info):
        info["leftEAR"] = [ self.computeEAR(l) for l in info["leftEye"] ]
        info["rightEAR"] = [ self.computeEAR(r) for r in info["rightEye"] ]
        info["EAR"] = [ (a+b) / 2 for a,b in zip(info["leftEAR"], info["rightEAR"])]

        if len(info["EAR"]) > 0:
            ear = info["EAR"][0]
            if ear < self.thres:
                self.counter += 1
            else:
                if self.counter >= self.counter_thres:
                    self.blinks += 1
                self.counter = 0
            allEAR.append( ear )
        info["BLINKS"] = self.blinks

    def computeEAR(self, p):
        A = distance.euclidean(p[1], p[5])
        B = distance.euclidean(p[2], p[4])
        C = distance.euclidean(p[0], p[3])
        return (A+B) / (2.0*C)
