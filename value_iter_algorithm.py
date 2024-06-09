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
disallowed_x = []
disallowed_y = []


# needs to be defined before the algorithm is run
# positions with +1 and -1 values
terminal_x = [0, 1 ]
terminal_y = [3, 3,]



# define blocked cells
for i in range(m.shape[0]):
    for j in range(m.shape[1]):
        # add to disallowed coordinates wherever -999 is found
        if m[i, j] == -999:
            disallowed_x.append(i)
            disallowed_y.append(j)
            
# number of iterations for converging grid values
iterations = 100


for _ in range(iterations):
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):

            if i in terminal_x and j in terminal_y:
                continue
            
            # print(f'i={i}, j={j}')

            # print(f'top {i - 1}, {j}')
            # print(f'down {i + 1}, {j}')
            # print(f'right {i}, {j + 1}')
            # print(f'left {i}, {j - 1}')
            
            
            
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
            
            
            
            
            
            
            if top_coord[0] in disallowed_y:
                top_coord[0] = i
            
            if down_coord[0] in disallowed_y:
                down_coord[0] = i
            
            if right_coord[1] in disallowed_x:
                right_coord[1] = j
            
            if left_coord[1] in disallowed_x:
                left_coord[1] = j
            
            
            top = m[top_coord[0], top_coord[1]]
            down = m[down_coord[0], down_coord[1]]
            right = m[right_coord[0], right_coord[1]]
            left = m[left_coord[0], left_coord[1]]
            
            # for each cell, we go top down right left
            
            
            direction_wise_state_rewards = [top, down, right, left]
            
            # top
            
            noisy_moves = [right, left]
            
            
            # print(living_reward + discount_factor * np.max([optimal_move_prob * top  + suboptimal_move_prob * left + suboptimal_move_prob * right],
            # [optimal_move_prob * right + suboptimal_move_prob * top + suboptimal_move_prob * down],
            # [optimal_move_prob * left + suboptimal_move_prob * top + suboptimal_move_prob * down],
            # [optimal_move_prob * down + suboptimal_move_prob * right + suboptimal_move_prob * left]))
            
            
            direction_rewards = np.array([[optimal_move_prob * top  + suboptimal_move_prob * left + suboptimal_move_prob * right],
            [optimal_move_prob * right + suboptimal_move_prob * top + suboptimal_move_prob * down],
            [optimal_move_prob * left + suboptimal_move_prob * top + suboptimal_move_prob * down],
            [optimal_move_prob * down + suboptimal_move_prob * right + suboptimal_move_prob * left]])
            
            # print(direction_rewards)
            
            V = living_reward + discount_factor * np.max(direction_rewards)
            
            # print(V)
                    
            # print('\n\n')
            # print(f'Top {top}')
            # print(f'Down {down}')
            # print(f'Right {right}')
            # print(f'Left {left}')

            m[i, j] = V
            


    # # get up down, right left state rewards
    # i = 0
    # j = 0




print(f'Final converged grid values\n\n{m}')