print('Importando Bibliotecas...')
#Importando Bibliotecas
import pandas as pd
import plotly.express as plot
import plotly
import pickle
import os
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3

print('Baixando dados...')
#Baixando dados e criando DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/sp.csv', sep=';') 
df2 = pd.read_csv('https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv', sep=';')
print('Preprocessando...')
#removendo possíveis valores NaN
df2 = df2.dropna() 
df = df.dropna() 

#sumarizando informações úteis
df_sumario = f'O DataFrame possui: {df.shape[0]} linhas e {df.shape[1]} colunas, das quais recebem os rótulos de: \n {list(df.columns)}' 
df2_sumario = f'O DataFrame possui: {df2.shape[0]} linhas e {df2.shape[1]} colunas, das quais recebem os rótulos de: \n {list(df2.columns)}' 
dfG = df2.groupby(['datahora']).sum() #agrupando por datahora e somando valores de outras colunas.
dfMed = df2.groupby(['semana_epidem']).mean() #agrupando por datahora e fazendo a média de valores de outras colunas

#reunindo informações gerais
visGeral1 = f'''__Informações gerais do cenário atual da pandemia de COVID 19 : __\n\tTOTAL DE CASOS ACUMULADOS : {int(df.iloc[[-1]]['casos_acum'].values)} pessoas infectadas \n\tTOTAL DE ÓBITOS ACUMULADOS : {int(df.iloc[[-1]]['obitos_acum'].values)} vidas perdidas \n\tDATA DO ÚLTIMO REPORT : {df.iloc[[-1]]['datahora'].values}'''
data = {'totalCasos_acum' : int(df.iloc[[-1]]['casos_acum'].values),
        'totalObt_acum' : int(df.iloc[[-1]]['obitos_acum'].values),
        'ultimoReport' : df.iloc[[-1]]['datahora'].values} #salvando dados caso seja necessáiro
print(f'Gerando gráficos referentes à seguinte situação : \n {visGeral1}')
#Montando alguns plots
casos_acum = plot.line(df,x='datahora',y='casos_acum') #série temporal de acumulo de casos
obiotos_acum = plot.line(df,x='datahora',y='obitos_acum') #série temporal de acumulo de obitos
nov_casos = plot.line(dfG,y='casos_novos') #Novos Casos em Série Temporal
nov_obitos = plot.line(dfG,y='obitos_novos') #Novos óbitos em Série Temporal
medM_casos = plot.line(dfMed,y='casos_novos') #Média Móvel de novos casos por semana epidemológica
medM_obitos = plot.line(dfMed,y='obitos_novos') #Média móvel de novos óbitos por semana epidemológica

graphs = [casos_acum,obiotos_acum,nov_casos,nov_obitos,medM_casos,medM_obitos]

paths = []
for i in range(len(graphs)):
    saver = plotly.io.write_image(graphs[i], f'{os.path.abspath(os.curdir)}/graphs{[i]}.jpg', format='jpg')
    paths.append(f'{os.path.abspath(os.curdir)}\graphs{[i]}.jpg')

print('Criando PDF...')
time.sleep(3)
cnv=canvas.Canvas(f'{os.path.abspath(os.curdir)}/report.pdf',pagesize=A3)
for i in range(len(paths)):
    cnv.drawImage(paths[i],20,586.7729)
    cnv.showPage()
    
cnv.save()
