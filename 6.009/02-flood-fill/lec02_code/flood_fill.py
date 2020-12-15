def flood_fill(image, location, color):
    # target_color = get_pixel(image, location)
    # flood_fill_recursive(image, location, target_color, color)
    # flood_fill_iterative(image, location, color)
    flood_fill_west_east(image, location, color)
    # flood_fill_recursive(image, location, target_color, color, COLORS[pygame.K_g])
    # flood_fill_iterative(image, location, color, COLORS[pygame.K_g])
    pass

def flood_fill_recursive(image, location, target_color, replace_color, goal_color=None):
    if target_color == replace_color:
        return False

    if not is_in_image(image, location):
        return False

    color = get_pixel(image, location)
    if target_color != color:
        return color == goal_color

    diffs = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != j and i + j != 0]
    set_pixel(image, location, replace_color)

    for diff in diffs:
        next_node = add_locs(location, diff) 
        if flood_fill_recursive(image, next_node, target_color, replace_color, goal_color):
            return True

    if goal_color is not None:
        set_pixel(image, location, color)

    return False


def flood_fill_iterative(image, location, color, goal_color=None):
    if not is_in_image(image, location):
        return
        
    target_color = get_pixel(image, location)
    if color == target_color:
        return

    queue = [location]
    visited = {location: None}
    diffs = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != j and i + j != 0]

    while len(queue) > 0:
        node = queue.pop(0)

        if goal_color is None:
            set_pixel(image, node, color)

        for diff in diffs:
            next_node = add_locs(node, diff) 
            if next_node not in visited and is_in_image(image, next_node):
                node_color = get_pixel(image, next_node)
                
                if node_color == target_color:
                    visited[next_node] = node
                    queue.append(next_node)
                elif goal_color == node_color:
                    while node is not None:
                        set_pixel(image, node, color)
                        node = visited[node]
                    return


def flood_fill_west_east(image, location, color):
    if not is_in_image(image, location):
        return

    target_color = get_pixel(image, location)
    if color == target_color:
        return

        
    def is_target_pixel(location):
        return location is not None and is_in_image(image, location) and get_pixel(image, location) == target_color

    queue = [location]
    while len(queue) > 0:
        node = queue.pop(0)
        w = node
        e = node

        while is_target_pixel(w):
            w = add_locs(w, (-1, 0))

        while is_target_pixel(e):
            e = add_locs(e, (1, 0))

        prev_north_node = None
        prev_south_node = None
        for i in range(w[0] + 1, e[0]):
            node = (i, node[1])
            set_pixel(image, node, color)
            north_node = add_locs(node, (0, -1))
            south_node = add_locs(node, (0, 1))
            
            if is_target_pixel(north_node) and not is_target_pixel(prev_north_node):
                queue.append(north_node)
            if is_target_pixel(south_node) and not is_target_pixel(prev_south_node):
                queue.append(south_node)

            prev_north_node = north_node
            prev_south_node = south_node



def add_locs(loc1, loc2):
    return (loc1[0] + loc2[0], loc1[1] + loc2[1]) 

##### IMAGE REPRESENTATION WITH SIMILAR ABSTRACTIONS TO LAB 1 AND 2

def is_in_image(image, location):
    return get_height(image) > location[0] >= 0 and get_width(image) > location[1] >= 0

def get_width(image):
    return image.get_width() // SCALE

def get_height(image):
    return image.get_height() // SCALE

def get_pixel(image, location):
    x, y = location
    color = image.get_at((x*SCALE, y*SCALE))
    return (color.r, color.g, color.b)

def set_pixel(image, location, color):
    x, y = location
    loc = x*SCALE, y*SCALE
    c = pygame.Color(*color)
    for i in range(SCALE):
        for j in range(SCALE):
            image.set_at((loc[0]+i, loc[1]+j), c)
    # comment out the two lines below to avoid redrawing the image every time
    # we set a pixel
    screen.blit(image, (0,0))
    pygame.display.flip()


import sys
import pygame
import os

from pygame.locals import *

root_folder = os.path.dirname(__file__)

COLORS = {
        pygame.K_r: (255, 0, 0),
        pygame.K_w: (255, 255, 255),
        pygame.K_k: (0, 0, 0),
        pygame.K_g: (0, 255, 0),
        pygame.K_b: (0, 0, 255),
        pygame.K_c: (0, 255, 255),
        pygame.K_y: (255, 230, 0),
        pygame.K_p: (179, 0, 199),
        pygame.K_o: (255, 77, 0),
        pygame.K_n: (66, 52, 0),
        pygame.K_e: (152, 152, 152),
}

SCALE = 10
IMAGE = root_folder + '/flood_input.png'
# IMAGE = root_folder + '/small_maze.png'
# IMAGE = root_folder + '/large_maze.png'
# IMAGE = root_folder + '/huge_maze.png'

pygame.init()
image = pygame.image.load(IMAGE)
dims = (image.get_width()*SCALE, image.get_height()*SCALE)
screen = pygame.display.set_mode(dims)
image = pygame.transform.scale(image, dims)
screen.blit(image, (0,0))
pygame.display.flip()
cur_color = COLORS[pygame.K_p]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key in COLORS:
                cur_color = COLORS[event.key]
                print(cur_color)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            flood_fill(image, (event.pos[0]//SCALE, event.pos[1]//SCALE), cur_color)
            screen.blit(image, (0,0))
            pygame.display.flip()
