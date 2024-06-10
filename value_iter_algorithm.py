import numpy as np

m = np.zeros((3, 4))
m[0, 3] = 1
m[1, 3] = -1

# -999 defines a blocked grid cell
m[1, 1] = -999


# calculating value function



noise = 0.2
optimal_move_prob = 1 - noise
suboptimal_move_prob = noise / 2
living_reward = 0
discount_factor = .9

disallowed_coords = []


# needs to be defined before the algorithm is run
# positions with +1 and -1 values
terminal_points = [[0, 3], [1, 3]]

# define blocked cells
for i in range(m.shape[0]):
    for j in range(m.shape[1]):
        # add to disallowed coordinates wherever -999 is found
        if m[i, j] == -999:
            # disallowed_x.append(i)
            # disallowed_y.append(j)
            disallowed_coords.append([i, j])



disallowed_coords = np.array(disallowed_coords)
# number of iterations for converging grid values
iterations = 1000


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


            if top == -999.0:
                top = 0
            
            if down == -999.0:
                down = 0
            
            if right == -999.0:
                right = 0
                
            if left == -999.0:
                left = 0
                
            
            # for each cell, we go top down right left
            
            direction_wise_state_rewards = [top, down, right, left]
            noisy_moves = [right, left]
            
            direction_rewards = np.array([[optimal_move_prob * top  + suboptimal_move_prob * left + suboptimal_move_prob * right],
            [optimal_move_prob * right + suboptimal_move_prob * top + suboptimal_move_prob * down],
            [optimal_move_prob * left + suboptimal_move_prob * top + suboptimal_move_prob * down],
            [optimal_move_prob * down + suboptimal_move_prob * right + suboptimal_move_prob * left]])
            
            # print(direction_rewards)
            
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
            

print(f'Final converged grid values\n\n{m}')