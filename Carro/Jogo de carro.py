import pygame
import random

pygame.init()

LARGURA, ALTURA = 400, 600
TAMANHO_VIA = LARGURA // 3
VELOCIDADE = 5
VELOCIDADE_CARRO = 10

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Corrida Infinita")

clock = pygame.time.Clock()

fundo_pista = pygame.image.load("pista.png").convert()
fundo_pista = pygame.transform.scale(fundo_pista, (LARGURA, ALTURA))
imagem_carro = pygame.image.load("carro.png").convert_alpha()
imagem_carro = pygame.transform.scale(imagem_carro, (50, 80))
imagens_obstaculos = [
    pygame.image.load("obstaculo1.png").convert_alpha(),
    pygame.image.load("obstaculo2.png").convert_alpha(),
    pygame.image.load("obstaculo3.png").convert_alpha(),
]
imagens_obstaculos = [pygame.transform.scale(img, (50, 80)) for img in imagens_obstaculos]

class Carro:
    def __init__(self):
        self.largura = 50
        self.altura = 80
        self.x = LARGURA // 2 - self.largura // 2
        self.y = ALTURA - self.altura - 10
        self.via = 1

    def mover_horizontal(self, direcao):
        if direcao == "esquerda" and self.via > 0:
            self.via -= 1
        elif direcao == "direita" and self.via < 2:
            self.via += 1
        self.x = self.via * TAMANHO_VIA + TAMANHO_VIA // 2 - self.largura // 2

    def mover_vertical(self, direcao):
        if direcao == "cima" and self.y > 0:
            self.y -= VELOCIDADE_CARRO
        elif direcao == "baixo" and self.y < ALTURA - self.altura:
            self.y += VELOCIDADE_CARRO

    def desenhar(self):
        tela.blit(imagem_carro, (self.x, self.y))

class Obstaculo:
    def __init__(self):
        self.largura = 50
        self.altura = 80
        self.via = random.randint(0, 2)
        self.x = self.via * TAMANHO_VIA + TAMANHO_VIA // 2 - self.largura // 2
        self.y = -self.altura
        self.imagem = random.choice(imagens_obstaculos)

    def mover(self):
        self.y += VELOCIDADE

    def desenhar(self):
        tela.blit(self.imagem, (self.x, self.y))

def tela_fim_jogo(pontuacao):
    fonte = pygame.font.Font(None, 35)
    rodando = True
    while rodando:
        tela.fill((0, 0, 0))
        texto_fim = fonte.render("Fim de Jogo", True, (255, 0, 0))
        texto_pontos = fonte.render(f"Seus pontos foram: {pontuacao}", True, (255, 255, 255))
        texto_reiniciar = fonte.render("Pressione R e jogue novamente", True, (255, 255, 255))
        texto_sair = fonte.render("ou pressione ESC para sair.", True, (255, 255, 255))

        tela.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, ALTURA // 4))
        tela.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, ALTURA // 2 - 40))
        tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 40))
        tela.blit(texto_sair, (LARGURA // 2 - texto_sair.get_width() // 2, ALTURA // 2 + 80))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    jogo()
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def jogo():
    rodando = True
    jogador = Carro()
    obstaculos = []
    pontuacao = 0
    fonte = pygame.font.Font(None, 36)

    while rodando:
        tela.blit(fundo_pista, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jogador.mover_horizontal("esquerda")
                if evento.key == pygame.K_RIGHT:
                    jogador.mover_horizontal("direita")
                if evento.key == pygame.K_UP:
                    jogador.mover_vertical("cima")
                if evento.key == pygame.K_DOWN:
                    jogador.mover_vertical("baixo")

        if random.randint(1, 30) == 1:
            obstaculos.append(Obstaculo())

        for obstaculo in obstaculos[:]:
            obstaculo.mover()
            if obstaculo.y > ALTURA:
                obstaculos.remove(obstaculo)
                pontuacao += 1
            obstaculo.desenhar()

            if (jogador.y < obstaculo.y + obstaculo.altura and
                jogador.y + jogador.altura > obstaculo.y and
                jogador.x < obstaculo.x + obstaculo.largura and
                jogador.x + jogador.largura > obstaculo.x):
                rodando = False

        jogador.desenhar()

        texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
        tela.blit(texto_pontuacao, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    tela_fim_jogo(pontuacao)

jogo()
