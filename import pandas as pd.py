import pandas as pd
from matplotlib import pyplot as plt

#df = pd.read_csv('/datasets/height_weight.csv')

comp_name_trips_amount =  pd.read_csv('/datasets/project_sql_result_01.csv')
print(comp_name_trips_amount.head(15))
print()
print(comp_name_trips_amount.info())
print()
sum_trips_amount = comp_name_trips_amount['trips_amount'].sum()
print('Numero Total de Viajes: ', sum_trips_amount)

dropoff_loc_avg_trips =  pd.read_csv('/datasets/project_sql_result_04.csv')
print(dropoff_loc_avg_trips)
print()
print(dropoff_loc_avg_trips.info())
print()
print(dropoff_loc_avg_trips.sample(10))
print()

# Identicamos si hay casos perdidos en comp_name_trips_amount

comp_name_trips_amount[comp_name_trips_amount['trips_amount'].isna()]
comp_name_trips_amount[comp_name_trips_amount['company_name'].isna()]

dropoff_loc_avg_trips[dropoff_loc_avg_trips['dropoff_location_name'].isna()]
dropoff_loc_avg_trips[dropoff_loc_avg_trips['average_trips'].isna()]

#  verificar si contamos con registros duplicados

comp_name_trips_amount.duplicated().sum()

dropoff_loc_avg_trips.duplicated().sum()

# Hacer gráficos: empresas de taxis y número de viajes con comp_name_trips_amount

from matplotlib import pyplot as plt

# Crear gráfico de barras

comp_name_trips_amount.plot(
    x = 'company_name',
    y = 'trips_amount',
    kind = 'bar',
    title='Number of trips per company',
    xlabel='Company Name',
    ylabel='Trips Amount',
    figsize=(15, 6)
)
plt.show()

top_10_dropoff_loc_avg_trips = dropoff_loc_avg_trips.sort_values(by='average_trips', ascending=False).head(10)

print(top_10_dropoff_loc_avg_trips)

# Graficamos los 10 barrios principales por número de finalizaciones con df dropoff_loc_avg_trips

top_10_dropoff_loc_avg_trips.plot(
    x = 'dropoff_location_name',
    y = 'average_trips',
    kind = 'bar',
    title='Main 10 drop off neighborhoods',
    xlabel='Dropoff Location Name',
    ylabel='Average Trips',
    figsize=(15, 6)
)
plt.show()

# Revisión de data frame

trip_info_loop_ohare =  pd.read_csv('/datasets/project_sql_result_07.csv')
print(trip_info_loop_ohare.info())
print()
print(trip_info_loop_ohare.sample(5))

# Convertir 'start_ts'a formato datetime

trip_info_loop_ohare['start_ts'] = pd.to_datetime(trip_info_loop_ohare['start_ts'])
print(trip_info_loop_ohare.info())

# Buscaremos probar la hipótesis alternativa de que "La duración promedio de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare cambia los sábados lluviosos".

from scipy import stats as st
import numpy as np
import pandas as pd

# Extraer los sábados de la columna 'start_ts'

start_ts_sabados = trip_info_loop_ohare[trip_info_loop_ohare['start_ts'].dt.dayofweek == 5]
print(start_ts_sabados.info())

# Sacamos el promedio de la columna 'duration_seconds'

avg_duration_seconds = start_ts_sabados['duration_seconds'].mean()
print(avg_duration_seconds)

# Sacamos el promedio de la columna 'duration_seconds' cuando las condiciones son buenas y malas

avg_duration_good_weather_sabados = start_ts_sabados[start_ts_sabados['weather_conditions'] == 'Good']['duration_seconds'].mean()
print('Duración promedio con condiciones buenas', avg_duration_good_weather_sabados)

avg_duration_bad_weather_sabados = start_ts_sabados[start_ts_sabados['weather_conditions'] == 'Bad']['duration_seconds'].mean()
print('Duración promedio con condiciones malas', avg_duration_bad_weather_sabados)

# Creamos una variable para cuando cuando 'weather_conditions' es buena y otra cuando es mala

good_weather_sabados = start_ts_sabados[start_ts_sabados['weather_conditions'] == 'Good']
bad_weather_sabados = start_ts_sabados[start_ts_sabados['weather_conditions'] == 'Bad']

#Hipótesis sobre la igualdad de las medias de muestras emparejadas

good_weather_sabados_sample = good_weather_sabados.sample(n=100)
bad_weather_sabados_sample = bad_weather_sabados.sample(n=100)

# Hacemos una prueba de Levene para mostrar si las varianzas son iguales.
# Calcular las varianzas para cada uno de los días (lluvioso y no lluvioso).

alpha = 0.05
prueba_levene, valor_p = st.levene(good_weather_sabados_sample['duration_seconds'], bad_weather_sabados_sample['duration_seconds'])
print("prueba levene:", prueba_levene)
print("valor_p:", valor_p)
if valor_p < alpha:
  print("Rechazar la hipótesis nula, las varianzas no son iguales")
else:
  print("No rechazar la hipótesis nula, las varianzas son iguales")

  prueba_t, valor_p = st.ttest_rel(good_weather_sabados_sample['duration_seconds'], bad_weather_sabados_sample['duration_seconds'])
alpha = 0.05
print("prueba t:", prueba_t)
print("valor_p:", valor_p)
if valor_p < alpha:
  print("Rechazar la hipótesis nula")
else:
  print("No rechazar la hipótesis nula")