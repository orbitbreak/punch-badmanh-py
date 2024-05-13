# Punch Badman-H right in the face by clicking on him.
# He is crafty though, and may attempt to dodge.
# 
# A basic pygame project.

import pygame, os
from pygame.locals import *

def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Image file', fullname, 'was not found.'
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Sound file', fullname, 'was not found.'
        raise SystemExit, message
    return sound


#classes for our game objects
class Fist(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0

    def update(self):
        # move the fist based on the mouse position
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        # eturns true if the fist collides with the target
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        # called to pull the fist back
        self.punching = 0


class BadmanH(pygame.sprite.Sprite):

	# moves badmanh across the screen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('badmanh.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        # move badmanh across the screen, and turn at the ends
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
           self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        # spin the badmanh image
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center = center)

    def punched(self):
        # start spinning
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((700, 300))
    pygame.display.set_caption('Punch Badman-H')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((100, 100, 100))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 48, bold = True)
        text = font.render("Punch Badman-H Right In His Stupid Face", 1, (150, 0, 0))
        textpos = text.get_rect(centerx = background.get_width() / 2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    badmanh = BadmanH()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, badmanh))

# main
    while 1:
        clock.tick(100)

    # input events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(badmanh):
                    punch_sound.play() # punch
                    badmanh.punched()
                else:
                    whiff_sound.play() # miss
            elif event.type is MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

    # redraw
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()

