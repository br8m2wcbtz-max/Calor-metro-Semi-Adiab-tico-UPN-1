import serial
import csv
from datetime import datetime
import time
import matplotlib.pyplot as plt

# Configuración
PUERTO_SERIAL = 'COM9'       # Cambiar según tu puerto
BAUDRATE = 9600
CSV_FILE = 'datos_Prueba_30ago2025_1028.csv'
INTERVALO_GUARDADO = 2      # Guardar cada 2 segundos (ajustable)

# Inicializar conexión serial
try:
    arduino = serial.Serial(PUERTO_SERIAL, BAUDRATE, timeout=2)
    print(f"Conexión establecida en {PUERTO_SERIAL}")
except serial.SerialException as e:
    print(f"Error al conectar: {e}")
    exit()

# Configurar CSV
with open(CSV_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Tiempo (s)', 'Temp1 (°C)', 'Temp2 (°C)', 'Humedad (%)', 'Temp_DHT (°C)'])

# Configurar gráficos
plt.ion()
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('Monitoreo de Sensores')

# Inicializar líneas para cada gráfico
lineas = {
    'temp1': axs[0].plot([], [], 'r-', label='Termocupla 1')[0],
    'temp2': axs[0].plot([], [], 'b-', label='Termocupla 2')[0],
    'humedad': axs[1].plot([], [], 'g-', label='Humedad')[0],
    'temp_dht': axs[1].plot([], [], 'm-', label='Temp DHT')[0]
}

axs[0].set_ylabel('Temperatura (°C)')
axs[1].set_ylabel('Humedad (%) / Temp (°C)')
axs[1].set_xlabel('Tiempo (s)')
for ax in axs:
    ax.legend(loc='upper left')
    ax.grid(True)

# Variables para almacenar datos
tiempos = []
datos = {
    'temp1': [], 'temp2': [], 
    'humedad': [], 'temp_dht': []
}

try:
    inicio = time.time()
    ultimo_guardado = inicio
    
    while True:
        if arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8').strip()
            if linea:
                try:
                    # Formato esperado: "temp1, temp2, humedad, temp_dht"
                    valores = [float(x) for x in linea.split(',')]
                    if len(valores) == 4:
                        tiempo_actual = time.time() - inicio
                        temp1, temp2, humedad, temp_dht = valores
                        
                        # Validar datos
                        if all((-50 <= temp1 <= 150, -50 <= temp2 <= 150, 
                               0 <= humedad <= 100, -50 <= temp_dht <= 150)):
                            
                            # Almacenar datos
                            tiempos.append(tiempo_actual)
                            datos['temp1'].append(temp1)
                            datos['temp2'].append(temp2)
                            datos['humedad'].append(humedad)
                            datos['temp_dht'].append(temp_dht)
                            
                            # Actualizar gráficos
                            for key, linea in lineas.items():
                                linea.set_xdata(tiempos)
                                linea.set_ydata(datos[key])
                            
                            axs[0].relim()
                            axs[0].autoscale_view()
                            axs[1].relim()
                            axs[1].autoscale_view()
                            fig.canvas.flush_events()
                            
                            # Guardar en CSV periódicamente
                            if time.time() - ultimo_guardado >= INTERVALO_GUARDADO:
                                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                with open(CSV_FILE, 'a', newline='') as f:
                                    writer = csv.writer(f)
                                    writer.writerow([
                                        timestamp, tiempo_actual, 
                                        temp1, temp2, humedad, temp_dht
                                    ])
                                ultimo_guardado = time.time()
                                print(f"Datos guardados: {timestamp}")
                        else:
                            print(f"Datos inválidos: {valores} (ignorados)")
                    else:
                        print(f"Formato incorrecto: {linea}")
                except ValueError:
                    print(f"Error al decodificar: {linea}")

except KeyboardInterrupt:
    print("\nDeteniendo el monitoreo...")
finally:
    # Guardar datos restantes
    if tiempos:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            for i, t in enumerate(tiempos):
                timestamp = datetime.fromtimestamp(inicio + t).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([
                    timestamp, t, 
                    datos['temp1'][i], datos['temp2'][i],
                    datos['humedad'][i], datos['temp_dht'][i]
                ])
    
    arduino.close()
    plt.ioff()
    plt.show()
    print("Datos guardados y puerto cerrado.")