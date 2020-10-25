#pycaged
Este modulo permite a extração de dataframes a partir dos microdados do CAGED. Ele conta com duas funções básicas:

getCagedState(ano, mes, uf):

	Retorna o seguinte dataframe:
		'Admitidos/Desligados' (classificação da operação)
		'Ano Declarado' (ano do relatório)
		'Seção' (seção da economia do emprego gerado/eliminado)
		'Sexo' (sexo do empregado)
		'Salário Mensal' (salário médio para aquele empregado(a), naquele setor da economia, naquele mês)
		'uf' (estado selecionado)
		'Count' (contagem de empregos gerados/eliminados)

getCagedMun(ano, mes, uf):

	Retorna o seguinte dataframe:
		'Município' (município da uf selecionada)
		'Admitidos/Desligados' (classificação da operação)
		'Ano Declarado' (ano do relatório)
		'Seção' (seção da economia do emprego gerado/eliminado)
		'Sexo' (sexo do empregado)
		'Salário Mensal' (salário médio para aquele empregado(a), naquele setor da economia, naquele mês)
		'uf' (estado selecionado)
		'Count' (contagem de empregos gerados/eliminados)


 Para fazer uma iteração com os dados completos dos municípios de um estado, desde 2015 (no exemplo, Alagoas (27)):
 ESTE PROCESSO PODE LEVAR ENTRE 40 E 100 MINUTOS
        __________________________________________
 #Criando a tabela final
CAGEDMun = pd.DataFrame(columns = [], index = None)
mes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
ano = 2015

#Iteração para os anos e meses
while ano < 2021:
    for i in mes:
        data = getCagedMun(ano, i, 27)
    
#Consolidando dados na tabela final
        CAGEDMun = CAGEDMun.append(data, ignore_index = True)
    ano += 1
    
CAGEDMun.to_csv('CAGEDMun.csv', encoding = 'iso-8859-1')
        _______________________________________________


Dicionário de Dados:

Admitidos : 1 / Desligados: 2
Sexo: Masculino (1), Feminino (2)

Códigos IBGE por Estado: 
https://www.oobj.com.br/bc/article/quais-os-c%C3%B3digos-de-cada-uf-no-brasil-465.html
Tabela com seções da economia do IBGE: 
https://docs.google.com/spreadsheets/d/1SKvOYhjIigkNh8kTvHwmjdGNvO5PHfYI/export?format=csv
    
