import numpy as np
import matplotlib.pyplot as plt

def circles_and_hyperbolas(circles):

    fig, ax = plt.subplots(figsize=(10, 10))
    t = np.linspace(-1, 1, 400)
    alpha = np.linspace(0, 2*np.pi, 400)

    for (Ox, Oy), r in circles:
        x = Ox + r * np.cos(alpha)
        y = Oy + r * np.sin(alpha)
        ax.plot(x, y)

    for i in range(len(circles) - 1):
        (x1, y1), r1 = circles[i]
        (x2, y2), r2 = circles[i+1]
        
        a = abs(r1 - r2) / 2
        c = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) / 2
        
        if c <= a:
            continue
            
        b = np.sqrt(c**2 - a**2)

        x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
        betta = np.arctan2(y2 - y1, x2 - x1)

        branch = 1 if r1 >= r2 else -1
        bx = branch * a * np.cosh(t)
        by = b * np.sinh(t)

        X = x0 + bx * np.cos(betta) - by * np.sin(betta)
        Y = y0 + bx * np.sin(betta) + by * np.cos(betta)

        ax.plot(X, Y)

    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    plt.show()

circles = [
    ((-3, 0), 2),
    ((5, 0), 3)
]

circles_and_hyperbolas(circles)