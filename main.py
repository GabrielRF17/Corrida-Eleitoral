import pygame
import os
from random import randint
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
    fundo=pygame.image.load('Fundo/0.jpg')
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

    def movimento(self, movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo):


        dx = 0
        dy = 0
        
        
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
inimigo = Lula('Bolsonaro', 200, 200, 2, 20)



run = True
while run:
    relogio.tick(FPS)

    desenho_tela()

    jogador.atualizar_animacao()
    jogador.desenho()
    inimigo.desenho()
    if jogador.vivo:
            if movimento_esquerda or movimento_direita or movimento_Cima or movimento_Baixo:
                jogador.atualizar_acao(1)
            
                
            else:
                #faz o bolsonaro se movimntar aleatoriamente atras do lula
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
            inimigo.movimento(movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo)


   
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
            if jogador.rect.colliderect(inimigo.rect):
                if pygame.time.get_ticks() - tempo > 10000:
                    run = False
            encontro = pygame.image.load('lulabolso.jpg')
            if jogador.rect.colliderect(inimigo.rect):
                tela.blit(encontro, (0, 0))
                pygame.display.update()
                pygame.time.delay(1000)
                run = False




    pygame.display.update()

pygame.quit()
