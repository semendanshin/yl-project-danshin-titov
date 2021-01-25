import pygame
import os
import sys
from random import randint


def load_im(name):
    fullname = os.path.join('imgs', name)
    try:
        return pygame.image.load(fullname)
    except FileNotFoundError:
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit(0)


class MySpriteGroup(pygame.sprite.Group):
    def draw(self, screen):
        for el in self.sprites():
            el.draw(screen)


class LoopedImage(pygame.sprite.Sprite):
    def __init__(self, img_name, speed, screen_size, *gropus):
        super().__init__(*gropus)
        self.speed = speed
        self.screen_size = screen_size
        self.image = load_im(img_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.w = self.rect.w * 2
        self.rect.x = 0
        self.rect.y = screen_size[1] - self.rect.size[1]
        self.shift = 0

    def update(self):
        self.shift = (self.shift + self.speed) % self.screen_size[0]

    def draw(self, screen):
        screen.blit(self.image, (-self.shift, self.rect.y))
        screen.blit(self.image, (self.rect.size[0] / 2 - self.shift, self.rect.y))

    def get_size(self):
        return self.rect.size

    def set_pos(self, pos):
        self.rect.x, self.rect.y = pos


class Sky(pygame.sprite.Sprite):
    def __init__(self, img_name, screen_size, *groups):
        super().__init__(*groups)
        self.screen_size = screen_size
        self.image = load_im(img_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, anim_count):
        super().__init__()
        self.images = [pygame.transform.scale(load_im(f'player/run_{i + 1}.png').convert_alpha(), (120, 142)) for i in range(anim_count)]
        self.anim_count = anim_count
        self.anim_ind = 0
        self.rect = self.images[self.anim_ind].get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1] - self.rect.size[1]
        self.ground_y_coord = self.rect.y
        self.jumping = False
        self.vy = 0
        self.t = 0
        self.g = 1

    def start_jump(self):
        if not self.jumping:
            self.vy = randint(20, 25)
            self.jumping = True
            self.t = 0
            self.g = 1

    def update(self):
        if self.jumping:
            if self.rect.y - (self.g * self.vy - self.t) >= self.ground_y_coord:
                self.rect.y = self.ground_y_coord
                self.jumping = False
            else:
                self.rect.y -= self.g * self.vy - self.t
            self.t += 1
        else:
            self.anim_ind = (self.anim_ind + 0.2) % (self.anim_count - 1)

    def draw(self, screen):
        screen.blit(self.images[round(self.anim_ind)], self.rect)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = self.width, self.height = screen.get_width(), screen.get_height()
        self.running = True
        self.clock = pygame.time.Clock()

    def load_objects(self, bg_num, player_num):
        self.background = MySpriteGroup()
        Sky('bg1/sky.png', self.screen_size, self.background)
        LoopedImage('bg1/clouds_1.png', 2, self.screen_size, self.background)
        LoopedImage('bg1/rocks.png', 5, self.screen_size, self.background)
        LoopedImage('bg1/ground1.png', 10, self.screen_size, self.background)
        self.ground = LoopedImage('ground.png', 25, self.screen_size)
        self.player = Player((200, self.height - self.ground.get_size()[1]), 6)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.start_jump()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen)
        self.ground.draw(self.screen)
        self.player.draw(self.screen)

    def main_loop(self):
        while self.running:
            print(self.clock.get_fps())
            self.clock.tick(60)
            self.check_events()

            self.ground.update()
            self.player.update()
            self.background.update()

            self.render()

            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('раннер')
    display_size = pygame.display.Info().current_w, pygame.display.Info().current_h
    SIZE = WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode(SIZE)
    game = Game(screen)
    game.load_objects(bg_num=1, player_num=1)
    game.main_loop()
    pygame.sprite.Group().draw()