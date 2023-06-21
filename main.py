import pygame
import random

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
        self.velocidade = 0.25


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

class BotaoPausa(pygame.sprite.Sprite):
    def __init__(self, imagem, posicao):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.topleft = posicao


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

class Coracao(pygame.sprite.Sprite):
    def __init__(self, imagem, posicao):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = posicao

# Função para carregar a imagem do coração
def carregar_imagem_coração(caminho):
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, (30, 30))

def criar_invasores(quantidade):
    invasores = pygame.sprite.Group()
    operacoes = ["+", "*", "/","-"]
    for _ in range(quantidade):
        operacao = random.choice(operacoes)
        invasor = Invasor(operacao)
        invasor.rect.x = random.randint(0, largura_tela - invasor.rect.width)
        invasor.rect.y = -invasor.rect.height

        colisoes = pygame.sprite.spritecollide(invasor, invasores, False)
        while colisoes:  # Verifica se houve colisão com outro invasor
            invasor.rect.x = random.randint(0, largura_tela - invasor.rect.width)
            invasor.rect.y = -invasor.rect.height
            colisoes = pygame.sprite.spritecollide(invasor, invasores, False)

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


def jogo():
    jogador = Jogador()
    balas = pygame.sprite.Group()

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
                    print("=", invasor.calcular_resposta())
                    if resposta_atual == str(invasor.calcular_resposta()):
                        jogador_acertou = True  # O jogador acertou a resposta

                if jogador_acertou:
                    invasores_certos = [invasor for invasor in invasores if str(invasor.calcular_resposta()) == resposta_atual]
                    for invasor in invasores_certos:
                        som_explosao.play()
                        invasores.remove(invasor)
                    pontuacao += len(invasores_certos)
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
        balas.update()

        if contador_tempo == 10 * 60:
            quantidade_invasores += 2
        elif contador_tempo == 20 * 60:
            quantidade_invasores += 4
        elif contador_tempo > 20 * 60 and contador_tempo % (10 * 60) == 0:
            quantidade_invasores += 1

        quantidade_invasores = min(quantidade_invasores, 10)

        while len(invasores) < quantidade_invasores:
            invasores.add(criar_invasores(1).sprites()[0])  # Criar um invasor e adicioná-lo ao grupo
        # Verificar se não há mais corações (Game Over)

        for invasor in invasores:
            if invasor.rect.bottom >= altura_tela:
                mostrar_mensagem("Game Over")
                rodando = False
                som_musica.stop()

        jogador_group = pygame.sprite.Group()
        jogador_group.add(jogador)
        jogador_group.draw(tela)
        coracoes.draw(tela)
        invasores.draw(tela)
        grupo_botoes.draw(tela)
        balas.draw(tela)

        for invasor in invasores:
            texto = fonte.render(f"{invasor.valor1} {invasor.operacao} {invasor.valor2} =", True, vermelho)
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

        contador_tempo += 1
        contador_velocidade += 1

        if contador_velocidade == 800:
            velocidade_invasores += 0.2
            contador_velocidade = 0
        if len(coracoes) == 0:
            mostrar_mensagem("Game Over")
            rodando = False
            som_musica.stop()

        for invasor in invasores:
            invasor.velocidade = velocidade_invasores

 

    exibir_menu()


exibir_menu()