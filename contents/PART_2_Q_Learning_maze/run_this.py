"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""



"""
1. 尝试指数方法；速度非常快,对于大地图也收敛很快;

TODO:
2. TODO 让两个boy一起跑来比较； 
3. TODO 最好能有动态的记分（-1，+1的总计分数，时间，episode，等等）
4. TODO 增加难度，增加动态的布景，看两个boy的适应能力；

"""



from contents.PART_2_Q_Learning_maze.maze_env import Maze
from contents.PART_2_Q_Learning_maze.RL_brain import QLearningTable
from contents.tool.utils import display_progress

display_steps = True # display steps in procedure, it make program VERY SLOW!
MAX_EPISODES = 400

def update():
    for episode in range(MAX_EPISODES):
        # initial observation
        observation = env.reset()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break

            if display_steps == True:
                display_progress(int(episode / MAX_EPISODES * 100))  # 显示命令行进度


    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    #RL = QLearningTable(actions=list(range(env.n_actions)))
    #RL = QLearningTable(actions=env.action_space)
    RL = QLearningTable(actions=env.action_space_exp)
    env.after(100, update)
    env.mainloop()

