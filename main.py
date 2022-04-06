import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
highscore = 0

# Dino Movements
RUNNING = [pygame.image.load(os.path.join("Assets/Dino" , "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino","DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino","DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino","DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino","DinoDuck2.png"))]

# Obstacles
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus","SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus","SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus","SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus","LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus","LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus","LargeCactus3.png"))]

# Flying Obstacle
PTERO = [pygame.image.load(os.path.join("Assets/Bird","Bird1.png")),
         pygame.image.load(os.path.join("Assets/Bird","Bird2.png"))]

# Surroundings
CLOUD = pygame.image.load(os.path.join("Assets/Other","Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other","Track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 9
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self,userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
        if (userInput[pygame.K_UP] or userInput[pygame.K_w] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s] or userInput[pygame.K_LALT]) and not self.dino_jump:
            self.dino_jump = False
            self.dino_run = False
            self.dino_duck = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True

    def duck(self):
        self.image = self.duck_img[self.step_index//5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self,SCREEN):
        SCREEN.blit(self.image,(self.dino_rect.x,self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500,3000)
            self.y = random.randint(50,100)

    def draw(self,SCREEN):
        SCREEN.blit(self.image,(self.x,self.y))

class Obstacle:
    def __init__(self, image,type):
        self.image = image
        self.type = type # 0,1,2 index in the array
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self,SCREEN):
        SCREEN.blit(self.image[self.type],self.rect)

class SmallCactus(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image,self.type)
        self.rect.y = 300

class Ptero(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image,self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self,SCREEN):
        if self.index >= 9:
            self.index =0
        SCREEN.blit(self.image[self.index//5],self.rect)
        self.index += 1

def HighScore():
    with open('highscore.txt') as f:
        return f.read()

def main():
    global game_speed ,x_pos_bg ,y_pos_bg , points , obstacles
    obstacles = []
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0

    font = pygame.font.Font("freesansbold.ttf",15)
    deathcount = 0
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()

    try:
        highscore = int(HighScore())
    except:
        highscore = 0

    def score():
        global points , game_speed , highscore
        points += 1
        if points % 100 ==0:
            game_speed += 1

        text = font.render("Score: " + str(points),True,(0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000 , 40)
        SCREEN.blit(text,text_rect)

    def background():
        global x_pos_bg,y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG,(x_pos_bg,y_pos_bg))
        SCREEN.blit(BG,(image_width + x_pos_bg,y_pos_bg))
        if x_pos_bg <= - image_width:
            SCREEN.blit(BG,(image_width + x_pos_bg,y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255))
        userInput = pygame.key.get_pressed() # returns a list so userInput is a list  of inputs

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0 :
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2) == 1 :
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2) == 2 :
                obstacles.append(Ptero(PTERO))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                #pygame.draw.rect(SCREEN, (255,0,0), player.dino_rect,2)
                pygame.time.delay(2000)
                deathcount +=1
                menu(deathcount)
        background()
        score()
        cloud.draw(SCREEN)
        cloud.update()

        clock.tick(30)
        pygame.display.update()

def menu(deathcount):
    global points , highscore
    run = True

    while run:
        SCREEN.fill((255,255,255))
        font = pygame.font.Font('freesansbold.ttf',30)


        if deathcount == 0:
            text = font.render('Press any key to Start',True,(0,0,0))

            Highscore = font.render('Highscore : ' + str(HighScore()),True,(0,0,0))
            Highscore_Rect = Highscore.get_rect()
            Highscore_Rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2 + 50)
            SCREEN.blit(Highscore,Highscore_Rect)

        elif deathcount>0:
            text = font.render('Press any key to Restart',True,(0,0,0))

            score = font.render('Your Score: '+ str(points),True,(0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH //2 , SCREEN_HEIGHT//2 +50)
            SCREEN.blit(score,scoreRect)

            highscore = max(points, highscore)
            with open(('highscore.txt'),'w') as f:
                f.write(str(highscore))
            Highscore = font.render('Highscore : ' + str(HighScore()), True, (0, 0, 0))
            Highscore_Rect = Highscore.get_rect()
            Highscore_Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(Highscore, Highscore_Rect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        SCREEN.blit(text,textRect)
        SCREEN.blit(RUNNING[0],(SCREEN_WIDTH//2 - 20,SCREEN_HEIGHT//2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
menu(deathcount=0)
#main()