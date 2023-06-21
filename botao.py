import pygame

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
jogo_em_execucao = True
class Botao(pygame.sprite.Sprite):
    def __init__(self, numero, posicao):
        pygame.sprite.Sprite.__init__(self)
        self.numero = numero
        self.imagem_normal = pygame.image.load(f"assets/{numero.lower()}.png")
        self.fonte = pygame.font.Font(None, 24)
        self.image = pygame.transform.scale(self.imagem_normal, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = posicao

    def atualizar_texto(self):
        self.texto = self.fonte.render(self.numero, True, branco)

    def update(self):
        pass

    def draw(self, tela):
        tela.blit(self.texto, self.rect)