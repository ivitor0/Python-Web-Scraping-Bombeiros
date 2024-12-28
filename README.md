# Scraping de Situação de Condomínios no Portal CBM-SE

Este projeto utiliza **Selenium** e **BeautifulSoup** para acessar e extrair informações sobre a situação de condomínios a partir do portal [CBM-SE](https://dat.cbm.se.gov.br/Portal/conprojeto). O código realiza buscas automáticas com base em um arquivo CSV contendo os dados de entrada (nome e CNPJ dos condomínios) e salva as informações extraídas em outro arquivo CSV.

## Funcionalidades

- Lê um arquivo CSV com os dados de condomínios e CNPJs.
- Acessa automaticamente o site do CBM-SE para realizar buscas.
- Verifica a situação e a última tramitação de cada condomínio.
- Trata erros de CNPJs inexistentes ou dados ausentes no portal.
- Salva os resultados em um novo arquivo CSV.

## Tecnologias Utilizadas

- **Python 3**
- **Selenium**
- **BeautifulSoup**
- **Pandas**
- **Chromedriver**

## Configuração do Ambiente

1. **Instale as dependências:**
   Certifique-se de ter o Python instalado e execute o comando abaixo para instalar os pacotes necessários:
   ```bash
   pip install selenium beautifulsoup4 pandas
   ```

2. **Baixe o Chromedriver:**
   - Baixe o Chromedriver compatível com a versão do seu Google Chrome em [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
   - Coloque o executável no caminho especificado no código.

3. **Prepare o arquivo CSV de entrada:**
   - O arquivo deve conter duas colunas:
     - **CONDOMINIOS**: Nome do condomínio ou empreendimento.
     - **CNPJ**: CNPJ do condomínio.
   - Salve o arquivo no formato CSV e especifique o caminho correto na variável `caminho` no código.

## Como Executar

1. Certifique-se de que o Chromedriver está configurado corretamente.
2. Altere a variável `caminho` para o caminho completo do arquivo CSV de entrada.
3. Execute o script:
   ```bash
   python nome_do_arquivo.py
   ```
4. O programa irá gerar um arquivo `Situação dos condomínios.csv` com os seguintes dados:
   - Nome do condomínio
   - CNPJ
   - Data da última tramitação
   - Situação

## Estrutura do Código

- **Leitura do CSV:** Carrega os dados de entrada com nomes e CNPJs.
- **Configuração do Selenium:** Configura o navegador em modo headless.
- **Iteração:** Busca cada CNPJ no portal, verifica as informações e trata erros.
- **Salvamento dos Resultados:** Exporta os dados extraídos para um arquivo CSV.

## Observações Importantes

- Certifique-se de que a estrutura do site alvo não mude, pois isso pode quebrar o código.
- Evite consultas em grande volume para não comprometer o desempenho do site ou violar políticas de uso.
- Para executar o script em máquinas sem interface gráfica, o modo **headless** já está ativado no Selenium.

## Exemplo de Saída

A saída gerada pelo programa será um arquivo CSV com o seguinte formato:

| Condominio          | CNPJ            | Data da última tramitação | Situação              |
|---------------------|-----------------|-------------------------|----------------------|
| Condomínio A       | 12.345.678/0001-99 | 01/12/2024             | Em Análise          |
| Condomínio B       | 98.765.432/0001-11 | -                       | Provavelmente Notificado |


