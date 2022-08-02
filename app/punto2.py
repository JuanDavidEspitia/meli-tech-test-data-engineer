import glob
import pandas as pd
import hashlib

# Primero especificamos un patrón de los archivos y lo pasamos como parámetro en la función glob para la ruta
# de datos y datos_complementos
print("Function Read Files in List String")
pathDatos = glob.glob('/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto2/*.csv')
pathComplementos = glob.glob('/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto2/datos_complementos/*.csv')
print("File List Path1: " + str(pathDatos))
print("File List Path2: " + str(pathComplementos))
list_data = []

# Ahora creamos una funcion que se encargue de leer los archivos para cada carpeta
print("Function Load Files")
def readFiles(csv_files):
  #files = glob.glob(ruta)
  list_data = []
  for filename in csv_files:
      data = pd.read_csv(filename)
      list_data.append(data)
  return list_data


# La funcion de readFiles retorna un lista de Dataframes por lo que debemos concatenarlos
# Hacemos uso de la funcion concat para concatenar
print("****** List Dataframes ******")
df1 = readFiles(pathDatos)
print(df1)
print(" Concat List Dataframes in one Dataframes of Data ")
dfDatos = pd.concat(readFiles(pathDatos), axis=0, ignore_index=True)
print(dfDatos)
print(" Concat List Dataframes in one Dataframes of Data Complements")
dfDatosComple = pd.concat(readFiles(pathComplementos), axis=0, ignore_index=True)
print(dfDatosComple)

# Consolidamos los dos dataframes en uno solo
print("Union Datos & Datos_Complement")
dfConsolidate = pd.concat([dfDatos,dfDatosComple])
print(dfConsolidate)

# Eliminimamos los duplicados del dataframe
print("Drop duplicates in Dataframe")
print(dfConsolidate.duplicated())
dfWithoutDuplicates = dfConsolidate.drop_duplicates()
print("Dataframe without duplicates")
print(dfWithoutDuplicates)

# Procedemos a concatenar el tipo y numero de cedula
print("Concat columns tipo_identificacion and numero_identificacion")
dfWithoutDuplicates['tipo_numero_identificacion'] = dfWithoutDuplicates['tipo_identificacion']+''+dfWithoutDuplicates['numero_identificacion'].apply(str)
#dfWithoutDuplicates['TIPO_NUMERO_IDENTIFICACION'] = dfWithoutDuplicates['tipo_identificacion']+dfWithoutDuplicates['numero_identificacion'].astype(str)
print(dfWithoutDuplicates)

# Procedemos a crear el campo hash para la tupla
print("Add column Hash")
dfWithoutDuplicates['hash'] = dfWithoutDuplicates['tipo_numero_identificacion'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
print(dfWithoutDuplicates.info())
print(dfWithoutDuplicates)

# Ahora creamos un dataframe de transacciones
print("Dataframe Transacciones")
dftransacciones = dfWithoutDuplicates.drop(['id','nombre','apellido','email','genero','numero_identificacion','tipo_identificacion','tipo_numero_identificacion'], axis=1)
print(dftransacciones.info())
print(dftransacciones)

# Ahora dejamos el Dataframe de solo clientes
print("Dataframe Clientes")
dfClientes = dfWithoutDuplicates.drop(['valor_tx','numero_identificacion','tipo_identificacion','tipo_numero_identificacion'], axis=1)
print(dfClientes.info())
print(dfClientes)

# Por ultimo mostramos un top 10 de cada uno de los dataframes
print("****** Top 10 ******")
print(dfClientes.value_counts().head(10))
print(dftransacciones.value_counts().head(10))
print("*********   TOP 10 BY TRX  *********")
print(dfClientes[dfClientes.hash.isin(dftransacciones['hash'].head(10))])

print("*********    Punto2 Finished   *********")











