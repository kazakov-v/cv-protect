import pygame
import cv2
import numpy as np

from utils import c2ImageToSurface, CLR, TextPrint


class Cap:
    def __init__(self, source='data/output.avi') -> None:
        self.cap = cv2.VideoCapture(source)  # , cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def draw(self, my_screen):
        if self.cap.isOpened():
            res, img = self.cap.read()
            if res:
                img = np.rot90(img)
                img = cv2.resize(img, (1080, 1920))
                img = img[600:1200, :].copy()
                my_screen.blit(c2ImageToSurface(img), [0, 0])


pygame.init()
# screen = pygame.display.set_mode([1024, 600], pygame.FULLSCREEN)
screen = pygame.display.set_mode([1024, 600])
pygame.display.set_caption("main")
done = False
clock = pygame.time.Clock()
pygame.joystick.init()
textPrint = TextPrint()
cap = Cap()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True

        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    screen.fill(CLR.WHITE)
    textPrint.reset()

    cap.draw(screen)

    joystick_count = pygame.joystick.get_count()
    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes))
        textPrint.indent()
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats))
        textPrint.indent()
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()
        textPrint.unindent()

    # cap.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
