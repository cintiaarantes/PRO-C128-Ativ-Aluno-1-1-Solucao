from selenium import webdriver # Módulo de automação de navegadores. Ele pode nos ajudar a abrir um navegador automaticamente
from selenium.webdriver.common.by import By #Usaremos o Selenium abrir uma página web automaticamente e para clicar em um botão.
from bs4 import BeautifulSoup # Módulo famoso para analisar/separar texto como HTML e executar ações nele, como encontrar tags HTML específicas
import requests # Módulo que obtem o código da página
import time # Biblioteca que fará nosso código aguardar por algum tempo para que a página web possa ser carregada corretamente antes de começarmos a coletar os dados.
import pandas as pd # Biblioteca para podermos exportar os dados que coletamos em um arquivo CSV
from selenium import webdriver
import os


# Se trocar o ChromeDriver, atualize o endereço abaixo para o endereço do seu chromedriver do seu PC
# Ela ajudará o pc a achar o chrome driver dentro desta pasta, pois pega o endereço da pasta.
dir = os.getcwd() + '\chromedriver-win64\chromedriver.exe'

#acessando o chrome driver no endereço guardado na variável dir. 
service = webdriver.ChromeService(executable_path=dir)

# Atribuindo o webdriver na variavel driver
driver = webdriver.Chrome(service=service)

# URL dos Exoplanetas da NASA - Link do site que queremos abrir utilizando o webdriver
driver.get('https://exoplanets.nasa.gov/exoplanet-catalog/')

time.sleep(10)

# Lista (vetor) para salvarmos todos os detalhes dos planetas
new_planets_data = []

# Função para extrair dados dos hiperlinks
def scrape_more_data(hyperlink):
    try:
        # Desafio 01: Crie uma variável chamada page e obtenha o conteúdo do hiperlink usando o método get() do módulo requests
        page = requests.get(hyperlink)

        # Desafio 02: Crie um objeto BeautifulSoup chamado soup para obter o código HTML usando page.content do módulo requests e html.parser
        soup = BeautifulSoup(page.content, "html.parser")

        #Desafio 03: Crie uma lista vazia chamada temp1_list para armazenar os dados temporariamente
        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_planets_data.append(temp_list)

    # Desafio 04: Escreva o bloco except para tratar a exceção para iterar e ir para o próximo link
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

csv_file_path = r'C:\aula127_teste\updated_scraped_data.csv'
# Desafio 05: Crie o planet_df_1 para armazenar o arquivo CSV atualizado da forma de um dataframe
planet_df_1 = pd.read_csv(csv_file_path)

# Loop para obter os dados do hiperlink. Método iterrows do pandas, para percorrer as linhas do dataframe e obter o hiperlink
for index, row in planet_df_1.iterrows():
    print(row['hyperlink'])
    scrape_more_data(row['hyperlink']) # Chamada do scrape_more_data e passagem do hiperlink para extrais mais dados
    print(f"Coleta de dados do hiperlink {index+1} concluída")


# Desafio 06: Crie uma nova lista scrapped_data, pois vamos manipula-lá para extração do '\n' (quebra de linha)
scrapped_data = []

for row in new_planets_data:
    replaced = []
    for el in row: 
        el = el.replace("\n", "") #Método replace irá extrair o '\n'
        replaced.append(el)
    scrapped_data.append(replaced)

print(scrapped_data) # A lista scrapped_data não contém nenhum caractere especial


headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]
new_planet_df_1 = pd.DataFrame(scrapped_data, columns = headers)
new_planet_df_1.to_csv('new_scraped_data.csv',index=True, index_label="id")