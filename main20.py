# TEE PELI TÄHÄN
import pygame
from random import randint, seed
from datetime import datetime
from csv import reader, writer

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((800,600))
        self.morko = pygame.image.load("hirvio.png")
        self.raha = pygame.image.load("kolikko.png")
        self.robo = pygame.image.load("robo.png")
        pygame.display.set_caption("Mörkö - Get the money and jump!")
        self.clock = pygame.time.Clock()
        self.hof = self.read_hof()
        # apumuuttujia
        self.m_w = self.morko.get_width()
        self.m_h = self.morko.get_height()
        self.robo_w = self.robo.get_width()
        self.robo_h = self.robo.get_height()
        # aloitusnäyttö
        self.alkuarvot()
        while True:
            self.get_events()
            self.map()
            self.header()
            self.morko_liikkuu()
            name1 = self.fontti2.render(f"Mörkö", True, (255, 255, 255))
            self.win.blit(name1, (400-name1.get_width()/2, 300-name1.get_height()))
            name2 = self.fontti.render(f"Get the money and jump!", True, (255, 255, 255))
            self.win.blit(name2, (400-name2.get_width()/2, 300))
            hof = self.fontti.render(f"Hit TAB to view the Hall of Fame", True, (255, 255, 255))
            self.win.blit(hof, (400-hof.get_width()/2, 500))
            pygame.display.flip()
            self.clock.tick(60)

    def alkuarvot(self):
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
        self.fontti3 = pygame.font.SysFont("Quivira", 12)
        self.over = False
    
    def read_hof(self):
        try:
            with open("hof.tsv") as file:
                hof = []
                data = reader(file, delimiter="\t")
                for row in data:
                    hof.append({"time": row[0], "points": int(row[1]), "name": row[2], "win": row[3]})
                return hof
        except:
            return []

    def write_hof(self):
        with open("hof.tsv", "w", newline="") as file:
            def order(i):
                return i["points"]
            hofs = sorted(self.hof, key=order, reverse=True)
            write = writer(file, delimiter="\t")
            if len(hofs) > 21:
                for i in range(20):
                    write.writerow(hofs[i].values())
            else:
                for row in hofs:
                    write.writerow(row.values())
    
    def halloffame(self):
        self.alkuarvot()
        self.hof = self.read_hof()
        while True:
            self.get_events()
            self.map()
            self.header()
            self.morko_liikkuu()
            hoftext = self.fontti2.render("Hall of Fame", True, (255,255,255))
            self.win.blit(hoftext, (400-hoftext.get_width()/2, 80))
            dtext = self.fontti.render(f" points              name             date & time    ", True, (255,255,255))
            self.win.blit(dtext, (400-dtext.get_width()/2, 150))
            if len(self.hof) < 10:
                x = 1
                for i in self.hof:
                    row = list(i.values())
                    if row[3] == "1":
                        text = self.fontti.render(f"{row[1]}   {row[2][:30]:.>30}   {row[0]:20}", True, (255,255,255))
                    else:    
                        text = self.fontti.render(f"( {row[1]}   {row[2][:30]:.>30}   {row[0]:20})", True, (255,255,255))
                    self.win.blit(text, (400-text.get_width()/2, 180+30*x))
                    x+=1
            else:
                for i in range(10):
                    row = list(self.hof[i].values())
                    if row[3] == "1":
                        text = self.fontti.render(f"{row[1]}   {row[2][:30]:.>30}   {row[0]:20}", True, (255,255,255))
                    else:    
                        text = self.fontti.render(f"( {row[1]}   {row[2][:30]:.>30}   {row[0]:20})", True, (255,255,255))
                    self.win.blit(text, (400-text.get_width()/2, 180+30*i))
            pygame.display.flip()
            self.clock.tick(60)

    def game(self):
        # alkuarvot
        self.alkuarvot()
        # peli käyntiin
        while True:
            self.get_events()
            self.window()
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.write_hof()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.write_hof()
                    exit()
                if event.key == pygame.K_F2:
                    self.game()
                if event.key == pygame.K_TAB:
                    self.halloffame()
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
                #print(pygame.key.name(event.key))

    def window(self):
        if self.game_over():
            return
        # kenttä
        self.map()
        #  mörkö liikkuu
        self.morko_liikkuu()
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
            if self.gforce > 0 and (self.mx < robo[0] < self.mx+self.m_w or self.mx < robo[0]+self.robo_w < self.mx+self.m_w) and robo[1] < self.my+self.m_h < robo[1]+20:
                robo[1] += 5
                self.points += 4
                self.gforce = -1
            if self.my+self.m_h-20 > robo[1] and (robo[0]+8 < self.mx+self.m_w < robo[0]+self.robo_w-8 or robo[0]+8 < self.mx < robo[0]+self.robo_w-8):
                self.over = True        # peli päättyy
                gameover = self.fontti2.render(f"GAME OVER", True, (255, 255, 255))
                hof = self.fontti.render(f"Hit TAB to view the Hall of Fame", True, (255, 255, 255))
                self.win.blit(gameover, (400-gameover.get_width()/2, 300-gameover.get_height()/2))
                if len(self.hof) < 10 or self.points > self.hof[9]["points"]:
                    help = self.fontti.render("save: RETURN", True, (255, 255, 255))
                    self.win.blit(help, (5, 5))
                    name = self.ask_name()
                    pygame.draw.line(self.win, (0,0,0), (0,18), (800,18), 36)
                    self.hof.append({"time": str(datetime.now())[:19], "points": self.points, "name": name, "win": 0})
                    self.write_hof()
                self.win.blit(hof, (400-hof.get_width()/2, 500))
        # pisteet näkyviin 
        self.header()
        if self.points > 30*self.lvl:
            self.lvl += 1
        # voitto
        if self.lvl == 11:
            self.victory()
        pygame.display.flip()
        self.clock.tick(60)

    def morko_liikkuu(self):
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

    def map(self):
        self.win.fill((150,150,255))
        pygame.draw.line(self.win, (0,220,0), (0,595), (800,595), 10)
        pygame.draw.line(self.win, (0,0,0), (0,18), (800,18), 36)

    def header(self):
        help = self.fontti.render("move: < ^ >     new game: F2     exit: ESC", True, (255, 255, 255))
        points = self.fontti.render(f"Level {self.lvl}/ 10     Points: {self.points}", True, (255, 255, 255))
        self.win.blit(help, (5, 5))
        self.win.blit(points, (795-points.get_width(), 5))

    def game_over(self):
        return self.over
    
    def victory(self):
        self.over = True
        gameover1 = self.fontti2.render(f"You did it,", True, (255, 255, 255))
        self.win.blit(gameover1, (400-gameover1.get_width()/2, 300-gameover1.get_height()))
        gameover2 = self.fontti2.render(f"got the money and jumped!", True, (255, 255, 255))
        self.win.blit(gameover2, (400-gameover2.get_width()/2, 300))
        hof = self.fontti.render(f"Hit TAB to view the Hall of Fame", True, (255, 255, 255))
        if len(self.hof) < 10 or self.points > self.hof[9]["points"]:
            help = self.fontti.render("save: RETURN", True, (255, 255, 255))
            self.win.blit(help, (5, 5))
            name = self.ask_name()
            pygame.draw.line(self.win, (0,0,0), (0,18), (800,18), 36)
            self.hof.append({"time": str(datetime.now())[:19], "points": self.points, "name": name, "win": 1})
            self.write_hof()
        self.win.blit(hof, (400-hof.get_width()/2, 500))

    def text(self, word, x, y):
        text = self.fontti.render("{}".format(word), True, (255,255,255))
        return self.win.blit(text,(x,y))
    def ask_name(self):
        word=""
        hoftext = self.fontti2.render("You got a high score!", True, (255, 255, 255))
        self.win.blit(hoftext, (400-hoftext.get_width()/2, 375))
        pygame.draw.line(self.win, (150, 150, 255), (0,455), (400,455), 30)
        self.text("Enter your name: ", 200, 440)
        pygame.display.flip()
        typing = True
        while typing:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    inkey = event.key
                    if 33 <= inkey <= 122 or inkey == pygame.K_SPACE:
                        word+=str(chr(inkey))
                    if inkey == pygame.K_BACKSPACE:
                        word = word[:-1]
                    if inkey == pygame.K_RETURN:
                        typing=False
                    pygame.draw.line(self.win, (150, 150, 255), (400,455), (800,455), 30)
                    self.text(word, 400, 440)
                    pygame.display.flip()
        return word


if __name__=="__main__":
    Game()
