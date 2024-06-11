# import the pygame module, so you can use it
import pygame
import numpy as np
import random
import time


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCKAGE_NUMBER = -999
block_size = 50
max_width_len = int(WINDOW_WIDTH / block_size)
max_height_len = int(WINDOW_HEIGHT / block_size)
NUM_BLOCKAGES = 7

# number of iterations for converging grid values
iterations = 20

print(f'max_width_len = {max_width_len}')
print(f'max_height_len = {max_height_len}')




# ************************************************************************************************************************************ #

# value iteration algorithm

m = np.zeros((int(max_height_len), int(max_width_len)), dtype=np.float16)


print(f'm shape = {m.shape}')

width_slice = int(max_width_len - 1) 
height_slice = int(max_height_len - 1 )
m[0, max_width_len - 1] = 1
m[1, max_width_len - 1] = -1

# BLOCKAGE_NUMBER defines a blocked grid cell


random_blockages = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(NUM_BLOCKAGES)]

print(f'Random blockages => {random_blockages}')

for blocked_coord in random_blockages:
    m[blocked_coord[0], blocked_coord[1]] = BLOCKAGE_NUMBER

print(m)


# calculating value function
noise = 0.2
optimal_move_prob = 1 - noise
suboptimal_move_prob = noise / 2
living_reward = 0
discount_factor = .9

disallowed_coords = []


# needs to be defined before the algorithm is run
# positions with +1 and -1 values
terminal_points = [[0, max_width_len - 1], [1, max_width_len - 1]]

# define blocked cells
for i in range(m.shape[0]):
    for j in range(m.shape[1]):
        # add to disallowed coordinates wherever BLOCKAGE_NUMBER is found
        if m[i, j] == BLOCKAGE_NUMBER:
            # disallowed_x.append(i)
            # disallowed_y.append(j)
            disallowed_coords.append([i, j])



disallowed_coords = np.array(disallowed_coords)

coord_direction_dict = {}

m_iterations = []


for _ in range(iterations):
    # print(f'\n\n\n\nEPOCH {_ + 1}')
    saved_values = {}
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            # print('\n\n')
            # print(f'FOR i={i}, j={j}')
            if [i, j] in terminal_points:
                # print(f'skipping for {i, j}')
                continue

            if any(np.array_equal(row, [i, j]) for row in disallowed_coords):
                # print(f'skipping for {i, j}')
                continue
            
            top_coord = [i - 1, j]
            down_coord = [i + 1, j]
            right_coord = [i, j + 1]
            left_coord = [i, j - 1]
            
            if top_coord[0] < 0:
                top_coord[0] = 0
            
            if down_coord[0] > m.shape[0] - 1:
                down_coord[0] = m.shape[0] - 1
            
            if right_coord[1] > m.shape[1] - 1:
                right_coord[1] = m.shape[1] - 1
            
            if left_coord[1] < 0:
                left_coord[1] = 0
            
            top = m[top_coord[0], top_coord[1]]
            down = m[down_coord[0], down_coord[1]]
            right = m[right_coord[0], right_coord[1]]
            left = m[left_coord[0], left_coord[1]]


            if int(top) == int(BLOCKAGE_NUMBER):
                top = 0
            
            if int(down) == int(BLOCKAGE_NUMBER):
                down = 0
            
            if int(right) == int(BLOCKAGE_NUMBER):
                right = 0
                
            if int(left) == int(BLOCKAGE_NUMBER):
                left = 0
                
            
            # for each cell, we go top down right left
            
            direction_wise_state_rewards = [top, down, right, left]
            noisy_moves = [right, left]
            
            direction_rewards = np.array([[optimal_move_prob * top  + suboptimal_move_prob * left + suboptimal_move_prob * right],
            [optimal_move_prob * right + suboptimal_move_prob * top + suboptimal_move_prob * down],
            [optimal_move_prob * left + suboptimal_move_prob * top + suboptimal_move_prob * down],
            [optimal_move_prob * down + suboptimal_move_prob * right + suboptimal_move_prob * left]])
            
            # print(direction_rewards)
            
            if np.argmax(direction_rewards) == 0:
                coord_direction_dict[f'{i}, {j}'] = 'top'
                
            elif np.argmax(direction_rewards) == 1:
                coord_direction_dict[f'{i}, {j}'] = 'right'
                
            elif np.argmax(direction_rewards) == 2:
                coord_direction_dict[f'{i}, {j}'] = 'left'
                
            elif np.argmax(direction_rewards) == 3:
                coord_direction_dict[f'{i}, {j}'] = 'down'
            
                
            V = living_reward + discount_factor * np.max(direction_rewards)
            
            # print(f'Top {top}')
            # print(f'Down {down}')
            # print(f'Right {right}')
            # print(f'Left {left}')

            saved_values[f'{i},{j}'] = V

    # updating grid values once iteration is complete
    for key in list(saved_values.keys()):
        coords = key.split(',')
        m[int(coords[0]), int(coords[1])] = saved_values[key]
    
    m_iterations.append(m.copy())
            

print(f'\n\n\nFinal converged grid values\n{m}')



print(f'\n\n\nCoordinate-Direction Dictionary\n{coord_direction_dict}')


# ************************************************************************************************************************************ #



print(f'WINDOW_WIDTH = {WINDOW_WIDTH}')
print(f'WINDOW_HEIGHT = {WINDOW_HEIGHT}')


BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)

running = True
pygame.init()


surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("reinforcement")

i = 1

def drawGrid(surface, block_size):
    
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(surface=surface, color=BLACK_COLOR, rect=rect, width=1)

left, right, up, down = False, False, False, False

font_instance = pygame.font.SysFont('Comic Sans MS', 10)
score = font_instance.render('0', False, BLACK_COLOR)

one_score = font_instance.render('1', False, BLACK_COLOR, 40)
minus_one_score = font_instance.render('-1', False, BLACK_COLOR, 40)

up_text = font_instance.render('up', False, BLACK_COLOR)
down_text = font_instance.render('down', False, BLACK_COLOR)
right_text = font_instance.render('right', False, BLACK_COLOR)
left_text = font_instance.render('left', False, BLACK_COLOR)


terminal_points = [[15, 0], [15, 1]]


m_iter_var = 0

scores_propagated = 0

while running:
    
    m = m_iterations[m_iter_var]
    surface.fill(WHITE_COLOR)

    # drawing grid
    drawGrid(surface, block_size)
    
    
    # drawing random blocks
    for coord in random_blockages:
        pygame.draw.rect(surface=surface, color=BLACK_COLOR, rect=pygame.Rect(block_size * coord[1], block_size * coord[0], block_size, block_size), width=0)
        
        
        
    
    # drawing scores
    for i in range(max_height_len):
        for j in range(max_width_len):
            if [i, j] not in terminal_points:
                if int(m[i, j]) == BLOCKAGE_NUMBER:
                    curr_mat_score = font_instance.render(str(m[i, j]), False, BLACK_COLOR)
                    surface.blit(curr_mat_score, dest=(j*block_size + 15, i*block_size + 15))
                elif int(m[i, j]) == 1 or int(m[i, j]) == -1:
                    curr_mat_score = font_instance.render("{:.2f}".format(m[i, j]), False, RED_COLOR)
                    surface.blit(curr_mat_score, dest=(j*block_size + 15, i*block_size + 15))
                    
                else:
                    if m_iter_var < 19:
                        # drawing scores other than termnial and blockages, IF all iterations of scores propagating not shown
                        # if all iterations of scores shown (iter var > 19) , show directions 
                        curr_mat_score = font_instance.render("{:.2f}".format(m[i, j]), False, BLACK_COLOR)
                        surface.blit(curr_mat_score, dest=(j*block_size + 15, i*block_size + 15))
                    
    
    
    if m_iter_var == 19:
        # drawing direction values
        for i in range(max_height_len):
            for j in range(max_width_len):
                if [i, j] not in terminal_points:
                    try:
                        curr_mat_score = font_instance.render(coord_direction_dict[f'{i}, {j}'], False, BLACK_COLOR)
                        surface.blit(curr_mat_score, dest=(j*block_size + 15, i*block_size + 15))
                    except:
                        pass
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    

    if m_iter_var < 19:
        m_iter_var += 1            
        time.sleep(0.5)
    pygame.display.flip()

            
pygame.quit()

