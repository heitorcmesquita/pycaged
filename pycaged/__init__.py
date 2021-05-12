from os import remove
from py7zr import SevenZipFile
import pandas as pd
import wget

#Extraindo dados mensais que serão utilizados
class caged:
    
    def __init__(self, ano, mes):
        self.year = str(ano)
        #Baixando dados de classificação de emprego do IBGE e criando dicionário de meses
        url = 'https://docs.google.com/spreadsheets/d/1Wm4MN_ARuGnMpIsbQY6Nm5tO4shGzQVM/export?format=xlsx'
        wget.download(url, 'cnae.xlsx')   
        cnae = pd.read_excel('cnae.xlsx', index_col = None)
        dicmes = {'01':'Janeiro', '02':'Fevereiro','03':'Março', '04':'Abril','05':'Maio', '06':'Junho', '07':'Julho', '08':'Agosto', '09':'Setembro', '10':'Outubro','11':'Novembro', '12':'Dezembro'}
        self.cnae = cnae
        self.dicmes = dicmes
        self.ano = ano
        self.mes = mes
        remove('cnae.xlsx')
        del url      
            
    def getDataMunicipios(self):
        
        if self.ano <2020: 
           #Baixando e extraindo microdados
            url = "ftp://ftp.mtps.gov.br/pdet/microdados/CAGED/"+self.year+"/CAGEDEST_"+self.mes+self.year+".7z"
            wget.download(url, 'caged.7z')
            archive = SevenZipFile('caged.7z', mode = 'r')
            archive.extractall()
            print('microdados baixados com sucesso, passando para leitura')
            
            #Lendo o arquivo txt (tem alguns sem '_')
            data = pd.DataFrame()
            try:
                for chunk in pd.read_csv('CAGEDEST_'+self.mes+self.year+'.txt', sep = ';', encoding = 'iso-8859-1', chunksize = 100000):
                    chunk = chunk[(chunk.UF == self.uf)].reset_index()
                    chunk['Salário Mensal'] = [d.replace(',','.') for d in chunk['Salário Mensal']]
                    chunk['Salário Mensal'] = pd.to_numeric(chunk['Salário Mensal'])
                    data = data.append(chunk)
            except:
                for chunk in pd.read_csv('CAGEDEST'+self.mes+self.year+'.txt', sep = ';', encoding = 'iso-8859-1', chunksize = 100000):
                    chunk = chunk[(chunk.UF == self.uf)].reset_index()
                    chunk['Salário Mensal'] = [d.replace(',','.') for d in chunk['Salário Mensal']]
                    chunk['Salário Mensal'] = pd.to_numeric(chunk['Salário Mensal'])
                    data = data.append(chunk)
            self.data = data
            
            #Excluindo os arquivos que já não serão usados
            archive.close()
            remove('caged.7z')
            try:
                remove('CAGEDEST_'+self.mes+self.year+'.txt')
            except:            
                remove('CAGEDEST'+self.mes+self.year+'.txt')
            del url
            print('microdados lidos, fazendo cálculos')
            
        elif self.ano >= 2020:
        
            #Baixando e extraindo microdados
            url = 'ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/Movimentações/'+ self.year+ '/' + self.dicmes[self.mes]+'/CAGEDMOV2020'+self.mes+'.7z'
            try:
                wget.download(url, 'caged.7z')
            except:
                print('Os microdados do mês selecionado ainda não estão disponíveis')   
            archive = SevenZipFile('caged.7z', mode = 'r')
            archive.extractall()
            print('microdados baixados com sucesso, passando para leitura')
            
           #Lendo o arquivo txt e filtrando por UF
            data = pd.DataFrame()
            for chunk in pd.read_csv('CAGEDMOV2020'+self.mes+'.txt', sep = ';', encoding = 'UTF-8', chunksize = 100000):
                chunk = chunk[(chunk.uf == self.uf)].reset_index()
                data = data.append(chunk)
            self.data = data
            print('microdados lidos, fazendo cálculos')
            
            #Excluindo os arquivos que já não serão usados
            archive.close()
            remove('caged.7z')
            remove('CAGEDMOV2020'+self.mes+'.txt')  
            del url

    def getMSubclasse(self, uf):
        self.uf = uf
        caged.getDataMunicipios(self)
        data = self.data
        
        if self.ano < 2020:
            #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
            data['Count'] = ''
            data3 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'CNAE 2.0 Subclas', 'Sexo'], as_index = False)['Salário Mensal'].median()
            data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'CNAE 2.0 Subclas', 'Sexo'], as_index = False)['Count'].count()   
            data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'CNAE 2.0 Subclas', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
            data['uf'] = self.uf
            data['Count'] = ''
            data['Salário Mensal Mediano'] = ''
            data['mes'] = self.mes
            
            #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
            for k in range(0,len(data2)):
                data['Count'][k] = data2['Count'][k] 
            for k in range(0,len(data3)):
                data['Salário Mensal Mediano'][k] = data3['Salário Mensal'][k] 
                   
            data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
            data['Salário Mensal'].fillna(0, inplace = True)
            data['Salário Mensal'] = data['Salário Mensal'].astype(int)
            data['Salário Mensal Mediano'].fillna(0, inplace = True)
            data['Salário Mensal Mediano'] = data['Salário Mensal Mediano'].astype(int)
            print('Os dados do mês ' + self.mes + ' de ' + self.year + ' foram retornados com sucesso')
            return data
        
        if self.ano >= 2020:
            #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
            data['região'] = self.year
            data['Count'] = ''
            data.rename(columns = {"município":"Município", "saldomovimentação":"Admitidos/Desligados", "região":"Ano Declarado", "subclasse":"CNAE 2.0 Subclas", 'sexo':'Sexo', 'salário':'Salário Mensal'}, inplace = True) 
            data3 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'CNAE 2.0 Subclas', 'Sexo'], as_index = False)['Salário Mensal'].median()
            data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'CNAE 2.0 Subclas', 'Sexo'], as_index = False)['Count'].count()   
            data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'CNAE 2.0 Subclas', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
            data['uf'] = self.uf
            data['Count'] = ''
            data['Salário Mensal Mediano'] = ''
            data['mes'] = self.mes
            
            #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
            for k in range(0,len(data2)):
                data['Count'][k] = data2['Count'][k] 
            for k in range(0,len(data3)):
                data['Salário Mensal Mediano'][k] = data3['Salário Mensal'][k] 
                   
            data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
            data['Sexo'] = data['Sexo'].replace(3,2)        
            data['Salário Mensal'].fillna(0, inplace = True)
            data['Salário Mensal'] = data['Salário Mensal'].astype(int)
            data['Salário Mensal Mediano'].fillna(0, inplace = True)
            data['Salário Mensal Mediano'] = data['Salário Mensal Mediano'].astype(int)
            print('Os dados do mês ' + self.mes + ' de ' + self.year + ' foram retornados com sucesso')
            return data
      
    def getMClasse(self, uf):
        self.uf = uf
        caged.getDataMunicipios(self)
        data = self.data
        
        if self.ano < 2020:
            #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
            data = pd.merge(data, self.cnae, left_on = 'CNAE 2.0 Subclas', right_on = 'Subclasse', how = 'left')            
            data['Count'] = ''
            data3 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Classe', 'Sexo'], as_index = False)['Salário Mensal'].median()
            data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Classe', 'Sexo'], as_index = False)['Count'].count()   
            data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Classe', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
            data['uf'] = self.uf
            data['Count'] = ''
            data['Salário Mensal Mediano'] = ''
            data['mes'] = self.mes
            
            #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
            for k in range(0,len(data2)):
                data['Count'][k] = data2['Count'][k] 
            for k in range(0,len(data3)):
                data['Salário Mensal Mediano'][k] = data3['Salário Mensal'][k] 
                   
            data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
            data['Salário Mensal'].fillna(0, inplace = True)
            data['Salário Mensal'] = data['Salário Mensal'].astype(int)
            data['Salário Mensal Mediano'].fillna(0, inplace = True)
            data['Salário Mensal Mediano'] = data['Salário Mensal Mediano'].astype(int)
            print('Os dados do mês ' + self.mes + ' de ' + self.year + ' foram retornados com sucesso')
            return data
        
        if self.ano >= 2020:
            #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
            data = pd.merge(data, self.cnae, left_on = 'subclasse', right_on = 'Subclasse', how = 'left')            
            data['região'] = self.year
            data['Count'] = ''
            data.rename(columns = {"município":"Município", "saldomovimentação":"Admitidos/Desligados", "região":"Ano Declarado", "subclasse":"CNAE 2.0 Subclas", 'sexo':'Sexo', 'salário':'Salário Mensal'}, inplace = True) 
            data3 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Classe', 'Sexo'], as_index = False)['Salário Mensal'].median()
            data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Classe', 'Sexo'], as_index = False)['Count'].count()   
            data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Classe', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
            data['uf'] = self.uf
            data['Count'] = ''
            data['Salário Mensal Mediano'] = ''
            data['mes'] = self.mes
            
            #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
            for k in range(0,len(data2)):
                data['Count'][k] = data2['Count'][k] 
            for k in range(0,len(data3)):
                data['Salário Mensal Mediano'][k] = data3['Salário Mensal'][k] 
                   
            data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
            data['Sexo'] = data['Sexo'].replace(3,2)        
            data['Salário Mensal'].fillna(0, inplace = True)
            data['Salário Mensal'] = data['Salário Mensal'].astype(int)
            data['Salário Mensal Mediano'].fillna(0, inplace = True)
            data['Salário Mensal Mediano'] = data['Salário Mensal Mediano'].astype(int)
            print('Os dados do mês ' + self.mes + ' de ' + self.year + ' foram retornados com sucesso')
            return data        

    def getMSecao(self, uf):
        self.uf = uf
        caged.getDataMunicipios(self)
        data = self.data
        
        if self.ano < 2020:
            #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
            data = pd.merge(data, self.cnae, left_on = 'CNAE 2.0 Subclas', right_on = 'Subclasse', how = 'left')            
            data['Count'] = ''
            data3 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].median()
            data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Count'].count()   
            data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
            data['uf'] = self.uf
            data['Count'] = ''
            data['Salário Mensal Mediano'] = ''
            data['mes'] = self.mes
            
            #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
            for k in range(0,len(data2)):
                data['Count'][k] = data2['Count'][k] 
            for k in range(0,len(data3)):
                data['Salário Mensal Mediano'][k] = data3['Salário Mensal'][k] 
                   
            data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
            data['Salário Mensal'].fillna(0, inplace = True)
            data['Salário Mensal'] = data['Salário Mensal'].astype(int)
            data['Salário Mensal Mediano'].fillna(0, inplace = True)
            data['Salário Mensal Mediano'] = data['Salário Mensal Mediano'].astype(int)
            print('Os dados do mês ' + self.mes + ' de ' + self.year + ' foram retornados com sucesso')
            return data
        
        if self.ano >= 2020:
            #Contando número de contratações e demissões em um DF separado. Fazendo a média salárial do agrupamento 
            data['região'] = self.year
            data['Count'] = ''
            data.rename(columns = {"município":"Município", "saldomovimentação":"Admitidos/Desligados", "região":"Ano Declarado", "seção":"Seção", 'sexo':'Sexo', 'salário':'Salário Mensal'}, inplace = True) 
            data3 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].median()
            data2 = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Count'].count()   
            data = data.groupby(['Município', 'Admitidos/Desligados', 'Ano Declarado', 'Seção', 'Sexo'], as_index = False)['Salário Mensal'].mean()           
            data['uf'] = self.uf
            data['Count'] = ''
            data['Salário Mensal Mediano'] = ''
            data['mes'] = self.mes
            
            #Trazendo dados de quantidade de contratações e demissões, e retornando DF    
            for k in range(0,len(data2)):
                data['Count'][k] = data2['Count'][k] 
            for k in range(0,len(data3)):
                data['Salário Mensal Mediano'][k] = data3['Salário Mensal'][k] 
                   
            data['Admitidos/Desligados'] = data['Admitidos/Desligados'].replace(2,-1)
            data['Sexo'] = data['Sexo'].replace(3,2)        
            data['Salário Mensal'].fillna(0, inplace = True)
            data['Salário Mensal'] = data['Salário Mensal'].astype(int)
            data['Salário Mensal Mediano'].fillna(0, inplace = True)
            data['Salário Mensal Mediano'] = data['Salário Mensal Mediano'].astype(int)
            print('Os dados do mês ' + self.mes + ' de ' + self.year + ' foram retornados com sucesso')
            return data            


def SubclasseMunicipios(ano, mes, uf):
    data = caged(ano, mes)
    data = data.getMSubclasse(uf)
    return data
    
def ClasseMunicipios(ano, mes, uf):
    data = caged(ano, mes)
    data = data.getMClasse(uf)
    return data    

def SecaoMunicipios(ano, mes, uf):
    data = caged(ano, mes)
    data = data.getMSecao(uf)
    return data          

