import pygame
from pygame.locals import *
from math import sin, cos, sqrt, radians
import random

#teste

#-----------------------COMANDOS-----------------------

#Clique na tecla R -> Gera novas paredes aleatoriamente

#Clique na tecla C -> Limpa todas as paredes

#Clique na tecla N -> Cria uma nova parede    
#Ao clicar n, os raios de luz deixarao de ser projetados
#Use o botao direito do mouse para selecionar as coordenadas 
#da parede

#------------------------------------------------------


#Iniciando a janela 
pygame.init()
height = 600
width = 600
win = pygame.display.set_mode((height,width))



#Variaveis
color = (0,0,0)
num_rays = 360
num_walls = 5


class Particle:
    def __init__(self, x, y):
        """Construtor da classe particula
        float, float -> Particle"""
        self.x = x
        self.y = y
        self.rays = []
    
    def update(self,x,y):
        """Funcao que atualiza a posicao da particula e seus raios
        float, float -> None"""
        self.x = x
        self.y = y
        for ray in self.rays:
            ray.move(self.x,self.y)
        
    
    def look_for_walls(self,walls):
        """Funcao que checa se um raio colidiu com uma parede, desenha sua trajetoria
        list -> None"""
        for i in range(len(self.rays)):
            closest = None                                  #Ponto mais perto
            record = 100000000000                           #Distancia da particula ate o ponto mais perto
            for wall in walls:
                point = self.rays[i].collision(wall)       
                if point:
                    distance = sqrt((self.rays[i].x - point[0])**2 + (self.rays[i].y - point[1])**2)
                    if distance < record:
                        record = distance
                        closest = point
            if closest:
                pygame.draw.line(win,color,(self.rays[i].x,self.rays[i].y),closest)
                    

class Ray:
    def __init__(self,x,y,angle):
        """Construtor da classe Ray
        float, float, float -> Ray"""
        self.x = x
        self.y = y
        self.dir = (sin(angle),cos(angle))
    
    def move(self,mx,my):
        """Funcao que move o raio de luz
        float, float -> None"""
        self.x = mx
        self.y = my
    
    def collision(self,wall):
        """Funcao que checa se o raio de luz colidiu com uma parede
        Wall -> Tuple/Bool """

        #Coordenadas da parede
        x1 = wall.x1
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2


        #Coordenadas do raio de luz
        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0]
        y4 = self.y + self.dir[1]


        #Utilizando a formula de "line-line intersection" para 
        #Determinar se o raio de luz colide com a parede
        den = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        if den == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if (t > 0 and t < 1 and u > 0):
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x,y)
        else:
            return False


class Wall:
    def __init__(self,x1,y1,x2,y2):
        """Construtor da classe Wall recebe as coordenadas da parede
        float, float, float, float -> Wall"""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self):
        """Desenha a parede
        None -> None"""
        pygame.draw.line(win,color,(self.x1, self.y1),(self.x2 ,self.y2))


def generateWalls():
    """Funcao que gera aleatoriamente paredes dentro do espaço permitido
    None -> None"""
    walls.clear()

    walls.append(Wall(0, 0, height, 0))
    walls.append(Wall(0, 0, 0, width))
    walls.append(Wall(height, 0, width, height))
    walls.append(Wall(0, width, height, width))

    for i in range(num_walls):
        x1 = random.randint(0, height)
        y1 = random.randint(0, width)
        x2 = random.randint(0, height)
        y2 = random.randint(0, width)
        walls.append(Wall(x1, y1, x2, y2))


def Draw(Particle,Walls):
    """Funcao que desenha as paredes e os raios de luz"""
    for wall in walls:
        wall.draw()
    Particle.look_for_walls(walls)



#Iniciando a particula
x, y = pygame.mouse.get_pos()
part = Particle(x,y)
for i in range(0, 360, int(360/num_rays)):
    part.rays.append(Ray(x, y,radians(i)))

#Iniciando as paredes
walls = []
generateWalls()

running = True                          #Bool para dizer se o progama esta rodando
casting = True                          #Bool para dizer se estamos projetando os raios de luz ou nao
new_wall_a = False                      #Variavel utilizada para criar uma nova parede
new_wall_b = False                      #Variavel utilizada para criar uma nova parede


while running:

    events = pygame.event.get()                                #Interacoes homem maquina
    mx, my = pygame.mouse.get_pos()                            #Posicao do mouse
    left, middle, right = pygame.mouse.get_pressed()           #Bool utilizado para o clique do mouse

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_r:                        #Evento de apertar r (gerar novas parede)
               generateWalls()
            if event.key == pygame.K_c:                        #Evento de apertar c (limpar as paredes)
                del walls[4:]
            if event.key == pygame.K_n:                        #Evento de apertar n (nova parede)
                casting = not casting
        if event.type == MOUSEBUTTONDOWN:      
            if left and not casting:
                if new_wall_a:
                    new_wall_b = (mx,my)
                    walls.append(Wall(new_wall_a[0], new_wall_a[1], new_wall_b[0], new_wall_b[1]))
                    new_wall_a = False
                    new_wall_b = False
                    casting = not casting
                else:
                    new_wall_a = (mx,my)
    part.update(mx,my)
    win.fill((255, 255, 255))

    #Desenhando
    if casting == True:
        Draw(part,walls)
    else:
        if new_wall_a:
            pygame.draw.line(win,(255,0,0),(new_wall_a[0],new_wall_a[1]),(mx,my))
        for wall in walls:
            wall.draw()

    pygame.display.update()