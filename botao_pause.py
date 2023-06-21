import pygame

class BotaoPausa(pygame.sprite.Sprite):
    def __init__(self, imagem, posicao):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.topleft = posicao