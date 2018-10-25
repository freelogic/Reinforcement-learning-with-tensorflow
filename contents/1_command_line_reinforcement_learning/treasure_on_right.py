"""
A simple example for Reinforcement Learning using table lookup Q-learning method.
An agent "o" is on the left of a 1 dimensional world, the treasure is on the rightmost location.
Run this program and to see how the agent will improve its strategy of finding the treasure.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import sys

import numpy as np
import pandas as pd
import time

np.random.seed(2)  # reproducible


N_STATES = 500   # the length of the 1 dimensional world
END_POS = N_STATES - 1 # 总共有n_states个位置,所以编号从0到n_states-1，结束位置标志是n_states-1
BEGIN_POS = 0 # 总共有n_states个位置,所以编号从0到n_states-1，开始位置标志是0
#ACTIONS = ['left', 'right']     # available actions
ACTIONS = ['l1', 'r1']     # available actions
ACTIONS_EXP = ['l1', 'r1','l2', 'r2','l4', 'r4','l8', 'r8','l16', 'r16','l32', 'r32','l64', 'r64','l128', 'r128']     # available actions
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 60   # maximum episodes
FRESH_TIME = 0.01    # fresh time for one move
#steps_table = [] # save steps used every EPISODE
display_steps = False # display steps in procedure, it make program VERY SLOW!


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),     # q_table initial values
        columns=actions,    # actions's name
    )
    # print(table)    # show table
    return table


def choose_action(state, q_table, actions):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
        #action_name = np.random.choice(ACTIONS)
        action_name = np.random.choice(actions)
    else:   # act greedy
        action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name

def get_env_feedback_orig(S, A):
    # This is how agent will interact with the environment
    if A == 'r1':    # move right
        if S == N_STATES - 2:   # terminate
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:   # move left
        R = 0
        if S == 0:
            S_ = S  # reach the wall
        else:
            S_ = S - 1
    return S_, R


def get_env_feedback(S, A):
    # This is how agent will interact with the environment
    if A[0] == 'r': # move right
        step_nbr = int(A[1:]) # get step number
        if S + step_nbr > END_POS: # beyond the end pos, new round again! start from begin pos
            R = 0
            S_ = BEGIN_POS
        elif S + step_nbr == END_POS: # reach end pos/goal! success!
            R = 1
            S_ = 'terminal'
        else:  # go right (step_nbr) steps and not reach/beyond end pos yet!
            R = 0
            S_ = S + step_nbr
    elif A[0] == 'l': # move left
        step_nbr = int(A[1:]) # get step number
        if S - step_nbr <= BEGIN_POS: # beyond/reach the begin pos/wall, new round again! start from begin pos
            R = 0
            S_ = BEGIN_POS
        else: # go left (step_nbr) steps and not reach/beyond the WALL/BEGIN pos yet!
            R = 0
            S_ = S - step_nbr
    else:
        print("[WARN]Bad action: '{0}'!".format(A))
        exit(-1)
    return S_, R

def update_env(S, episode, step_counter):
    # This is how environment be updated
    env_list = ['-']*(N_STATES-1) + ['T']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)
        print('\r                                ', end='')
    else:
        #env_list[S] = 'o'
        env_list[S] = str(S)
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl(get_env_feedback_func,actions):
    # main part of RL loop
    #q_table = build_q_table(N_STATES, ACTIONS)
    steps_table = []
    q_table = build_q_table(N_STATES, actions)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        #update_env(S, episode, step_counter)
        if display_steps == False:
            display_progress(int(episode / MAX_EPISODES * 100))  # 显示命令行进度
        while not is_terminated:

            A = choose_action(S, q_table,actions)
            #S_, R = get_env_feedback(S, A)  # take action & get next state and reward
            S_, R = eval(get_env_feedback_func)(S, A) # dynamic/runtime get func name and handler first before call it!
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()   # next state is not terminal
            else:
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode

            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            S = S_  # move to next state

            if display_steps:
                update_env(S, episode, step_counter+1)
            step_counter += 1
        steps_table.append(step_counter) # save steps used

    return q_table,steps_table

def display_progress(percent):
    bar_length=20 #20个字符宽度的进度条;
    hashes = '>' * int(percent/100.0 * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
    sys.stdout.flush()
    #time.sleep(0.01)

if __name__ == "__main__":

    """
    func_list = [get_env_feedback, get_env_feedback2]

    for func in func_list:
        func_name = func.__name__
        print('RUN: {0}'.format(func_name))
        q_table, steps_table = rl(func_name,ACTIONS)
        print('\r\nSteps-table: \n{0}'.format(steps_table))
        print('\r\nQ-table:\n{0}'.format(q_table))
        print('\r\n') 
    """

    env_feedback_func = [get_env_feedback]
    #actions_list = [ACTIONS, ACTIONS_EXP]
    actions_list = [ACTIONS_EXP]

    for actions in actions_list:
        print('RUN in actions mode: {0}'.format(actions))
        q_table, steps_table = rl(env_feedback_func[0].__name__,actions)
        print('\r\nSteps-table: \n{0}'.format(steps_table))
        print('\r\nQ-table:\n{0}'.format(q_table))
        print('\r\n')

# TODO 增加时间的统计；步骤统计;形成table供显示;
# TODO 将steps递减和round弄成二维表；动态比较两种方法的情况；
# TODO 如果能将时间显示在图表上就更好了；
# TODO 添加多核计算(纯python无框架用多进程；如果是keras_tf等框架尝试多线程?了解一下keras_tf框架)
# TODO 研究cartpole立杆子和开小车的GYM游戏