import pygame as pg
import capture

from utils import c2ImageToSurface, CLR, TextPrint

MODE = dict(work='edit', edit='move', move='work')

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
        key = pg.key.get_pressed()
        mod = pg.key.get_mods()

        if key[pg.K_ESCAPE]:
            done = True
        if key[pg.K_TAB]:
            cap.mode = MODE[cap.mode]

        if mod == 0 and cap.mode == 'edit':
            if key[pg.K_RIGHT]:
                cap.edit += 1
                if cap.edit > 31:
                    cap.edit = 0
            if key[pg.K_LEFT]:
                cap.edit -= 1
                if cap.edit < 0:
                    cap.edit = 31
            if key[pg.K_UP]:
                cap.edit -= 8
                if cap.edit < 0:
                    cap.edit += 32
            if key[pg.K_DOWN]:
                cap.edit += 8
                if cap.edit > 31:
                    cap.edit -= 32

        if mod & pg.KMOD_SHIFT and cap.mode == 'edit':
            edit = cap.edit
            ln = edit // 8
            cl = edit % 8
            if key[pg.K_RIGHT]:
                cap.mesh[ln, cl] += (1, 0)
                cap.calc_data()
            if key[pg.K_LEFT]:
                cap.mesh[ln, cl] -= (1, 0)
                cap.calc_data()
            if key[pg.K_UP]:
                cap.mesh[ln, cl] -= (0, 1)
                cap.calc_data()
            if key[pg.K_DOWN]:
                cap.mesh[ln, cl] += (0, 1)
                cap.calc_data()

        if mod == 0 and cap.mode == 'move':
            if key[pg.K_RIGHT]:
                cap.mesh += (1, 0)
                cap.calc_data()
            if key[pg.K_LEFT]:
                cap.mesh -= (1, 0)
                cap.calc_data()
            if key[pg.K_UP]:
                cap.mesh -= (0, 1)
                cap.calc_data()
            if key[pg.K_DOWN]:
                cap.mesh += (0, 1)
                cap.calc_data()

    screen.fill(CLR.MAGENTA)
    textPrint.reset()

    screen.blit(c2ImageToSurface(cap.img()), [0, 0])

    pg.display.flip()
    clock.tick(10)

pg.quit()
