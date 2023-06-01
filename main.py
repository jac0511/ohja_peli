# TEE PELI TÄHÄN
import pygame
from random import randint, seed

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((800,600))
        self.morko = pygame.image.load("hirvio.png")
        self.raha = pygame.image.load("kolikko.png")
        self.robo = pygame.image.load("robo.png")
        pygame.display.set_caption("Mörkö - get the money and jump")
        self.clock = pygame.time.Clock()
        # apumuuttujia
        self.m_w = self.morko.get_width()
        self.m_h = self.morko.get_height()
        self.robo_w = self.robo.get_width()
        self.robo_h = self.robo.get_height()
        # pelin aloitus
        self.game()

    def game(self):
        # alkuarvot
        self.lvl = 1
        self.mx, self.my = 20, 590-self.m_h
        self.rahet = [[800, 450]]
        self.army = []
        # kenttä aina sama vaikka asiat satunnaisissa paikoissa:
        seed(2)
        self.right, self.left = False, False
        self.gforce = 0
        self.points = 0
        self.fontti = pygame.font.SysFont("Quivira", 24)
        self.fontti2 = pygame.font.SysFont("Quivira", 48)
        self.over = False
        # peli käyntiin
        while True:
            self.get_events()
            self.window()
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_F2:
                    self.game()
                if self.game_over():
                    return
                # lukossa kun peli päättynyt: 
                if event.key == pygame.K_UP and -1.4 < self.gforce < 1.4:
                    self.gforce = -7
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_RIGHT:
                    self.right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right = False

    def window(self):
        if self.game_over():
            return
        # kenttä
        self.win.fill((150,150,255))
        pygame.draw.line(self.win, (0,220,0), (0,595), (800,595), 10)
        pygame.draw.line(self.win, (0,0,0), (0,18), (800,18), 36)
        #  mörkö liikkuu
        if self.right == True and self.mx < 800-self.m_w:
            self.mx += 2
        if self.left == True and self.mx > 0:
            self.mx -= 3
        if self.gforce != 0 and self.my <= 591-self.m_h:
            self.my += self.gforce
            if self.my > 590-self.m_h:
                self.my = 590-self.m_h
                self.gforce = 0
            else:
                self.gforce += 0.2
        self.win.blit(self.morko, (self.mx, self.my))
        # satunnaisarvot rahelle ja robolle
        rnd = randint(0, 360//(self.lvl//3+1))
        if rnd < 1:
            self.army.append([800, 590-self.robo_h])
        if 9 <= rnd <= 9+self.lvl//3:
            self.rahet.append([800, randint(590//(self.lvl+1), 590-self.raha.get_height())])
        i = 0
        # rahet liikkuu 
        for rahe in self.rahet:
            rahe[0] -= 1
            i += 1
            self.win.blit(self.raha, (rahe[0], rahe[1]))
            # rahe poistuu
            if rahe[0] < -50:
                self.rahet.remove(rahe) 
                self.points -= 1
            # osuma raheen
            if (self.mx < rahe[0]+5 < self.mx+self.m_w or self.mx < rahe[0]+35 < self.mx+self.m_w) and (self.my < rahe[1]+5 < self.my+self.m_h or self.my < rahe[1]+35 < self.my+self.m_h):
                self.rahet.remove(rahe) 
                self.points += 2
        # robot liikkuu
        for robo in self.army:
            if robo[1] > 590-self.robo_h:
                robo[1] += 5
            robo[0] -= self.lvl/4+0.75
            self.win.blit(self.robo, (robo[0], robo[1]))
            # robo poistuu
            if robo[0] < -150:
                self.army.remove(robo)  
                self.points -= 2
            if robo[1] > 600:
                self.army.remove(robo)
            # roboon osuu
            if self.gforce > 0 and (self.mx < robo[0] < self.mx+self.m_w or self.mx < robo[0]+self.robo_w < self.mx+self.m_w) and robo[1] < self.my+self.m_h < robo[1]+10:
                robo[1] += 5
                self.points += 4
                self.gforce = -1
            if self.my+self.m_h-10 > robo[1] and (robo[0]+8 < self.mx+self.m_w < robo[0]+self.robo_w-8 or robo[0]+8 < self.mx < robo[0]+self.robo_w-8):
                self.over = True        # peli päättyy
                gameover = self.fontti2.render(f"GAME OVER", True, (255, 255, 255))
                self.win.blit(gameover, (400-gameover.get_width()/2, 300-gameover.get_height()/2))
        if self.points > 60*self.lvl:
            self.lvl += 1
        # pisteet näkyviin 
        help = self.fontti.render("move: < ^ >     new game: F2     exit: ESC", True, (255, 255, 255))
        points = self.fontti.render(f"Taso {self.lvl}/ 10     Pisteet: {self.points}", True, (255, 255, 255))
        self.win.blit(help, (5, 5))
        self.win.blit(points, (795-points.get_width(), 5))
        # voitto
        if self.lvl == 11:
            self.over = True
            gameover1 = self.fontti2.render(f"You did it,", True, (255, 255, 255))
            self.win.blit(gameover1, (400-gameover1.get_width()/2, 300-gameover1.get_height()))
            gameover2 = self.fontti2.render(f"got the money and jumped!", True, (255, 255, 255))
            self.win.blit(gameover2, (400-gameover2.get_width()/2, 300))
        pygame.display.flip()
        self.clock.tick(60)

    def game_over(self):
        return self.over

if __name__=="__main__":
    Game()