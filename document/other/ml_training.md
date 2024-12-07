# Documentação: Treinamento de Modelos de Machine Learning para o Projeto FarmTech Solutions - Fase 4

Este documento descreve o processo de treinamento dos modelos de Machine Learning utilizados na Fase 4 do projeto FarmTech Solutions.  A Fase 4 visa aprimorar a aplicação desenvolvida na Fase 3, incorporando recursos como Scikit-learn, Streamlit e otimizações no ESP32 para um sistema de irrigação automatizado mais inteligente e eficiente.  Este notebook Jupyter foca especificamente no treinamento e avaliação de diferentes modelos de classificação para prever a necessidade de irrigação.

## 1. Contexto e Objetivo

O objetivo principal desta etapa é criar um modelo preditivo que utilize dados de sensores (umidade do solo, níveis de nutrientes, tipo de cultura e estágio fenológico) para prever se a irrigação é necessária. Este modelo será integrado ao sistema de irrigação automatizado, permitindo uma gestão mais eficiente da água e nutrientes.

## 2. Dados

Para o treinamento dos modelos, foram utilizados dados simulados gerados pela função `generate_fake_irrigation_data`.  Esta função cria um dataset sintético que imita dados reais de sensores, permitindo o desenvolvimento e teste do sistema de machine learning antes da integração com sensores físicos.

### 2.1. Lógica de Geração de Dados Sintéticos

A função `generate_fake_irrigation_data` utiliza distribuições Gaussianas para gerar valores realistas para as variáveis de entrada:

* **Níveis de nutrientes (K e P):**  Distribuições Gaussianas são usadas para simular a variação natural nos níveis de potássio (K) e fósforo (P) no solo.  As médias e desvios padrão dessas distribuições podem ser ajustados para refletir diferentes condições do solo.  Os valores gerados são limitados a faixas realistas através da função `np.clip`.

* **pH do solo:** Similarmente, a variação do pH é simulada por meio de uma distribuição Gaussiana, com restrições para manter os valores dentro de uma faixa aceitável para a maioria das culturas.

* **Umidade do solo:**  A umidade é gerada com uma distribuição Gaussiana e também é limitada a uma faixa razoável (de 10% a 80%).

* **Tipo de cultura e estágio fenológico:**  Estes são selecionados aleatoriamente de um conjunto pré-definido de culturas e estágios de crescimento.

* **Decisão de irrigação:** A lógica de decisão para a irrigação (`Irrigate`) é baseada em regras condicionais que levam em consideração o tipo de cultura, o estágio fenológico, e os níveis de umidade, potássio e fósforo e o pH.  Essas regras foram definidas com base no conhecimento agronômico básico, podendo ser ajustadas para simular diferentes estratégias de irrigação.

* **Introdução de ruído:**  Para tornar o dataset mais realista, a função inclui uma probabilidade de adicionar ruído à decisão de irrigação. Isso simula a imprevisibilidade de fatores externos que podem influenciar a necessidade de irrigação.  Esse ruído é adicionado com maior probabilidade quando os valores das variáveis estão próximos dos limites de suas faixas.

A flexibilidade da função `generate_fake_irrigation_data` permite a geração de datasets com diferentes tamanhos (`num_samples`), níveis de ruído (`noise_probability`) e sementes aleatórias (`seed`), permitindo a experimentação e o ajuste dos modelos de machine learning a diferentes cenários.  O código da função `generate_fake_irrigation_data` está presente no notebook Jupyter.


As features (variáveis independentes) do dataset incluem:

* **K:** Nível de Potássio (mg/kg)
* **P:** Nível de Fósforo (mg/kg)
* **pH:** Nível de pH do solo
* **Moisture:** Umidade do solo (%)
* **Crop:** Tipo de cultura (Corn, Soybean, Wheat)
* **Phenological_Stage:** Estágio fenológico da cultura (V6, R1, R6, Flowering, Maturity)

A variável dependente (variável a ser prevista) é:

* **Irrigate:** Variável booleana indicando se a irrigação é necessária (True/False).


## 3. Pré-processamento de Dados

Antes do treinamento, os dados foram pré-processados para garantir a qualidade e a consistência:

* **Normalização:** As features numéricas (K, P, pH, Moisture) foram normalizadas usando `StandardScaler` do Scikit-learn, para que todas as features tenham a mesma escala e evitem que features com valores maiores dominem o modelo.
* **Codificação One-Hot:** As features categóricas (Crop, Phenological_Stage) foram codificadas usando `One-Hot Encoding` para que possam ser utilizadas pelos modelos de Machine Learning.
* **Divisão dos Dados:** Os dados foram divididos em conjuntos de treinamento e teste (80% para treinamento e 20% para teste) usando `train_test_split` do Scikit-learn, garantindo uma avaliação imparcial do desempenho dos modelos.

## 4. Modelos Treinados

Os seguintes modelos de classificação foram treinados e avaliados:

* **Rede Neural Artificial (MLP Classifier):** Modelo de aprendizado profundo.
* **Random Forest:** Modelo baseado em árvores de decisão.
* **Regressão Logística:** Modelo linear para classificação binária.
* **K-Nearest Neighbors (KNN):** Modelo baseado na distância entre os dados.
* **Máquina de Vetores de Suporte (SVM):** Modelo que busca um hiperplano ótimo para separar as classes.
* **Naive Bayes:** Modelo probabilístico baseado no teorema de Bayes.


Para cada modelo, foram calculadas as seguintes métricas de desempenho:

* **Acurácia:** Proporção de predições corretas.
* **Precisão:** Proporção de verdadeiros positivos entre todas as predições positivas.
* **Recall:** Proporção de verdadeiros positivos entre todas as amostras positivas reais.
* **F1-score:** Média harmônica entre precisão e recall.


## 5. Resultados e Avaliação

Os resultados do treinamento e avaliação de cada modelo são apresentados na seção 4 do notebook Jupyter.  A tabela abaixo resume as principais métricas obtidas:

| Modelo                  | Acurácia | Precisão | Recall  | F1-score |
|--------------------------|----------|----------|---------|----------|
| Rede Neural Artificial   | 0.88     | 0.84     | 0.72    | 0.78     |
| Random Forest           | 0.86     | 0.78     | 0.72    | 0.75     |
| Regressão Logística     | 0.78     | 0.68     | 0.45    | 0.54     |
| K-Nearest Neighbors     | 0.86     | 0.86     | 0.62    | 0.72     |
| Support Vector Machine  | 0.77     | 0.65     | 0.45    | 0.53     |
| Naive Bayes             | 0.78     | 0.71     | 0.41    | 0.52     |


Com base nesses resultados, o modelo de **Rede Neural Artificial** apresentou o melhor desempenho global, com maior acurácia e F1-score. No entanto, a escolha do melhor modelo dependerá do contexto e da priorização entre precisão e recall.


## 6. Perspectivas e Próximos Passos

Os modelos treinados serão integrados à aplicação FarmTech Solutions, utilizando a biblioteca `Streamlit` para a criação de um painel interativo para monitoramento e controle do sistema de irrigação. Os resultados da predição serão utilizados para otimizar o processo de irrigação, reduzindo o consumo de água e melhorando a eficiência da produção agrícola.  O código otimizado para o ESP32 será responsável pela coleta de dados e comunicação com o painel Streamlit.


## 7. Salvamento dos Modelos

Os modelos treinados foram salvos utilizando a função `save_trained_model`. Esta função atualmente salva apenas as informações meta (nome, tipo, parâmetros, métricas) dos modelos em um banco de dados (a função `create_ml_model` foi assumida como existente). O próprio modelo treinado é salvo em um arquivo pickle, mas essa funcionalidade está comentada no código.  A recuperação dos modelos para uso subsequente necessita de implementação adicional.

