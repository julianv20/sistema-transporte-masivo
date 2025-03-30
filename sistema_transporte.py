import heapq
import matplotlib.pyplot as plt
import networkx as nx


class SistemaTransporte:
    def __init__(self):
        # Base de conocimiento: representación del sistema de transporte
        # Formato: {estacion: {estacion_vecina: (tiempo, linea)}}
        self.red_transporte = {}

        # Coordenadas de las estaciones para visualización
        self.coordenadas = {}

        # Líneas de transporte (para visualización)
        self.lineas = {}

    def agregar_estacion(self, nombre, x, y):
        """Agrega una estación al sistema con sus coordenadas"""
        if nombre not in self.red_transporte:
            self.red_transporte[nombre] = {}
            self.coordenadas[nombre] = (x, y)

    def agregar_conexion(self, origen, destino, tiempo, linea):
        """Agrega una conexión entre dos estaciones con su tiempo y línea"""
        # Asegurarse de que ambas estaciones existan
        if origen not in self.red_transporte or destino not in self.red_transporte:
            raise ValueError("Las estaciones deben existir antes de conectarlas")

        # Agregar conexión (ambas direcciones para que sea bidireccional)
        self.red_transporte[origen][destino] = (tiempo, linea)
        self.red_transporte[destino][origen] = (tiempo, linea)

        # Registrar la línea
        if linea not in self.lineas:
            self.lineas[linea] = set()
        self.lineas[linea].add((origen, destino))
        self.lineas[linea].add((destino, origen))

    def distancia_euclidiana(self, estacion1, estacion2):
        """Calcula la distancia euclidiana entre dos estaciones (heurística)"""
        x1, y1 = self.coordenadas[estacion1]
        x2, y2 = self.coordenadas[estacion2]
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def encontrar_mejor_ruta(self, origen, destino):
        """Encuentra la mejor ruta entre origen y destino usando A*"""
        if origen not in self.red_transporte or destino not in self.red_transporte:
            return None, None

        # Cola de prioridad para A*: (prioridad, tiempo_actual, estacion, ruta, lineas_usadas)
        cola = [(0, 0, origen, [origen], [])]
        heapq.heapify(cola)

        # Conjunto de estaciones visitadas
        visitadas = set()

        while cola:
            # Obtener el nodo con menor prioridad (f = g + h)
            _, tiempo_actual, estacion_actual, ruta, lineas = heapq.heappop(cola)

            # Si llegamos al destino, retornamos la ruta y el tiempo
            if estacion_actual == destino:
                return ruta, tiempo_actual, lineas

            # Si ya visitamos esta estación, continuamos
            if estacion_actual in visitadas:
                continue

            # Marcar como visitada
            visitadas.add(estacion_actual)

            # Explorar vecinos
            for vecino, (tiempo, linea) in self.red_transporte[estacion_actual].items():
                if vecino not in visitadas:
                    # Calcular nuevo tiempo considerando transferencias
                    nuevo_tiempo = tiempo_actual + tiempo

                    # Penalización por cambio de línea (5 minutos)
                    if lineas and lineas[-1] != linea:
                        nuevo_tiempo += 5

                    # Actualizar ruta y líneas
                    nueva_ruta = ruta + [vecino]
                    nuevas_lineas = lineas + [linea]

                    # Calcular heurística (distancia directa al destino)
                    h = self.distancia_euclidiana(vecino, destino)

                    # Prioridad = tiempo actual + heurística
                    prioridad = nuevo_tiempo + h

                    # Agregar a la cola
                    heapq.heappush(
                        cola,
                        (prioridad, nuevo_tiempo, vecino, nueva_ruta, nuevas_lineas),
                    )

        # Si no hay ruta
        return None, None, None

    def visualizar_red(self):
        """Visualiza la red de transporte"""
        G = nx.Graph()

        # Agregar nodos
        for estacion, (x, y) in self.coordenadas.items():
            G.add_node(estacion, pos=(x, y))

        # Colores para las líneas
        colores = {
            "Línea A": "red",
            "Línea B": "blue",
            "Línea C": "green",
            "Línea D": "orange",
        }

        # Crear figura
        plt.figure(figsize=(12, 8))
        pos = nx.get_node_attributes(G, "pos")

        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightgray")
        nx.draw_networkx_labels(G, pos)

        # Dibujar aristas por línea
        for linea, conexiones in self.lineas.items():
            edges = list(conexiones)
            color = colores.get(linea, "black")
            nx.draw_networkx_edges(
                G, pos, edgelist=edges, width=2, edge_color=color, label=linea
            )

        plt.legend()
        plt.axis("off")
        plt.title("Red de Transporte Masivo")
        plt.tight_layout()
        plt.savefig("red_transporte.png")
        plt.close()

    def visualizar_ruta(self, ruta, lineas):
        """Visualiza una ruta específica en la red"""
        if not ruta or len(ruta) < 2:
            return

        G = nx.Graph()

        # Agregar nodos
        for estacion, (x, y) in self.coordenadas.items():
            G.add_node(estacion, pos=(x, y))

        # Colores para las líneas
        colores = {
            "Línea A": "red",
            "Línea B": "blue",
            "Línea C": "green",
            "Línea D": "orange",
        }

        # Crear figura
        plt.figure(figsize=(12, 8))
        pos = nx.get_node_attributes(G, "pos")

        # Dibujar todos los nodos
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightgray")

        # Destacar nodos en la ruta
        nx.draw_networkx_nodes(
            G, pos, nodelist=ruta, node_size=500, node_color="yellow"
        )

        # Destacar nodos de origen y destino
        nx.draw_networkx_nodes(
            G, pos, nodelist=[ruta[0]], node_size=600, node_color="green"
        )
        nx.draw_networkx_nodes(
            G, pos, nodelist=[ruta[-1]], node_size=600, node_color="red"
        )

        nx.draw_networkx_labels(G, pos)

        # Dibujar aristas por línea (versión tenue)
        for linea, conexiones in self.lineas.items():
            edges = list(conexiones)
            color = colores.get(linea, "black")
            nx.draw_networkx_edges(
                G, pos, edgelist=edges, width=1, edge_color=color, alpha=0.3
            )

        # Dibujar la ruta resaltada
        ruta_edges = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]
        colores_ruta = [colores.get(lineas[i], "black") for i in range(len(lineas))]

        for i, edge in enumerate(ruta_edges):
            nx.draw_networkx_edges(
                G, pos, edgelist=[edge], width=4, edge_color=colores_ruta[i]
            )

        plt.legend([f"Línea {linea}" for linea in colores])
        plt.axis("off")
        plt.title("Ruta Óptima en la Red de Transporte")
        plt.tight_layout()
        plt.savefig("ruta_optima.png")
        plt.close()


def crear_sistema_ejemplo():
    """Crea un sistema de transporte de ejemplo"""
    sistema = SistemaTransporte()

    # Agregar estaciones (nombre, coordenada x, coordenada y)
    sistema.agregar_estacion("Terminal Norte", 0, 10)
    sistema.agregar_estacion("Parque Central", 5, 8)
    sistema.agregar_estacion("Universidad", 10, 10)
    sistema.agregar_estacion("Hospital", 8, 5)
    sistema.agregar_estacion("Centro Comercial", 3, 3)
    sistema.agregar_estacion("Estadio", 7, 2)
    sistema.agregar_estacion("Terminal Sur", 12, 0)
    sistema.agregar_estacion("Biblioteca", 15, 7)
    sistema.agregar_estacion("Aeropuerto", 18, 5)
    sistema.agregar_estacion("Playa", 20, 0)

    # Agregar conexiones (origen, destino, tiempo en minutos, línea)
    # Línea A: Norte-Sur
    sistema.agregar_conexion("Terminal Norte", "Parque Central", 5, "Línea A")
    sistema.agregar_conexion("Parque Central", "Hospital", 4, "Línea A")
    sistema.agregar_conexion("Hospital", "Centro Comercial", 3, "Línea A")
    sistema.agregar_conexion("Centro Comercial", "Estadio", 4, "Línea A")
    sistema.agregar_conexion("Estadio", "Terminal Sur", 6, "Línea A")

    # Línea B: Este-Oeste
    sistema.agregar_conexion("Terminal Norte", "Universidad", 7, "Línea B")
    sistema.agregar_conexion("Universidad", "Biblioteca", 6, "Línea B")
    sistema.agregar_conexion("Biblioteca", "Aeropuerto", 5, "Línea B")

    # Línea C: Diagonal
    sistema.agregar_conexion("Parque Central", "Universidad", 4, "Línea C")
    sistema.agregar_conexion("Universidad", "Hospital", 3, "Línea C")
    sistema.agregar_conexion("Hospital", "Estadio", 5, "Línea C")
    sistema.agregar_conexion("Estadio", "Terminal Sur", 6, "Línea C")
    sistema.agregar_conexion("Terminal Sur", "Playa", 8, "Línea C")

    # Línea D: Conexiones adicionales
    sistema.agregar_conexion("Centro Comercial", "Universidad", 6, "Línea D")
    sistema.agregar_conexion("Biblioteca", "Hospital", 7, "Línea D")
    sistema.agregar_conexion("Aeropuerto", "Playa", 9, "Línea D")

    return sistema


def main():
    # Crear sistema de ejemplo
    sistema = crear_sistema_ejemplo()

    # Visualizar red completa
    sistema.visualizar_red()

    # Definir origen y destino para la búsqueda
    origen = "Terminal Norte"
    destino = "Playa"

    print(f"Buscando la mejor ruta de {origen} a {destino}...")

    # Encontrar la mejor ruta
    ruta, tiempo_total, lineas_usadas = sistema.encontrar_mejor_ruta(origen, destino)

    if ruta:
        print(f"Ruta encontrada en {tiempo_total} minutos:")

        # Mostrar ruta con detalles
        ultima_linea = None
        for i in range(len(ruta) - 1):
            estacion_actual = ruta[i]
            siguiente_estacion = ruta[i + 1]
            linea_actual = lineas_usadas[i]

            # Verificar si hay cambio de línea
            cambio_linea = ultima_linea is not None and ultima_linea != linea_actual

            if cambio_linea:
                print(f"  Cambiar a {linea_actual} en {estacion_actual}")

            tiempo = sistema.red_transporte[estacion_actual][siguiente_estacion][0]
            print(
                f"  De {estacion_actual} a {siguiente_estacion} ({tiempo} min) - {linea_actual}"
            )

            ultima_linea = linea_actual

        # Visualizar la ruta
        sistema.visualizar_ruta(ruta, lineas_usadas)

        print("\nRuta completa:", " -> ".join(ruta))
        print(f"Tiempo total: {tiempo_total} minutos")
        print(f"Líneas utilizadas: {', '.join(set(lineas_usadas))}")
    else:
        print(f"No se encontró una ruta de {origen} a {destino}")


if __name__ == "__main__":
    main()
