import numpy as np
import matplotlib.pyplot as plt

def distance(x, y, circle):
    (ox, oy), r = circle
    return np.hypot(x - ox, y - oy) - r

def circles_Voronoi(circles, margin=5):
    fig, ax = plt.subplots(figsize=(10, 10))
    alpha = np.linspace(0, 2*np.pi, 400)
    t = np.linspace(-8, 8, 1000)

    x_edge, y_edge = [], []
    for i, ((Ox, Oy), r) in enumerate(circles, start=1):
        x = Ox + r*np.cos(alpha)
        y = Oy + r*np.sin(alpha)
        ax.plot(x, y, color='k')
        ax.plot(Ox, Oy, 'ko', markersize=4)
        ax.text(
            Ox, Oy,
            f"C{i}",
            fontsize=10,
            ha='right',
            va='bottom'
        )
        x_edge += [Ox - r, Ox + r]
        y_edge += [Oy - r, Oy + r]

    x_min, x_max = min(x_edge) - margin, max(x_edge) + margin
    y_min, y_max = min(y_edge) - margin, max(y_edge) + margin

    res = 200
    xs = np.linspace(x_min, x_max, res)
    ys = np.linspace(y_min, y_max, res)
    XX, YY = np.meshgrid(xs, ys)

    region = np.zeros_like(XX, dtype=int)

    for i in range(len(circles)):
        d = distance(XX, YY, circles[i])
        if i == 0:
            min_dist = d
        else:
            closer = d < min_dist
            region[closer] = i
            min_dist = np.minimum(min_dist, d)

    ax.pcolormesh(XX, YY, region, cmap='tab10', shading='auto', alpha=0.2)

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

mines = np.random.uniform([0, 0], [50, 100], size=(10, 2))

d_list = []

for i in range(len(mines)):
    distances = []
    for j in range(len(mines)):
        if i != j:
            distances.append(
                np.hypot(mines[i,0] - mines[j,0], mines[i,1] - mines[j,1])
            )
    d_min = min(distances)
    d_list.append(d_min)

e = max(0.01, 0.9*(min(d_list)/2 - 0.2))

circles = []
for i in range(len(mines)):
    r = max(0.01, d_list[i]/2 - e)
    circles.append(((mines[i,0], mines[i,1]), r))

circles_Voronoi(circles)