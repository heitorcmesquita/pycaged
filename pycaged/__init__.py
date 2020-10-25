from os import remove
from py7zr import SevenZipFile
import pandas as pd
import wget

def getCagedState(ano, mes, uf):
    
    ''' ano = int; mes = str; uf = int (Código IBGE)
    Retorna um dataframe com um resumo dos microdados do CAGED para o mês e estado selecionados
    
    O README.txt deste pacote mostra um código para uma iteração completa destes dados.
    Acesse em https://github.com/heitorcmesquita/pycaged
    '''
   
    #Dicionário para concatenar url de 2020
    dicmes = {'01':'Janeiro', '02':'Fevereiro','03':'Março', '04':'Abril','05':'Maio', '06':'Junho', '07':'Julho', '08':'Agosto', '09':'Setembro', '10':'Outubro','11':'Novembro', '12':'Dezembro'}
    year = str(ano)
    
    #Baixando dados de classificação de emprego do IBGE
    url2 = 'https://docs.google.com/spreadsheets/d/1SKvOYhjIigkNh8kTvHwmjdGNvO5PHfYI/export?format=csv'
    wget.download(url2, 'cnae.csv')   
    cnae = pd.read_csv('cnae.csv', sep = ',', index_col = None, encoding = 'UTF-8')

    if ano <2020: 
       #Baixando e extraindo microdados
        url = "ftp://ftp.mtps.gov.br/pdet/microdados/CAGED/"+year+"/CAGEDEST_"+mes+year+".7z"
        wget.download(url, 'caged.7z')
        archive = SevenZipFile('caged.7z', mode = 'r')
        archive.extractall()
        print('microdados baixados com sucesso, passando para leitura')
        
        #Lendo o arquivo txt (tem alguns sem '_'). Depois, deletando arquivos
        try:
            data = pd.read_csv('CAGEDEST_'+mes+year+'.txt', sep = ';', encoding = 'iso-8859-1')
        except:
            data = pd.read_csv('CAGEDEST'+mes+year+'.txt', sep = ';', encoding = 'iso-8859-1');
        archive.close()
        remove('caged.7z')
        try:
            remove('CAGEDEST_'+mes+year+'.txt')
        except:            
            remove('CAGEDEST'+mes+year+'.txt')  
        print('microdados lidos, fazendo cálculos')
            
        #Filtrando por UF, unindo dados de classificação do IBGE, preenchendo valores da seçao e tratando dados de salário
        data = data[(data.UF == uf)].reset_index()
        data = pd.merge(data, cnae, left_on = 'CNAE 2.0 Classe', right_on = 'Classe', how = 'left')
        data['Seção'].fillna('NA', inplace = True)
        data['Salário Mensal'] = [d.replace(',','.') for d in data['Salário Mensal']]
        data['Salário Mensal'] = pd.to_numeric(data['Salário Mensal'])
        
        #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
        data['Count'] = ''
        data2 = data.groupby(['Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Count'].count()   
        data = data.groupby(['Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
        data['uf'] = uf
        data['Count'] = '';
        data['mes'] = mes
        
        #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
        for k in range(0,len(data2)):
            data['Count'][k] = data2['Count'][k] 
        
        data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
        print('Os dados do mês' + mes + ' de ' + year + 'foram retornados com sucesso')
        remove('cnae.csv')
        return data
        
    elif ano == 2020:
        #Baixando e extraindo microdados
        url = 'ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/Movimentações/2020/'+dicmes[mes]+'/CAGEDMOV2020'+mes+'.7z'
        try:
            wget.download(url, 'caged.7z')
        except:
            print('Os microdados do mês selecionado ainda não estão disponíveis')   
        archive = SevenZipFile('caged.7z', mode = 'r')
        archive.extractall()
        print('microdados baixados com sucesso, passando para leitura')
        
       #Lendo o arquivo txt e filtrando por UF. Depois, deletando arquivos baixados
        data = pd.read_csv('CAGEDMOV2020'+mes+'.txt', sep = ';', encoding = 'UTF-8')
        data = data[(data.uf == uf)].reset_index()
        archive.close()
        remove('caged.7z')
        remove('CAGEDMOV2020'+mes+'.txt')  
        print('microdados lidos, fazendo cálculos')
            
        #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
        data = data[(data.uf == uf)].reset_index()
        data['região'] = '2020'
        data['Count'] = ''
        data.rename(columns = {"saldomovimentação":"Admitidos/Desligados", "região":"Ano Declarado", "seção":"Seção", 'sexo':'Sexo', 'salário':'Salário Mensal'}, inplace = True) 
        data2 = data.groupby(['Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Count'].count()   
        data = data.groupby(['Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
        data['uf'] = uf
        data['Count'] = ''
        data['mes'] = mes
        
        #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
        for k in range(0,len(data2)):
            data['Count'][k] = data2['Count'][k] 
        
        data['Sexo'] = data['Sexo'].replace(3,2)
        print('Os dados do mês' + mes + ' de ' + year + 'foram retornados com sucesso')
        remove('cnae.csv')
        return data
    
def getCagedMun(ano, mes, uf):
   
    ''' ano = int; mes = str; uf = int (Código IBGE)
    Retorna um dataframe com um resumo dos microdados do CAGED para o mês e estado selecionados
    
    O README.txt deste pacote mostra um código para uma iteração completa destes dados.
    Acesse em https://github.com/heitorcmesquita/pycaged
    '''
    
    #Dicionário para concatenar url de 2020
    dicmes = {'01':'Janeiro', '02':'Fevereiro','03':'Março', '04':'Abril','05':'Maio', '06':'Junho', '07':'Julho', '08':'Agosto', '09':'Setembro', '10':'Outubro','11':'Novembro', '12':'Dezembro'}
    year = str(ano)
    
    #Baixando dados de classificação de emprego do IBGE
    url2 = 'https://docs.google.com/spreadsheets/d/1SKvOYhjIigkNh8kTvHwmjdGNvO5PHfYI/export?format=csv'
    wget.download(url2, 'cnae.csv')   
    cnae = pd.read_csv('cnae.csv', sep = ',', index_col = None, encoding = 'UTF-8')

    if ano <2020: 
       #Baixando e extraindo microdados
        url = "ftp://ftp.mtps.gov.br/pdet/microdados/CAGED/"+year+"/CAGEDEST_"+mes+year+".7z"
        wget.download(url, 'caged.7z')
        archive = SevenZipFile('caged.7z', mode = 'r')
        archive.extractall()
        print('microdados baixados com sucesso, passando para leitura')
        
        #Lendo o arquivo txt (tem alguns sem '_'). Depois, deletando arquivos
        try:
            data = pd.read_csv('CAGEDEST_'+mes+year+'.txt', sep = ';', encoding = 'iso-8859-1')
        except:
            data = pd.read_csv('CAGEDEST'+mes+year+'.txt', sep = ';', encoding = 'iso-8859-1');
        archive.close()
        remove('caged.7z')
        try:
            remove('CAGEDEST_'+mes+year+'.txt')
        except:            
            remove('CAGEDEST'+mes+year+'.txt')  
        print('microdados lidos, fazendo cálculos')
            
        #Filtrando por UF, unindo dados de classificação do IBGE, preenchendo valores da seçao e tratando dados de salário
        data = data[(data.UF == uf)].reset_index()
        data = pd.merge(data, cnae, left_on = 'CNAE 2.0 Classe', right_on = 'Classe', how = 'left')
        data['Seção'].fillna('NA', inplace = True)
        data['Salário Mensal'] = [d.replace(',','.') for d in data['Salário Mensal']]
        data['Salário Mensal'] = pd.to_numeric(data['Salário Mensal'])
        
        #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
        data['Count'] = ''
        data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Count'].count()   
        data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
        data['uf'] = uf
        data['Count'] = ''
        data['mes'] = mes
        
        #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
        for k in range(0,len(data2)):
            data['Count'][k] = data2['Count'][k] 
               
        data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
        print('Os dados do mês' + mes + ' de ' + year + 'foram retornados com sucesso')
        remove('cnae.csv')
        return data
        
    elif ano == 2020:
        #Baixando e extraindo microdados
        url = 'ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/Movimentações/2020/'+dicmes[mes]+'/CAGEDMOV2020'+mes+'.7z'
        try:
            wget.download(url, 'caged.7z')
        except:
            print('Os microdados do mês selecionado ainda não estão disponíveis')   
        archive = SevenZipFile('caged.7z', mode = 'r')
        archive.extractall()
        print('microdados baixados com sucesso, passando para leitura')
        
       #Lendo o arquivo txt e filtrando por UF. Depois, deletando arquivos baixados
        data = pd.read_csv('CAGEDMOV2020'+mes+'.txt', sep = ';', encoding = 'UTF-8')
        data = data[(data.uf == uf)].reset_index()
        archive.close()
        remove('caged.7z')
        remove('CAGEDMOV2020'+mes+'.txt')  
        print('microdados lidos, fazendo cálculos')
            
        #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
        data = data[(data.uf == uf)].reset_index()
        data['região'] = '2020'
        data['Count'] = ''
        data.rename(columns = {"município":"Município", "saldomovimentação":"Admitidos/Desligados", "região":"Ano Declarado", "seção":"Seção", 'sexo':'Sexo', 'salário':'Salário Mensal'}, inplace = True) 
        data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Count'].count()   
        data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
        data['uf'] = uf
        data['Count'] = ''
        data['mes'] = mes
        
        #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
        for k in range(0,len(data2)):
            data['Count'][k] = data2['Count'][k] 
        
        data['Sexo'] = data['Sexo'].replace(3,2) 
        print('Os dados do mês' + mes + ' de ' + year + 'foram retornados com sucesso')
        remove('cnae.csv')
        return data

if __name__ == "__main__":
    main()
    
