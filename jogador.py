import pygame

pygame.init()

largura_tela = 800
altura_tela = 600

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = (largura_tela // 2) - 10
        self.rect.bottom = altura_tela - 10
        self.velocidade = 5

    def update(self):
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas_pressionadas[pygame.K_RIGHT] and self.rect.right < largura_tela:
            self.rect.x += self.velocidade

