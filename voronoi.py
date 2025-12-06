import matplotlib.pyplot as plt
import math
import random

def voronoi(sites, pad):
    xs = [p[0] for p in sites]
    ys = [p[1] for p in sites]
    
    xl, xr = min(xs), max(xs)
    yt, yb = max(ys), min(ys)
    
    box = [
        (xl - pad, yt + pad),
        (xr + pad, yt + pad),
        (xr + pad, yb - pad),
        (xl - pad, yb - pad)
    ]
    
    final_cells = []

    for i, site in enumerate(sites):
        current_cell = box[:]
        
        for j, other in enumerate(sites):
            if i == j:
                continue
            
            current_cell = clip_polygon(current_cell, site, other)
            
            if not current_cell:
                break
        
        final_cells.append(current_cell)
        
    return final_cells

def clip_polygon(subject_polygon, site, other):
    new_polygon = []
    
    for k in range(len(subject_polygon)):
        curr_v = subject_polygon[k]
        prev_v = subject_polygon[k - 1]
        
        curr_in = is_closer(curr_v, site, other)
        prev_in = is_closer(prev_v, site, other)
        
        if curr_in and prev_in:
            new_polygon.append(curr_v)
            
        elif prev_in and not curr_in:
            intersect = get_intersection(prev_v, curr_v, site, other)
            new_polygon.append(intersect)
            
        elif not prev_in and curr_in:
            intersect = get_intersection(prev_v, curr_v, site, other)
            new_polygon.append(intersect)
            new_polygon.append(curr_v)
        
    return new_polygon

def dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def is_closer(p, site, other):
    return dist(p, site) < dist(p, other)

# Calculates where the edge intersects the bisector
def get_intersection(A, B, site, other):
    
    ax, ay = A
    bx, by = B
    sx, sy = site
    ox, oy = other
    
    dx_edge = bx - ax
    dy_edge = by - ay
    
    #a*x + b*y + c = 0
    a = 2 * (sx - ox)
    b = 2 * (sy - oy)
    c = ox**2 + oy**2 - sx**2 - sy**2
    
    
    # P = A + t * (B - A)
    # a(ax + t*dx) + b(ay + t*dy) + c = 0
    denom = a * dx_edge + b * dy_edge
    
    if denom == 0: return A # Lines are parallel
    
    t = -(a * ax + b * ay + c) / denom
    
    return (ax + t * dx_edge, ay + t * dy_edge)


my_sites = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(10)]
    
cells = voronoi(my_sites, pad=2)
    
plt.figure(figsize=(8, 8))

cmap = plt.get_cmap("tab10")  

for i, cell in enumerate(cells):
  color = cmap(i % 10)
    
  x_poly = [p[0] for p in cell] + [cell[0][0]]
  y_poly = [p[1] for p in cell] + [cell[0][1]]

  plt.plot(x_poly, y_poly, 'k-')
  plt.fill(x_poly, y_poly, color=color, alpha=0.3)
        
sx = [p[0] for p in my_sites]
sy = [p[1] for p in my_sites]
plt.plot(sx, sy, 'ro')
    
plt.title("Voronoi Diagram")
plt.show()
