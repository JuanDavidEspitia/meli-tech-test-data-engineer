import pandas as pd
import numpy as np

# Genermos las variables de las rutas de los archivos
pathSalarios = "/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto1/salarios.csv"
pathCompras = "/Users/JuanEspitia/Documents/Github/data-engineer/meli-tech-test-data-engineer/data/punto1/compras.csv"

# Cargamos los dos archivos de datos en DF independientes
dfSalarios = pd.read_csv(pathSalarios)
dfCompras = pd.read_csv(pathCompras)

#dfSalarios = pd.read_csv(r'data/punto1/salarios.csv')
print("****  Dataframe de Salarios ****")
print(dfSalarios)
print("****  Dataframe de Compras ****")
print(dfCompras)

print("Cantidad de Registros set de Salarios: " + str(len(dfSalarios)))
print("Cantidad de Registros set de Compras: "  + str(len(dfCompras)))

# De acuerdo al set de datos SALARIOS ¿Cuántos cargos estaban ocupados solamente por una persona en 2011?
print("**************    Punto 1   **************")
print("Filtramos el set de Salarios por el año 2011")
dfFilterYear = dfSalarios[dfSalarios.Year == 2011]
print(len("Cantidad de Salarios en el 2011: " + str(len(dfFilterYear))))
# Agrupamos el DF de Cargos ocupados por una sola persona
dfCargoByPerson = dfFilterYear.groupby(['JobTitle', 'Id']).size().sort_values(ascending=False).reset_index(name='Cantidad')
print(dfCargoByPerson)
#Ahora Filtramos los que solo hayan sido ocupados por una sola persona
dfOnlyPerson = dfCargoByPerson[dfCargoByPerson.Cantidad == 1]
print("Cantidad de Cargos que son ocupados por una sola persona: "+ str(len(dfOnlyPerson)))



print("**************    Punto 2   **************")
#De acuerdo al set de datos SALARIOS ¿Cuánta gente tiene la palabra 'MANAGER' en su cargo?
print("Filtramos por el campo JobTitle todos aquellos que contengan la palabra manager")
dfManagers = dfSalarios.JobTitle.str.contains('MANAGER')
print(dfManagers)
print("Cantidad de personas cuyo cargo contiene MANAGER: " + str(sum(dfManagers)))



print("**************    Punto 3   **************")
# De acuerdo al set de datos SALARIOS ¿Cuál es el nombre de la persona que menos gana (incluyendo beneficios - TotalPayBenefits)?
print("Comparamos el menor salario de la columna TotalPayBenefits y lo comparamos con la persona que tiene el menor valor")
dfMinSalary = dfSalarios[dfSalarios.TotalPayBenefits==dfSalarios.TotalPayBenefits.min()]
print("La persona con el menor salario es: 1")
print(dfMinSalary)



print("**************    Punto 4   **************")
# De acuerdo al set de datos SALARIOS¿Cuál es el salario base (BasePay) promedio de todos los empleados para el año (2012)?
print("Filtramos el DF de Salarios por el año 2012 y luego con el campo BasePay sacamos el promedio de salarios")
meanSalary = dfSalarios[dfSalarios.Year==2012].BasePay.mean()
print("El Salario base promedio es de: " + str(meanSalary))



print("**************    Punto 5   **************")
# De acuerdo al set de datos SALARIOS ¿Cuál fue la suma total pagada con beneficios por los dos trabajos más populares?.
print("Hacemos uso del metodo value_conts() para obtener el numero de ocurrencias de cada uno y asi obtener el mas popular")
dfMorePopulars = dfSalarios.JobTitle.value_counts().head(2)
print(dfMorePopulars)
# Posteriormente usamos la sentecia para sumar el total de benefios pagados de ambos trabajos
print(sum(dfSalarios[dfSalarios.JobTitle.isin(dfSalarios.JobTitle.value_counts().head(2).index)].TotalPayBenefits))



print("**************    Punto 6   **************")
# De acuerdo al set de datos COMPRAS ¿Cuáles son los 5 proveedores de correo electrónico más comunes,
# con cuantos usuarios está asociado cada uno? (hotmail.com,gmai.com, etc)
print("Hacemos un split en el campo de correo separado por el @ para separar el dominio")
print("Posteriormente contamos las ocurrencias de cada dominio y listamos los 5 primeros")
dominiosEmail = dfCompras.Email.str.split("@", expand=True)[1].value_counts().head(5)
print(dominiosEmail)



print("**************    Punto 7   **************")
# De acuerdo al set de datos COMPRAS ¿Cuántas personas tienen una tarjeta de crédito que expira en 2025?
print("Con el Campo CC Exp Date lo usamos para validar si contine la cadena /25, que indica que vence en el 2025")
#dfExpDate = dfCompras['CC Exp Date'].str.contains("/25")
dfExpDate = dfCompras[dfCompras['CC Exp Date'].str.contains("/25")]
print(dfExpDate)
print("La cantidad de personas que vencen la tarjeta de credito en 2025 son: " + str(len(dfExpDate)))





print("**************    Punto 8   **************")
# De acuerdo al set de datos COMPRAS ¿Cuántas personas tienen tarjetas Mastercard e hicieron una compra por más de $20?
print("Realizamos dos filtros")
print("1. Donde el CC Provider sea Mastercard")
print("2. Donde el precio de las compras sea superior a 20")
dfMaster = dfCompras[(dfCompras['CC Provider'] == 'Mastercard') & (dfCompras['Purchase Price'] > 20)]
print("Cantidad de personas con Mastercard y compra superior a los 20$: " + str(len(dfMaster)))




print("**************    Punto 9   **************")
# De acuerdo al set de datos COMPRAS ¿Alguien hizo una compra desde Lot: "90 WT", ¿cuál fue el precio de compra de esta transacción?
print("Filtramos en el campo Lot el valor 90 WT y mostramos solamente el precio")
dfLot90 = dfCompras[dfCompras['Lot']=='90 WT']['Purchase Price'].reset_index(name='Precio')
print(dfLot90)




print("**************    Punto 10   **************")
# De acuerdo al set de datos COMPRAS ¿ Cuánto suma el total de precio de compras para las dos compañías menos populares?, ¿Cuáles son esas dos compañías?
print("Filtramos las dos compañias con mayor ocurrencia en el set de datos")
print("Luego sumamos el campo Purchase Price ")
print("Total de precio de las dos compañias mas populares: " + str(sum(dfCompras[dfCompras.Company.isin(dfCompras.Company.value_counts().tail(2).index)]['Purchase Price'])))

print("Las compañias son: ")
print(dfCompras.Company.value_counts().tail(2))
