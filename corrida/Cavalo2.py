import pygame
import random

pygame.init()

LARGURA, ALTURA = 800, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida Infinita do Cavalo")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)

relogio = pygame.time.Clock()

fonte = pygame.font.Font(None, 36)
fonte_game_over = pygame.font.Font(None, 72)

fundo = pygame.image.load("fundo_velho_oeste.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
imagem_cavalo = pygame.image.load("cavalo.png")
imagem_cavalo = pygame.transform.scale(imagem_cavalo, (50, 50))
imagem_obstaculo_terrestre = pygame.image.load("obstaculo_terrestre.png")
imagem_obstaculo_terrestre = pygame.transform.scale(imagem_obstaculo_terrestre, (30, 50))
imagem_obstaculo_aereo = pygame.image.load("obstaculo_aereo.png")
imagem_obstaculo_aereo = pygame.transform.scale(imagem_obstaculo_aereo, (40, 40))

cavalo = pygame.Rect(100, ALTURA - 100, 50, 50)
pulando = False
velocidade_pulo = 15
gravidade = 1
velocidade_y = 0

obstaculos = []
temporizador_obstaculo = 0

pontuacao = 0
velocidade_obstaculo = 8
frequencia_obstaculo = 90
executando = True
jogo_acabou = False

def desenhar_fundo():
    tela.blit(fundo, (0, 0))

def desenhar_cavalo():
    tela.blit(imagem_cavalo, (cavalo.x, cavalo.y))

def desenhar_pontuacao():
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto_pontuacao, (10, 10))

def desenhar_game_over():
    texto_game_over = fonte_game_over.render("Você perdeu!", True, VERMELHO)
    tela.blit(texto_game_over, (LARGURA // 2 - 150, ALTURA // 2 - 50))

while executando:
    tela.fill(BRANCO)
    desenhar_fundo()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE] and not pulando and not jogo_acabou:
        pulando = True
        velocidade_y = -velocidade_pulo

    if pulando:
        cavalo.y += velocidade_y
        velocidade_y += gravidade
        if cavalo.y >= ALTURA - 100:
            cavalo.y = ALTURA - 100
            pulando = False

    if not jogo_acabou:
        temporizador_obstaculo += 1
        if temporizador_obstaculo > frequencia_obstaculo:
            temporizador_obstaculo = 0
            if random.choice([True, False]):
                novo_obstaculo = {
                    "retangulo": pygame.Rect(LARGURA, ALTURA - 100, 30, 50),
                    "imagem": imagem_obstaculo_terrestre,
                }
            else:
                novo_obstaculo = {
                    "retangulo": pygame.Rect(LARGURA, ALTURA - 150, 40, 40),
                    "imagem": imagem_obstaculo_aereo,
                }
            obstaculos.append(novo_obstaculo)

    for obstaculo in obstaculos[:]:
        obstaculo["retangulo"].x -= velocidade_obstaculo
        if cavalo.colliderect(obstaculo["retangulo"]):
            jogo_acabou = True
        elif obstaculo["retangulo"].x < 0:
            obstaculos.remove(obstaculo)

    if not jogo_acabou:
        pontuacao += 1
        if pontuacao % 20 == 0:
            velocidade_obstaculo += 1

    desenhar_cavalo()

    for obstaculo in obstaculos:
        tela.blit(obstaculo["imagem"], (obstaculo["retangulo"].x, obstaculo["retangulo"].y))

    desenhar_pontuacao()

    if jogo_acabou:
        desenhar_game_over()

    pygame.display.flip()
    relogio.tick(30)

pygame.quit()

