import pygame
import random

largura_tela = 800
altura_tela = 600



class Invasor(pygame.sprite.Sprite):
    def __init__(self, operacao):
        super().__init__()
        self.image = pygame.image.load("assets/enemy1.png").convert_alpha()  # Carrega a imagem do invasor
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona a imagem para o tamanho desejado
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - self.rect.width)
        self.rect.y = -self.rect.height
        self.operacao = operacao
        self.valor1 = random.randint(1, 9)
        self.valor2 = random.randint(1, 9)
        self.resposta = self.calcular_resposta()
        self.velocidade = 0.17


    def calcular_resposta(self):
        if self.operacao == "+":
            return self.valor1 + self.valor2
        elif self.operacao == "-":
            return self.valor1 - self.valor2
        elif self.operacao == "*":
            return self.valor1 * self.valor2
        elif self.operacao == "/":
            return int(self.valor1 / self.valor2)

    def update(self):
        self.rect.y += self.velocidade
