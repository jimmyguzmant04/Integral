import numpy as np
import statistics as stats
from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64

#Jimmy Guzman, 2021-2273
#Brian Peralta, 2021-2214
#Elvis Musseb, 2021- 2048
#Joel Matos, 2021-1050
#Josue Mesa, 2021-1155

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('integral.html')

@app.route('/integral', methods=['POST'])
def calcular():
    datos = []
    for i in range(1, 6):
        valor = int(request.form.get(f'd{i}'))
        datos.append(valor)
    
    n = len(datos)
    total = sum(datos)
    promedio = total / n
    moda = stats.mode(datos)
    q1 = np.percentile(datos, 25)
    q2 = np.percentile(datos, 50)
    q3 = np.percentile(datos, 75)
    RI = q3 - q1
    varianza = np.var(datos)
    Desviacion_estandar = math.sqrt(varianza)
    CV = (Desviacion_estandar / promedio) * 100
    
    # Media armonica
    Media_armonica = stats.harmonic_mean(datos)
    # Media geometrica
    Media_Geometica = stats.geometric_mean(datos)
    
    unique_values, counts = np.unique(datos, return_counts=True)
    total_count = len(datos)
    relative_frequencies = counts / total_count
    
    frequency_table = np.array([unique_values, counts, relative_frequencies]).T
    
    # Convertir frequency_table a una lista de Python
    frequency_list = frequency_table.tolist()
    
    # Extraer valores, frecuencias normales y frecuencias relativas
    values = [int(item[0]) for item in frequency_list]
    frequencies = [int(item[1]) for item in frequency_list]
    relative_frequencies = [item[2] for item in frequency_list]
    
    # Crear el gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(values, frequencies, color='blue')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title('Gráfico de Barras - Tabla de Frecuencia')
    plt.grid(True)
    
    # Guardar el gráfico en un objeto BytesIO y codificarlo en base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return render_template('resultado.html', promedio=promedio, moda=moda, q1=q1, q2=q2, q3=q3, varianza=varianza,
     Desviacion_estandar=Desviacion_estandar,
     CV=CV, frequency_table=frequency_table, plot_data=plot_data, RI=RI
    , Media_armonica= Media_armonica, Media_Geometica=Media_Geometica)

if __name__ == '__main__':
    app.run(debug=True)
