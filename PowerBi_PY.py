# O código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script:

# dataset = pandas.DataFrame(Date, Open, High, Low, Close)
# dataset = dataset.drop_duplicates()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Configurações iniciais de fonte
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams["font.sans-serif"] = 'Verdana'

def candlestick(date, open, high, low, close):
    fig, ax = plt.subplots(figsize=(30,11), dpi=72, facecolor='#edf3ee')
    ax.set_facecolor("#edf3ee")

    # Definindo as cores de cada candle
    cores = ["#5B855C" if close > open else "#DA1E37" for close, open in zip(close, open)]

    # Candlestick corpo + pavio
    sns.barplot(x=date, y=np.abs(open-close), bottom=np.min((open,close), axis=0), width=0.8, palette=cores, ax = ax)
    sns.barplot(x=date, y=high-low, bottom=low, width=0.1, palette=cores, ax = ax)

    # Média móvel de 7 e 30 períodos
    mav_7 = close.rolling(7).mean()
    mav_30 = close.rolling(30).mean()
    sns.lineplot(x=ax.get_xticks(), y=mav_7, label = "MAV 7", color = "#E76F51", linewidth = 4, ax = ax)
    sns.lineplot(x=ax.get_xticks(), y=mav_30, label = "MAV 30", color = "#023E8A", linewidth = 4, ax = ax)

    # Min e Max Global
    for i in range(0, len(date)):
      if low[i] == np.min(low):
        ax.annotate('Mínimo', xy = (ax.get_xticks()[i], low[i]), xytext=(15, -15), fontsize=26,
                    textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
      if high[i] == np.max(high):
        ax.annotate('Máximo', xy = (ax.get_xticks()[i], high[i]), xytext=(15, 15), fontsize=26,
                    textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))

    # Valor Atual
    ax.axhline(y = close[len(close)-1], color = "grey", linestyle='--') # Não conseguimos ler o último valor com -1

    ## Personalizando o gráfico
    # Ajustando os ticks dos eixos x e y
    plt.setp(ax, xticks = ax.get_xticks(), yticks = ax.get_yticks(),
             xticklabels = [date[i].strftime('%b %Y') for i in ax.get_xticks()],
             yticklabels= [f'R$ {valor:.2f}' for valor in ax.get_yticks()])

    # Ajustando tamanhos dos labels, retirando títulos e bordas
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='both', labelsize=32)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(4))
    sns.despine()
    plt.legend(fontsize=28, facecolor="#EDF3EE", edgecolor="#EDF3EE")
    plt.grid(alpha=0.2)

    # Ajustando o limite de y para um respiro
    plt.ylim(ax.get_ylim()[0]-0.5, ax.get_ylim()[1]+0.5)

dataset["Date"] = pd.to_datetime(dataset["Date"], format="%Y-%m-%dT%H:%M:%S")

candlestick( dataset["Date"], dataset["Open"], dataset["High"], dataset["Low"], dataset["Close"])

plt.subplots_adjust(left=0.07, bottom=0.05, right=0.95, top=0.95)
plt.show()