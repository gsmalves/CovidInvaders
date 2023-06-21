import pygame

class BotaoRemover(pygame.sprite.Sprite):
    def __init__(self, imagem, posicao):
        super().__init__()
        self.image = imagem.convert_alpha()  # Carrega a imagem
        self.rect = self.image.get_rect()
        self.rect.topleft = posicao

    def atualizar(self):
        pass

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)