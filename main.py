import pygame as pg
import capture

from utils import c2ImageToSurface, CLR, TextPrint

pg.init()
# screen = pg.display.set_mode([1024, 600], pg.FULLSCREEN)
screen = pg.display.set_mode([1024, 600])
pg.display.set_caption("main")
done = False
clock = pg.time.Clock()
textPrint = TextPrint()
cap = capture.Cap()

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            done = True
        if pg.key.get_pressed()[pg.K_TAB]:
            mode = cap.mode
            if mode == 'work':
                cap.mode = 'edit'
            if mode == 'edit':
                cap.mode = 'move'
            if mode == 'move':
                cap.mode = 'work'

    screen.fill(CLR.MAGENTA)
    textPrint.reset()

    screen.blit(c2ImageToSurface(cap.img()), [0, 0])

    pg.display.flip()
    clock.tick(100)

pg.quit()
