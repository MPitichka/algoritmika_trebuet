from pygame import *
from random import randint
w = 700
h = 500

window = display.set_mode((w,h))
display.set_caption('Шутер')

bg = transform.scale(image.load('galaxy.jpg'), (w,h))

class GameSprite(sprite.Sprite):
    def __init__(self, imagefile, x,y,w=50,h=50,speed=0):
        super().__init__()
        self.image = transform.scale(image.load(imagefile), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        k = key.get_pressed()
        if k[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if k[K_RIGHT] and self.rect.x < w - 30:
            self.rect.x += self.speed
        if k[K_SPACE]:
            fire_sound.play()
            bullets.add(Bullet('bullet.png', self.rect.centerx,self.rect.top,10,20,5))

lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        global lost, w
        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(0,w)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Player('rocket.png', w//2,h-80,50,75,5)
ufos = sprite.Group()
bullets = sprite.Group()
for i in range(6):
    ufo1 = Enemy('ufo.png', randint(0,w), 0,75,50,randint(1,4))
    ufos.add(ufo1)

mixer.init()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None,36)

lose_text = font1.render('ТЫ проиграл!', 1,(255,0,0))
win_text = font1.render('Ты выйграл!', 1,(0,255,0))

run = True
finish = False
while run:
    window.blit(bg,(0,0))
    text_lose = font1.render('Пропущено:'+str(lost),1,(255,255,255))
    window.blit(text_lose,(10,40))
    text_score = font1.render('СЧет:' +str(score),1,(255,255,255))
    window.blit(text_score,(10,20))
    rocket.reset()
    ufos.draw(window)
    bullets.draw(window)
    if finish == False:

        
        rocket.update()
        
        ufos.update()
        
        bullets.update()

    if lost > 3 or sprite.spritecollide(rocket, ufos, False):
        window.blit(lose_text, (280,250))
        finish = True
    
    if score >= 10:
        window.blit(win_text, (280,250))
        finish = True
    sprite_list = sprite.groupcollide(ufos,bullets,True,True)
    for item in sprite_list:
        score += 1
        ufos.add(Enemy('ufo.png', randint(0,w), 0,75,50,randint(1,4)))
    for e in event.get():
        if e.type == QUIT:
            run = False

    display.update()
    time.delay(18)