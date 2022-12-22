
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import pandas as pd

#Essa primeira parte busca em algum lugar do computador um arquivo .csv
# que deve conter na primeira coluna o nome do condondomio ou empreendimento a ser pesquisado
# e na segunda o seu respectivo cnpj

caminho = 'D:/Personal Files/Downloads/Artigos download/listacond (1).csv'
cond = pd.read_csv(caminho)
cond.columns = ["CONDOMINIOS", "CNPJ"]
# print(cond.head())
Lista_Condominios = cond.values.tolist()
print(Lista_Condominios[0][1])
print(type(Lista_Condominios[0][1]))
resultado = []
k = 100

#Criação do objeto options possibilita adicionar algumas opções no selenium
#O argumento "--headless" impede que o chromedriver abra sempre uma nova janela a cada busca
options = Options()
options.add_argument('--headless')

for i in range(0,100):
    k-=1
    print(f'Faltam {k} CNPJ')

    #Acenssando a página de tramitações
    website = 'https://dat.cbm.se.gov.br/Portal/conprojeto'
    path = 'D:/Personal Files/Downloads/chromedriver.exe'
    navegador = webdriver.Chrome(path, options=options)
    navegador.get(website)

    #Seleciona a barra de pesquisa do site, preenche-a com um cnpj e envia.
    BarraPesquisa = navegador.find_element(By.NAME, 'data[Projeto][cnpj]')
    BarraPesquisa.send_keys(Lista_Condominios[i][1])
    BarraPesquisa.submit()

    # A função do try-except aqui é verificar se o cnpj realmente existe na base de dados do CBM
    # Caso não na tabela de saída as informações serão preenchidas com '-'
    try:

        #Busca pelo elemento que acessa os detalhes do processo e click
        a = navegador.find_element(By.XPATH, "//a[@title='Visualizar Processo dessa Edificação']")
        a.click()

        #Transformando a página em um objeto do BeautifulSoup
        PagDetalhes = BeautifulSoup(navegador.page_source, 'html.parser')

        # O BeautifulSoup é utilizado nessa parte do código para de certa forma fracionar o meu elemento html da página
        # E ficar mais fácil encontrar a data em questão
        timeline = PagDetalhes.find('div', attrs={'class': 'timeline-item clearfix'})
        UltimaTramitacao = PagDetalhes.find('h5', attrs={'class': "widget-title smaller"})

        #Criar uma expressão regular de data para ser buscada na fração do html que será transformada em texto
        r = re.compile(r'\d{2}\/\d{2}\/\d{4}')

        if UltimaTramitacao == None:
            results = [Lista_Condominios[i][0], Lista_Condominios[i][1], '-', "Provavelmente Notificado"]
            resultado.append(results)
            pass
        else:
            #Transforma o html em texto e busca a expressão regular
            data = UltimaTramitacao.text
            data_tramitacao = r.findall(data)[0]

            # Buscando a situação
            st = PagDetalhes.find('div', attrs={'class': "timeline-item clearfix"})
            st2 = st.find('div', attrs={'class': "widget-main"})
            situacao = st2.text.strip()
            results = [Lista_Condominios[i][0], Lista_Condominios[i][1], data_tramitacao, situacao]
            resultado.append(results)
        navegador.close()
    except NoSuchElementException:
        results1 = [Lista_Condominios[i][0], Lista_Condominios[i][1], '-', '-']
        resultado.append(results1)
        pass

#Salvando as informações no arquivo .csv
dados = pd.DataFrame(resultado, columns=['Condominio','CNPJ','Data da última tramitação','Situação'])
dados.to_csv('Situação dos condomínios.csv',index=False,encoding='utf-8-sig')