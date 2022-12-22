
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import pandas as pd


caminho = 'D:/Personal Files/Downloads/Artigos download/listacond (1).csv'
cond = pd.read_csv(caminho)
cond.columns = ["CONDOMINIOS", "CNPJ"]
# print(cond.head())
lista = cond.values.tolist()
print(lista[0][1])
print(type(lista[0][1]))
resultado = []
k = 100

options = Options()
options.add_argument('--headless')

for i in range(0,5):
    k-=1
    print(f'Faltam {k} CNPJ')
    #Acenssando a página de tramitações
    website = 'https://dat.cbm.se.gov.br/Portal/conprojeto'
    path = 'D:/Personal Files/Downloads/chromedriver.exe'
    driver = webdriver.Chrome(path, options=options)
    driver.get(website)

    elemento = driver.find_element(By.NAME,'data[Projeto][cnpj]')
    elemento.send_keys(lista[i][1])
    elemento.submit()

    try:
        a = driver.find_element(By.XPATH, "//a[@title='Visualizar Processo dessa Edificação']")
        a.click()

        # Buscando a data da última tramitação
        site = BeautifulSoup(driver.page_source, 'html.parser')
        timeline = site.find('div', attrs={'class': 'timeline-item clearfix'})
        dt = site.find('h5', attrs={'class': "widget-title smaller"})
        r = re.compile(r'\d{2}\/\d{2}\/\d{4}')
        if dt == None:
            results = [lista[i][0],lista[i][1],'-', "Provavelmente Notificado"]
            resultado.append(results)
            pass
        else:
            data = dt.text
            data_tramitacao = r.findall(data)[0]
            # Buscando a situação
            st = site.find('div', attrs={'class': "timeline-item clearfix"})
            situacao = st.text.replace("\n", "")
            # replace(" ", "")
            tratramento = re.sub(r'\s+\s', " ", situacao)
            tratramento1 = re.sub(r'E.+\d{2}\:\d{2}', '', tratramento)

            results = [lista[i][0],lista[i][1],data_tramitacao, tratramento1]
            resultado.append(results)
        driver.close()
    except NoSuchElementException:
        results1 = [lista[i][0],lista[i][1],'-', '-']
        resultado.append(results1)
        pass
print(resultado)
dados = pd.DataFrame(resultado, columns=['Condominio','CNPJ','Data da última tramitação','Situação'])
dados.to_csv('A5.csv',index=False,encoding='utf8')