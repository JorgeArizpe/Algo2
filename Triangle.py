import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def draw_3d_pixel(x, y, z, size=0.05):
    """
    Dibuja un 'pixel' 3D en forma de cubo en la posición especificada
    """
    vertices = (
        (x + size, y + size, z + size),
        (x - size, y + size, z + size),
        (x - size, y - size, z + size),
        (x + size, y - size, z + size),
        (x + size, y + size, z - size),
        (x - size, y + size, z - size),
        (x - size, y - size, z - size),
        (x + size, y - size, z - size),
    )

    edges = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    )

    glBegin(GL_QUADS)
    for face in ((0, 1, 2, 3), (4, 5, 6, 7), (0, 3, 7, 4), (1, 2, 6, 5), (0, 1, 5, 4), (2, 3, 7, 6)):
        glColor3f(0.7, 0.7, 1.0)
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.2, 0.2, 0.8)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def bresenham_3d_line(x0, y0, z0, x1, y1, z1):
    """
    Dibuja una línea 3D entre dos puntos usando el algoritmo de Bresenham
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)

    xs = 1 if x1 > x0 else -1
    ys = 1 if y1 > y0 else -1
    zs = 1 if z1 > z0 else -1

    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x0 != x1:
            draw_3d_pixel(x0 * 0.1, y0 * 0.1, z0 * 0.1)
            x0 += xs
            if p1 >= 0:
                y0 += ys
                p1 -= 2 * dx
            if p2 >= 0:
                z0 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y0 != y1:
            draw_3d_pixel(x0 * 0.1, y0 * 0.1, z0 * 0.1)
            y0 += ys
            if p1 >= 0:
                x0 += xs
                p1 -= 2 * dy
            if p2 >= 0:
                z0 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z0 != z1:
            draw_3d_pixel(x0 * 0.1, y0 * 0.1, z0 * 0.1)
            z0 += zs
            if p1 >= 0:
                y0 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x0 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx

def draw_3d_triangle(p1, p2, p3):
    """
    Dibuja un triángulo 3D usando tres puntos
    """
    bresenham_3d_line(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
    bresenham_3d_line(p2[0], p2[1], p2[2], p3[0], p3[1], p3[2])
    bresenham_3d_line(p3[0], p3[1], p3[2], p1[0], p1[1], p1[2])

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Definir los vértices del triángulo
    triangle_points = [
        (0, 5, 0),    # Punto superior
        (-5, -5, 0),  # Punto inferior izquierdo
        (5, -5, 0)    # Punto inferior derecho
    ]

    rotation = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glRotatef(1, 1, 1, 1)  # Rotación continua
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Dibujar el triángulo
        draw_3d_triangle(triangle_points[0], triangle_points[1], triangle_points[2])

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()