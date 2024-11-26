import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações principais
LARGURA, ALTURA = 400, 600
TAMANHO_VIA = LARGURA // 3
VELOCIDADE = 5

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)

# Inicializa a tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Corrida Infinita")

# Carrega o relógio
clock = pygame.time.Clock()

# Classe para o carro do jogador
class Carro:
    def __init__(self):
        self.largura = 50
        self.altura = 80
        self.x = LARGURA // 2 - self.largura // 2
        self.y = ALTURA - self.altura - 10
        self.via = 1  # Começa na via do meio (0, 1, 2)

    def mover(self, direcao):
        if direcao == "esquerda" and self.via > 0:
            self.via -= 1
        elif direcao == "direita" and self.via < 2:
            self.via += 1
        self.x = self.via * TAMANHO_VIA + TAMANHO_VIA // 2 - self.largura // 2

    def desenhar(self):
        pygame.draw.rect(tela, AZUL, (self.x, self.y, self.largura, self.altura))

# Classe para os obstáculos
class Obstaculo:
    def __init__(self):
        self.largura = 50
        self.altura = 80
        self.via = random.randint(0, 2)
        self.x = self.via * TAMANHO_VIA + TAMANHO_VIA // 2 - self.largura // 2
        self.y = -self.altura

    def mover(self):
        self.y += VELOCIDADE

    def desenhar(self):
        pygame.draw.rect(tela, VERMELHO, (self.x, self.y, self.largura, self.altura))

# Função principal
def jogo():
    rodando = True
    jogador = Carro()
    obstaculos = []
    pontuacao = 0
    fonte = pygame.font.Font(None, 36)

    while rodando:
        tela.fill(PRETO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jogador.mover("esquerda")
                if evento.key == pygame.K_RIGHT:
                    jogador.mover("direita")

        # Gera novos obstáculos
        if random.randint(1, 30) == 1:
            obstaculos.append(Obstaculo())

        # Movimenta e desenha os obstáculos
        for obstaculo in obstaculos[:]:
            obstaculo.mover()
            if obstaculo.y > ALTURA:
                obstaculos.remove(obstaculo)
                pontuacao += 1
            obstaculo.desenhar()

            # Verifica colisão
            if (jogador.y < obstaculo.y + obstaculo.altura and
                jogador.y + jogador.altura > obstaculo.y and
                jogador.x < obstaculo.x + obstaculo.largura and
                jogador.x + jogador.largura > obstaculo.x):
                rodando = False

        # Desenha o jogador
        jogador.desenhar()

        # Exibe a pontuação
        texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Inicia o jogo
jogo()
