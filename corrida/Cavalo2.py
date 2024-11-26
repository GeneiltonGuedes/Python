import random

import pygame

pygame.init()

LARGURA, ALTURA = 900, 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida Infinita do Cavalo")

AZUL_CEU = (135, 206, 235)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)

relógio = pygame.time.Clock()

fonte = pygame.font.Font(None, 36)
fonte_fim_de_jogo = pygame.font.Font(None, 72)

chão = pygame.image.load("fundo.png")
chão = pygame.transform.scale(chão, (LARGURA, 120))
imagem_cavalo = pygame.image.load("cavalo.png")
imagem_cavalo = pygame.transform.scale(imagem_cavalo, (60, 60))
imagem_obstáculo_terrestre = pygame.image.load("obstaculo_terrestre.png")
imagem_obstáculo_terrestre = pygame.transform.scale(imagem_obstáculo_terrestre, (40, 60))
imagem_obstáculo_aéreo = pygame.image.load("obstaculo_aereo.png")
imagem_obstáculo_aéreo = pygame.transform.scale(imagem_obstáculo_aéreo, (50, 50))
imagem_nuvem = pygame.image.load("nuvem.png")
imagem_nuvem = pygame.transform.scale(imagem_nuvem, (90, 60))
imagem_árvore = pygame.image.load("arvore.png")
imagem_árvore = pygame.transform.scale(imagem_árvore, (70, 110))

nuvens = [
    {"x": random.randint(0, LARGURA), "y": random.randint(20, 100), "velocidade": random.uniform(1, 3)}
    for _ in range(5)
]

árvores = [
    {"x": random.randint(0, LARGURA), "y": ALTURA - 220, "velocidade": random.uniform(2, 5)}
    for _ in range(3)
]

cavalo = pygame.Rect(100, ALTURA - 150, 50, 50)
pulando = False
velocidade_pulo = 15
gravidade = 1
velocidade_y = 0

obstáculos = []
temporizador_obstáculo = 0

pontuação = 0
velocidade_obstáculo = 8
frequência_obstáculo = 90
executando = True
jogo_acabou = False


def desenhar_fundo():
    tela.fill(AZUL_CEU)


def desenhar_chão():
    tela.blit(chão, (0, ALTURA - 120))


def desenhar_cavalo():
    tela.blit(imagem_cavalo, (cavalo.x, cavalo.y))


def desenhar_pontuação():
    texto_pontuação = fonte.render(f"Pontuação: {pontuação}", True, PRETO)
    tela.blit(texto_pontuação, (10, 10))


def desenhar_fim_de_jogo():
    texto_fim_de_jogo = fonte_fim_de_jogo.render("Você perdeu!", True, VERMELHO)
    tela.blit(texto_fim_de_jogo, (LARGURA // 2 - 150, ALTURA // 2 - 50))


def desenhar_nuvens():
    for nuvem in nuvens:
        tela.blit(imagem_nuvem, (nuvem["x"], nuvem["y"]))
        nuvem["x"] -= nuvem["velocidade"]
        if nuvem["x"] < -80:
            nuvem["x"] = LARGURA
            nuvem["y"] = random.randint(20, 100)
            nuvem["velocidade"] = random.uniform(1, 3)


def desenhar_árvores():
    for árvore in árvores:
        tela.blit(imagem_árvore, (árvore["x"], árvore["y"]))
        árvore["x"] -= árvore["velocidade"]
        if árvore["x"] < -60:
            árvore["x"] = LARGURA
            árvore["velocidade"] = random.uniform(2, 5)


while executando:
    desenhar_fundo()
    desenhar_nuvens()
    desenhar_árvores()
    desenhar_chão()

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
        if cavalo.y >= ALTURA - 150:
            cavalo.y = ALTURA - 150
            pulando = False

    if not jogo_acabou:
        temporizador_obstáculo += 1
        if temporizador_obstáculo > frequência_obstáculo:
            temporizador_obstáculo = 0
            if random.choice([True, False]):
                novo_obstáculo = {
                    "retângulo": pygame.Rect(LARGURA, ALTURA - 150, 30, 50),
                    "imagem": imagem_obstáculo_terrestre,
                }
            else:
                novo_obstáculo = {
                    "retângulo": pygame.Rect(LARGURA, ALTURA - 200, 40, 40),
                    "imagem": imagem_obstáculo_aéreo,
                }
            obstáculos.append(novo_obstáculo)

    for obstáculo in obstáculos[:]:
        obstáculo["retângulo"].x -= velocidade_obstáculo
        if cavalo.colliderect(obstáculo["retângulo"]):
            jogo_acabou = True
        elif obstáculo["retângulo"].x < 0:
            obstáculos.remove(obstáculo)

    if not jogo_acabou:
        pontuação += 1
        if pontuação % 20 == 0:
            velocidade_obstáculo += 1

    desenhar_cavalo()

    for obstáculo in obstáculos:
        tela.blit(obstáculo["imagem"], (obstáculo["retângulo"].x, obstáculo["retângulo"].y))

    desenhar_pontuação()

    if jogo_acabou:
        desenhar_fim_de_jogo()

    pygame.display.flip()
    relógio.tick(30)

pygame.quit()
