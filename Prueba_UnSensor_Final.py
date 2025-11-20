import serial
import csv
from datetime import datetime
import time
import matplotlib.pyplot as plt

# Configuración
PUERTO_SERIAL = 'COM9'       # Cambiar según tu puerto
BAUDRATE = 9600
CSV_FILE = 'Prueba_UnaTermocupla_06sep2025_1234.csv'
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
    writer.writerow(['Timestamp', 'Tiempo (s)', 'Temp1 (°C)'])

# Configurar gráficos
plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Monitoreo de Temperatura - Termocupla')

# Inicializar línea para el gráfico
linea_temp, = ax.plot([], [], 'r-', label='Termocupla 1')

ax.set_ylabel('Temperatura (°C)')
ax.set_xlabel('Tiempo (s)')
ax.legend(loc='upper left')
ax.grid(True)

# Variables para almacenar datos
tiempos = []
temperaturas = []

try:
    inicio = time.time()
    ultimo_guardado = inicio
    
    while True:
        if arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8').strip()
            if linea:
                try:
                    # Formato esperado: solo la temperatura de la termocupla
                    temperatura = float(linea)
                    tiempo_actual = time.time() - inicio
                    
                    # Validar datos
                    if -50 <= temperatura <= 150:
                        
                        # Almacenar datos
                        tiempos.append(tiempo_actual)
                        temperaturas.append(temperatura)
                        
                        # Actualizar gráfico
                        linea_temp.set_xdata(tiempos)
                        linea_temp.set_ydata(temperaturas)
                        
                        ax.relim()
                        ax.autoscale_view()
                        fig.canvas.flush_events()
                        
                        # Guardar en CSV periódicamente
                        if time.time() - ultimo_guardado >= INTERVALO_GUARDADO:
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            with open(CSV_FILE, 'a', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow([timestamp, tiempo_actual, temperatura])
                            ultimo_guardado = time.time()
                            print(f"Datos guardados: {timestamp} - Temp: {temperatura}°C")
                    else:
                        print(f"Temperatura inválida: {temperatura}°C (ignorada)")
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
                writer.writerow([timestamp, t, temperaturas[i]])
    
    arduino.close()
    plt.ioff()
    plt.show()
    print("Datos guardados y puerto cerrado.")
