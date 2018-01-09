import pygame
from pygame import gfxdraw

NUM_KEYS = 128

class Key(object):
    def __init__(self, index, width, height):
        self.index = index
        self.width = width - 4
        self.height = height
        self.left_edge = index * width
        self.state = 0
        self.channel = 0 # 0-15
        self.colour_off = pygame.Color(30, 30, 30)
        # Unique color for each channel
        self.colour_on = [(int(c*360.0/16), 100, 100, 100) for c in range(16)]

    def draw(self, surface):
        colour = pygame.Color(0, 0, 0)
        if self.state:
            colour.hsva = self.colour_on[self.channel]
        else:
            colour = self.colour_off
        pygame.draw.rect(surface, colour, (self.left_edge, 0, self.width, self.height))

class Display(object):
    def __init__(self):
        self.running = True
        self.screen = None

        # Pygame setup
        pygame.init()
        disp_info = pygame.display.Info()
        pygame.display.set_caption("MIDI-visualizer")
        self.width = int(disp_info.current_w)
        self.height = int(disp_info.current_h) 
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE)

        # Keys setup
        self.keys_width = float(self.width) / NUM_KEYS
        self.keys_height = 50
        self.keys = []
        for key_index in range(NUM_KEYS):
            key = Key(key_index, self.keys_width, self.keys_height)
            self.keys.append(key)
            key.draw(self.screen)

        ## Color scheme
        self.bg_color = pygame.Color(5, 5, 5)
        ## Font
        # self.pFont = pygame.font.SysFont("monospace", int(self.width/(self.width/17)), True)

    def receive(self, msg):
        key = self.keys[msg.note]
        if msg.type == 'note_on':
            key.state = 1
            key.channel = msg.channel
        elif msg.type == 'note_off':
            key.state = 0
            key.channel = msg.channel
        key.draw(self.screen)
        self.update()

    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
