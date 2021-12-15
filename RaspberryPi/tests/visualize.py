# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
import numpy as np

vectors = []
def add_vectors(x_comp, y_comp, color):
    v = (np.multiply(x_comp, 50).astype(int), np.multiply(y_comp, 50).astype(int), color)
    vectors.append(v)

def draw_vectors(screen, x_comp, y_comp, color):
    start_pos = [(400,100), (100,100), (100,400), (400,400)]
    end_pos = [(start_pos[0][0] - x_comp[0], start_pos[0][1] - y_comp[0]), 
                (start_pos[1][0] - x_comp[1], start_pos[1][1] - y_comp[1]),
                (start_pos[2][0] - x_comp[2], start_pos[2][1] - y_comp[2]),
                (start_pos[3][0] - x_comp[3], start_pos[3][1] - y_comp[3])]

    for i in range(4):
        # arrow_angle = math.atan2(y_comp[i], x_comp[i])
        # arrow_x = math.cos(arrow_angle) * 5 + 5
        # arrow_y = math.sin(arrow_angle) * 5 + 5
        pygame.draw.line(screen, color, start_pos[i], end_pos[i], width=2)
        pygame.draw.circle(screen, color, end_pos[i], 5, width=0)


def visualize():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])
    
    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        # pygame.draw.rect(screen, (0, 0, 255), (250, 250, 250,250), 75)
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 300, 300), width=2)
                # , border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1)
        
        for v in vectors:
            x_comp = v[0]
            y_comp = v[1]
            color = v[2]
            draw_vectors(screen, x_comp, y_comp, color)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

# testing example
# visualize([([50,50,100,100],[0,0,50,0], (255,0,0)), 
#                     ([50,50,0,20],[0,30,50,80], (0,255,0)), 
#                     ([40,40,0,20],[50,10,10,0], (0,0,255))])