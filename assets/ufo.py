from random import randint
import pygame 
import time

pygame.mixer.init()
pygame.mixer.music.load('assets/space.ogg')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound('assets/fire.ogg')

win_width = 700
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('UFO')
background = pygame.transform.scale(pygame.image.load('assets/galaxy.jpg'), (win_width, win_height))
clock = pygame.time.Clock()
score = 0
missed = 0
bullets = pygame.sprite.Group()

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

win_text = font.render('You win!', True, (255, 255, 255))
lose_text = font.render('You lose!', True, (255, 255, 255))

game = True
finish = False
pause = False

last_time_fire = time.time()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[pygame.K_d] and self.rect.x < win_width - 80:
            self.rect.x += 5
        if keys[pygame.K_SPACE]:
            fire_sound.play()
    def fire(self):
        global last_time_fire
        current_time = time.time()
        if current_time - last_time_fire > 0.01:  # Fire rate limit
            last_time_fire = current_time
            bullet = Bullet('assets/bullet.png', self.rect.centerx - 10, self.rect.y, 20, 40)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed 
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(5, win_width - self.rect.width)
            self.speed = randint(1, 4)
            self.rect.x += self.speed
            missed += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 10
        if self.rect.y < -50:
            self.kill()

player = Player('assets/ufo.png', 300, 400, 80, 80)
aliens = pygame.sprite.Group()
for i in range(7):
    alien = Enemy('assets/asteroid.png', randint(5, win_width - 80), -40, 80, 80)
    alien.speed = randint(1, 4)
    aliens.add(alien)
    rocket = Enemy('assets/rocket.png', randint(5, win_width - 80), -40, 80, 80)
    rotated_surface = pygame.transform.rotate(rocket.image, 180)
    rocket.image = rotated_surface
    rocket.speed = randint(1, 3)
    aliens.add(rocket)
paused_surface = font.render('Paused', True, (255, 255, 255))
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player.fire()
            if e.key == pygame.K_ESCAPE:  # Перенесіть сюди і змініть e.type на e.key
                pause = not pause 

    if pause :
        window.blit(paused_surface, (win_width // 2 - paused_surface.get_width() // 2, win_height // 2 - paused_surface.get_height() // 2))
        pygame.display.update()
                
        

    if not finish and not pause:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        aliens.update()
        aliens.draw(window)
        bullets.update()
        bullets.draw(window)

        score_label = font.render(f'Score: {score}', True, (255, 255, 255))
        missed_label = font.render(f'Misses: {missed}', True, (255, 255, 255))
        window.blit(score_label, (10, 10))
        window.blit(missed_label, (10, 40))

        collides = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for c in collides:
            score += 1
            alien = Enemy('assets/asteroid.png', randint(5, win_width - 80), -40, 80, 80)
            rocket = Enemy('assets/rocket.png', randint(5, win_width - 80), -40, 80, 80)
            rotated_surface = pygame.transform.rotate(rocket.image, 180)
            rocket.image = rotated_surface
        if pygame.sprite.spritecollide(player, aliens, False) or missed >= 100:
            finish = True
            window.blit(lose_text, (win_width // 2 - lose_text.get_width() // 2, win_height // 2 - lose_text.get_height() // 2))
        if score >= 100:
            finish = True
            window.blit(win_text, (win_width // 2 - win_text.get_width() // 2, win_height // 2 - win_text.get_height() // 2))

        pygame.display.update()

    if pause:
        window.blit(paused_surface, (win_width // 2 - paused_surface.get_width() // 2, win_height // 2 - paused_surface.get_height() // 2))
    clock.tick(60)