import pygame

def exibir_menu():
    largura_tela = 800
    altura_tela = 600

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Menu")

    branco = (255, 255, 255)
    preto = (0, 0, 0)

    fonte = pygame.font.Font(None, 36)
    jogar_texto = fonte.render("JOGAR", True, branco)
    sair_texto = fonte.render("SAIR", True, branco)

    jogar_retangulo = jogar_texto.get_rect()
    jogar_retangulo.center = (largura_tela // 2, altura_tela // 2 - 50)

    sair_retangulo = sair_texto.get_rect()
    sair_retangulo.center = (largura_tela // 2, altura_tela // 2 + 50)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                if jogar_retangulo.collidepoint(posicao_mouse):
                    rodando = False
                elif sair_retangulo.collidepoint(posicao_mouse):
                    pygame.quit()
                    exit()

        tela.fill(preto)
        tela.blit(jogar_texto, jogar_retangulo)
        tela.blit(sair_texto, sair_retangulo)

        pygame.display.flip()

    return True
