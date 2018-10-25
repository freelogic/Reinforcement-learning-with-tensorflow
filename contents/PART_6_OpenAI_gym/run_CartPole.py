"""
Deep Q network,

Using:
Tensorflow: 1.0
gym: 0.7.3
"""

"""
CC: 这个线性agent因为可以撰写环境反馈程序，所以简单的增加指数级的ACTION并更新环境反馈函数就行了；
比如cartpole这个agent因为是通过物理环境反馈的小车速度和位置，杆子的角度和速度，所以无法更新环境反馈代码，所以需要直接设计一个外挂的指数级别的ACTION积累函数，其实就是长短记忆！！！
看是否能利用神经网络引入指数效果？神经网络的框架还是不错的。
"""

import gym
from contents.PART_6_OpenAI_gym.RL_brain import DeepQNetwork

env = gym.make('CartPole-v0')
env = env.unwrapped

print(env.action_space)
print(env.observation_space)
print(env.observation_space.high)
print(env.observation_space.low)

RL = DeepQNetwork(n_actions=env.action_space.n,
                  n_features=env.observation_space.shape[0],
                  learning_rate=0.01, e_greedy=0.9,
                  replace_target_iter=100, memory_size=2000,
                  e_greedy_increment=0.001,)

total_steps = 0
print(env.action_space.n)
print(env.observation_space.shape)


for i_episode in range(100):

    observation = env.reset()
    ep_r = 0
    while True:
        env.render()

        action = RL.choose_action(observation)

        observation_, reward, done, info = env.step(action)

        # the smaller theta and closer to center the better
        x, x_dot, theta, theta_dot = observation_
        r1 = (env.x_threshold - abs(x))/env.x_threshold - 0.8
        r2 = (env.theta_threshold_radians - abs(theta))/env.theta_threshold_radians - 0.5
        reward = r1 + r2

        RL.store_transition(observation, action, reward, observation_)

        ep_r += reward
        if total_steps > 1000:
            RL.learn()

        if done:
            print('episode: ', i_episode,
                  'ep_r: ', round(ep_r, 2),
                  ' epsilon: ', round(RL.epsilon, 2))
            break

        observation = observation_
        total_steps += 1

RL.plot_cost()
