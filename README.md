
# pycaged

Este é um módulo para extrair relatórios a partir dos microdados do CAGED. Consolidando os dados do CAGED antigo com o novo. (As ressalvas metodológicas do Ministério da Economia devem ser consideradas)

## Instalação

Instale no prompt de comando (Windows) com o comando:

```bash
pip install pycaged
```

## Uso no python

```python
import pycaged

#Ano (int), mes(str), uf(int, código ibge da UF)
pycaged.SubclasseMunicipios(ano, mes, uf)   #<---- Nível mais desagregado

	"Retorna o dataframe com dados CAGED dos municípios da UF selecionada a nível Subclasse de classificação de emprego (CNAE 2.0)"

#Ano (int), mes(str), uf(int, código ibge da UF)
pycaged.ClasseMunicipios(ano, mes, uf)

	"Retorna o dataframe com dados CAGED dos municípios da UF selecionada a nível de Classe de classificação de emprego (CNAE 2.0)"
	
#Ano (int), mes(str), uf(int, código ibge da UF)
pycaged.SecaoMunicipios(ano, mes, uf)    #<----- Nível menos agregado

	"Retorna o dataframe com dados CAGED dos municípios da UF selecionada a nível de Seção de classificação de emprego (CNAE 2.0)"
```
## Contributing
Contribuições serão bem-vindas.

## Licença
[MIT](https://choosealicense.com/licenses/mit/)

## Extraindo bases de dados completas
```
## Extração de dados completos
É possível fazer uma iteração com os dados completos dos municípios de um estado desde 2015:
 ESTE PROCESSO PODE LEVAR ENTRE 40 E 100 MINUTOS
        __________________________________________
 
 ```python
 #Exemplo : Criando uma tabela para uma sequência de anos
CAGEDMun = pd.DataFrame(columns = [], index = None)
mes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
ano = 2015

#Iteração para os anos e meses (usamos Alagoas, 27, como exemplo)
while ano < 2022:
    for i in mes:
        data = pycaged.SecaoMunicipios(ano, i, 27)
    
#Consolidando dados na tabela final
        CAGEDMun = CAGEDMun.append(data, ignore_index = True)
    ano += 1
    
CAGEDMun.to_csv('CAGEDMun.csv', encoding = 'iso-8859-1')
  ```

## Dicionário de Dados:
Admitidos/Desligados: Contratação (1), Demissão(2) 

Sexo: Masculino (1), Feminino (2)

Classificação de Setores CNAE 2.0:
https://docs.google.com/spreadsheets/d/1bMFKpREb4YlW2ZzW1WVLdMN59ol-iLw5/export?format=xlsx

Códigos IBGE por Estado:
 https://www.oobj.com.br/bc/article/quais-os-c%C3%B3digos-de-cada-uf-no-brasil-465.html
