import numpy as np
import pygame


class CLR:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


def c2ImageToSurface(cvImage):
    if cvImage.dtype.name == 'uint16':
        cvImage = (cvImage / 256).astype('uint8')
    size = cvImage.shape[1::-1]
    if len(cvImage.shape) == 2:
        cvImage = np.repeat(cvImage.reshape(size[1], size[0], 1), 3, axis=2)
        format = 'RGB'
    else:
        format = 'RGBA' if cvImage.shape[2] == 4 else 'RGB'
        cvImage[:, :, [0, 2]] = cvImage[:, :, [2, 0]]
    surface = pygame.image.frombuffer(cvImage.flatten(), size, format)
    return surface.convert_alpha() if format == 'RGBA' else surface.convert()


class TextPrint(object):
    def __init__(self):
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 40)

    def print(self, my_screen, text_string):
        text_bitmap = self.font.render(text_string, True, CLR.RED)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height

    def reset(self):
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15

    def indent(self):
        self.x_pos += 10

    def unindent(self):
        self.x_pos -= 10
