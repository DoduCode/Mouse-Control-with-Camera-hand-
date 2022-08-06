import tkinter as tk
from tkinter import BOTTOM, X, ttk
import tkinter.ttk as ttk
from tkinter.ttk import *
import cv2 # pip install opencv-python
from cvzone.HandTrackingModule import HandDetector # pip install cvzone
import mouse # pip install mouse

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Camera Control")
        self.geometry("700x400")

        self.camnum = 0
        available_cams = find_available_cameras()
        for cam in available_cams:
            self.b1 = Button(self, text = cam, command = lambda m = self.camnum: self.setcam(m), width = 350)
            self.b1.pack(ipady = 16)

        self.test = Button(self, text = "Test Cam", command = lambda m = self.camnum: self.testcam(m))
        self.start = Button(self, text = 'Start', command = lambda m = self.camnum: self.cam(m))
        self.test.pack(side = BOTTOM)
        self.start.pack(side = BOTTOM)

    def setcam(self, num):
        self.camnum = num

    def testcam(self, cnum):
        cap = cv2.VideoCapture(cnum)
        cap.set(3, self.winfo_screenwidth())
        cap.set(4, self.winfo_screenheight())

        while True:
            success, frame = cap.read()
            cv2.imshow("Hands", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def cam(self, cnum):
        cap = cv2.VideoCapture(cnum)
        cap.set(3, self.winfo_screenwidth())
        cap.set(4, self.winfo_screenheight())

        detector = HandDetector(maxHands = 1, detectionCon = 0.8)

        while True:
            success, frame = cap.read()
            hands, img = detector.findHands(frame)
            cv2.imshow("Hands", img)

            if hands:
                hand = hands[0]
                lmList = hand['lmList']
                
                mouse.click('left')
                mouse.move(lmList[0][0], lmList[0][1], duration = 0.1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

def find_available_cameras():
    available_cameras = []
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        pass

    else:
        available_cameras.append(0)

    camnum = 1
    while camnum != 5:
        cap = cv2.VideoCapture(camnum)
        if not cap.isOpened():
            pass

        else:
            available_cameras.append(camnum)

        camnum += 1

    return available_cameras

if __name__ == "__main__":
    app = App()
    app.mainloop()