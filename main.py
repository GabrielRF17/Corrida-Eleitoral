import pygame
import os

pygame.init()


TELA_LARGURA = 800
TELA_ALTURA = 900

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption('JOGO EM PYGAME :')


relogio = pygame.time.Clock()
FPS = 60

GRAVIDADE = 0.75

movimento_esquerda = False
movimento_direita = False


tela_fundo = (0,255,255)
GREEN = (0, 179, 113)

def desenho_tela():
    tela.fill(tela_fundo)
    pygame.draw.line(tela, GREEN, (0, 600), (TELA_LARGURA, 600))
    


class Soldado(pygame.sprite.Sprite):
    def __init__(self, jogador_tipo, x, y, scale, velocidade):

        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.jogador_tipo = jogador_tipo
        self.velocidade = velocidade
        self.vel_y = 0
        self.direcao = 1
        self.pular = False
        self.no_ar = True
        self.virar = False
        self.animacao_lista = []
        self.frame_index = 0
        self.acao = 0
        self.atualizar_tempo = pygame.time.get_ticks()

        animacao_tipo = ['jogador_Idle', 'Correr', 'pular']

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

    def movimento(self, movimento_esquerda, movimento_direita):


        dx = 0
        dy = 0

        if movimento_esquerda:
            dx = -self.velocidade
            self.virar = True
            self.direcao = -1
        if movimento_direita:

            dx = self.velocidade
            self.virar = False
            self.direcao = 1

        if self.pular == True and self.no_ar == False:

                self.vel_y = -15
                self.pular = False
                self.no_ar = True


        self.vel_y += GRAVIDADE
        if self.vel_y > 10:
            
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.no_ar = False

        self.rect.x += dx
        self.rect.y += dy

    def atualizar_animacao(self):
            ANIMACAO_FRESH = 100

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


jogador = Soldado('jogador', 200, 200, 2, 5)



run = True
while run:
    relogio.tick(60)

    desenho_tela()

    jogador.atualizar_animacao()
    jogador.desenho()
    

    if jogador.vivo:
            if jogador.no_ar:
                jogador.atualizar_acao(2)
            elif movimento_esquerda or movimento_direita:
                jogador.atualizar_acao(1)
            else:
                jogador.atualizar_acao(0)
            jogador.movimento(movimento_esquerda, movimento_direita)

    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                    run = False

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                            movimento_esquerda = True
                    if event.key == pygame.K_d:
                            movimento_direita = True
                    if event.key == pygame.K_w and jogador.vivo:
                            jogador.pular = True
                    if event.key == pygame.K_ESCAPE:
                            run = False

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                            movimento_esquerda = False
                    if event.key == pygame.K_d:
                            movimento_direita = False

    pygame.display.update()

pygame.quit()
