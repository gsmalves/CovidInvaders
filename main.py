import pygame
import random
import math
import os
from jogador import Jogador
from invasor import Invasor
from bala import Bala
from botao import Botao
from botao_remove import BotaoRemover
from vida import Coracao


pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Covid Invaders Matemático")

clock = pygame.time.Clock()

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
jogo_em_execucao = True


# Função para carregar a imagem do coração
def carregar_imagem_coração(caminho):
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, (30, 30))

def criar_invasores(quantidade):
    invasores = pygame.sprite.Group()
    operacoes = ["+", "*", "/", "-"]
    distancia_minima = 100  # Distância mínima desejada entre os invasores
    
    for _ in range(quantidade):
        operacao = random.choice(operacoes)
        invasor = Invasor(operacao)
        invasor.rect.x = random.randint(0, largura_tela - invasor.rect.width)
        invasor.rect.y = -invasor.rect.height

        colisoes = pygame.sprite.spritecollide(invasor, invasores, False)
        while colisoes:  # Verifica se houve colisão com outro invasor ou se está muito próximo
            invasor.rect.x = random.randint(0, largura_tela - invasor.rect.width)
            invasor.rect.y = -invasor.rect.height

            colisoes = pygame.sprite.spritecollide(invasor, invasores, False)

            # Verifica se o novo invasor está muito próximo de outros invasores
            for invasor_existente in invasores:
                distancia = math.sqrt((invasor.rect.x - invasor_existente.rect.x) ** 2 +
                                      (invasor.rect.y - invasor_existente.rect.y) ** 2)
                if distancia < distancia_minima:
                    colisoes.append(invasor_existente)
                    break

        if operacao == "+":
            invasor.valor1 = random.randint(0, 10)
            invasor.valor2 = random.randint(0, 10)
            invasor.resposta = invasor.valor1 + invasor.valor2
        elif operacao == "*":
            invasor.valor1 = random.randint(0, 10)
            invasor.valor2 = random.randint(0, 10)
            invasor.resposta = invasor.valor1 * invasor.valor2
        elif operacao == "-":
            invasor.valor1 = random.randint(1, 10)
            invasor.valor2 = random.randint(0, invasor.valor1 - 1)  # Garante que valor2 seja menor que valor1
            invasor.resposta = invasor.valor1 - invasor.valor2
        else:  # Operação de divisão
            invasor.valor2 = random.randint(1, 10)
            invasor.valor1 = invasor.valor2 * random.randint(1, 10)  # Garante que valor1 seja um múltiplo de valor2
            invasor.resposta = int(invasor.valor1 / invasor.valor2)

        invasores.add(invasor)
    return invasores

def criar_bala(jogador, direcao_x, direcao_y):
    bala = Bala(jogador.rect.centerx, jogador.rect.centery, direcao_x, direcao_y)
    return bala

def mostrar_mensagem(texto):
    fonte = pygame.font.Font(None, 36)
    mensagem = fonte.render(texto, True, branco)
    tela.blit(mensagem, (largura_tela // 2 - mensagem.get_width() // 2, altura_tela // 2 - mensagem.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Carregar imagem de fundo
fundo = pygame.image.load("assets/back.png")
fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

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

    ajuda_texto = fonte_descricao.render("AJUDA", True, branco)
    ajuda_rect = ajuda_texto.get_rect()
    ajuda_rect.center = (largura_tela // 2, altura_tela // 2 + 90)

    sair_texto = fonte_descricao.render("SAIR", True, branco)
    sair_rect = sair_texto.get_rect()
    sair_rect.center = (largura_tela // 2, altura_tela // 2 + 130)

    # Carregar imagens dos inimigos
    inimigo_images = []
    inimigo_rects = []

    imagens_inimigos = [
        "assets/virus (2).png",
        "assets/virus.png",
        "assets/virus (2).png",
        "assets/virus (3).png",
        "assets/vaccine (2).png",
        "assets/protect.png",
    ]  # Adicione os nomes das novas imagens de inimigos aqui

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
                elif recordes_rect.collidepoint(evento.pos):
                    # Abrir tela de recordes
                    exibir_recordes()
                elif ajuda_rect.collidepoint(evento.pos):
                    # Abrir tela de ajuda
                    exibir_ajuda()
                elif sair_rect.collidepoint(evento.pos):
                    rodando = False

        tela.blit(fundo, (0, 0))
        tela.blit(titulo_texto, titulo_rect)
        tela.blit(descricao_texto, descricao_rect)
        tela.blit(jogar_texto, jogar_rect)
        tela.blit(recordes_texto, recordes_rect)
        tela.blit(ajuda_texto, ajuda_rect)
        tela.blit(sair_texto, sair_rect)

        # Exibir imagens dos inimigos
        for inimigo_rect, inimigo_image in zip(inimigo_rects, inimigo_images):
            tela.blit(inimigo_image, inimigo_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def salvar_pontuacao(pontuacao):
    with open("recordes.txt", "a") as arquivo:
        arquivo.write(f"{pontuacao}\n")


def carregar_recordes():
    if not os.path.isfile("recordes.txt"):
        return []  # Retorna uma lista vazia se o arquivo não existir

    recordes = []
    with open("recordes.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            pontuacao = linha.strip()
            if pontuacao.isdigit():
                recordes.append(int(pontuacao))
    return recordes

  
def exibir_recordes():
    pygame.init()

    largura_tela = 800
    altura_tela = 600

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Covid Invaders Matemático")

    clock = pygame.time.Clock()

    cor_titulo = (255, 189, 89)  # #FFBD59
    branco = (255, 255, 255)

    fonte_titulo = pygame.font.Font("ArchivoBlack-Regular.ttf", 36)
    fonte_pontuacao = pygame.font.Font("ArchivoBlack-Regular.ttf", 24)
    fonte_botao = pygame.font.Font("ArchivoBlack-Regular.ttf", 30)

    fundo = pygame.image.load("assets/back.png")
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    titulo_texto = fonte_titulo.render("RECORDES", True, cor_titulo)
    titulo_rect = titulo_texto.get_rect()
    titulo_rect.center = (largura_tela // 2, 100)

    recordes = carregar_recordes()
    recordes_ordenados = sorted(recordes, reverse=True)
    recordes_ordenados = recordes_ordenados[:8]

    voltar_texto = fonte_botao.render("VOLTAR", True, branco)
    voltar_rect = voltar_texto.get_rect()
    voltar_rect.center = (largura_tela // 2 + 300, altura_tela - 50)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if voltar_rect.collidepoint(evento.pos):
                    # Voltar ao menu
                    rodando = False
                    exibir_menu()

        tela.blit(fundo, (0, 0))
        tela.blit(titulo_texto, titulo_rect)

        posicao_y = 200
        espacamento = 50
        numeracao = 1

        for pontuacao in recordes_ordenados:
            numeracao_texto = fonte_pontuacao.render(f"{numeracao}.", True, branco)
            numeracao_rect = numeracao_texto.get_rect()
            numeracao_rect.center = (largura_tela // 2 - 100, posicao_y)

            pontuacao_texto = fonte_pontuacao.render(str(pontuacao), True, branco)
            pontuacao_rect = pontuacao_texto.get_rect()
            pontuacao_rect.center = (largura_tela // 2, posicao_y)

            tela.blit(numeracao_texto, numeracao_rect)
            tela.blit(pontuacao_texto, pontuacao_rect)

            numeracao += 1
            posicao_y += espacamento

        pygame.draw.rect(tela, cor_titulo, voltar_rect)
        tela.blit(voltar_texto, voltar_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def exibir_ajuda():
    pygame.init()

    largura_tela = 800
    altura_tela = 600

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Covid Invaders Matemático")

    clock = pygame.time.Clock()

    cor_titulo = (255, 189, 89)  # #FFBD59
    branco = (255, 255, 255)

    fonte_titulo = pygame.font.Font("ArchivoBlack-Regular.ttf", 36)
    fonte_texto = pygame.font.Font("ArchivoBlack-Regular.ttf", 24)
    fonte_botao = pygame.font.Font("ArchivoBlack-Regular.ttf", 30)

    fundo = pygame.image.load("assets/back.png")
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    titulo_texto = fonte_titulo.render("AJUDA", True, cor_titulo)
    titulo_rect = titulo_texto.get_rect()
    titulo_rect.center = (largura_tela // 2, 100)

    ajuda_texto = "O jogador deve utilizar o teclado númerico na tela do jogo\npara inserir o valor correspondente a operação do vírus\nem seguida deve apertar Space para confirmar.\nSe a resposta for correta, o vírus será eliminado.\nSe for errada, o jogador perde uma das 3 vidas."
    linhas = ajuda_texto.split("\n")
    texto_renderizado = []
    for linha in linhas:
        texto = fonte_texto.render(linha, True, branco)
        texto_renderizado.append(texto)

    posicao_y = 200
    espacamento = 40

    voltar_texto = fonte_texto.render("VOLTAR", True, branco)
    voltar_rect = voltar_texto.get_rect()
    voltar_rect.center = (largura_tela // 2, altura_tela - 50)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if voltar_rect.collidepoint(evento.pos):
                    exibir_menu()

        tela.blit(fundo, (0, 0))
        tela.blit(titulo_texto, titulo_rect)

        posicao_y = 200  # Reinicia a posição Y a cada iteração

        for texto in texto_renderizado:
            texto_rect = texto.get_rect()
            texto_rect.center = (largura_tela // 2, posicao_y)
            tela.blit(texto, texto_rect)
            posicao_y += espacamento

        tela.blit(voltar_texto, voltar_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def jogo():
    jogador = Jogador()
   

    pontuacao = 0
    fonte = pygame.font.Font(None, 36)

    grupo_botoes = pygame.sprite.Group()
    posicao_x = largura_tela - 50  # Posição inicial X para o primeiro botão

    largura_botao = 30  # Largura do botão em pixels
    espacamento = 5  # Espaçamento entre os botões em pixels

    for numero in reversed(range(10)):
        botao = Botao(str(numero), (posicao_x + 45, altura_tela - 50))
        botao.atualizar_texto()
        grupo_botoes.add(botao)
        posicao_x -= largura_botao + espacamento  # Atualizar a posição X para o próximo botão

    # Adicionar botão de remoção
    remover_imagem = pygame.transform.scale(pygame.image.load("assets/remover.png"), (largura_botao, largura_botao))
    botao_remover = BotaoRemover(remover_imagem, (posicao_x + 45, altura_tela - 50))
    grupo_botoes.add(botao_remover)

    # Atualizar a posição X do botão 9 para acomodar o botão remover ao lado esquerdo
    posicao_x -= largura_botao + espacamento

    # Atualizar a posição dos botões restantes
    for botao in grupo_botoes:
        botao.rect.x -= (largura_botao + espacamento)
    imagem_coracao = carregar_imagem_coração("assets/heart.png")
    # Criar grupo de corações
    coracoes = pygame.sprite.Group()
    posicao_x_coracoes = largura_tela - 680  # Posição inicial X para o primeiro coração
    espacamento_coracoes = 35  # Espaçamento entre os corações em pixels
    vida_maxima = 3

    # Adicionar corações ao grupo
    for i in range(vida_maxima):
        coracao = Coracao(imagem_coracao, (posicao_x_coracoes, altura_tela - 50))
        coracoes.add(coracao)
        posicao_x_coracoes -= espacamento_coracoes

    som_musica = pygame.mixer.Sound("assets/musica.mp3")
    som_musica.play(-1)  # Reproduzir música em loop contínuo
    som_explosao = pygame.mixer.Sound("assets/efeitobomba.mp3")
    
    imagem_pause = pygame.image.load("assets/play-button.png")

    imagem_explosao = pygame.image.load("assets/explosion.png").convert_alpha()
    imagem_explosao = pygame.transform.scale(imagem_explosao, (50, 50))

    
    # Redimensionar a imagem do botão de pausa para as dimensões desejadas
    largura_botao_pause = 30
    altura_botao_pause = 30
    imagem_pause = pygame.transform.scale(imagem_pause, (largura_botao_pause, altura_botao_pause))

    # Definir a posição do botão de pausa no canto superior direito da tela
    posicao_x_pause = largura_tela - largura_botao_pause - 10
    posicao_y_pause = 10

    rodando = True
    contador_tempo = 0
    quantidade_invasores = 0
    invasores = pygame.sprite.Group()

    velocidade_invasores = 1
    contador_velocidade = 0

    resposta_atual = ""  # Declaração da variável resposta_atual
    mostrar_valor = True  # Controla a exibição do valor inserido

    pausado = False  # Variável para controlar o estado de pausa do jogo

    while rodando:

        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                jogador_acertou = False  # Variável para indicar se o jogador acertou a resposta

                for invasor in invasores:
                    if resposta_atual == str(invasor.calcular_resposta()):
                        jogador_acertou = True  # O jogador acertou a resposta

                if jogador_acertou:
                    invasores_certos = [invasor for invasor in invasores if str(invasor.calcular_resposta()) == resposta_atual]
                    for invasor in invasores_certos:
                        som_explosao.play()
                        invasores.remove(invasor)
                        tela.blit(imagem_explosao, invasor.rect.center)
                        pygame.display.flip()
                    pontuacao += len(invasores_certos)
                    pygame.time.wait(200) 
                else:
                    print('Resposta incorreta')
                    if len(coracoes) > 0:
                        coracao_perdido = coracoes.sprites()[-1]
                        coracoes.remove(coracao_perdido)

                resposta_atual = ""  # Limpar a resposta atual
                mostrar_valor = True  # Exibir o valor inserido novamente

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if posicao_x_pause <= evento.pos[0] <= posicao_x_pause + largura_botao_pause and posicao_y_pause <= evento.pos[1] <= posicao_y_pause + altura_botao_pause:
                        pausado = not pausado
                    if pausado:
                        som_musica.stop()
                    else:
                        som_musica.play(-1)

                    for botao in grupo_botoes:
                        if botao.rect.collidepoint(evento.pos):
                            if botao is botao_remover:
                                resposta_atual = resposta_atual[:-1]  # Remove o último caractere
                            else:
                                resposta_atual += botao.numero
                                botao.atualizar_texto()  # Atualizar o texto do botão

        if pausado:
            continue

        tela.blit(fundo, (0, 0))
        tela.blit(imagem_pause, (posicao_x_pause, posicao_y_pause))
        
        jogador.update()
        invasores.update()

        #logica para  incremento dos invasores a cada x segundos
        if contador_tempo == 4 * 60:
            quantidade_invasores += 1
        elif contador_tempo == 15 * 60:
            quantidade_invasores += 1
        elif contador_tempo == 20 * 60:
            quantidade_invasores += 2
        elif contador_tempo > 20 * 60 and contador_tempo % (10 * 60) == 0:

            quantidade_invasores += 1

        quantidade_invasores = min(quantidade_invasores, 10)
        
        contador_tempo += 1
        contador_velocidade += 1

        if contador_velocidade == 900:
            velocidade_invasores += 0.1
            contador_velocidade = 0

        while len(invasores) < quantidade_invasores:
            invasores.add(criar_invasores(1).sprites()[0])  # Criar um invasor e adicioná-lo ao grupo
        # Verificar se não há mais corações (Game Over)

        for invasor in invasores:
            if invasor.rect.bottom >= altura_tela:
                if len(coracoes) > 0:
                    coracao_perdido = coracoes.sprites()[-1]
                    coracoes.remove(coracao_perdido)
                invasores.remove(invasor)


        jogador_group = pygame.sprite.Group()
        jogador_group.add(jogador)
        jogador_group.draw(tela)
        coracoes.draw(tela)
        invasores.draw(tela)
        grupo_botoes.draw(tela)
        

        for invasor in invasores:
            texto = fonte.render(f"{invasor.valor1} {invasor.operacao} {invasor.valor2} = ?", True, vermelho)
            tela.blit(texto, (invasor.rect.x, invasor.rect.y + invasor.rect.height))

        grupo_botoes.update()
        grupo_botoes.draw(tela)

        if mostrar_valor:
            resposta_texto = fonte.render(resposta_atual, True, branco)
            tela.blit(resposta_texto, (10, altura_tela - 50))

        pontuacao_texto = fonte.render("Pontuação: " + str(pontuacao), True, branco)
        tela.blit(pontuacao_texto, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        if len(coracoes) == 0:
            salvar_pontuacao(pontuacao)
            mostrar_mensagem("Game Over")
            rodando = False
            som_musica.stop()

        for invasor in invasores:
            invasor.velocidade = velocidade_invasores

    exibir_menu()

if __name__ == '__main__':
    exibir_menu()