import cv2
from threading import Thread
from queue import Queue
class VideoStream:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.Q = Queue(maxsize = 10000)
        self.stopped = False
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True
    
    def start(self):
        self.t.start()
        return self

    def update(self):
        while True:
            if self.stopped: 
                self.cap.release()
                return
            if not self.Q.full():
                more, frame = self.cap.read()
                if more: self.Q.put(frame)
                else: self.stop()

    def read(self):
        if self.Q.empty(): return None
        else: return self.Q.get()

    def stop(self):
        self.stopped = True
