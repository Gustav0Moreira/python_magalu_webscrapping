#WebScrapping de Produtos e Preços nas Lojas Magazine Luize
#Utilização do Selenium, para WebDriver, e Openpyxl, para extrair os dados e formatalos em xlsx
#Os comentários neste código tem como intuito auxiliar quem ler e também,_ 
#_tentar, repassar algum conhecimento quanto aos módulos e lógica utilizada
#Projeto criado por Gustavo Moreira



from selenium import webdriver #WebDriver
from webdriver_manager.chrome import ChromeDriverManager #Gerenciador de Versionamento do Navegador e seus serviços 
from selenium.webdriver.chrome.service import Service #Gerenciador de Versionamento do Navegador, mas do Selenium
from selenium.webdriver.common.by import By #Direcionador de elementos
from collections import defaultdict
from decimal import Decimal


def get_info_site(k_w):
    """
        Esta Função recebe uma palavra-chave e a utiliza dentro 
        de um requesição web para buscar por produtos no site
        Magazine Luiza e retorna um dicionário com informações
        dos produtos.
    """


    servico = Service(ChromeDriverManager().install()) #Ativação do gerenciador
    navegador = webdriver.Chrome(service=servico) #Ativação do Navegador Automatizado, e definição de qual navegador será utilizado para o webscrapping
    url = navegador.get(f'https://www.magazineluiza.com.br/busca/{k_w}') #Direcionamento web do WebDriver

    #------Variavéis------
    produto_titulo = "//h2[@data-testid='product-title']"
    produto_preco = "//p[@data-testid='price-value']"
    produto_url = "//a[@data-testid='product-card-container']"
    dic_de_produtos = defaultdict(dict)
    dic_produtos_result = defaultdict(dict)


    #------Extração_dos_dados-------
    titulos = navegador.find_elements(By.XPATH, produto_titulo) #Extrair o objeto dos elementos
    titulos = [x.text.lower() for x in titulos] #formata os objetos dos elementos como texto e atribui como uma lista

    precos = navegador.find_elements(By.XPATH, produto_preco) #Extrai o texto com o valor dos produtos
    precos = [x.text.replace(',', '.') for x in precos] #Altera a formtação do valor do produto, pois python não aceita "," em numéricos

    urls = navegador.find_elements(By.XPATH, produto_url) #extrai o link dos produtos
    urls = [x.get_attribute('href') for x in urls]

    for titulo, preco, link in zip(titulos, precos, urls): #Cria um loop onde irá iterar sobres os text dos elementos. Zip é utilizado para garantir a atribuição em grupo
        dic_de_produtos[(titulo)][("Valor")] = float(preco.split()[1][:3]) #split é acionado devido ao valor dos precos ser recebido como R$ 00.00, o R$ é separado de 00.00, e apenas utilizado o numeros
        dic_de_produtos[(titulo)][("URL")] = link
    
    for i, x in enumerate(dic_de_produtos.items()):
        dic_produtos_result[(i)]= x

    dict(dic_produtos_result)
    for x in dic_produtos_result.items():
        print(x)
    # for x, y in dic_de_produtos.items():
    #     print(f"\n{x}\nR$ {y}\n")


     #----debug dos items do dict----
    # for i, o in dic_de_produtos.items():
    #     print(f'Produto: {i[:40] if len(i) > 30 else i[:]}... \t Valor: R$ {o:.2f}')
    # print(f'A média de preço de produtos de {palavra_chave} é: R$ {sum(dic_de_produtos.values()) / len(dic_de_produtos.values()):.2f}')
    #-------------------------------
    
    return dic_produtos_result

   


while True:
    palavra_chave = input("Digite o que gostaria de pesquisar: ")

    produto_dict = get_info_site(palavra_chave)


