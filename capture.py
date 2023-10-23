import cv2
import numpy as np
# from gpiozero import CPUTemperature, LED

# import main

# relay = LED(14)
# temp = CPUTemperature()


class Cap:
    def __init__(self, source='data/output.avi') -> None:
        self.cap = cv2.VideoCapture(source)  # , cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.mode = 'work'
        self.edit = 0
        try:
            self.mesh = np.load('data.npy')
        except FileNotFoundError:
            arr = np.zeros((4, 8, 2))
            for i in range(4):
                for j in range(8):
                    arr[i, j] = (j, i)
            self.mesh = arr * 120 + (90, 100)
        self.calc_data()

    def calc_data(self):
        self.data = []
        for p in self.mesh.round(0).reshape(32, 2):
            self.data.append((int(p[0]), int(p[1])))
        np.save('data', self.mesh)

    def img(self) -> np.array:
        if self.cap.isOpened():
            res, img = self.cap.read()
            if res:
                img = np.rot90(img)
                img = cv2.resize(img, (1080, 1920))
                img = img[600:1200, :].copy()

                is_cycle_enabled = True
                for pnt in self.data:  # Main checking
                    x, y = pnt
                    pnt = (x, y)
                    sz = 3
                    val = int(img[y-sz:y+sz, x-sz:x+sz].sum() // 2400)

                    img = cv2.rectangle(
                        img, (x-sz-1, y-sz-1), (x+sz+1, y+sz+1),
                        (255, 255, 255), 1
                    )
                    clr = (255, 255, 255)
                    if val < 2:
                        clr = (0, 0, 255)
                        is_cycle_enabled = False  # !!!!!!!!!!!!!!!!!
                    if val > 3:
                        clr = (0, 255, 0)

                    img = cv2.circle(img, pnt, 20, clr, 5)
                    img = cv2.putText(
                        img, '  '+str(val),
                        pnt, cv2.FONT_HERSHEY_SIMPLEX, 1,
                        clr, 3
                    )

                img[:25, :] = (0, 0, 0)
                clr = (255, 255, 0)
                if self.mode == 'edit':
                    clr = (0, 255, 255)
                    x, y = self.data[self.edit]
                    img = cv2.rectangle(
                        img, (x-25, y-25), (x+25, y+25),
                        (255, 255, 0), 7
                    )
                if self.mode == 'move':
                    clr = (0, 0, 255)
                    x1, y1 = self.data[0]
                    x2, y2 = self.data[31]
                    img = cv2.rectangle(
                        img, (x1-35, y1-35), (x2+35, y2+35),
                        (0, 255, 255), 5
                    )
                img = cv2.putText(
                    img, self.mode.upper(),
                    (450, 23), cv2.FONT_HERSHEY_PLAIN, 2,
                    clr, 4
                )
                img = cv2.putText(
                    img, 'CPU = 65.6C',
                    (25, 23), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2
                )
                # if is_cycle_enabled:
                #     relay.on()
                # else:
                #     relay.off()
                clr = (0, 255, 0) if is_cycle_enabled else (0, 0, 255)
                img[-25:, :] = clr

                return img
        return np.zeros((10, 10, 3), dtype='uint8')
