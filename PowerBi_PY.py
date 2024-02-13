import yfinance as yf
import fundamentus
import pandas as pd

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




#%%