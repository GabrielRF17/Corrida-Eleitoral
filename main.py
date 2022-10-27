from email.mime import image
import pygame
import os
from pygame import font
from random import randint
import random
from yaml import load
pygame.init()

TELA_LARGURA = 1380
TELA_ALTURA = 640

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption('Fome Zero')

relogio = pygame.time.Clock()
FPS = 60

#Colocando a música de fundo do jogo

pygame.mixer.init()
pygame.mixer.music.load('musicafundo.mp3')
pygame.mixer.music.play(-1)

tempo =  0
movimento_esquerda = False
movimento_direita = False
movimento_Cima = False
movimento_Baixo = False

tela_fundo = (227, 38, 54)

def desenho_tela():
    fundo=pygame.image.load('0.jpg')
    tela.blit(fundo,(0,0))

class Lula(pygame.sprite.Sprite):
    def __init__(self, jogador_tipo, x, y, scale, velocidade):
    
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.jogador_tipo = jogador_tipo
        self.velocidade = velocidade
        self.vel_y = 0
        self.direcao = 1
        self.virar = False
        self.animacao_lista = []
        self.frame_index = 0
        self.acao = 0
        self.atualizar_tempo = pygame.time.get_ticks()
        self.p=0
        h=0
        animacao_tipo = ['Parado', 'Correr' ]
        scale=1
        for animacao in animacao_tipo:
            temp_list = []
            numero_de_frames = len(os.listdir(f'img/{self.jogador_tipo}/{animacao}'))
            for i in range(numero_de_frames):
                img = pygame.image.load(f'img/{self.jogador_tipo}/{animacao}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animacao_lista.append(temp_list)

        self.image = self.animacao_lista[self.acao][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def comida(self):
        self.rect.x =randint(10,500)
        self.rect.y=randint(10,500)
    def mov1(self,movimento_esquerda):
            self.rect.x = -500
    def mov(self,movimento_direita):
            dx=0
            if self.rect.x>randint(1500,100000):
                self.rect.x=-50
            dx = self.velocidade
            self.virar = False
            self.direcao = 1
            self.rect.x += dx
            

    def movimento(self, movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo):


        dx = 0
        dy=0
        
        if movimento_esquerda and self.rect.x > 0:
            
            dx = -self.velocidade
            self.virar = True
            self.direcao = -1
            
        if movimento_direita and self.rect.x < 1300:

            dx = self.velocidade
            self.virar = False
            self.direcao = 1
        
        if movimento_Baixo and self.rect.y < 560:

            dy = self.velocidade
            self.virar = False
            self.direcao = 1
            
        if movimento_Cima and self.rect.y > 0:

            dy = -self.velocidade
            self.virar = False
            self.direcao = -1
            
        if movimento_esquerda and movimento_Baixo:
            self.virar = True
        
        if movimento_esquerda and movimento_Cima:
            self.virar = True
        
        self.rect.x += dx
        self.rect.y += dy
       
        
    def atualizar_animacao(self):
            ANIMACAO_FRESH = 150

            self.image = self.animacao_lista[self.acao][self.frame_index]

            if pygame.time.get_ticks() - self.atualizar_tempo > ANIMACAO_FRESH:
                self.atualizar_tempo = pygame.time.get_ticks()
                self.frame_index += 1

            if self.frame_index >= len(self.animacao_lista[self.acao]):
                self.frame_index = 0

    def atualizar_acao(self, new_action):
        if new_action != self.acao:
                self.acao = new_action

                self.frame_index = 0
                self.atualizar_tempo = pygame.time.get_ticks()

    def desenho(self):
            tela.blit(pygame.transform.flip(self.image, self.virar, False), self.rect)

#personagens e seu local de imagens, local no mapa e velocidade
jogador = Lula('Lula', 50, 50, 2, 10)
inimigo = Lula('Bolsonaro', 500, 500, 2, 25)
jacare =  Lula('inimigo',50,200,2,20)
jacare1 = Lula('inimigo',-50,400,2,15)
jacare2 = Lula('inimigo',10,350,2,25)
jacare3 = Lula('inimigo',20,300,2,12)
jacare4 = Lula('inimigo',-30,250,2,10)
jacare5 = Lula('inimigo',50,250,2,19)
jacare6 = Lula('inimigo',-50,250,2,15)
jacare7 = Lula('inimigo',10,250,2,22)
jacare8 = Lula('inimigo',20,250,2,22)
jacare9 = Lula('inimigo',-30,250,2,17)
bife = Lula('Bife',50,50,2,0)
cerveja = Lula('Cerveja',50,50,2,0)

p=0
pontuacao=0
aleatorio=1
run = True
while run:
    
    txt= str(pontuacao)
    pygame.font.init()
    fonte=pygame.font.get_default_font()
    fontesys=pygame.font.SysFont(fonte, 60)
    txttela = fontesys.render(txt, 1, (0,0,0)) 
    tela.blit(txttela,(1300,0)) 
    pygame.display.update() 
    relogio.tick(FPS)
    
    desenho_tela()

    jogador.atualizar_animacao()
    jogador.desenho()
    inimigo.desenho()
    jacare.desenho()
    jacare1.desenho()
    jacare2.desenho()
    jacare3.desenho()
    jacare4.desenho()
    jacare5.desenho()
    jacare6.desenho()
    jacare7.desenho()
    jacare8.desenho()
    jacare9.desenho()
    if aleatorio==0:
        bife.desenho()
    else:
        cerveja.desenho()
    if jogador.vivo:
            if movimento_esquerda or movimento_direita or movimento_Cima or movimento_Baixo:
                jogador.atualizar_acao(1)
            
                
            else:
                #faz o bolsonaro se movimntar aleatoriamente atras do lula
               if p==1: 
                if inimigo.rect.x > jogador.rect.x:
                    inimigo.rect.x -= inimigo.velocidade
                if inimigo.rect.x < jogador.rect.x:
                    inimigo.rect.x += inimigo.velocidade
                if inimigo.rect.y > jogador.rect.y:
                    inimigo.rect.y -= inimigo.velocidade
                if inimigo.rect.y < jogador.rect.y:
                    inimigo.rect.y += inimigo.velocidade
                jogador.atualizar_acao(0)
                inimigo.atualizar_acao(0)
            jogador.movimento(movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo)
            if p==1:
             inimigo.movimento(movimento_direita, movimento_esquerda,movimento_Baixo ,movimento_Cima )
            else:
                inimigo.mov1(True)
            jacare.mov(True)
            jacare1.mov(True)
            jacare2.mov(True)
            jacare3.mov(True)
            jacare4.mov(True)
            jacare5.mov(True)
            jacare6.mov(True)
            jacare7.mov(True)
            jacare8.mov(True)
            jacare9.mov(True)



   
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                    run = False

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                            movimento_esquerda = True
                    if event.key == pygame.K_d:
                            movimento_direita = True
                    if event.key == pygame.K_w:
                            movimento_Cima = True
                    if event.key == pygame.K_s:
                            movimento_Baixo = True
                    
                    if event.key == pygame.K_ESCAPE:
                            run = False

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                            movimento_esquerda = False
                    if event.key == pygame.K_d:
                            movimento_direita = False
                    if event.key == pygame.K_w:
                            movimento_Cima = False
                    if event.key == pygame.K_s:
                            movimento_Baixo = False
                            
            #se lula encontar com bolsonaro depois de 10 segudos que o jogo começou, o jogo acaba
            encontro = pygame.image.load('lulabolso.jpg')
            if pygame.time.get_ticks() - tempo > 0:
             if jogador.rect.colliderect(inimigo.rect ) or  jogador.rect.colliderect(jacare.rect) or  jogador.rect.colliderect(jacare1.rect ) or  jogador.rect.colliderect(jacare2.rect ) or  jogador.rect.colliderect(jacare3.rect ) or  jogador.rect.colliderect(jacare4.rect ) or  jogador.rect.colliderect(jacare5.rect ) or  jogador.rect.colliderect(jacare6.rect ) or  jogador.rect.colliderect(jacare7.rect ) or  jogador.rect.colliderect(jacare8.rect ) or  jogador.rect.colliderect(jacare9.rect ):
                tela.blit(encontro, (0, 0))
                pygame.display.update()
                
                run = False
            if jogador.rect.colliderect(bife.rect) or jogador.rect.colliderect(cerveja.rect):
                
                pygame.display.update()
                
                if aleatorio==1:
                    cerveja.comida()
                    pontuacao+=10
                    aleatorio=0 
                else:
                    bife.comida()
                    pontuacao+=10
                    aleatorio=1
                
                



               

            
            


    pygame.display.update()

pygame.quit()
