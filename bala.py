import pygame


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao_x, direcao_y):
        super().__init__()
        self.image = pygame.image.load("assets/bala.png")
        self.image = pygame.transform.scale(self.image, (40, 20))  # Redimensionar a imagem da bala
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direcao_x = direcao_x
        self.direcao_y = direcao_y
        self.velocidade = 5

    def update(self):
        self.rect.x += self.direcao_x * self.velocidade
        self.rect.y += self.direcao_y * self.velocidade