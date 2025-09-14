# Tech Challenge - Fase 4

Neste projeto desenvolvemos um modelo preditivo de redes neurais Long Short Term Memory (LSTM) que faz previsões do fechamamento da ação SAPR4 na bolsa de valores, com base em dados históricos obtidos através do Yahoo Finance. Esse modelo foi implementado em uma API Restful desenvolvida com FastAPI, que recebe uma data e retorna uma previsão do preço da ação.

O projeto inclui:
- Coleta e tratamento de dados históricos da empresa escolhida;
- Construção e treinamento de um modelo LSTM;
- Deploy do modelo por meio de uma API;
- Previsão acessível via requisições HTTP (GET ou POST);
- Possibilidade de consulta futura informando uma data como parâmetro.

Desenvolvido por: Bianca Gobe, Emerson Quirino e Mayara Reghin

Projeto desenvolvido para a pós-graduação em Machine Learning Engineering da FIAP



## 📊 Redes Neurais LSTM

O projeto utiliza redes neurais do tipo Long Short-Term Memory (LSTM), uma variação das redes neurais recorrentes (RNN) especialmente desenvolvida para lidar com dados sequenciais e séries temporais. As LSTMs são capazes de aprender padrões de longo prazo, superando limitações comuns das RNNs tradicionais, tornando-as altamente eficazes na modelagem de comportamentos temporais complexos, como tendências e sazonalidades presentes nos dados do mercado financeiro.

Neste projeto, as LSTMs foram aplicadas para prever o valor de fechamento das ações da Companhia de Saneamento Parana SANEPAR na bolsa de valores, com base no histórico de preços. O modelo foi treinado utilizando dados diários.. 

O código do treinamento do modelo está disponível também no Google Colab: [Colab](https://colab.research.google.com/drive/11CINwt-G1YskeQQOo03HMhs9sbwC_o71?usp=sharing)


## 🛠️ Tecnologias Utilizadas
- 📦 Python 3.11
- 🧠 TensorFlow / Keras – Treinamento do modelo LSTM
- 📊 Pandas, Numpy, Scikit-learn – Manipulação e pré-processamento de dados
- 📈 yfinance – Coleta de dados financeiros da empresa
- 🚀 FastAPI – Criação da API REST
- 🐳 Docker – Containerização da aplicação
- ☁️ AWS EC2 e AWS Cloudwatch - Deploy e monitoramento da aplicação em nuvem




## 🚀 Funcionalidades da API

**Previsão do valor das ações SARP4:** Retorno da previsão de valor das ações SARP4 a partir de uma data

**Autenticação:** As rotas da API são protegidas por autenticação JWT (JSON Web Token), garantindo maior segurança e controle de acesso. Os usuários podem criar suas contas, alterar seus dados, consultar e deletar sua conta. O token é válido por 30 minutos a partir do momento do login e pode ser reiniciado.

**Documentação:** Documentação automática com Swagger

## 📍 Documentação do projeto

Confira todos os detalhes e explicações do projeto na documentação: [Documentação em PDF](https://drive.google.com/file/d/1Q2Z5QjMYYyif0PZ0xNESWkkeaYoXwDWe/view)

Veja também o vídeo apresentando o projeto: [Vídeo](https://drive.google.com/file/d/1ehfGJlS6lXTnKiejsAA7LHs7nY4kxczP/view)

## 🧪 Como Executar o Projeto

0. Pré-requisitos

Instalação do Python 3.11
Instalação do Docker

1. Clone o Repositório
```bash
git clone https://github.com/mayarareghin/tech-challenge-4-previsao-acao-SAPR4.git
```

2. Construa a imagem docker:
```bash
docker build -t api-previsao-acoes .
```

3. Inicialize o banco de dados com o Alembic:
```bash
alembic upgrade head
```

4. Execute o contêiner:
```bash
docker run -d -p 8000:8000 api-previsao-acoes
```

5. Acesse a API no navegador:
```arduino
http://localhost:8000/docs
```

### 🤝 Contribuindo
Fork este repositório.
Crie sua branch (git checkout -b feature/nova-funcionalidade).
Faça commit das suas alterações (git commit -m 'Adiciona nova funcionalidade').
Faça push para sua branch (git push origin feature/nova-funcionalidade).
Abra um Pull Request. instalar, configurar e usar o projeto. Ele também cobre contribuições, contato, licença e agradecimentos, tornando-o completo e fácil de entender para novos desenvolvedores.

