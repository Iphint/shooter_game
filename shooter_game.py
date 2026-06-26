from pygame import * # type: ignore
from random import randint
from time import time as timer

# backsong music
mixer.init() # type: ignore
mixer.music.load('space.ogg') # type: ignore
mixer.music.play(-1) # type: ignore
fire_sound = mixer.Sound('fire.ogg') # type: ignore

# images
img_back = "galaxy.jpg" # type: ignore
img_hero = "rocket.png" # type: ignore
img_enemy = "ufo.png" # type: ignore
img_bullet = "bullet.png" # type: ignore
img_asteroid = "asteroid.png" # type: ignore

# score
score = 0
lost = 0
max_lost = 3
goal = 10
life = 3

# fonts
font.init() # type: ignore
font2 = font.SysFont('Arial', 26) # type: ignore
win = font2.render("YOU WIN!", 1, (255, 255, 255)) # type: ignore
lose = font2.render("YOU LOSE!", 1, (255, 255, 255)) # type: ignore
font2 = font.SysFont('Arial', 36) # type: ignore

# window
win_width = 700
win_height = 500
display.set_caption("Shooter") # type: ignore
window = display.set_mode((win_width, win_height)) # type: ignore
background = transform.scale(image.load(img_back), (win_width, win_height)) # type: ignore

# superclass for sprites
class GameSprite(sprite.Sprite): # type: ignore
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self) # type: ignore
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) # type: ignore
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) # type: ignore

# player class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() # type: ignore
        if keys[K_LEFT] and self.rect.x > 5: # type: ignore
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80: # type: ignore
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15) # type: ignore
        bullets.add(bullet)

# enemy class
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10) # type: ignore
monsters = sprite.Group() # type: ignore
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) # type: ignore
    monsters.add(monster)

asteroid = sprite.Group() # type: ignore
for i in range(1, 3):
    rock = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 7)) # type: ignore
    asteroid.add(rock)

bullets = sprite.Group() # type: ignore
finish = False
run = True
rel_time = False
num_fire = 0

while run:
    for e in event.get(): # type: ignore
        if e.type == QUIT: # type: ignore
            run = False
        elif e.type == KEYDOWN: # type: ignore
            if e.key == K_SPACE: # type: ignore
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        # background
        window.blit(background, (0, 0))

        # score text
        text = font2.render("Score: " + str(score), 1, (255, 255, 255)) # type: ignore
        window.blit(text, (10, 20))

        # lost text
        text_lose = font2.render("Lost: " + str(lost), 1, (255, 255, 255)) # type: ignore
        window.blit(text_lose, (10, 50))

        # ship
        ship.update()
        ship.reset()

        # monsters / enemy
        monsters.update()
        monsters.draw(window)

        # asteroid
        asteroid.update()
        asteroid.draw(window)

        # bullets
        bullets.update()
        bullets.draw(window)

        # reload
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        # collision
        collides = sprite.groupcollide(monsters, bullets, True, True) # type: ignore
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        # win conditions
        if score >= goal:
            finish = True
            mixer.music.stop() # type: ignore
            window.blit(background, (0, 0))
            draw.rect(window, (0, 100, 0), (170, 140, 360, 180)) # type: ignore
            draw.rect(window, (255, 255, 255), (170, 140, 360, 180), 4) # type: ignore
            win_text = font2.render("YOU WIN!", True, (255, 255, 255))
            score_text = font2.render("Final Score: " + str(score), True, (255, 255, 0))
            info_text = font2.render("Great job, pilot!", True, (255, 255, 255))
            window.blit(win_text, (265, 165))
            window.blit(score_text, (230, 215))
            window.blit(info_text, (230, 260))

        # collision ship with monster
        if sprite.spritecollide(ship, monsters, True):  # type: ignore
            life -= 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # collision ship with asteroid
        if sprite.spritecollide(ship, asteroid, True):  # type: ignore
            life -= 1
            rock = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
            asteroid.add(rock)

        # lose conditions
        if life <= 0 or lost >= max_lost:
            finish = True
            mixer.music.stop() # type: ignore
            window.blit(background, (0, 0))
            draw.rect(window, (120, 0, 0), (170, 140, 360, 180)) # type: ignore
            draw.rect(window, (255, 255, 255), (170, 140, 360, 180), 4) # type: ignore
            lose_text = font2.render("YOU LOSE!", True, (255, 255, 255))
            score_text = font2.render("Final Score: " + str(score), True, (255, 255, 0))
            info_text = font2.render("Try again, pilot!", True, (255, 255, 255))
            window.blit(lose_text, (255, 165))
            window.blit(score_text, (230, 215))
            window.blit(info_text, (230, 260))

        # text life
        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        elif life == 1:
            life_color = (150, 0, 0)
        text_life = font2.render(str(life), 1, life_color) # type: ignore
        window.blit(text_life, (650, 10))
        
        display.update() # type: ignore
    time.delay(50) # type: ignore



