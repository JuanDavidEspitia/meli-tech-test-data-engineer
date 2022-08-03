import pandas as pd
import json
import requests
import numpy as np
from functools import reduce

# leemos cada uno de los set de datos

# Cargamos las variables con las rutas de los archivos locales
pathCompras = "/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto3/datos_compras_v2.csv"
pathCatalogoXML = "/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto3/bookCatalog.xml"
pathOut = "/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto3/output/"

# leemos el archivo  CSV de compras
# Lo cargamos a DF
dfCompras = pd.read_csv(pathCompras)
print("************       Dataset de Compras      ************")
print(dfCompras.value_counts().head(10))
print(dfCompras.info())
print(dfCompras.describe())
print("Cantidad de registros: " + str(len(dfCompras)))

# Leemos el archivo XML
# Debemos instalar el paquete de python lxml comando = pip install lxml
# Uso constantemente el metodo values_counts, por que me permite ver todos los campos de del set de datos
dfCatalogo = pd.read_xml(pathCatalogoXML)
print("************       Dataset de Catalogos      ************")
print(dfCatalogo.value_counts().head(10))
print(dfCatalogo.info())
print(dfCatalogo.describe())
print("Cantidad de registros: " + str(len(dfCatalogo)))
dfCatalogo.to_csv(pathOut + "/Catalogs.csv", index=False, sep ='|')


# leemos ahora la API Rest
# https://restcountries.com/v3.1/all
# https://restcountries.com/v2/all
# https://restcountries.com/#api-endpoints-v3-subregion
res = requests.get("https://restcountries.com/v2/all")
j = res.json()
dfRestCountries = pd.read_json(json.dumps(j))
print("************       Dataset de Paises      ************")
print(dfRestCountries)
print(dfRestCountries.info())
dfRestCountries.to_csv(pathOut + "/Countries.csv", index=False)

# Comenzamos con la transformacion en el dataset de
print("Casteo de Float64 a Int64 y renombrado de campo")
dfCompras['numericCode'] = dfCompras["ccn3(Codigo_pais)"].fillna(0).apply(np.int64)
# Borramos la columna con la siguiente sentencia sin necesidad de reasignarel df
dfCompras.drop('ccn3(Codigo_pais)', axis=1, inplace=True)
print(dfCompras)
print(dfCompras.dtypes)

# Ahora cruzamos la los sets de datos para tener una sabana de datos mas nutrida de informacion
# Usamos la sentencia left para no excluir aquellos registros del set de compras que no tienen codigo de pais
dfMerged = reduce(lambda x,y: pd.merge(x,y, on='numericCode', how='left'), [dfCompras, dfRestCountries])
print(dfMerged)

# Ahora realizamos el renombrado del campo llave en el set de catalogos
print(dfCatalogo.columns)
print("Rename column ID by BOOK_ID")
dfCatalogo.rename(columns={'id': 'book_id'}, inplace=True)
print(dfCatalogo.columns)
print(dfCatalogo.columns)
print(dfCatalogo)

# Luego de tener el dataset podemos cruzar los dos sets de datos resultantes
dfCompraFull = reduce(lambda x,y: pd.merge(x,y, on='book_id', how='left'), [dfMerged, dfCatalogo])
print(dfCompraFull)
print(dfCompraFull.info())


print("*******************************************")
print("********** Preguntas de Negocio ***********")
print("*******************************************")
# Cual es el nombre de de los clientes con las compras mas costosas
dfCompraFull['TotalPrice'] = dfCompraFull.apply(lambda row: (row['price']*row['cuantos_libros']), axis=1)
print(dfCompraFull[['venta_id','alpha3Code', 'first_name','price', 'cuantos_libros', 'TotalPrice']].sort_values(['TotalPrice'], ascending=[False]))
print(dfCompraFull.TotalPrice.max())


# Cual es el pais con mas usuarios que compran libros
print("Top de los paises donde mas libros se vendieron")
print(dfCompraFull.groupby(['name'])['cuantos_libros'].agg('sum').sort_values(ascending=False).reset_index(name='Cantidad'))


# Cual es el libro mas costoso que se vendio en USA
print("El libro mas caro que se vendio en USA fue: ")
dfTest = dfCompraFull[dfCompraFull['alpha3Code'].str.contains('USA', na=False)].sort_values(['price'])
print(dfTest[['title','price']].sort_values(['price'], ascending=[False]))







