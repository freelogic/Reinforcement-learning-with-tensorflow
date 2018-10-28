"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

"""
说明: 此代码是基于开源github项目morvan的强化学习教育视频和TF实现源码的例子而来,因为其简单易学,用来尝试新的方法成本比较低;
再次特别对morvan大神表示感谢! 如有任何涉及版权等问题,请积极联系我本人给予配合处理,谢谢!
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
        self.DEF_AGENT_INIT_POS = [0,1]
        self.ORIGIN = np.array([20, 20])  # 左上角方块（40x40）的中心坐标
        self.action_space = ['u1', 'd1', 'l1', 'r1']
        self.action_space_exp = ['u1', 'd1', 'l1', 'r1','u2', 'd2', 'l2', 'r2',
                                 'u4', 'd4', 'l4', 'r4','u8', 'd8', 'l8', 'r8']
        #self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self.hells = []
        self.heavens = []
        self.hells_grid_pos = [] #多个地狱的grid坐标(简易,方便逻辑计算,而不是像素值)
        self.heavens_grid_pos = [] #多个天堂的grid坐标(简易,方便逻辑计算,而不是像素值)
        #self.elements = []
        self._build_maze()
        self._agents = []


    def create_agent(self, color): #init_pos=[0,1]表示其实位置在第1行,第2列
        # CREATE agent(旅行男孩)
        center = self.ORIGIN + np.array([UNIT * self.DEF_AGENT_INIT_POS[0], UNIT * self.DEF_AGENT_INIT_POS[1]])
        agent = self.canvas.create_rectangle(  # 方块是15+15=30像素见方的方块，比棋盘小）
            center[0] - 15, center[1] - 15,
            center[0] + 15, center[1] + 15,
            fill=color)
        self._agents.append(agent)
        return agent

    def _build_elements(self):
        #hell_list = self.elements[0] #多个地狱
        #hells_grid_pos = self.elements[0]  # 多个地狱
        # CREATE HELL #黑色方块是地狱
        for hell in self.hells_grid_pos:
            center = self.ORIGIN + np.array([UNIT * hell[0], UNIT * hell[1]])
            self.one_hell = self.canvas.create_rectangle( # 方块是15+15=30像素见方的方块，比棋盘小）
                center[0] - 15, center[1] - 15,
                center[0] + 15, center[1] + 15,
            fill='black')
            self.hells.append(self.one_hell)

        #heaven_list = self.elements[1] #多个天堂
        #heavens_grid_pos = self.elements[1]  # 多个天堂
        # CREATE heaven #黄色圆是天堂
        for heaven in self.heavens_grid_pos:
            center = self.ORIGIN + np.array([UNIT * heaven[0], UNIT * heaven[1]])
            self.one_heaven = self.canvas.create_oval( # 是15+15=30像素见方的圆，比棋盘标准grid小）
                center[0] - 15, center[1] - 15,
                center[0] + 15, center[1] + 15,
            fill='yellow')
            self.heavens.append(self.one_heaven)

        # add all scene(fixed elements) into pos list;

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

        # create scene  # 部署场景scene
        self.hells_grid_pos = [[14,5],[13,6],[14,7],[10, 10], [9, 11], [11, 11]] #多个地狱
        self.heavens_grid_pos = [[14,6], [10, 11]] #多个天堂
        #self.elements = [hell_list,heaven_list]
        self._build_elements()



        # pack all
        self.canvas.pack()

    def reset_agent(self, agent):
        self.update()
        time.sleep(0.05)
        cur_pos = self.canvas.coords(agent)
        self.canvas.move(agent, -cur_pos[0]+5, -cur_pos[1]+5)
        return cur_pos

    def reset_all_agent(self):
        self.update()
        time.sleep(0.05)
        for agent in self._agents:
            #self.canvas.delete(agent)
            cur_pos = self.canvas.coords(agent)
            self.canvas.move(agent, -cur_pos[0]+5, -cur_pos[1]+5)
        #self._init_agent()
        return self.DEF_AGENT_INIT_POS

        # return observation
        # return self.canvas.coords(self.boy)

    def find_target(self, target, elements):
        grid_pos = self.tranfor_to_grid_pos(target)
        for element in elements:
            if grid_pos == self.tranfor_to_grid_pos(self.canvas.coords(element)):
                return True
        return False

    def l1_l2_has_intersection(self,l1,l2):
        intersection_list = []
        find_intersection = False
        for item in l1:
            if item in l2:
                intersection_list.append(item)
                find_intersection = True
        return find_intersection, intersection_list

    def reach_and_passby_hell(self, cur_state, old_state): #直线障碍物检测
        #return False #短路操作用来debug
        # list的交集,并集和差集
        # https://www.cnblogs.com/lzq1987/p/6701196.html
        # 算法,取出直线的x或y上的分量组成list；取出环境element的同样分量的list,交集=0则为空;

        # 先转换为gird坐标(简单,非像素pixel)
        cs = self.tranfor_to_grid_pos(cur_state)
        os = self.tranfor_to_grid_pos(old_state)
        line_list=[]
        if cs[0] == os[0]: #x相等,形成垂线段yline
            if cs[1] == os[1]: #重合点,不再计算,上次应该计算过了;返回false
                return False
            elif cs[1] > os[1]:
                for i in range(os[1], cs[1]):
                    line_list.append([os[0],i])
                # hells列表集合与y_line_list求交集,非0则为TRUE返回,reach或者经过passby地狱
                flag, intersection_list = self.l1_l2_has_intersection(line_list,self.hells_grid_pos)
                return flag
            else:
                for i in range(cs[1], os[1]):
                    line_list.append([os[0],i])
                # hells列表集合与y_line_list求交集,非0则为TRUE返回,reach或者经过passby地狱
                flag, intersection_list = self.l1_l2_has_intersection(line_list,self.hells_grid_pos)
                return flag
        elif cs[1] == os[1]: #y相等,形成水平线段xline
            if cs[0] > os[0]:
                for i in range(os[0], cs[0]):
                    line_list.append([i,os[1]])
                # hells列表集合与y_line_list求交集,非0则为TRUE返回,reach或者经过passby地狱
                flag, intersection_list = self.l1_l2_has_intersection(line_list,self.hells_grid_pos)
                return flag
            else:
                for i in range(cs[0], os[0]):
                    line_list.append([i,os[1]])
                # hells列表集合与y_line_list求交集,非0则为TRUE返回,reach或者经过passby地狱
                flag, intersection_list = self.l1_l2_has_intersection(line_list,self.hells_grid_pos)
                return flag
        else:
            return False



    def update_reward(self, state, old_state):
        # reward function
        #if state_ == self.canvas.coords(self.oval):
        if self.reach_and_passby_hell(state, old_state):
            reward = -1
            done = True
            state = 'terminal'
        elif self.find_target(state, self.heavens):
            reward = 2
            done = True
            state = 'terminal'
        #elif state in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
        elif self.find_target(state, self.hells):
            reward = -1
            done = True
            state = 'terminal'
        else:
            reward = 0
            done = False

        return state, reward, done

    def tranfor_to_pixel_pos_central(self, pixel_pos):
        # 说明/举例: [5,5,35,35](block的左上P1和右下P2) = [20,20](block中心点) = 都是左上角第一块block的表达;
        pixel_pos_central=[]
        pixel_pos_central.append(int((pixel_pos[0] + pixel_pos[2]) / 2))
        pixel_pos_central.append(int((pixel_pos[1] + pixel_pos[3]) / 2))
        return pixel_pos_central

    def tranfor_to_grid_pos(self, pixel_pos):
        # 说明/举例: [5,5,35,35](block的左上P1和右下P2) = [0,0](block中心点) = 都是左上角第一块block的表达;
        pixel_pos_central = self.tranfor_to_pixel_pos_central(pixel_pos)
        grid_pos = []
        grid_pos.append(pixel_pos_central[0] // UNIT)
        grid_pos.append(pixel_pos_central[1] // UNIT)
        return grid_pos

    def update_agent(self, action, agent):

        #self.action_space = ['u1', 'd1', 'l1', 'r1']
        #self.action_space_exp = ['u1', 'd1', 'l1', 'r1','u2', 'd2', 'l2', 'r2',
        #                         'u4', 'd4', 'l4', 'r4','u8', 'd8', 'l8', 'r8']

        s = self.canvas.coords(agent)
        gs = self.tranfor_to_grid_pos(s)
        delta = np.array([0, 0])
        step_nbr = int(action[1:])
        if action[0] == 'u': #up
            delta[1] = 0 if gs[1] <= step_nbr else -step_nbr #够移动就记录位移delta,否则归0贴左上或贴右下边缘
        elif action[0] == 'd': #down
            delta[1] = step_nbr if gs[1] <= (MAZE_H - 1 - step_nbr) else (MAZE_H - 1 - gs[1])  # 够移动就记录位移delta,否则归0贴左上或贴右下边缘
        elif action[0] == 'r': #right
            delta[0] = step_nbr if gs[0] <= (MAZE_W - 1 - step_nbr) else (MAZE_W - 1 - gs[0])  # 够移动就记录位移delta,否则归0贴左上或贴右下边缘
        elif action[0] == 'l': #left
            delta[0] = 0 if gs[0] <= step_nbr else -step_nbr  # 够移动就记录位移delta,否则归0贴左上或贴右下边缘

        old_state = self.get_state(agent)
        self.canvas.move(agent, delta[0]*UNIT, delta[1]*UNIT)  # move agent

        return old_state


    def step(self, action, agent):
        s = self.update_agent(action, agent) # move agent
        s_ = self.canvas.coords(agent)  # next state
        return self.update_reward(s_, s)
        #return update_agent_and_rewards(action, agent)


    def get_state(self, agent):
        return self.canvas.coords(agent)  # current status

    def render(self):
        time.sleep(0.001)
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