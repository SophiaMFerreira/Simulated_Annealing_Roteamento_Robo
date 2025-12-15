# 🤖 Projeto Simulated Annealing – Roteamento de Robô

**Autoras**: Nadine Vasconcellos e Sophia Ferreira

**Descrição Geral**: O projeto aplica a **meta-heurística** Simulated Annealing (S.A.) ao problema de roteamento de um robô em um tabuleiro com obstáculos. O robô deve sair da posição inicial (0, 0) e alcançar o objetivo (N–1, N–1), buscando **minimizar o custo total** da rota.
O processo combina uma fase construtiva (geração da rota inicial) e uma fase de busca local (refinamento por reparo de colisões e remoção de ciclos), repetindo diversas execuções e aceitando (ou rejeitando) novas soluções conforme a temperatura do S.A.

---

## 📝 Metaheurística Utilizada

* **Tipo:** Simulated Annealing (S.A.)
* **Fase ativa:** Construtiva + Busca Local
* **Temperatura Inicial:** 2162
* **Temperatura Final:** 25
* **Resfriamento:** exponencial (dependente da iteração `j`)
* **Número de execuções (critério global):** 6000 (`jMaximo`)
* **Critério de platô:** 40 (`plator`) iterações sem melhoria antes de parar a busca local

---

## ⚙️ Sobre a Solução com Simulated Annealing

### 🔧 Fase Construtiva

Na fase construtiva, o robô constrói uma rota até o objetivo usando uma função que tenta aproximar a posição do destino, ajustando primeiro o eixo **Y** e depois o eixo **X**. Quando o próximo passo cai em obstáculo, o algoritmo executa um **desvio aleatório válido** para continuar a trajetória.

---

### 💰 Função de Cálculo de Custo

A função `calculaCusto(rota)` avalia a qualidade da trajetória do robô e define o que é “melhor” para o algoritmo. Ela soma um custo base por passo e adiciona penalidades quando ocorrem situações indesejáveis (obstáculo, revisita e movimento “para trás”).

```python
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
```

#### ⚖️ Penalidades Consideradas

| Situação                                 | Penalidade |
| ---------------------------------------- | ---------- |
| Passo Normal                             | +1         |
| Colisão com obstáculo                    | +50        |
| Revisita de célula (ciclo/loop)          | +10        |
| Movimento “para trás” (dx < 0 ou dy < 0) | +10        |

✅ **Quanto menor o custo, melhor a rota.**

Essas penalizações incentivam o robô a:

* evitar obstáculos,
* evitar retornar a células já visitadas,
* e reduzir movimentos para esquerda/baixo (que geram `dx < 0` ou `dy < 0`).

---

### 🔧 Função de Construção/Re-conexão: `encontraObjetivo(posicao, objetivo)`

Essa função é usada na fase construtiva e também na busca local. Ela tenta aproximar o robô do objetivo (ou de um objetivo intermediário), fazendo até **dois passos por chamada**:

1. ajusta o eixo **Y** (cima/baixo)
2. ajusta o eixo **X** (direita/esquerda)
   
Se o passo planejado cair em obstáculo, o código chama um movimento aleatório.

```python
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
```

📌 **Resumo do comportamento**

* Se o robô está “abaixo” do objetivo em Y → tenta subir.
* Se está “acima” do objetivo em Y → tenta descer.
* Depois tenta avançar em X: direita (ou esquerda se necessário).
* Em obstáculo: desvia com `geraMovimentoAleatorio`.

---

### 🚧 Tratamento de Obstáculos: `geraMovimentoAleatorio(posicao)`

Quando o robô precisa desviar, esta função sorteia um movimento entre 4 direções até gerar um destino **dentro do tabuleiro**.
⚠️ Ela **não impede** cair em obstáculo; apenas impede sair do tabuleiro.

```python
def geraMovimentoAleatorio(posicao):
    coordenadaDestino = [-1,-1];
    while(coordenadaDestino[0] < 0  or coordenadaDestino[0] >= N or coordenadaDestino[1] < 0 or coordenadaDestino[1] >= N):
        movimento = random.randint(1,4);
        movX, movY = movimentos[movimento];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    return [0, coordenadaDestino];    
```

---

### 🔎 Remoção de Ciclos: `removeCiclos(rota, inicioCorte, fimCorte)`

O algoritmo tenta remover “voltas” da rota (quando uma posição aparece novamente) cortando trechos intermediários.

```python
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
```

📌 **O que ela faz (na prática)**

* Procura se `rota[inicioCorte]` aparece mais à frente.
* Se aparecer, avança `fimCorte` recursivamente.
* Ao identificar trecho repetido, “corta” o ciclo concatenando pedaços da lista.

---

### 🌡️ Critério de Aceitação + Resfriamento: `temperagem(...)`

Essa função é o núcleo do Simulated Annealing:

* decide se a solução nova é aceita (variável booleana retornada),
* e atualiza a temperatura pela equação de resfriamento exponencial.

```python
def temperagem(energiaCorrente, energiaNova, temperaturaCorrente, tempo):
    cttResfriamento = 0.32
    variacaoTemperatura = energiaNova - energiaCorrente;
    aceitacao = False
    if(variacaoTemperatura >= 0):
        aceitacao = True;
    else:
        if (random.random() <= math.exp((variacaoTemperatura) / temperaturaCorrente )):
            aceitacao = True;
        else:
            aceitacao = False;
    temperaturaCorrente = temperaturaFinal + ((temperaturaInicial - temperaturaFinal) * math.exp(-cttResfriamento * tempo));  
    return temperaturaCorrente, aceitacao;
```

📌 **Interpretação do que o código implementa**

* Calcula `variacaoTemperatura = novoCusto - custoAtual`.
* Se a variação for ≥ 0, aceita diretamente.
* Caso contrário, aceita com probabilidade `exp(variacao / T)`.
* Depois atualiza `T` com:
  [
  T = T_f + (T_i - T_f)\cdot e^{-k\cdot tempo}
  ]
  onde `tempo` é a iteração `j`.

---

## 🔎 Fase de Busca Local (refinamento da rota)

Após construir a rota e remover ciclos, o algoritmo entra em uma busca local enquanto:

* `temperaturaCorrente > temperaturaFinal` e
* `iPlator < plator`

Nesta fase, o código percorre a `novaRota` e tenta **reparar colisões com obstáculos**:

* separa a rota em “antes” e “depois” do ponto problemático,
* aplica um passo aleatório,
* reconecta usando `encontraObjetivo` até alcançar um ponto do trecho posterior,
* remove ciclos e reavalia custo,
* decide aceitar usando `temperagem`.

Trecho principal da busca local (conforme implementado):

```python
while(temperaturaCorrente > temperaturaFinal and iPlator < plator):
    if(not explorar):
        novaRota = rota[:];
        iPlator = 0;
            
    for coordenada in novaRota:
        if coordenada in obstaculos:
            rotaAntesColisao = novaRota[:coordenada];
            rotaAposColisao = novaRota[coordenada + 1:];
            objCoordenadaDestino = geraMovimentoAleatorio(rotaAntesColisao[-1]);
            posicao = objCoordenadaDestino[1][:];
            rotaAntesColisao.append(posicao);
            while(posicao != rotaAposColisao[0]):
                rotaAntesColisao, posicao =  encontraObjetivo(posicao, rotaAposColisao[0]);
            novaRota = rotaAntesColisao[:] + rotaAposColisao[1:];
```

Depois, o algoritmo remove ciclos novamente, calcula o novo custo e decide aceitação:

```python
novoCusto = calculaCusto(novaRota);
temperaturaCorrente, explorar = temperagem(custo, novoCusto, temperaturaCorrente, j);
```

E por fim atualiza a melhor solução global:

```python
if(melhorCusto > novoCusto):
    melhorCusto = novoCusto;
    melhorRota = novaRota[:];
```

---

### 🧭 Resultado Final

Ao final das execuções, o algoritmo: exibe graficamente a melhor rota encontrada e imprime o melhor custo final.

* Melhor Custo Final SA: 278

<div align="center">
  <img width="500" alt="melhorCustoSA" src="https://github.com/user-attachments/assets/501ae2ab-a1b5-44b7-b702-c56e723fdb5e" />
</div>

