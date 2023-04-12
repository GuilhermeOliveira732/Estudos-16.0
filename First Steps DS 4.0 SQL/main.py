import pandas as pd
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy
import datetime


# Análise de um banco de dados de informações acerca de acidentes
# e incidentes aéreos divulgado pelo CENIPA, procurando pelos tipos de
# ocorrências mais comuns, modelos mais comuns em acidentes,
# média de acidentes/incidentes por ano, etc
# Inicialmente, fazer tudo com SQL e sem usar Pandas, e, refazer com o Pandas depois
# Comparar aviação geral/aviação comercial
# ver a evolução dos acidentes/incidentes aeronáuticos de cada categoria ao longo dos anos
# ver quais são os modelos com maior proporção de acidente/incidente por unidade existente


# criando a conexão com o banco de dados
conn = sqlite3.connect(r'C:\Users\guiga\Desktop\Pasta\AcidentesBrasil.db')
print('Conexão criada')

# cria o cursor
cursor = conn.cursor()
print('Cursor criado')

# printa na tela os 10 primeiros resultados para a tabela aircrafts
# para aviação geral
acft_geral = cursor.execute('''SELECT field3, field8, field16 FROM aircrafts WHERE field16 != "REGULAR"''')

# calcula valores referentes à aviação geral, bem como o valor total de
# ocorrências na aviação geral
soma_gen = 0
for row in acft_geral:
    soma_gen = soma_gen + 1

# printa na tela os 10 primeiros resultados para a tabela aircrafts
# para aviação regular
acft_regular = cursor.execute('''SELECT field3, field8, field16 FROM aircrafts WHERE field16 = "REGULAR"''')

# calcula os valores referentes à aviação regular, bem como o valor total de
# ocorrências na aviação regular
soma_reg = 0
for row in acft_regular:
    soma_reg = soma_reg + 1

# criando listas para utilizar os dados para a criação do gráfico
# que mostrará a proporção entre ocorrências da aviação regular
# e da aviação geral

keys = [soma_gen, soma_reg]
labels = ['Geral', 'Regular']
for key in keys:
    if key == soma_gen:
        print(key, 'Geral')
    else:
        print(key, 'Regular')
print('*'*100)

# gráfico que mostra a proporção de ocorrências entre a aviação geral e regular
plt.pie(keys, labels=labels, autopct='%1.1f%%')
plt.title('Proporção ocorrências aviação geral vs regular:')
plt.show()

# filtrando as 10 aeronaves mais comuns em ocorrências na aviação geral
# limpando também valores de aeronaves de modelos iguais, como C172L e C172N
modelos_geral = cursor.execute(
    '''SELECT COUNT(field1), CASE 
WHEN field8 LIKE '%210%' THEN 'C210' 
WHEN field8 LIKE '%206%' THEN 'C206' 
WHEN field8 LIKE '%185%' THEN 'C185' 
WHEN field8 LIKE '%182%' THEN 'C182' 
WHEN field8 LIKE '%180%' THEN 'C180' 
WHEN field8 LIKE '%170%' THEN 'C170'
WHEN field8 LIKE '%172%' THEN 'C172' 
WHEN field8 LIKE '%152%' THEN 'C150/152' 
WHEN field8 LIKE '%150%' THEN 'C150/152' 
WHEN field8 LIKE '%140%' THEN 'C140' 
WHEN field8 LIKE '%EMB-810%' THEN 'EMB-810'
WHEN field8 LIKE '%EMB-720%' THEN 'EMB-720'
WHEN field8 LIKE '%EMB-20%' THEN 'EMB-201/202'
WHEN field8 LIKE '%PA-28%' THEN 'PA-28'
WHEN field8 LIKE '%PA-34%' THEN 'PA-34'
WHEN field8 LIKE '%R44%' THEN 'R44' 
WHEN field8 LIKE '%R22%' THEN 'R22' 
WHEN field8 LIKE '%58%' THEN 'B58' 
ELSE field8 END AS modelos_comuns FROM 
aircrafts WHERE field16 !='REGULAR' 
GROUP BY field8 ORDER BY count(field1) DESC LIMIT 14;''')

# cria um dicionário para ser manipulado na sequência
dicionário = {}
for valor, chave in cursor:
    if chave in dicionário:
        dicionário[chave] += valor
    else:
        dicionário[chave] = valor
resultado = [(valor, chave) for chave, valor in dicionário.items()]

# cria listas vazias para armazenar as informações a
# serem exibidas no grãfico
keys = []
values = []
resultado_ordenado = dict(sorted(dicionário.items(), key=lambda x: x[1], reverse=True))

# separa os itens mais comuns e agrupa os menos
# comuns em um item único chamado "OUTROS"
print('10 modelos mais comuns em ocorrências (aviação geral):')
for key, value in resultado_ordenado.items():
    print((value, key))
    keys.append(key)
    values.append(value)
print('*'*100)

# Cria o gráfico de barras
fig, ax = plt.subplots()
ax.bar(keys, values)

# Rotaciona os valores da legenda em 90 graus
plt.xticks(rotation=90)

# nome do gráfico
plt.title('Modelos mais comuns em acidentes/incidentes (aviação geral)')

# exibe o gráfico
plt.show()

# filtrando as 10 aeronaves mais comuns em ocorrências na aviação geral
# limpando também valores de aeronaves de modelos iguais, como C172L e C172N
modelos_regular = cursor.execute(
    '''SELECT COUNT(field1), CASE
WHEN field8 LIKE '%A320-2%' THEN 'A32C'
WHEN field8 LIKE '%A319-1%' THEN 'A32C'
WHEN field8 LIKE '%A330-%' THEN 'A33C'
WHEN field8 LIKE '%ATR-42-%' THEN 'ATR-42'
WHEN field8 LIKE '%ATR-72-%' THEN 'ATR-72'
WHEN field8 LIKE '%727-2%' THEN '727-200'
WHEN field8 LIKE '%737-2%' THEN '737-200'
WHEN field8 LIKE '%737-3%' THEN '737CL'
WHEN field8 LIKE '%737-4%' THEN '737CL'
WHEN field8 LIKE '%737-5%' THEN '737CL'
WHEN field8 LIKE '%737-7%' THEN '737NG'
WHEN field8 LIKE '%737-8%' THEN '737NG'
ELSE field8 END AS modelos_comuns FROM 
aircrafts WHERE field16 ='REGULAR' AND FIELD8 != 'EMB-810D'
GROUP BY field8 ORDER BY count(field1) DESC;''')

# cria um dicionário para ser manipulado na sequência
dicionário = {}
for valor, chave in modelos_regular:
    if chave in dicionário:
        dicionário[chave] += valor
    else:
        dicionário[chave] = valor
resultado = [(valor, chave) for chave, valor in dicionário.items()]

# cria listas vazias para armazenar as informações a
# serem exibidas no grãfico
keys = []
values = []
outrosMod = 0
resultado_ordenado = dict(sorted(dicionário.items(), key=lambda x: x[1], reverse=True))

# separa os itens mais comuns e agrupa os menos
# comuns em um item único chamado "OUTROS"
print('Modelos mais comuns em ocorrências (aviação regular):')
for key, value in resultado_ordenado.items():
    print((value, key))
    keys.append(key)
    values.append(value)
print('*'*100)

# Cria o gráfico de barras
fig, ax = plt.subplots()
ax.bar(keys, values)

# Rotaciona os valores da legenda em 90 graus
plt.xticks(rotation=90)

# nome do gráfico
plt.title('Modelos mais comuns em acidentes/incidentes (aviação geral)')

# exibe o gráfico
plt.show()

# ver as ocorrências mais comuns em cada categoria
# filtra as ocorrências pelo id da ocorrência as quais aconteceram
# com aeronaves operando na aviação regular
pesquisa = cursor.execute('''SELECT field3, field16 FROM aircrafts WHERE field16 = "REGULAR" ORDER BY field1 DESC''')

# na lista ocor_reg, ficam as informações desejadas para a filtragem das
# informações a serem utilizadas no próximo gráfico
ocor_reg = []
for row in pesquisa:
    ocor_reg.append(row)

# mostra os tipos de ocorrências mais comuns na aviação regular
p_regular = cursor.execute('''SELECT COUNT(o.field4), o.field4 
FROM occurrences o
JOIN aircrafts a ON a.field3 = o.field2
WHERE a.field16 = 'REGULAR'
GROUP BY o.field4 ORDER BY COUNT() DESC''')

kOco_reg = []
vOco_reg = []
oOco_reg = 0
print('Tipos de ocorrências mais comuns a aviação regular:')
for key, value in p_regular:
    if key > 3:
        print(key, value)
        kOco_reg.append(key)
        vOco_reg.append(value)
    else:
        oOco_reg = oOco_reg + key
kOco_reg.append(oOco_reg)
vOco_reg.append('Outros')
print(oOco_reg, 'Outros')
print('*'*100)

# gráfico que mostra as modalidades de ocorrências mais comuns
# na aviação regular
plt.pie(kOco_reg, labels=vOco_reg, autopct='%1.1f%%')
plt.title('Tipos de ocorrências mais comuns a aviação regular:')
plt.show()

# mostra os tipos de ocorrências mais comuns na aviação geral
p_geral = cursor.execute('''SELECT COUNT(o.field4), o.field4 
FROM occurrences o
JOIN aircrafts a ON a.field3 = o.field2
WHERE a.field16 != 'REGULAR'
GROUP BY o.field4 ORDER BY COUNT() DESC''')

kOco_gen = []
vOco_gen = []
oOco_gen = 0
print('Tipos de ocorrências mais comuns a aviação geral:')
for key, value in p_geral:
    if key > 25:
        print(key, value)
        kOco_gen.append(key)
        vOco_gen.append(value)
    else:
        oOco_gen = oOco_gen + key
kOco_gen.append(oOco_reg)
vOco_gen.append('Outros')
print(oOco_gen, 'Outros')
print('*'*100)

# gráfico que mostra as modalidades de ocorrências mais comuns
# na aviação geral
plt.pie(kOco_gen, labels=vOco_gen, autopct='%1.1f%%')
plt.title('Tipos de ocorrências mais comuns a aviação geral:')
plt.show()

# buscando dados para a evolução de ocorrências para a aviação regular
# ao longo dos anos
# filtrando os ids de ocorrências na aviação regular
h_regular = cursor.execute('''
SELECT SUBSTR(occurrences.field9, 1, 4) as year, 
COUNT(aircrafts.field3) as num_occurrences
FROM aircrafts
JOIN occurrences ON aircrafts.field3 = occurrences.field2
WHERE aircrafts.field16 = "REGULAR" AND occurrences.field3 = "ACCIDENT"
GROUP BY year
ORDER BY year''')

dados_h_reg = []
for i in h_regular:
    dados_h_reg.append(i)

# Extrai os anos e as contagens em listas separadas
anos_reg = [d[0] for d in dados_h_reg]
contagens_reg = [d[1] for d in dados_h_reg]

# filtrando os ids de ocorrências na aviação geral
h_gen = cursor.execute('''
SELECT SUBSTR(occurrences.field9, 1, 4) as year, 
COUNT(aircrafts.field3) as num_occurrences
FROM aircrafts
JOIN occurrences ON aircrafts.field3 = occurrences.field2
WHERE aircrafts.field16 != "REGULAR" AND occurrences.field3 = "ACCIDENT"
GROUP BY year
ORDER BY year''')

dados_h_gen = []
for i in h_gen:
    dados_h_gen.append(i)

# Extrai os anos e as contagens em listas separadas
anos_gen = [d[0] for d in dados_h_gen]
contagens_gen = [d[1] for d in dados_h_gen]


plt.plot(anos_reg, contagens_reg, color='blue', label="Regular")
plt.plot(anos_gen, contagens_gen, color='red', label="Geral")
plt.xlabel('Ano')
plt.ylabel('Ocorrências')
plt.title('Evolução acidentes/ano aviação regular')
for i in range(len(anos_reg)):
    plt.annotate(contagens_reg[i], (anos_reg[i], contagens_reg[i]))
    plt.annotate(contagens_gen[i], (anos_gen[i], contagens_gen[i]))
plt.legend()
plt.show()