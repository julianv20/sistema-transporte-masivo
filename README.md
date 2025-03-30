# Sistema Inteligente de Rutas para Transporte Masivo

Este proyecto implementa un sistema inteligente basado en conocimiento que utiliza estrategias de búsqueda heurística y representación de conocimiento mediante reglas lógicas para encontrar la ruta óptima entre dos puntos en un sistema de transporte masivo.

## Características

- Implementación del algoritmo A\* para búsqueda de rutas óptimas
- Representación del conocimiento mediante grafos
- Consideración de tiempos de viaje y transbordos entre líneas
- Visualización gráfica de la red de transporte y las rutas encontradas
- Extensible para diferentes sistemas de transporte

## Requisitos

- Python 3.8 o superior
- Bibliotecas: networkx, matplotlib

## Instalación

1. Clonar el repositorio:

```bash
https://github.com/julianv20/sistema-transporte-masivo.git
cd sistema-transporte-masivo
```

2. Crear un entorno virtual (opcional pero recomendado):

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install networkx matplotlib
```

## Uso

Ejecutar el programa principal:

```bash
python sistema_transporte.py
```

### Personalización

Para adaptar el sistema a un transporte masivo diferente, modifica la función `crear_sistema_ejemplo()` en el archivo `sistema_transporte.py`:

```python
# Ejemplo de personalización
def crear_sistema_mi_ciudad():
    sistema = SistemaTransporte()

    # Agregar estaciones con sus coordenadas
    sistema.agregar_estacion("Estación A", x, y)
    sistema.agregar_estacion("Estación B", x, y)
    # ...

    # Agregar conexiones con tiempos y líneas
    sistema.agregar_conexion("Estación A", "Estación B", tiempo, "Línea 1")
    # ...

    return sistema
```

Modifica también la función `main()` para usar tu sistema personalizado:

```python
def main():
    sistema = crear_sistema_mi_ciudad()
    # ...
    origen = "Estación A"
    destino = "Estación Z"
    # ...
```

## Estructura del Proyecto

- `sistema_transporte.py`: Archivo principal con la implementación del sistema
- `red_transporte.png`: Visualización de la red completa (generada al ejecutar)
- `ruta_optima.png`: Visualización de la ruta encontrada (generada al ejecutar)
- `docs/`: Documentación adicional y pruebas realizadas

## Fundamentos Teóricos

Este proyecto se basa en los siguientes conceptos de inteligencia artificial:

1. **Sistemas Basados en Conocimiento**: La red de transporte se modela como una base de conocimiento que contiene información sobre estaciones, conexiones, tiempos y líneas.

2. **Algoritmos de Búsqueda Heurística**: Se utiliza el algoritmo A\* para encontrar la ruta más eficiente, combinando:

   - Costo acumulado del camino recorrido
   - Heurística estimada (distancia euclidiana al destino)

3. **Representación del Conocimiento**: El sistema utiliza grafos para representar la red de transporte y reglas lógicas para determinar los mejores caminos.

## Autores

- Julian Vanegas

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
