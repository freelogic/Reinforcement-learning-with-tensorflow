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
2. 让两个agent一起跑来比较了;很清晰exp指数比非指数快的多,更快锁定天堂吃肉;

TODO:
2.5 TODO 要让指数agent不能穿透hell直达天堂,比如d4,下降4格子就到天堂,但是路上穿透地狱hell,这应该不行的;
3. TODO 最好能有动态的记分（-1，+1的总计分数，时间，episode，等等）
4. TODO 增加难度，增加动态的布景，看两个boy的适应能力；

"""



from contents.PART_2_Q_Learning_maze.maze_env import Maze
from contents.PART_2_Q_Learning_maze.RL_brain import QLearningTable
from contents.tool.utils import display_progress

display_interval = 5 # display steps in procedure, it make program VERY SLOW!
MAX_EPISODES = 400

def update(RL):
    #for episode in range(MAX_EPISODES):
        # initial observation
        #observation = env.reset()
    observation = env.reset_all_agent()
    episode=0

    while True:
        for rl in RL:
            brain = rl[0]
            agent = rl[1]
            # fresh env
            env.render()
            observation = env.get_state(agent)

            # RL choose action based on observation
            action = brain.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action,agent)

            # RL learn from this transition
            brain.learn(str(observation), action, reward, str(observation_))

            # swap observation
            #observation = observation_
            observation = env.get_state(agent)

            # break while loop when end of this episode
            if done:
                 observation = env.reset_agent(agent)
                 episode = episode + 1
                 #break #永久跑下去,直到累计成功/失败总计超过MAX_EPISODES就退出

            if episode >= MAX_EPISODES:
                exit(0)


            if episode % display_interval  == 1:
                display_progress(int(episode / MAX_EPISODES * 100))  # 显示命令行进度


    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    #RL = QLearningTable(actions=list(range(env.n_actions)))
    brain1 = QLearningTable(actions=env.action_space)
    brain2 = QLearningTable(actions=env.action_space_exp)

    RL=[]
    RL.append([brain1,env.create_agent('red')])
    RL.append([brain2,env.create_agent('blue')])
    env.after(100, update(RL))
    env.mainloop()

