from threading import Thread
import cv2


class Camera:
    def __init__(self, id: str, display=False, **window_size):
        self.display = display

        self.cap = cv2.VideoCapture(id, cv2.CAP_V4L2)
        self.frame = None

        camera_stream = Thread(target=self.stream_camera)
        camera_stream.setDaemon(True)
        camera_stream.start()

    def stream_camera(self):
        while True:
            frame = self.cap.read()

            if frame is not None:
                self.frame = frame

                if self.display:
                    pass
