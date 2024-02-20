import yfinance as yf
import fundamentus
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Definindo a carteira de ações
carteira_yf = ['ABEV3.SA', 'B3SA3.SA', 'ELET3.SA', 'GGBR4.SA', 'ITSA4.SA',
            'PETR4.SA', 'RENT3.SA', 'SUZB3.SA', 'VALE3.SA', 'WEGE3.SA']

df = yf.download(carteira_yf, start="2022-08-01", end="2023-08-01")
df.head(3)

cotacoes = df.stack(level = 1)
cotacoes

## Resetando os índices e recomendando a coluna dos ativos
cotacoes = cotacoes.reset_index().rename(columns = {"Ticker": "Ativo"})

# Verificando se a coluna "Ativo" foi renomeada corretamente
print(cotacoes.columns)

## Organizando do df
cotacoes = cotacoes[["Date", "Open", "High", "Low", "Close", "Ativo"]]
cotacoes.head(10)

cotacoes.info()


####
# # Código completo para introduzir ao PowerBi sobre a obtenção dos dados históricos das cotações da carteira de 01/08/2022 à 01/08/2023
# Importando a biblioteca
# import yfinance as yf

# # Definindo a carteira de ações
# carteira_yf = ['ABEV3.SA', 'B3SA3.SA', 'ELET3.SA', 'GGBR4.SA', 'ITSA4.SA',
#                'PETR4.SA', 'RENT3.SA', 'SUZB3.SA', 'VALE3.SA', 'WEGE3.SA']

# #  Carregando os dados da carteira
#  df = yf.download(carteira_yf, start="2022-08-01", end="2023-08-01")

# #  Passando os ativos para o multindex do df
#  cotacoes = df.stack(level=1)

# # Resetando os índices e renomenado a coluna dos ativos
#  cotacoes = cotacoes.reset_index().rename(columns={"Ticker": "Ativo"})

# # Organizando o df
# cotacoes = cotacoes[["Date", "Open", "High", "Low", "Close", "Ativo"]]

# del carteira_yf, df
####

# lendo um papel específico
weg = fundamentus.get_papel("WEGE3")
weg

carteira_fund = ["ABEV3", "B3SA3", "ELET3", "GGBR4", "ITSA4",
                "PETR4", "RENT3", "SUZB3", "VALE3", "WEGE3"]

# Lendo um papel específico
ABEV3 = fundamentus.get_papel("ABEV3")
B3SA3 = fundamentus.get_papel("B3SA3")
ELET3 = fundamentus.get_papel("ELET3")
GGBR4 = fundamentus.get_papel("GGBR4")
ITSA4 = fundamentus.get_papel("ITSA4")
PETR4 = fundamentus.get_papel("PETR4")
RENT3 = fundamentus.get_papel("RENT3")
SUZB3 = fundamentus.get_papel("SUZB3")
VALE3 = fundamentus.get_papel("VALE3")
WEGE3 = fundamentus.get_papel("WEGE3")

# Criando um dicionário para armazenar as informações de cada papel
ind = pd.concat([ABEV3, B3SA3, ELET3, GGBR4, ITSA4, PETR4, RENT3, SUZB3, VALE3, WEGE3])[['Setor', 'Cotacao', 'Min_52_sem', 'Max_52_sem', 'Valor_de_mercado',
                                            'Nro_Acoes', 'Patrim_Liq','Receita_Liquida_12m','Receita_Liquida_3m',
                                            'Lucro_Liquido_12m', 'Lucro_Liquido_3m']]
ind.head(3)

ind.info()

# Passando o ticker para uma coluna
ind = ind.reset_index()
ind.rename(columns={"index":"Ativo"}, inplace=True)

# Alterando colunas object para numeric
colunas = ['Cotacao', 'Min_52_sem', 'Max_52_sem', 'Valor_de_mercado', 'Nro_Acoes', 'Patrim_Liq',
        'Receita_Liquida_12m', 'Receita_Liquida_3m', 'Lucro_Liquido_12m', 'Lucro_Liquido_3m']
ind[colunas] = ind[colunas].apply(pd.to_numeric, errors='coerce', axis=1)

ind.head()

ind_2 = fundamentus.get_detalhes_raw().reset_index()
ind_2 = ind_2.query("papel in @carteira_fund")

ind_2 = ind_2[['papel','P/L', 'Div.Yield','P/VP','ROE']].reset_index(drop=True)

ind_2.rename(columns={'papel': 'Ativo','Div.Yield':'DY'}, inplace= True)
ind_2.head()


# o código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script:

# dataset = pandas.DataFrame(Date, Open, High, Low, Close)
# dataset = dataset.drop_duplicates()

# Configurações iniciais de fonte
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams["font.sans-serif"] = 'Verdana'

def candlestick(date, open, high, low, close):
    fig, ax = plt.subplots(figsize=(30,11), dpi=72, facecolor='#edf3ee')
    ax.set_facecolor("#edf3ee")

    # Definindo as cores de cada candle
    cores = ["green" if close > open else "red" for close, open in zip(close, open)]

    # Candlestick corpo + pavio
    sns.barplot(x=date, y=np.abs(open-close), bottom=np.min((open,close), axis=0), width=0.8, palette=cores, ax = ax)
    sns.barplot(x=date, y=high-low, bottom=low, width=0.1, palette=cores, ax = ax)

    ## código omitido

    ## Personalizando o gráfico
    # Ajustando os ticks dos eixos x ey 
    plt.setp(ax, xticks = ax.get_xticks(), yticks = ax.get_yticks(),
            xticklabels = [date[i].strftime('%b %Y') for i in ax.get_xticks()],
            yticklabels= [f'R$ {valor:.2f}' for valor in ax.get_yticks()])
    
    ## trecho de código omitido

    # Ajustando tamanhos dos labels, retirando títulos e bordas
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params (axis='both', labelsize=32)
    ax.xaxis.set_major_locator (mticker. MaxLocator (4))
    sns.despine()
    plt.grid(alpha=0.2)

    #Ajustando o limite de y para um respiro 
    plt.ylim(ax.get_ylim()[0]-0.5, ax.get_ylim()[1] +0.5)
    
    #Ajustando o limite de y para um respiro 
    plt.ylim(ax.get_ylim()[0]-0.5, ax.get_ylim()[1] +0.5)

# os dataset são expecíficos para o PowerBi 

dataset["Date"] = pd.to_datetime(dataset["Date"], format="%Y-%m-%dT%H:%M:%S")

candlestick(dataset["Date"], dataset["Open"], dataset["High"], dataset["Low"], dataset["Close"])

plt.subplots_adjust(left=0.07, bottom=0.05, right=0.95, top=0.95)
plt.show()

#%%