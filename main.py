
import pygame
import os
from pygame import font
from random import randint
import random
pygame.init()

#tamanho da tela
TELA_LARGURA = 1380
TELA_ALTURA = 640

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption('Corrida Eleitoral')

relogio = pygame.time.Clock()
FPS = 60

#Colocando a música de fundo do jogo

pygame.mixer.init()
'''pygame.mixer.music.load('musicafundo.mp3')
pygame.mixer.music.play()'''
#inicia fase -1 para mostrar menu inicial
fase = -1
movimento_esquerda = False
movimento_direita = False
movimento_Cima = False
movimento_Baixo = False

#coloca o fundo
def desenho_tela():
    
    if fase == -2:
        fundo=(pygame.image.load('Fundo/instrucoes.png'))
    elif fase ==-1:
        fundo=(pygame.image.load('Fundo/Inicio.png'))
    elif fase ==0:
        fundo=(pygame.image.load('Fundo/0.jpg'))
    elif fase ==1:
        fundo=(pygame.image.load('Fundo/0.jpg'))
    elif fase == 2:
        fundo=(pygame.image.load('Fundo/0.jpg'))
    tela.blit(fundo,(0,0))


class eleicao(pygame.sprite.Sprite):
    def __init__(self, jogador_tipo, x, y,  velocidade):
    
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
        #gambiarra pra bug q n sei como resolver para bolsonaro parecer q ta correndo
        
        animacao_tipo = ['0.png', '1.png','2.png']
        #recebe qtas imagens tem
        for animacao in animacao_tipo:
            temp_list = []
            #quantidade de frames em cada pack
            numero_de_frames = len(os.listdir(f'img/{self.jogador_tipo}'))
            #for ate ultima imagem
            for i in range(numero_de_frames):
                #poe na tela cada imagem para formar animação
                img = pygame.image.load(f'img/{self.jogador_tipo}/{i}.png')
                #append adiciona a imagem no fim da lista
                temp_list.append(img)
                #adiciona temp list no final da lista
            self.animacao_lista.append(temp_list)

        self.image = self.animacao_lista[self.acao][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def comida(self):
        #faz aparecer em lugar aleatorio
        self.rect.x =randint(10,500)
        self.rect.y=randint(10,500)
    
    def mov(self,movimento_direita):
            #move o personagem sempre para direito 
            dx=0
            #faz spawnar aleatoriamente
            if self.rect.x>randint(1500,100000):
                self.rect.x=-50
            dx = self.velocidade
            self.virar = False
            self.direcao = 1
            self.rect.x += dx
            

    def movimento(self, movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo):


        dx=0
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
    def mov1(self, movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo):


        dx = 0
        dy=0
        
        if movimento_esquerda:
            
            dx = -self.velocidade
            self.virar = True
            self.direcao = -1
            
        if movimento_direita:

            dx = self.velocidade
            self.virar = False
            self.direcao = 1
        
        if movimento_Baixo:

            dy = self.velocidade
            self.virar = False
            self.direcao = 1
            
        if movimento_Cima:

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
            #caso condição seja verdadeira frame_index vai para proxima imagem do pack (milissegundos)
            if pygame.time.get_ticks() - self.atualizar_tempo > ANIMACAO_FRESH:
                self.atualizar_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            #quando framde_index for maior que a quantidade de imagens no pack ele é reiniciado
            if self.frame_index >= len(self.animacao_lista[self.acao]):
                self.frame_index = 0

    def atualizar_acao(self, new_action):
        if new_action != self.acao: 
                self.acao = new_action

                self.frame_index = 0
                self.atualizar_tempo = pygame.time.get_ticks()

    def desenho(self):
            #vira imagem
            tela.blit(pygame.transform.flip(self.image, self.virar, False), self.rect)

#personagens e seu local de imagens, local no mapa e velocidade
caminhao = eleicao ('Caminhao',1800,500,10)
Lula = eleicao('Lula', 1500, 550,  10)
Bolsonaro = eleicao('Bolsonaro', 1410, 550,  10)
faca= eleicao("faca",50,200,10)
faca1= eleicao("faca",-50,400,14)
faca2= eleicao("faca",10,350,22)
faca3= eleicao("faca",-30,250,12)
faca4= eleicao("faca",20,300,17)
faca5= eleicao("faca",-30,250,18)
faca6= eleicao("faca",50,250,15)
faca7= eleicao("faca",-50,250,10)
faca8= eleicao("faca",10,250,16)
faca9= eleicao("faca",20,250,14)
jacare =  eleicao('inimigo',50,200,10)
jacare1 = eleicao('inimigo',-50,400,14)
jacare2 = eleicao('inimigo',10,350,22)
jacare3 = eleicao('inimigo',20,300,12)
jacare4 = eleicao('inimigo',-30,250,17)
jacare5 = eleicao('inimigo',50,250,18)
jacare6 = eleicao('inimigo',-50,250,15)
jacare7 = eleicao('inimigo',10,250,16)
jacare8 = eleicao('inimigo',20,250,14)
jacare9 = eleicao('inimigo',-30,250,17)
bife = eleicao('Bife',100,100,0)
cerveja = eleicao('Cerveja',150,50,0)
arma = eleicao('arma',100,100,0)
remedio = eleicao ('remedio',150,50,0)
Fase = eleicao('fase',100,520,0)
seta = eleicao('seta',50,50,0)
pegadinha = eleicao ('pegadinha',1280, 480,0)
cont=0
opcao=0
x= True
run=True
#parte do menu
while run:
    #faz o bolsonaro e lula ficar correndo :)
    desenho_tela()
    Lula.atualizar_animacao()
    Lula.desenho()
    Bolsonaro.atualizar_animacao()
    Bolsonaro.desenho()
    #enquanto X for True vai aparecer a setinha do menu
    if x:
        seta.desenho()
        seta.atualizar_animacao()
    #faz personagens irem para esquerda
    if Lula.rect.x > -200 and Bolsonaro.rect.x > -190 and (cont == 0 or cont==3):
        Lula.mov1(True,False,False,False)
        Bolsonaro.mov1(True,False,False,False)
        
    
    #faz personagens irem para direita
    elif Lula.rect.x <= 1500 and Bolsonaro.rect.x <1490 and cont ==1:
        Lula.mov1(False,True,False,False)
        Bolsonaro.mov1(False,True,False,False)
    #faz povo e caminhao ir pra esquerda
    elif Lula.rect.x > -700 and Bolsonaro.rect.x > -690 and cont==2:
        Lula.atualizar_animacao()
        Lula.desenho()
        Bolsonaro.atualizar_animacao()
        Bolsonaro.desenho()
        caminhao.atualizar_animacao()
        caminhao.desenho()
        Lula.mov1(True,False,False,False)
        Bolsonaro.mov1(True,False,False,False)
        caminhao.mov1(True,False,False,False)
    #caso tudo seja falso cont add +1 ao chegar em >4 ele zera e a animação volta do inicio
    else:
        cont=cont+ 1
        if cont>4:
            
            cont=0
            caminhao = eleicao ('Caminhao',1800,500,10)
    #parte q mexe no menuzin
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            #a cada clique na seta para cima é decrementado 1 posiçao
            if event.key == pygame.K_UP :
             if opcao >0:
                opcao= opcao -1
           #faz o contrario de cima
            if event.key == pygame.K_DOWN :
             if opcao <4: 
                opcao= opcao +1
            #caso aperte tecla de voltar x volta a ser True e volta a aparece seta e volta pro menu
            if event.key == pygame.K_BACKSPACE:
                    fase=-1
                    x=True
            #caso clique em alguma opcao x se torna falso e seta some.
            if event.key == pygame.K_SPACE:
                x=False
                if opcao == 0:
                    #caso jogador escolha o lula z recebe jogador e w o outro
                    z=Lula
                    w=Bolsonaro
                    x1=bife
                    x2=cerveja
                    fase=0
                    
                    run= False
                    

                if opcao == 1:
                    #caso escola bolsonaro z recebe inimigo
                    z=Bolsonaro
                    w=Lula
                    x1=arma
                    x2=remedio
                    run=False
                    fase=0
                if opcao == 2:
                    fase=-2
                if opcao == 3:
                    run = False
    #posiçao da seta
    if opcao == 0:
        seta = eleicao('seta',520,180,0)
    if opcao == 1:
        seta = eleicao('seta',370,250,0)
    if opcao == 2:
        seta = eleicao('seta',350,330,0)
    if opcao == 3:
        seta = eleicao('seta',510,400,0)
        False
        
    pygame.display.update() 
cont=0
pontuacao=0
aleatorio=1
#caso usuario n escolha a opçao de sair(3) o jogo continua
if opcao != 3:
    run = True
while run:
    
    txt= str(pontuacao)
    pygame.font.init()
    fonte=pygame.font.get_default_font()
    fontesys=pygame.font.SysFont(fonte, 60)
    txttela = fontesys.render(txt, 1, (0,0,0)) 
    tela.blit(txttela,(1300,0)) 
    
    relogio.tick(FPS)
    pygame.display.update() 
    desenho_tela()

    z.atualizar_animacao()
    z.desenho()
    if fase == 2:
        w.desenho()
    if fase == 0 or fase == 2:
     if z==Lula:
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
     elif z== Bolsonaro:
        faca.desenho()
        faca1.desenho()
        faca2.desenho()
        faca3.desenho()
        faca4.desenho()
        faca5.desenho()
        faca6.desenho()
        faca7.desenho()
        faca8.desenho()
        faca9.desenho()
    if fase ==1:
        Fase.desenho()
        pegadinha.desenho()
    if fase == 0 or fase == 2: 
     #aparece um item por vez
     if aleatorio==0:
        x1.desenho()
     else:
        x2.desenho()
    if z.vivo:
            if movimento_esquerda or movimento_direita or movimento_Cima or movimento_Baixo:
                z.atualizar_acao(1)
            
                
            else:
             if fase == 2:
                #faz o bolsonaro se movimntar aleatoriamente atras do lula
               
                if w.rect.x > z.rect.x:
                    w.rect.x -= w.velocidade
                if w.rect.x < z.rect.x:
                    w.rect.x += w.velocidade
                if w.rect.y > z.rect.y:
                    w.rect.y -= w.velocidade
                if w.rect.y < z.rect.y:
                    w.rect.y += w.velocidade
                z.atualizar_acao(0)
                w.atualizar_acao(0)
            
            z.movimento(movimento_esquerda, movimento_direita, movimento_Cima, movimento_Baixo)
            w.movimento(movimento_direita, movimento_esquerda,movimento_Baixo ,movimento_Cima )
            if z==Lula:
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
            elif z==Bolsonaro:
             faca.mov(True)
             faca1.mov(True)
             faca2.mov(True)
             faca3.mov(True)
             faca4.mov(True)
             faca5.mov(True)
             faca6.mov(True)
             faca7.mov(True)
             faca8.mov(True)
             faca9.mov(True)



   
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                    run = False

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        fase=fase+1
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
            
            if fase ==0 or fase ==2:
              if Lula.rect.colliderect(jacare.rect) or  Lula.rect.colliderect(jacare1.rect ) or  Lula.rect.colliderect(jacare2.rect ) or  Lula.rect.colliderect(jacare3.rect ) or  Lula.rect.colliderect(jacare4.rect ) or  Lula.rect.colliderect(jacare5.rect ) or  Lula.rect.colliderect(jacare6.rect ) or  Lula.rect.colliderect(jacare7.rect ) or  Lula.rect.colliderect(jacare8.rect ) or  Lula.rect.colliderect(jacare9.rect ):
                
                encontro = pygame.image.load('img/bolsonaroganho.png')
                tela.blit(encontro, (0, 0))
                pygame.display.update()
                run = False
                #muda o audio para o audio de derrota
                pygame.mixer.music.load('derrota.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.9)
                pygame.display.update()
                pygame.time.delay(5000)
                run = False
                pygame.quit()

              if Bolsonaro.rect.colliderect(faca.rect) or  Bolsonaro.rect.colliderect(faca1.rect ) or  Bolsonaro.rect.colliderect(faca2.rect ) or  Bolsonaro.rect.colliderect(faca3.rect ) or  Bolsonaro.rect.colliderect(faca4.rect ) or  Bolsonaro.rect.colliderect(faca5.rect ) or  Bolsonaro.rect.colliderect(faca6.rect ) or  Bolsonaro.rect.colliderect(faca7.rect ) or  Bolsonaro.rect.colliderect(faca8.rect ) or  Bolsonaro.rect.colliderect(faca9.rect ):
                encontro = pygame.image.load('img/lulaganho.png')
                tela.blit(encontro, (0, 0))
                pygame.display.update()
                run = False
                
                #muda o audio para o audio de derrota
                pygame.mixer.music.load('derrota.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.9)
                pygame.display.update()
                pygame.time.delay(5000)
                run = False
                pygame.quit()
            if z.rect.colliderect(w.rect ) :
              if fase == 2:
                if z==Lula:
                    encontro = pygame.image.load('img/bolsonaroganho.png')
                    tela.blit(encontro, (0, 0))
                    pygame.display.update()
                    
                    pygame.mixer.music.load('derrota.mp3')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.9)
                    pygame.display.update()
                    pygame.time.delay(3000)

                    run = False
                elif z==Bolsonaro:
                    encontro = pygame.image.load('img/lulaganho.png')
                    tela.blit(encontro, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(3000)

                    run = False

                pygame.quit()

            if fase == 0 or fase == 2: 
             if aleatorio==1:    
                if z.rect.colliderect(cerveja.rect):
                    pygame.display.update()
                    cerveja.comida()
                    pontuacao+=15
                    aleatorio=0 
             else:
                if z.rect.colliderect(bife.rect):
                    pygame.display.update()
                    bife.comida()
                    pontuacao+=15
                    aleatorio=1
    # se a pontuação for maior que 100, o jogo acaba
    
    if pontuacao>=14 and cont ==0:
        if z==Bolsonaro:
            Lula = eleicao('Lula', 3000, 3000,  0)
        elif z==Lula: 
            Bolsonaro = eleicao('Bolsonaro', 3000, 3000,  0)
        fase = 1
        #Escreve na tela ache o portal para passar de fase
        pygame.font.init()
        fonte=pygame.font.get_default_font()
        fontesys=pygame.font.SysFont(fonte, 40)
        txttela = fontesys.render('Vote no seu candidato', 1, (0,0,0))
        tela.blit(txttela,(550,0))
        run = True

        if Lula.rect.colliderect(Fase.rect):
            fase=2
            cont =1
            pontuacao=0
        elif Lula.rect.colliderect(pegadinha.rect):
            encontro = pygame.image.load('img/bolsonaroganho.png')
            tela.blit(encontro, (0, 0))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
        if Bolsonaro.rect.colliderect(pegadinha.rect) :
            cont =1
            fase=2
            pontuacao=0
        elif Bolsonaro.rect.colliderect(Fase.rect):
            encontro = pygame.image.load('img/lulaganho.png')
            tela.blit(encontro, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            run =False
    elif pontuacao >=15 and z==Lula:
        encontro = pygame.image.load('img/lulaganho.png')
        tela.blit(encontro, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)

        run = False
    elif pontuacao >=15 and z==Bolsonaro:
        encontro = pygame.image.load('img/bolsonaroaganho.png')
        tela.blit(encontro, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)

        run = False
    pygame.display.update()

pygame.quit()
