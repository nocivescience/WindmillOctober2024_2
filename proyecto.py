from manim import *
import random
import numpy as np

class RotatingLine(Scene):
    def construct(self):
        # Crear 4 puntos aleatorios
        points = [self.random_point() for _ in range(4)]
        point_mobs = [Dot(point=point, color=WHITE) for point in points]
        self.add(*point_mobs)

        angle = np.pi / 6  # Ángulo inicial en PI/6
        angle_speed = 0.02  # Velocidad de rotación
        current_pivot_index = 0  # Índice del pivote actual
        line_length = 5  # Longitud de la línea
        previous_pivot_index = None  # Para rastrear el pivote anterior

        line = Line(start=points[current_pivot_index], end=points[current_pivot_index] + np.array([line_length, 0, 0]), color=RED)
        self.add(line)

        # Ciclo de animación
        for _ in range(300):  # Duración de la animación
            self.wait(0.01)  # Esperar un poco para suavizar la animación

            # Actualizar el ángulo
            angle += angle_speed

            # Calcular el nuevo extremo de la línea
            line_vector = np.array([line_length * np.cos(angle), line_length * np.sin(angle), 0])
            line.put_start_and_end_on(points[current_pivot_index], points[current_pivot_index] + line_vector)

            # Verificar si la línea está cerca angularmente a otro punto
            closest_point_index = self.find_closest_point_index(points, points[current_pivot_index], angle, current_pivot_index)

            if closest_point_index is not None and closest_point_index != previous_pivot_index:
                # Guardar el pivote anterior
                previous_pivot_index = current_pivot_index
                current_pivot_index = closest_point_index

    def random_point(self):
        return np.array([random.uniform(-3, 3), random.uniform(-3, 3), 0])

    def find_closest_point_index(self, points, pivot, current_angle, current_index):
        closest_index = None
        smallest_angle_diff = float('inf')

        for i, point in enumerate(points):
            if i != current_index:
                # Calcular el ángulo entre el pivote actual y el punto
                angle_to_point = np.arctan2(point[1] - pivot[1], point[0] - pivot[0])

                # Encontrar la diferencia angular
                angle_diff = abs((angle_to_point - current_angle + 2 * np.pi) % (2 * np.pi))

                # Si la diferencia angular es pequeña, consideramos que estamos cerca de ese punto
                if angle_diff < 0.1 and angle_diff < smallest_angle_diff:
                    smallest_angle_diff = angle_diff
                    closest_index = i

        return closest_index
