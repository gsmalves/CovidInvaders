import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Covid Invaders")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Carregando imagens
player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy1.png")
projectile_img_g = pygame.image.load("assets/projetil_branco.png")

projectile_img = pygame.transform.scale(projectile_img_g, (64, 64))



# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Classe do inimigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 5)

# Classe do projétil
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = projectile_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Grupo de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Jogador
player = Player()
all_sprites.add(player)

# Criação de inimigos
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # Verifica colisões entre projéteis e inimigos
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

   
    # Verifica colisões entre jogador e inimigos
    if pygame.sprite.spritecollide(player, enemies, False):
        running = False

    # Preenche o fundo com a cor preta
    screen.fill(BLACK)

    # Desenha todos os sprites na tela
    all_sprites.draw(screen)

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de atualização
    clock.tick(60)

# Encerra o Pygame
pygame.quit()
