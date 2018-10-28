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
说明: 此代码是基于开源github项目morvan的强化学习教育视频和TF实现源码的例子而来,因为其简单易学,用来尝试新的方法成本比较低;
再次特别对morvan大神表示感谢! 如有任何涉及版权等问题,请积极联系我本人给予配合处理,谢谢!

1. 尝试指数方法；速度非常快,对于大地图也收敛很快;
2. 让两个agent一起跑来比较了;很清晰exp指数比非指数快的多,更快锁定天堂吃肉;
3  实现了让指数agent不能穿透hell直达天堂,比如d4,下降4格子就到天堂,但是路上穿透地狱hell,这应该不行,且等价于进入hell死亡扣分;
4. 增加了简陋的动态的记分（reward）

TODO:
4. TODO 将env和agent面向对象化, 布景支持模板,且可以旋转,但时间间隔变化,还能发射子弹等待；
5. TODO 增加多维度的指数队列,来记忆动作(可能留给cartpole或者开小车游戏等更能体现出效果的agent实验项目再实现,看情况);

"""



from contents.PART_2_Q_Learning_maze.maze_env import Maze
from contents.PART_2_Q_Learning_maze.RL_brain import QLearningTable
from contents.tool.utils import display_progress

display_interval = 2 # display steps in procedure, it make program VERY SLOW!
MAX_EPISODES = 400
K = [0,1];

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
            agent_name = rl[2]

            # fresh env
            env.render()
            observation = env.get_state(agent)

            # RL choose action based on observation
            action = brain.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action,agent)
            rl[3] += reward

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
                 score_summary = "{0}: score=[{1}]".format(agent_name, rl[3])

            if episode >= MAX_EPISODES:
                exit(0)

            #score_summary = "{0}: score=[{1}]".format(agent_name,agent_score)
            if episode % display_interval  == 1:
                display_progress(int(episode / MAX_EPISODES * 100), score_summary)  # 显示命令行进度


    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Maze();  RL=[]; brain=[]; agent=[]; agent_name=['red','blue']
    #RL = QLearningTable(actions=list(range(env.n_actions)))
    brain.append(QLearningTable(actions=env.action_space))
    brain.append(QLearningTable(actions=env.action_space_exp))

    agent.append(env.create_agent(agent_name[0]))
    agent.append(env.create_agent(agent_name[1]))

    for k in K:
        RL.append([brain[k],agent[k],agent_name[k],0])

    env.after(100, update(RL))
    env.mainloop()

