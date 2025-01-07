from pygame import *
from random import *
from time import time as timer
mixer.init()


w_wid = 700
w_hei = 500
win = display.set_mode(
    (w_wid,w_hei)
)
display.set_caption('Shooter')
background = transform.scale(
    image.load('war.jpeg'),
    (w_wid,w_hei)
)

mixer.music.load('War.mp3')
mixer.music.play()
fire_Sound = mixer.Sound('fire.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image),(size_x,size_y)
        )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < w_wid-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)


lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= w_hei:
            self.rect.x = randint(80,w_wid-80)
            self.rect.y = 0
            lost += 1


class Astro(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= w_hei:
            self.rect.x = randint(80,w_wid-80)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.SysFont('Arial',60)
font2 = font.SysFont('Arial',36)
font3 = font.SysFont('Arial',30)


tank = Player('tank3.png',5,w_hei-100,80,100,10)
asteroids = sprite.Group()
monsters = sprite.Group()
for e in range(5):
    monster = Enemy('ufo.png',randint(80,w_wid-80),-40,80,50,randint(1,5))
    monsters.add(monster)
for e in range(2):
    asteroid = Astro('asteroid.png',randint(80,w_wid-80),-40,80,50,randint(1,2))
    asteroids.add(asteroid)

bullets = sprite.Group()

run = True
finish = False 
score1 = 0
rel_time = False
num_fire = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    fire_Sound.play()
                    tank.fire()
                    num_fire += 1
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start = timer()
    if not finish:
        win.blit(background,(0,0))
        tank.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        text_win = font2.render('Счёт: ' + str(score1),1,(0,0,0))
        text_lose = font2.render('Пропущено: ' + str(lost),1,(0,0,0))
        winner = font1.render('Ты победитель!',1,(0,255,0))
        loser = font1.render('Ты проиграл!',1,(255,0,0))
        sprites_list = sprite.groupcollide(
            monsters,bullets,True,True
        )
        if rel_time == True:
            end = timer()
            if end-start < 3:
                reload1 = font3.render('Подожди,идёт перезарядка...',1,(255,10,10))
                win.blit(reload1,(260,460))
            else:
                num_fire = 0
                rel_time = False
        for e in sprites_list:
            score1 += 1
            monster = Enemy('ufo.png',randint(80,w_wid-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        if score1 >= 10:
            win.blit(winner,(180,200)) 
            finish = True
        if lost >= 3 or sprite.spritecollide(tank,monsters,False) or sprite.spritecollide(tank,asteroids,False):
            win.blit(loser,(200,200))
            finish = True               
        win.blit(text_win,(10,20))
        win.blit(text_lose,(10,50))
        monsters.draw(win)
        asteroids.draw(win)
        bullets.draw(win)
        tank.reset()
        display.update()
    time.delay(60)