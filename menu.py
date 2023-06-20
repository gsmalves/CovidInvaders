import pygame
from main import jogo

def exibir_menu():
    pygame.init()
    
    largura_tela = 800
    altura_tela = 600

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Covid Invaders Matemático")

    clock = pygame.time.Clock()

    branco = (255, 255, 255)
    cor_titulo = (255, 189, 89)  # #FFBD59

    fonte_titulo = pygame.font.Font("ArchivoBlack-Regular.ttf", 48)
    fonte_descricao = pygame.font.Font("ArchivoBlack-Regular.ttf", 24)

    fundo = pygame.image.load("assets/back.png")
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    titulo_texto = fonte_titulo.render("Covid Invaders", True, cor_titulo)
    titulo_rect = titulo_texto.get_rect()
    titulo_rect.center = (largura_tela // 2, altura_tela // 2 - 80)

    descricao_texto = fonte_descricao.render("Missão Matemática", True, cor_titulo)
    descricao_rect = descricao_texto.get_rect()
    descricao_rect.center = (largura_tela // 2, altura_tela // 2 - 50)

    jogar_texto = fonte_descricao.render("JOGAR", True, branco)
    jogar_rect = jogar_texto.get_rect()
    jogar_rect.center = (largura_tela // 2, altura_tela // 2 + 10)

    recordes_texto = fonte_descricao.render("RECORDES", True, branco)
    recordes_rect = recordes_texto.get_rect()
    recordes_rect.center = (largura_tela // 2, altura_tela // 2 + 50)

    sair_texto = fonte_descricao.render("SAIR", True, branco)
    sair_rect = sair_texto.get_rect()
    sair_rect.center = (largura_tela // 2, altura_tela // 2 + 90)

    # Carregar imagens dos inimigos
    inimigo_images = []
    inimigo_rects = []

    imagens_inimigos = ["assets/virus (2).png", "assets/virus.png", "assets/virus (2).png", "assets/virus (3).png","assets/vaccine (2).png","assets/protect.png"]  # Adicione os nomes das novas imagens de inimigos aqui

    posicoes_inimigos = [
        (largura_tela // 2 - 270, altura_tela // 2 - 100),
        (largura_tela // 2 - 100, altura_tela // 2 - 180),
        (largura_tela // 2 + 100, altura_tela // 2 - 190),
        (largura_tela // 2 + 250, altura_tela // 2 - 120),
        (largura_tela // 2 + 180, altura_tela // 2 + 150),
        (largura_tela // 2 - 180, altura_tela // 2 + 150),
        ]  # Ajuste as coordenadas (posições) de cada inimigo conforme necessário

    for i, imagem in enumerate(imagens_inimigos):
        inimigo_image = pygame.image.load(imagem)
        inimigo_image = pygame.transform.scale(inimigo_image, (65, 65))  # Redimensionar as imagens dos inimigos
        inimigo_images.append(inimigo_image)

        posicao_x, posicao_y = posicoes_inimigos[i]

        inimigo_rect = inimigo_image.get_rect()
        inimigo_rect.center = (posicao_x, posicao_y)
        inimigo_rects.append(inimigo_rect)
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if jogar_rect.collidepoint(evento.pos):
                    # Iniciar o jogo
                    jogo()
                elif sair_rect.collidepoint(evento.pos):
                    rodando = False

        tela.blit(fundo, (0, 0))
        tela.blit(titulo_texto, titulo_rect)
        tela.blit(descricao_texto, descricao_rect)
        tela.blit(jogar_texto, jogar_rect)
        tela.blit(recordes_texto, recordes_rect)
        tela.blit(sair_texto, sair_rect)

        # Exibir imagens dos inimigos
        for inimigo_rect, inimigo_image in zip(inimigo_rects, inimigo_images):
            tela.blit(inimigo_image, inimigo_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()