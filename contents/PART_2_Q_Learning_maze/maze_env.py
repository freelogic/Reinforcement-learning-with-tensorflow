"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""


import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
#MAZE_H = 4  # grid height
MAZE_H = 16  # grid height
#MAZE_W = 4  # grid width
MAZE_W = 16


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u1', 'd1', 'l1', 'r1']
        self.action_space_exp = ['u1', 'd1', 'l1', 'r1','u2', 'd2', 'l2', 'r2',
                                 'u4', 'd4', 'l4', 'r4','u8', 'd8', 'l8', 'r8']
        #self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self.hells = []
        self.heavens = []
        #self.boy
        self._build_maze()

    def _build_boy(self, scene_boy_list,origin):
        # CREATE BOY #红色方块是旅行男孩
        for boy in scene_boy_list:
            center = origin + np.array([UNIT * boy[0], UNIT * boy[1]])
            self.boy = self.canvas.create_rectangle(  # 方块是15+15=30像素见方的方块，比棋盘小）
                center[0] - 15, center[1] - 15,
                center[0] + 15, center[1] + 15,
                fill='red')

    def _build_scene(self, scene_list):
        # create origin
        origin = np.array([20, 20])  # 左上角方块（40x40）的中心坐标

        scene_hell_list = scene_list[0] #多个地狱
        # CREATE HELL #黑色方块是地狱
        for hell in scene_hell_list:
            center = origin + np.array([UNIT * hell[0], UNIT * hell[1]])
            self.one_hell = self.canvas.create_rectangle( # 方块是15+15=30像素见方的方块，比棋盘小）
                center[0] - 15, center[1] - 15,
                center[0] + 15, center[1] + 15,
            fill='black')
            self.hells.append(self.one_hell)

        scene_heaven_list = scene_list[1] #多个天堂
        # CREATE heaven #黄色圆是天堂
        for heaven in scene_heaven_list:
            center = origin + np.array([UNIT * heaven[0], UNIT * heaven[1]])
            self.one_heaven = self.canvas.create_oval( # 是15+15=30像素见方的圆，比棋盘标准grid小）
                center[0] - 15, center[1] - 15,
                center[0] + 15, center[1] + 15,
            fill='yellow')
            self.heavens.append(self.one_heaven)

        scene_boy_list = scene_list[2]  # 探索男孩只能1个位置
        self._build_boy(scene_boy_list,origin)

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        """
        # create origin
        origin = np.array([20, 20]) #左上角方块（40x40）的中心坐标

        # hell  #黑色方块是地狱
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle( # 方块是15+15=30像素见方的方块，比棋盘小）
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        # hell
        hell2_center = origin + np.array([UNIT, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')

        # create oval  # 黄色圆是天堂
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create red rect  #红色是旅行者
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        """

        # create scene  # 部署场景scene
        scene_hell_list = [[14,5],[13,6],[14,7],[10, 10], [9, 11], [11, 11]] #多个地狱
        scene_heaven_list = [[14,6], [10, 11]] #多个天堂
        scene_boy_list = [[0, 1]] #探索男孩只能1个位置
        scene_list = [scene_hell_list,scene_heaven_list,scene_boy_list]
        self._build_scene(scene_list)


        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.05)
        self.canvas.delete(self.boy)
        origin = np.array([20, 20])
        #self.rect = self.canvas.create_rectangle(
        #    origin[0] - 15, origin[1] - 15,
        #    origin[0] + 15, origin[1] + 15,
        #    fill='red')

        self._build_boy([[1,0]], origin)

        # return observation
        return self.canvas.coords(self.boy)

    def coords_is_same(self, state, targets):
        for target in targets:
            if state == self.canvas.coords(target):
                return True
        return False

    def handle_reward(self,state):
        # reward function
        #if state_ == self.canvas.coords(self.oval):
        if self.coords_is_same(state, self.heavens):
            reward = 1
            done = True
            state = 'terminal'
        #elif state in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
        elif self.coords_is_same(state, self.hells):
            reward = -1
            done = True
            state = 'terminal'
        else:
            reward = 0
            done = False

        return state, reward, done

    def handle_agent(self,action):
        """
        self.action_space = ['u1', 'd1', 'l1', 'r1']
        self.action_space_exp = ['u1', 'd1', 'l1', 'r1','u2', 'd2', 'l2', 'r2',
                                 'u4', 'd4', 'l4', 'r4','u8', 'd8', 'l8', 'r8']
        """
        s = self.canvas.coords(self.boy)
        base_action = np.array([0, 0])
        if action[0] == 'u': #up
            step_nbr = int(action[1:])
            if s[1] > UNIT * step_nbr:
                base_action[1] -= UNIT * step_nbr
        elif action[0] == 'd': #down
            step_nbr = int(action[1:])
            if s[1] < (MAZE_H - 1 - step_nbr) * UNIT:
                base_action[1] += UNIT * step_nbr
        elif action[0] == 'r': #right
            step_nbr = int(action[1:])
            if s[0] < (MAZE_W - 1 - step_nbr) * UNIT:
                base_action[0] += UNIT * step_nbr
        elif action[0] == 'l': #left
            step_nbr = int(action[1:])
            if s[0] > UNIT * step_nbr:
                base_action[0] -= UNIT * step_nbr

        self.canvas.move(self.boy, base_action[0], base_action[1])  # move agent
        """
        s = self.canvas.coords(self.boy)
        base_action = np.array([0, 0])
        if action == 0:  # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:  # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.boy, base_action[0], base_action[1])  # move agent
        """

    def step(self, action):
        self.handle_agent(action)
        s_ = self.canvas.coords(self.boy)  # next state
        return self.handle_reward(s_)

    def render(self):
        time.sleep(0.01)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()