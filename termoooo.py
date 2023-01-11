from time import sleep
from random import choice
import pandas as pd
from unidecode import unidecode
import requests, json


letrasAmare = []
letrasVerd = []
letrasVerm = []
palpites = []
acerto = False
teclado1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ç',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M']

# Seção de perfis
perfis = pd.read_csv('perfil.csv', encoding='UTF=8', sep=',')
lista_nome = perfis['nome'].tolist()


tabela = pd.read_csv("palavras.csv")  # Extrair tabela
tabela.dropna(inplace=True)  # Deletar espaços em branco

listapalavras = tabela['palavras'].tolist()  # Transformar em lista


# Para sortear palvara diferente de uma já usada
while True:
    palavraOrig = choice(listapalavras).upper()  # Sortear palavra
    if palavraOrig != 'USED':
        break

palavra = unidecode(palavraOrig)  # Palavra sem acentos
tamPalavra = len(palavra)

while True:
    proc = str(input('Olá! Seja bem vindo ao Termooo, jogo para descobrir palavras.\nInsira o nome do seu perfil(Somente três letras!):\n==>')).upper().strip()
    if len(proc) == 3:
        break
    else:
        print('Insira um nome com 3 letras!')
    
# Conferir se perfil existe
if proc in lista_nome:
    print(f'\nSeja bem vindo de volta {proc}! Vamos começar!')
else:
    data = {
    'nome': [proc],  # Criação de novo perfil
    '1': [0],
    '2':[0],
    '3':[0],
    '4':[0],
    '5':[0],
    '6':[0],
    'falha':[0],
    'seq':[0]
    }

    df = pd.DataFrame(data)
    df.to_csv('perfil.csv', mode='a', index=False, header=False)
    print(f'Novo perfil criado com sucesso!')

# Para obter a posição do perfil
try:
    indes = int(perfis[perfis['nome'] == f'{proc}'].index.values)
except:
    print()

print(f'A palavra tem {tamPalavra} letras')
for tent in range(1, 7):  # Palpites
    g = 0
    while True:  
        p = 1
        print('====================')
        for i in teclado1:

            # PRINTAR FORMATO TECLADO
            p += 1
            if p == 12:
                print(end='\n ')
            if p == 22:
                print(end='\n  ')

            # PRINTAR LETRAS
            if i in letrasVerd:
                print(f'\033[1;32m{i}\033[m', end=' ')
            elif i in letrasAmare:
                print(f'\033[1;33m{i}\033[m', end=' ')
            elif i in letrasVerm:
                print(' ', end=' ')
            else:
                print(f'{i}', end=' ')

        while True:
            palp = str(input(f'\nInsira o {tent}º palpite: ')).strip()
            if palp in listapalavras:
                palp = palp.upper()
                break
            else:
                print('Essa palavra não existe!')

        if len(palp) == tamPalavra:
            palpites.append(palp)
            break
        
        print(f'ERRO! INSIRA UMA PALAVRA COM {tamPalavra} LETRAS.')

    # Verificação de acerto
    if palp == palavra:
        for i in palavraOrig:
            print(f'\033[1;32m{i}\033[m', end='')
            sleep(0.3)
        print(f'\nParabéns! Você acertou em {tent} tentativas')

        # Somar um para as tentativas
        novo_valor = int(perfis[perfis['nome'] == f'{proc}'][f'{tent}']) + 1
        perfis.loc[indes, f'{tent}'] = novo_valor
        perfis.to_csv('perfil.csv', index=False)

        acerto = True
        break

    else:
        # Verificação de letras
        for c in palp:
            if c == palavra[g]:
                print(f'\033[1;32m{c}\033[m', end='')
                if c not in letrasVerd:
                    letrasVerd.append(c)
                    if c in letrasAmare:
                        letrasAmare.remove(c)

            if c in palavra and c != palavra[g]:
                print(f'\033[1;33m{c}\033[m', end='')
                if c not in letrasAmare and c not in letrasVerd:
                    letrasAmare.append(c)

            if c not in palavra:
                print(f'\033[1;31m{c}\033[m', end='')
                if c not in letrasVerm:
                    letrasVerm.append(c)
            sleep(0.3)
            g += 1
    print('\n====================')

    # Print de histórico
    for w in palpites:
        n = 0
        print('    ', end=' ')
        for c in w:
            if c == palavra[n]:
                print(f'\033[1;32m{c}\033[m', end=' ')

            if c in palavra and c != palavra[n]:
                print(f'\033[1;33m{c}\033[m', end=' ')

            if c not in palavra:
                print(f'\033[1;31m{c}\033[m', end=' ')
            n += 1
        print()

    p = 0
    print('    ', end=' ')
    # Print do escopo
    for c in palavra:
        if c in letrasVerd:
            print(f'\033[1;32m{c}\033[m', end=' ')

        else:
            print('_', end=' ')
        p += 1
    print()

    # Você errou
if acerto == False:
    print('Você perdeu...tente novamente')
    print(f'Palavra do dia: {palavraOrig}')
    
    # Somar um para a falhas
    novo_valor = int(perfis[perfis['nome'] == f'{proc}']['falha']) + 1
    perfis.loc[indes, 'falha'] = novo_valor
    perfis.to_csv('perfil.csv', index=False)
    
    acerto = True

# Distribuição de tentativas
print(f'Distribuição de tentativas de {proc}')
for c in range(1, 7):
    distr = int(perfis[perfis['nome'] == f'{proc}'][f'{c}'])
    print(f'{c} ', distr * '#', distr)

print('Errrrouu',int(perfis[perfis['nome'] == f'{proc}']['falha']) * '#', int(perfis[perfis['nome'] == f'{proc}']['falha']))


# Compartilhamento
print('Deseja compartilhar? Copie o texto abaixo:')
for w in palpites:
        n = 0
        print('    ', end=' ')
        for c in w:
            if c == palavra[n]:
                print(f'\033[1;32m#\033[m', end=' ')

            if c in palavra and c != palavra[n]:
                print(f'\033[1;33m#\033[m', end=' ')

            if c not in palavra:
                print(f'\033[1;31m#\033[m', end=' ')
            n += 1
        print()

# Deletar palavra usada, salvar csv
if acerto:
    tabela['palavras'] = tabela['palavras'].replace(palavraOrig.lower(), 'used')
    tabela.to_csv('palavras.csv', index=False)
    print('Palavra excluída com sucesso')
