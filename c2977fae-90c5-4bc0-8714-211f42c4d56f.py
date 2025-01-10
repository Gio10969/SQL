# # Proyecto 

# ## Introcucción .

# Descripción del proyecto
# Estás trabajando como analista para Zuber, una nueva empresa de viajes compartidos que se está lanzando en Chicago. Tu tarea es encontrar patrones en la información disponible. Quieres comprender las preferencias de los pasajeros y el impacto de los factores externos en los viajes.
# 
# Al trabajar con una base de datos, analizarás los datos de los competidores y probarás una hipótesis sobre el impacto del clima en la frecuencia de los viajes.

# ## Descripción de los datos
# Una base de datos con información sobre viajes en taxi en Chicago:
# 
# -**tabla neighborhoods**: datos sobre los barrios de la ciudad
# 
# -**name**: nombre del barrio.
# 
# -**neighborhood_id**: código del barrio.
# 
# -**tabla cabs**: datos sobre los taxis.
# 
# 
# -**cab_id**: código del vehículo.
# 
# -**vehicle_id**: ID técnico del vehículo.
# 
# -**company_name**: la empresa propietaria del vehículo.
# 
# -**tabla trips**: datos sobre los viajes.
# 
# 
# -**trip_id**: código del viaje.
# 
# -**cab_id**: código del vehículo que opera el viaje.
# 
# -**start_ts**: fecha y hora del inicio del viaje (tiempo redondeado a la hora).
# 
# -**end_ts**: fecha y hora de finalización del viaje (tiempo redondeado a la hora).
# 
# -**duration_seconds**: duración del viaje en segundos.
# 
# -**distance_miles**: distancia del viaje en millas.
# 
# -**pickup_location_id**: código del barrio de recogida.
# 
# -**dropoff_location_id**: código del barrio de finalización.
# 
# -**tabla weather_records**: datos sobre el clima.
# 
# 
# -**record_id**: código del registro meteorológico.
# 
# -**ts**: fecha y hora del registro (tiempo redondeado a la hora).
# 
# -**temperature**: temperatura cuando se tomó el registro.
# 
# -**description**: breve descripción de las condiciones meteorológicas, por ejemplo, "lluvia ligera" o "nubes dispersas".

# ![image.png](attachment:image.png)

# # Explorar datos

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, levene 


# In[2]:


df_trips = pd.read_csv('/datasets/project_sql_result_01.csv')
df_dropoff = pd.read_csv('/datasets/project_sql_result_04.csv')
df = pd.read_csv('/datasets/project_sql_result_07.csv')


# In[3]:


print("Datos del primer archivo:")
print(df_trips.head())
print(df_trips.info())


# In[4]:


print("\nDatos del segundo archivo:")
print(df_dropoff.head())
print(df_dropoff.info())


# In[5]:


df_trips['trips_amount'] = pd.to_numeric(df_trips['trips_amount'], errors='coerce')
df_dropoff['average_trips'] = pd.to_numeric(df_dropoff['average_trips'], errors='coerce')

top_10_dropoff = df_dropoff.sort_values(by='average_trips', ascending=False).head(10)
print("\nLos 10 principales barrios en términos de finalización del recorrido:")
print(top_10_dropoff)


# Para los datos proporcionados se muestran los valores de las empresas con mayor cantidad de viajes realizados, liderando "Flash Cab" que consta con casi 20000 viajes realizados (empresas de taxis), filtraremos las que mas viajes realizan para determinar un filtro de ellas en futuros datos, además se observan los valores de las 10 principales locaciones de "terminos de recorrido de estos viajes" todos teniendo en punto de inicio el aeropuerto.

# ## Graficas

# In[6]:


# Filtrar los datos para incluir solo empresas de taxis con más de 2500 viajes
df_filtered = df_trips[df_trips['trips_amount'] > 2500]

# Gráfico: Empresas de taxis y número de viajes (filtrado)
plt.figure(figsize=(12, 6))
plt.bar(df_filtered['company_name'], df_filtered['trips_amount'])
plt.xlabel('Empresa de Taxis')
plt.ylabel('Número de Viajes')
plt.title('Número de Viajes por Empresa de Taxis (Filtrado)')
plt.xticks(rotation=45, ha='right')
plt.show()


# En esta grafica se puede observar las empresas de taxis que mas viajes realizaron desde el aeropuerto, filtradas a las que obtienen mas de 2500 viajes con "Flash Cab" como la lider teniendo 19000 viajes aproximadamente, y "Nova Taxi Afiliation Llc" con la minima con poco mas de 2500 viajes.

# In[7]:


# Gráfico: Los 10 principales barrios por número de finalizaciones
plt.figure(figsize=(10, 6))
plt.bar(top_10_dropoff['dropoff_location_name'], top_10_dropoff['average_trips'])
plt.xlabel('Barrio de Finalización del Viaje')
plt.ylabel('Promedio de Viajes')
plt.title('Los 10 Principales Barrios por Número de Finalizaciones de Viaje')
plt.xticks(rotation=45, ha='right')
plt.show()


# Este grafico muestra las 10 locaciones que se utilizaron como destino desde el aeropuerto, con "Loop" con mas de 10000 viajes realizados hacia allí y a "Sheffield & DePaul" con poco mas de 1200 destinos finalizados. 


# ## Prueba de hipotesis.

# In[8]:


# Filtrar los datos para obtener los viajes los sábados
df['start_ts'] = pd.to_datetime(df['start_ts']) # Convertir start_ts a tipo datetime
df['day_of_week'] = df['start_ts'].dt.dayofweek # Obtener el día de la semana (0: Lunes, 6: Domingo)
saturdays = df[df['day_of_week'] == 5] # Filtrar para obtener solo los sábados


# Utilizaremos un test de hipótesis de dos muestras para determinar si hay una diferencia significativa en las duraciones de los viajes entre los sábados lluviosos y no lluviosos basándonos en el valor p obtenido del test de hipótesis, decidiremos si rechazamos o no la hipótesis nula.

# In[9]:


saturdays_rainy = saturdays[saturdays['weather_conditions'] == 'Bad']
saturdays_not_rainy = saturdays[saturdays['weather_conditions'] == 'Good']
t_statistic, p_value = ttest_ind(saturdays_rainy['duration_seconds'], saturdays_not_rainy['duration_seconds'])

alfa = 0.05

print("Resultado del test de hipótesis:")
print("Valor p:", p_value)
if p_value < alfa:
    print("La duración promedio de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare es significativamente diferente los sábados lluviosos en comparación con los sábados no lluviosos.")
else:
    print("No hay suficiente evidencia para rechazar la hipótesis nula.")


# In[10]:


statistic, p_value_levene = levene(saturdays_rainy['duration_seconds'], saturdays_not_rainy['duration_seconds'])
print("Resultado del test de Levene:")
print("Valor p:", p_value_levene)
if p_value_levene < alfa:
    print("Las varianzas de los dos grupos son significativamente diferentes.")
else:
    print("No hay suficiente evidencia para rechazar la igualdad de varianzas.")


# El resultado del test de Levene muestra un valor p de 0.5332, lo que indica que no hay suficiente evidencia para rechazar la igualdad de varianzas entre los dos grupos. Esto significa que podemos asumir que las varianzas de las duraciones de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare son similares entre los sábados lluviosos y no lluviosos.
# 
# Con esta información, podemos proceder con el test t de Student estándar para comparar las medias de los dos grupos y determinar si hay una diferencia significativa en la duración promedio de los viajes entre los sábados lluviosos y no lluviosos.

# ## Conclusión.

# El primer resultado del test de hipótesis muestra un valor p muy pequeño (6.52e-12), lo que indica que hay una diferencia significativa en la duración promedio de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare entre los sábados lluviosos y no lluviosos. Con un nivel de significancia de 0.05, rechazamos la hipótesis nula y concluimos que la duración promedio de los viajes es significativamente diferente en los sábados lluviosos en comparación con los sábados no lluviosos.
# 
# Para el segundo resultado del test de Levene muestra un valor p de 0.5332, lo que indica que no hay suficiente evidencia para rechazar la igualdad de varianzas entre los dos grupos. Esto significa que podemos asumir que las varianzas de las duraciones de los viajes desde el Loop hasta el Aeropuerto Internacional O'Hare son similares entre los sábados lluviosos y no lluviosos.
# 
# Con esta información, podemos proceder con el test t de Student estándar para comparar las medias de los dos grupos y determinar si hay una diferencia significativa en la duración promedio de los viajes entre los sábados lluviosos y no lluviosos.

