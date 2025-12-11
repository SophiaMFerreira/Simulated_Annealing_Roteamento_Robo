# 🤖 Projeto Simulated Annealing – Roteamento de Robô
 <!--
Temperatura: Inicial, final, taxa de redução
Fase de busca local: Estratégia de modificação
Estratégia de aceitação de soluções: Melhora x Piora
Critério de parada por temperatura
Critério de finalização


*Comparar o GRASP e o SA-->

**Autoras**: Nadine Vasconcellos e Sophia Ferreira

**Descrição Geral**: O projeto aplica a meta-heurística Simulated Annealing ao problema de roteamento de um robô em um tabuleiro com obstáculos. O objetivo é conduzir o robô da posição inicial (0, 0) até o destino (N – 1, N – 1), minimizando o custo total da rota e evitando posições com obstáculos e movimentos desfavoráveis.

O algoritmo inicia com uma solução base (rota inicial) e, a partir dela, realiza perturbações controladas — pequenas modificações na rota — que podem ser aceitas ou rejeitadas conforme o critério de Metropolis, que considera a variação de custo e a temperatura corrente. À medida que a temperatura diminui, o sistema se torna mais seletivo, favorecendo soluções cada vez melhores até convergir para um caminho final de alto desempenho.

---

## 📝 Metaheurística Utilizada

- **Tipo:** Simulated Annealing (S.A.)  
- **Fase construtiva: ** A movimentação do robô se dá de modo diagonal, gerando um movimento aleatório ao colidir com um obstáculo
- **Fase de busca local:** Remoção de colisões introduzindo um movimento novo e aleatório
- **Temperatura inicial:** 25
- **Temperatura final:** 25°
- **Esquema de resfriamento:** ??? geométrico, gostaria de INOVAR
- **Estratégia de aceitação de soluções** Melhora ou inalteração, ou aceito pela probabilidade de Metropolis
- **Critério de finalização:** combinação dos critérios abaixo 
    - **Número de execuções máxima:** 10000 `jMaximo = 10000;`
    - **Critério de parada por temperatura (platô):** 400 `plator = 400;`
    - **Critério de parada por temperatura:** temperatura corrente igual a temperatura mínima

---

## ⚙️ Sobre a Solução de Simulated Annealing

### 🔧 Fase Construtiva

Na fase construtiva, o robô inicia sua trajetória movendo-se diagonalmente, ou seja, alternando os movimentos no eixo Y e no eixo X  até alcançar o objetivo final, independentemente de sua localização.
O algoritmo trabalha sobre um tabuleiro de dimensão N × N, contendo obstáculos gerados aleatoriamente, e em cada iteração o robô calcula o próximo movimento conforme as regras abaixo.

#### 🧩 1. Movimentação Principal
O comportamento da trajetória é controlado pelas condições de sentido:

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

#### 🚧 2. Tratamento de Obstáculos
Quando o próximo passo encontra um obstáculo `if(tuple(coordenadaDestino) in obstaculos)`, a função `geraMovimentoAleatorio()` é chamada:

```python

```

Essa função gera uma Lista de Candidatos Restrita (LCR) contendo até 3 movimentos entre os 4 possíveis, excluindo aqueles que: 
- Colidem com obstáculos
- Saem dos limites do tabuleiro

#### 🎯 3. Cálculo da Qualidade (Pesos)
Dentro da função `geraMovimentoAleatorio()`, é feita a atribuição de pesos para cada direção, conforme a tabela abaixo:

| Movimento                        | Peso | Qualidade   |
|----------------------------------|------|-------------|
| Mov no eixo Y a favor do objetivo| 10   | Ótima       |
| Mov no eixo X a favor do objetivo| 10   | Ótima       |
| Mov no eixo Y contra do objetivo | 5    | Média       |
| Mov no eixo X contra do objetivo | 5    | Média       |
| Y a favor + Obstáculo ou Retorno | 1    | Ruim        |
| X a favor + Obstáculo ou Retorno | 1    | Ruim        |
| Y contra + Obstáculo ou Retorno  | 0.5  | Ruim        |
| X contra + Obstáculo ou Retorno  | 0.5  | Ruim        |
| Mov no eixo Y fora do tabuleiro  | 0    | Descartada  |
| Mov no eixo X fora do tabuleiro  | 0    | Descartada  |

Após atribuir os pesos, o movimento é sorteado aleatoriamente, porém ponderado conforme esses valores. Movimentos com peso maior têm maior probabilidade de serem escolhidos.

Em seguida, um movimento é **sorteado entre os candidatos da LCR** com base nos pesos da tabela (quanto maior a qualidade, maior a probabilidade de escolha), e o robô **retoma sua movimentação diagonal** conforme o movimento que havia sido interrompido.

Para que o robô encontre corretamente seu objetivo, ao atingir as coordenadas *x* ou *y* correspondentes ao destino, ele passa a se mover apenas no sentido necessário até o alcançar.  
Quando encontra um novo obstáculo, é chamada a função `geraMovimentoAleatorio()` para decidir o próximo passo.

**Observações:**
- O robô **pode colidir com obstáculos**;  
- **Retornos a posições já visitadas** são possíveis, mas penalizados;  
- A **hierarquia de movimentos** orienta a busca sem eliminar a aleatoriedade do processo.

---

### 💰 Função de Cálculo de Custo

A função `calculaCusto(rota)` é responsável por avaliar a qualidade da trajetória do robô, atribuindo um custo total que representa o “esforço” da rota.
Ela é utilizada tanto na fase construtiva para acompanhar o desempenho parcial da rota quanto na busca local para verificar se uma alteração melhora a solução.

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

Cada célula visitada contribui com um custo base de 1 ponto. Entretanto, situações indesejáveis adicionam penalidades específicas que aumentam o custo total.


#### ⚖️ Penalidades Consideradas

| Situação                            | Penalidade | 
|-------------------------------------|------------|
| Passo Normal                        | +1         | 
| Colisão com obstáculo               | +50        | 
| Movimento “retroceder”              | +10        | 
| Revisita de célula                  | +10        | 


- Quanto menor o custo, melhor a rota.
- Penalizações incentivam o robô a:
    - Evitar obstáculos
    - Evitar retornar a células já visitadas
    - Seguir consistentemente no sentido Right–Up.
- Em execuções iniciais, o custo tende a ser alto (por rota aleatória e colisões), **reduzindo gradualmente** conforme a busca local corrige desvios, até **estabilizar** próximo de 300.

---

#### ✂️ Refinamento Pré-Busca Local

Antes de iniciar a fase de busca local, a rota base passa por um processo de refinamento para evitar desperdício de tempo computacional em soluções excessivamente longas ou redundantes devido à presença de ciclos — trechos em que o robô retorna a uma coordenada já visitada, criando caminhos desnecessariamente extensos. Para evitar que esses ciclos aumentem o custo e prejudiquem o desempenho do SA, é aplicada a função `removeCiclos(rota, inicioCorte, fimCorte)` uma rotina de remoção de ciclos, que identifica e elimina esses retornos, preservando apenas o trecho útil da rota.


### 🔎 Fase de Busca Local

Após a construção completa da rota e removidos os ciclos, o algoritmo aplica uma busca local para ampliar o espaço de busca, saindo de mínimos locais e refinar a solução provocando redução do custo total.
A busca local na heurística SA busca não somente melhorar soluções viáveis já existentes, mas ampliar a varredura de soluções possíveis, aceitando inclusive soluções piores, para que em seguida as refine.

#### ⚙️ 1. Estrutura da Função

É coletada uma solução inicial que servirá de base para busca:

**a) Se a solução apresentar redução de custo, ela será mantida para refinamento**

Se o robô retornar a uma célula já visitada, o trecho entre as duas ocorrências é eliminado, reduzindo revisitas e evitando loops desnecessários.

```python
def buscaLocal(rota):
    posicoesVisitadas = {} #Guarda cada posição já visitada e o índice onde ela apareceu pela primeira vez
    rotaSemCiclo = [] #Nova rota sem repetições, versão "limpa" da original

    for posicao in rota:
        coordenadaPosicao = tuple(posicao);
        if coordenadaPosicao in posicoesVisitadas:
            indiceRepetido = posicoesVisitadas[coordenadaPosicao]; 
            rotaSemCiclo = rotaSemCiclo[:indiceRepetido + 1]; #Remoção da parte intermediária
            posicoesVisitadas = {tuple(rotaSemCiclo[i]): i for i in range(len(rotaSemCiclo))}; #Reconstrói o dicionário de posições já visitadas
        else:
            posicoesVisitadas[coordenadaPosicao] = len(rotaSemCiclo);
            rotaSemCiclo.append(posicao); 

    melhorRota = rotaSemCiclo[:] 
    melhorCusto = calculaCusto(melhorRota)
```

Efeito: corta rotas redundantes, encurta o caminho e diminui o custo de revisitas.


**b) Reparo de Um Passo**

Depois da limpeza de ciclos, o algoritmo verifica cada ponto intermediário da rota.
Quando um ponto é **problemático**, ou seja, quando está em uma coordenada de obstáculo ou resulta de um movimento para trás (Left-Down), tenta substituir por um ponto vizinho melhor, mantendo a coerência do trajeto **diagonal** da heurística Right-Up


```python
i = 1;
    while i < len(melhorRota) - 1:
        anterior = melhorRota[i - 1];
        atual    = melhorRota[i];
        proxima  = melhorRota[i + 1];

        dx = atual[0] - anterior[0];
        dy = atual[1] - anterior[1];

        if (tuple(atual) in obstaculos) or (dx < 0 or dy < 0): #Se o ponto atual for um obstáculo ou se o passo for "para trás" (Left-Down) esse trecho deve ser melhorado
            custoAtual = melhorCusto;
            for mov in (2, 1): #Teste das melhores alternativas, canditados de reparo
                movX, movY = movimentos[mov];
                nx, ny = anterior[0] + movX, anterior[1] + movY;
                if not (0 <= nx < N and 0 <= ny < N): #Fora do limite do tabuleiro
                    continue
                if (nx, ny) in obstaculos: #Caiu no obstaculo
                    continue
                if [nx, ny] == proxima:
                    continue

                rotaTeste = melhorRota[:i] + [[nx, ny]] + melhorRota[i + 1:]; #Cria uma nova rota substituindo as coordenadas problemáticas pela coordenada candidata
                custoTeste = calculaCusto(rotaTeste);
```

➡️ Efeito: corrige pequenos desvios da rota, privilegiando os movimentos Right–Up e reduzindo penalidades desnecessárias.


#### 💡 2. Integração com o GRASP

A busca local é aplicada após cada construção de rota:

```python
custo = calculaCusto(rota)

    for j in range(10):
        rotaBuscaLocal = buscaLocal(rota);
        custoRotaLocal = calculaCusto(rotaBuscaLocal);
        if (custoRotaLocal < custo):
            custo = custoRotaLocal;
            rota = rotaBuscaLocal[:];

    if (custo < melhorCusto): #Verifica se a rota atual é melhor que a rota encontrada até agora
        melhorCusto = custo;
        melhorRota = rota[:];
        iP = 0;
    else:
        iP += 1;
    i += 1;
```

Assim, a cada iteração do GRASP, a solução é:
- Construída aleatoriamente (Right–Up + LCR), ou seja, segue um padrão guiado mas tem flexibilidade inteligente para se desviar de obstáculos.
- Avaliada pela função de custo;
- Refinada pela busca local.

---

### 🧭 Resultado Final

Após várias iterações, o custo médio começa alto e diminui progressivamente conforme as rotas são refinadas.
O algoritmo para quando o melhor custo não melhora em 100 execuções consecutivas (condição de platô), resultando em soluções estáveis com custos próximos de 150.


<div align="center">
        <img width="600" alt="PlotGrasp143VIVA" src="https://github.com/user-attachments/assets/a7fa1b79-9bf1-49fc-b2f9-9297d5c6cbd9" />
</div>

<!-- Vamos entender a Lei de Resfriamento de Newton (Newton’s Law of Cooling) de forma matemática, profunda e estruturada, para que você possa aplicar corretamente no Simulated Annealing.

📘 1. O que a Lei realmente diz (ideia física)

A lei afirma que:

A taxa de variação da temperatura de um corpo é proporcional à diferença entre sua temperatura e a temperatura do ambiente.

Em outras palavras:

Quanto mais quente o corpo está comparado ao ambiente, mais rápido ele esfria.

Conforme o corpo se aproxima da temperatura ambiente, a velocidade do resfriamento diminui naturalmente.

Essa relação é exponencial, não linear.

📐 2. Expressão matemática fundamental

A lei é expressa como uma equação diferencial de 1ª ordem:

𝑑
𝑇
𝑑
𝑡
=
−
𝑘
(
𝑇
(
𝑡
)
−
𝑇
∞
)
dt
dT
	​

=−k(T(t)−T
∞
	​

)

Onde:

𝑇
(
𝑡
)
T(t) = temperatura do corpo no tempo 
𝑡
t

𝑇
∞
T
∞
	​

 = temperatura do ambiente (constante)

𝑘
>
0
k>0 = constante de resfriamento

𝑑
𝑇
𝑑
𝑡
dt
dT
	​

 = taxa de variação da temperatura

👉 Essa equação afirma que a inclinação da curva 
𝑇
(
𝑡
)
T(t) é proporcional ao quanto o corpo ainda está mais quente que o ambiente.

🧮 3. Solução da equação diferencial

Vamos resolver a equação:

𝑑
𝑇
𝑑
𝑡
=
−
𝑘
(
𝑇
(
𝑡
)
−
𝑇
∞
)
dt
dT
	​

=−k(T(t)−T
∞
	​

)

Primeiro, isolamos termos:

𝑑
𝑇
𝑇
−
𝑇
∞
=
−
𝑘
 
𝑑
𝑡
T−T
∞
	​

dT
	​

=−kdt

Integramos em ambos os lados:

∫
1
𝑇
−
𝑇
∞
 
𝑑
𝑇
=
−
𝑘
∫
𝑑
𝑡
∫
T−T
∞
	​

1
	​

dT=−k∫dt

Isso resulta em:

ln
⁡
∣
𝑇
−
𝑇
∞
∣
=
−
𝑘
𝑡
+
𝐶
ln∣T−T
∞
	​

∣=−kt+C

Aplicamos exponencial:

𝑇
−
𝑇
∞
=
𝐶
𝑒
−
𝑘
𝑡
T−T
∞
	​

=Ce
−kt

Agora usamos a condição inicial:

Para 
𝑡
=
0
t=0, 
𝑇
(
0
)
=
𝑇
0
T(0)=T
0
	​

:

𝑇
0
−
𝑇
∞
=
𝐶
T
0
	​

−T
∞
	​

=C

Substituímos:

𝑇
(
𝑡
)
=
𝑇
∞
+
(
𝑇
0
−
𝑇
∞
)
𝑒
−
𝑘
𝑡
T(t)=T
∞
	​

+(T
0
	​

−T
∞
	​

)e
−kt
🎯 4. O que isto significa na prática

A curva de resfriamento é:

Rápida no início

Lenta no final

Assintótica: nunca atinge exatamente a temperatura ambiente

O formato é sempre uma curva exponencial decrescente:

𝑇
(
𝑡
)
=
𝑇
∞
+
𝐴
𝑒
−
𝑘
𝑡
T(t)=T
∞
	​

+Ae
−kt

com 
𝐴
=
𝑇
0
−
𝑇
∞
A=T
0
	​

−T
∞
	​

.

Exemplo:
Se 
𝑇
0
=
300
T
0
	​

=300, 
𝑇
∞
=
25
T
∞
	​

=25, 
𝑘
=
0.1
k=0.1:

𝑇
(
𝑡
)
=
25
+
275
𝑒
−
0.1
𝑡
T(t)=25+275e
−0.1t
🔥 5. Aplicação direta no Simulated Annealing

No SA, a “temperatura” artificial deve diminuir gradualmente, permitindo:

maior aceitação de movimentos ruins no começo (exploração)

menor aceitação depois (exploração → exploração controlada)

A lei fornece exatamente isso.

🔧 Forma adaptada para SA:

Tome a fórmula:

𝑇
(
𝑡
)
=
𝑇
∞
+
(
𝑇
0
−
𝑇
∞
)
𝑒
−
𝑘
𝑡
T(t)=T
∞
	​

+(T
0
	​

−T
∞
	​

)e
−kt

Interprete:

𝑇
0
T
0
	​

 → temperatura inicial (ex.: 2658)

𝑇
∞
T
∞
	​

 → temperatura final mínima (ex.: 25)

𝑘
k → quanto rápido o SA resfria

𝑡
t → iteração atual

Implementação típica:

def temperatura(t, T0, Tmin, k):
    return Tmin + (T0 - Tmin) * math.exp(-k * t)

📌 6. Escolha de k

O parâmetro 
𝑘
k:

se pequeno → resfriamento lento (mais exploratório)

se grande → resfriamento rápido (pode cair em ótimos locais)

Valores típicos:
✔ 0.0005 a 0.05 (dependendo do número total de iterações)

💡 7. Por que esta lei serve tão bem para o SA

✔ É exponencial → mesmo formato usado nos papers clássicos
✔ Diminui rápido no início e lento depois → exatamente o comportamento desejado
✔ Possui limites definidos (
𝑇
0
T
0
	​

 e 
𝑇
∞
T
∞
	​

)
✔ Fácil de ajustar com 
𝑘
k
-->