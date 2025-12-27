import numpy as np
import matplotlib.pyplot as plt

def circles_Voronoi(circles, margin=5):

    fig, ax = plt.subplots(figsize=(10, 10))
    alpha = np.linspace(0, 2*np.pi, 400)

    x_edge, y_edge = [], []
    for (Ox, Oy), r in circles:
        x = Ox + r*np.cos(alpha)
        y = Oy + r*np.sin(alpha)
        ax.plot(x, y, color='k')
        x_edge += [Ox - r, Ox + r]
        y_edge += [Oy - r, Oy + r]

    x_min, x_max = min(x_edge) - margin, max(x_edge) + margin
    y_min, y_max = min(y_edge) - margin, max(y_edge) + margin

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    x_grid = np.arange(x_min, x_max + 0.05, 0.01) 
    y_grid = np.arange(y_min, y_max + 0.05, 0.01)
    X, Y = np.meshgrid(x_grid, y_grid)

    all_dists = []
    for (Ox, Oy), r in circles:
      all_dists.append(np.hypot(X - Ox, Y - Oy) - r)
    
    closest = np.argmin(all_dists, axis=0)
    ax.contourf(X, Y, closest, levels=np.arange(len(circles)) + 0.5)
    ax.contour(X, Y, closest, levels=np.arange(len(circles)) + 0.5, colors='k')

    ax.set_aspect('equal', adjustable='box')
    plt.show()

circles = [
    ((-3, 0), 2),
    ((5, 0), 3),
    ((0, 7), 2),
    ((-7, -6), 2),
    ((8, -5), 2)
]

circles_Voronoi(circles, margin=5)