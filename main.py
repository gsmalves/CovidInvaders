import pygame
import random
import operator

pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Covid Invaders Matemático")

clock = pygame.time.Clock()

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 10
        self.velocidade = 5

    def update(self):
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas_pressionadas[pygame.K_RIGHT] and self.rect.right < largura_tela:
            self.rect.x += self.velocidade

class Invasor(pygame.sprite.Sprite):
    def __init__(self, operacao):
        super().__init__()
        self.image = pygame.image.load("enemy1.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = 1
        self.operacao = operacao
        self.valor1 = random.randint(1, 10)
        self.valor2 = random.randint(1, 10)
        self.resposta = self.calcular_resposta()

    def calcular_resposta(self):
        operadores = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv
        }
        operador = operadores[self.operacao]
        return operador(self.valor1, self.valor2)

    def update(self):
        self.rect.y += self.velocidade

class Bala(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bala.png")
        self.rect = self.image.get_rect()
        self.velocidade = -5

    def update(self):
        self.rect.y += self.velocidade

def criar_invasores(quantidade):
    invasores = pygame.sprite.Group()
    operacoes = ["+", "-", "*", "/"]
    for _ in range(quantidade):
        operacao = random.choice(operacoes)
        invasor = Invasor(operacao)
        invasores.add(invasor)
    return invasores

def criar_bala(jogador):
    bala = Bala()
    bala.rect.centerx = jogador.rect.centerx
    bala.rect.bottom = jogador.rect.top
    return bala

def mostrar_mensagem(texto):
    fonte = pygame.font.Font(None, 36)
    mensagem = fonte.render(texto, True, branco)
    tela.blit(mensagem, (largura_tela // 2 - mensagem.get_width() // 2, altura_tela // 2 - mensagem.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Carregar imagem de fundo
fundo = pygame.image.load("back.png")
fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

def jogo():
    jogador = Jogador()
    invasores = criar_invasores(10)
    balas = pygame.sprite.Group()

    pontuacao = 0
    fonte = pygame.font.Font(None, 36)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    bala = criar_bala(jogador)
                    balas.add(bala)

        tela.blit(fundo, (0, 0))

        jogador.update()
        invasores.update()
        balas.update()

        colisoes = pygame.sprite.groupcollide(balas, invasores, True, True)
        for bala, invasor in colisoes.items():
            pontuacao += 1

        for invasor in invasores:
            if invasor.rect.bottom >= altura_tela:
                mostrar_mensagem("Game Over")
                rodando = False

        jogador_colisoes = pygame.sprite.spritecollide(jogador, invasores, False)
        if jogador_colisoes:
            mostrar_mensagem("Game Over")
            rodando = False

        jogador_group = pygame.sprite.Group()
        jogador_group.add(jogador)
        jogador_group.draw(tela)

        invasores.draw(tela)
        balas.draw(tela)

        for invasor in invasores:
            texto = fonte.render(f"{invasor.valor1} {invasor.operacao} {invasor.valor2} =", True, vermelho)
            tela.blit(texto, (invasor.rect.x, invasor.rect.y + invasor.rect.height))

        pontuacao_texto = fonte.render("Pontuação: " + str(pontuacao), True, branco)
        tela.blit(pontuacao_texto, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

jogo()
