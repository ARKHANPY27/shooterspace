from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg"
img_player = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)

score = 0
missed = 0
goal = 10
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, image_path, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = speed

    def reset(self):
        window.blit(self.image, self.rect.topleft)

    def draw(self):
        window.blit(self.image, self.rect.topleft)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 5, self.rect.top, 10, 20, -10)
        bullets.add(bullet)
        fire_sound.play()

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global score
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

player = Player(img_player, 5, win_height - 100, 80, 100, 10)
bullets = sprite.Group()
enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy(img_enemy, randint(80, win_width - 0), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)

finish = False
run = True
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        hits = sprite.groupcollide(enemies, bullets, True, True)
        not_hits = sprite.groupcollide(enemies, bullets, False, False)
        for hit in hits:
            score += 1
            new_enemy = Enemy(img_enemy, randint(0, win_width - 50), randint(-100, -40), 50, 50, randint(2, 5))
            enemies.add(new_enemy)

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose_text, (win_width // 2 - 100, win_height // 2))

        if missed >= 3:
            finish = True
            lose_text = font1.render("YOU LOSE!", True, (0, 0, 0))
            window.blit(lose_text, (win_width // 2 - 100, win_height // 2))

        if score >= goal:
            finish = True
            win_text = font1.render("YOU WIN!", True, (0, 0, 0))
            window.blit(win_text, (win_width // 2 - 100, win_height // 2))

        score_text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        missed_text = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(score_text, (10, 20))
        window.blit(missed_text, (10, 50))
        window.blit(text_lose, (10, 50))
        
        player.update()
        player.draw()
        player.reset()


        bullets.update()
        bullets.draw(window)

        enemies.update()
        enemies.draw(window)
        collides = sprite.groupcollide(enemies, bullets, True, True)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, Reload . . .', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            enemies.add(monster)

        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, enemies, False)
            sprite.spritecollide(player, asteroids, False)
            life = life - 1
            finish = True
            window.blit(text_lose, (200, 200))
        
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    else:
        score = 0
        lost = 0
        run = 0

        for b in bullets:
            b.kill()
        for m in enemies:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,6):
            enemy = Enemy(img_enemy, randint(80, win_width - 0), -40, 80, 50, randint(1, 5))
            enemies.add(enemy)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50)