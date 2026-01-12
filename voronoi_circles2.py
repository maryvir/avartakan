
import numpy as np
import matplotlib.pyplot as plt

def distance(x, y, circle):
    (ox, oy), r = circle
    return np.hypot(x - ox, y - oy) - r

def circles_Voronoi(circles, margin=5):
    fig, ax = plt.subplots(figsize=(10, 10))
    alpha = np.linspace(0, 2*np.pi, 400)
    t = np.linspace(-3, 3, 1500)

    x_edge, y_edge = [], []
    for (Ox, Oy), r in circles:
        x = Ox + r*np.cos(alpha)
        y = Oy + r*np.sin(alpha)
        ax.plot(x, y, color='k')
        x_edge += [Ox - r, Ox + r]
        y_edge += [Oy - r, Oy + r]

    x_min, x_max = min(x_edge) - margin, max(x_edge) + margin
    y_min, y_max = min(y_edge) - margin, max(y_edge) + margin

    n = len(circles)
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), r1 = circles[i]
            (x2, y2), r2 = circles[j]
            
            a = abs(r1 - r2) / 2
            c = np.hypot(x2 - x1, y2 - y1) / 2
            
            if c <= a: continue
                
            b = np.sqrt(c**2 - a**2)
            x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
            betta = np.arctan2(y2 - y1, x2 - x1)

            branch = 1 if r1 >= r2 else -1
            bx = branch * a * np.cosh(t)
            by = b * np.sinh(t)

            X = x0 + bx * np.cos(betta) - by * np.sin(betta)
            Y = y0 + bx * np.sin(betta) + by * np.cos(betta)

            clip = []
            for px, py in zip(X, Y):
                dij = distance(px, py, circles[i])
                keep = True
                for k in range(n):
                    if k == i or k == j: 
                      continue
                    if distance(px, py, circles[k]) < dij:
                        keep = False
                        break
                clip.append(keep)

            clip = np.array(clip)
            ax.plot(X[clip], Y[clip], 'k', linewidth=2)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    
    plt.show()

circles = [
    ((-3, 0), 2),
    ((5, 0), 3),
    ((0, 7), 2),
    ((-7, -6), 2),
    ((8, -5), 2)
]

circles_Voronoi(circles)