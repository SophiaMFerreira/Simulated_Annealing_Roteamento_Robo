'''
    Projeto Simulated Annealing: Nadine Vasconcellos e Sophia Ferreira
    Problema de Roteamento de Robô
'''

import random
import matplotlib.pyplot as plt
import math

#Ambiente
random.seed(3)  #para gerar as mesmas instâncias a partir da mesma semente
N = 30
Obs = N*10
inicio = [0, 0]
objetivo = [N-1, N-1]
obstaculos = set() #gera os obstáculos sem repetição de coordenadas
while len(obstaculos) < Obs:
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    if (x, y) != inicio and (x, y) != objetivo:
        obstaculos.add((x, y))
obstaculos = list(obstaculos) #transformação em lista para facilitar o uso de métodos
obstaculos.sort()

#Coordenadas dos movimentos possíveis: 1=Cima, 2=Direita, 3=Baixo, 4=Esquerda
movimentos = {
    1: (0, 1),   # Cima
    2: (1, 0),   # Direita
    3: (0, -1),  # Baixo
    4: (-1, 0)   # Esquerda
}

pesoMovimentos = {
    1: 10,   # Cima
    2: 10,   # Direita
    3: 5,    # Baixo
    4: 5     # Esquerda
}

random.seed();
tamanhoLCR = 2;
temperaturaInicial = 2162;
temperaturaFinal = 25;

def imprimeGrafico(melhorRota):
    x=[]
    y=[]
    for i in range(len(obstaculos)):
        x.append(obstaculos[i][0]);
        y.append(obstaculos[i][1]);
    plt.scatter(x, y, color='#f15bb5');
    
    x=[];
    y=[];
    z=[];
    w=[];
    for coordenada in melhorRota:
        x.append(coordenada[0]);
        y.append(coordenada[1]);
        if tuple(coordenada) in obstaculos:
           z.append(coordenada[0]);
           w.append(coordenada[1]);
    plt.scatter(x, y, color='#00f5d4');
    plt.scatter(z, w, color='#d00000', marker='x');
    plt.show();
    
def calculaCusto(rota):
    custo = 0;
    visitadas = set();

    for i in range(len(rota) - 1):
        posicaoAtual = rota[i];
        proxima = rota[i + 1];

        if tuple(posicaoAtual) in obstaculos:
            custo += 50;
        else:
            custo += 1;

        if tuple(posicaoAtual) in visitadas:
            custo += 10;

        dx = proxima[0] - posicaoAtual[0];
        dy = proxima[1] - posicaoAtual[1];
        if dx < 0 or dy < 0:
            custo += 10;

        visitadas.add(tuple(posicaoAtual));

    return custo

def encontraObjetivo(posicao, objetivo):
    coordenadaDestino = posicao[:];
    
    if(posicao[1] < objetivo[1]):
        movX, movY = movimentos[1];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    elif(posicao[1] > objetivo[1]):
            movX, movY = movimentos[3];
            coordenadaDestino[0] = movX + posicao[0];
            coordenadaDestino[1] = movY + posicao[1];
    if(tuple(coordenadaDestino) in obstaculos):
        objCoordenadaDestino = geraMovimentoAleatorio(posicao);
        posicao = objCoordenadaDestino[1][:];
    else:
        posicao = coordenadaDestino[:];
    rota.append(posicao);
    
    if(posicao == objetivo):
        return rota, posicao;
    
    if(posicao[0] < objetivo[0]):
        movX, movY = movimentos[2];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    elif(posicao[0] > objetivo[0]):
        movX, movY = movimentos[4];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    if(tuple(coordenadaDestino) in obstaculos):
        objCoordenadaDestino = geraMovimentoAleatorio(posicao);
        posicao = objCoordenadaDestino[1][:];
    else:
        posicao = coordenadaDestino[:];
    rota.append(posicao);
    return rota, posicao;   

def geraMovimentoAleatorio(posicao):
    '''
    listaDestinos = [];
    coordenadaDestino = inicio[:];
    
    for movimento in movimentos:
        listaDestinos.append([movimento, inicio[:], 0]);
        
    for movimento in movimentos:
        movX, movY = movimentos[movimento];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
        listaDestinos[movimento-1][1] = coordenadaDestino[:];
        if tuple(coordenadaDestino) in obstaculos or tuple(coordenadaDestino) in rota:
            listaDestinos[movimento-1][2] = pesoMovimentos[movimento] * 50;
        elif coordenadaDestino[0] < 0  or coordenadaDestino[0] >= N or coordenadaDestino[1] < 0 or coordenadaDestino[1] >= N:
            listaDestinos[movimento-1][2] = pesoMovimentos[movimento] * 100;
        else:
            listaDestinos[movimento-1][2] = pesoMovimentos[movimento];
    
    LCR = sorted(listaDestinos, key=lambda objDestino: objDestino[2])[0:tamanhoLCR];
    pesos = [];
    for objDestino in LCR:
        if tuple(objDestino[1]) in obstaculos:
            pesos.append(pesoMovimentos[objDestino[0]] / 10);
        elif objDestino[1][0] < 0  or objDestino[1][0] >= N or objDestino[1][1] < 0 or objDestino[1][1] >= N:
            pesos.append(0);
        else:
            pesos.append(pesoMovimentos[objDestino[0]]);
            
    return random.choices(LCR, weights=pesos, k=1)[0]; '''

    coordenadaDestino = [-1,-1];
    while(coordenadaDestino[0] < 0  or coordenadaDestino[0] >= N or coordenadaDestino[1] < 0 or coordenadaDestino[1] >= N):
        movimento = random.randint(1,4);
        movX, movY = movimentos[movimento];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    return [0, coordenadaDestino];    

def removeCiclos(rota, inicioCorte, fimCorte):
    if(len(rota) < 2):
        return rota;
    
    if(rota[inicioCorte] in rota[fimCorte:]):
        return removeCiclos(rota, inicioCorte, fimCorte + 1);
        
    elif(inicioCorte != fimCorte):
        rota = rota[:inicioCorte + 1] + rota[fimCorte:];
        inicioCorte = 0;
        fimCorte = 0;
        return rota;

def temperagem(energiaCorrente, energiaNova, temperaturaCorrente):
    variacaoTemperatura = energiaNova - energiaCorrente;
    aceitacao = False
    if(variacaoTemperatura >= 0):
        aceitacao = True;
    else:
        if (random.random() <= math.exp((variacaoTemperatura) / temperaturaCorrente )):
            aceitacao = True;
        else:
            aceitacao = False;
    temperaturaCorrente = temperaturaCorrente * 0.995;    
    return temperaturaCorrente, aceitacao;
#------------------------------------------------------------------------------------------------------------------------------------------

temperaturaCorrente = temperaturaInicial;
plator = 400;

jMaximo = 10000;
melhorCusto = 99999;
melhorRota = [];

for j in range(0, jMaximo):
    posicao = inicio[:];
    rota = [inicio[:]];    
    iPlator  = 0;
    
    while(posicao != objetivo):
        rota, posicao =  encontraObjetivo(posicao, objetivo);
    i = 0;
    while(i < len(rota)):
        rota = removeCiclos(rota, i, 0)
        i += 1;
    custo = calculaCusto(rota);
    
    if(melhorCusto > custo):
        melhorCusto = custo;
        melhorRota = rota[:];
        iPlator = 0;
        print("Melhor Custo Parcial:", melhorCusto)
    else:
        iPlator += 1;

    novaRota = rota[:];
    explorar = True;
    while(explorar and temperaturaCorrente > temperaturaFinal and iPlator == plator):
        for coordenada in novaRota:
            if coordenada in obstaculos:
                rotaAntesColisao = novaRota[:coordenada];
                rotaAposColisao = novaRota[coordenada + 1:];
                objCoordenadaDestino = geraMovimentoAleatorio(rotaAntesColisao[-1]);
                posicao = objCoordenadaDestino[1][:];
                rotaAntesColisao.append(posicao);
                while(posicao != rotaAposColisao[0]):
                    rotaAntesColisao, posicao =  encontraObjetivo(posicao, rotaAposColisao[0], False);
                novaRota = rotaAntesColisao[:] + rotaAposColisao[1:];
        i = 0;
        while(i < len(novaRota)):
            novaRota = removeCiclos(novaRota, i, 0)
            i += 1;
        novoCusto = calculaCusto(novaRota);
        
        temperaturaCorrente, explorar = temperagem(custo, novoCusto, temperaturaCorrente);
        if(melhorCusto > novoCusto):
            melhorCusto = novoCusto;
            melhorRota = novaRota[:];
            iPlator = 0;
            print("Melhor Custo Parcial:", melhorCusto)
        else:
            iPlator += 1;

imprimeGrafico(melhorRota);
print("\n========== Resultado SA ==========")
print("Melhor custo Final: ", melhorCusto);