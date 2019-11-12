import numpy as np
from sklearn import preprocessing
from gym.envs.registration import register, make
import gym
import random
import matplotlib.pyplot as plt
from array import *

ENV_NAME = 'bitmexEnvironment-v0'
EPISODES = 10

if ENV_NAME in gym.envs.registry.env_specs:
    del gym.envs.registry.env_specs[ENV_NAME]

# registration
register(
    id=ENV_NAME,
    entry_point='bitmexLib:bitmexEnvironment',
    max_episode_steps=10000,
)
theta_space = np.linspace(-1, 1, 10)
theta_dot_space = np.linspace(0, 10000, 10)


env = make(ENV_NAME)  # make the environment

file_name = '..\\data\\small_batch.csv'
feature_list = ["O_Scaled", "H_Scaled", "L_Scaled", "C_Scaled", "V_Scaled", "VWap_Scaled",
                "EMA5_Scaled", "EMA10_Scaled", "EMA20_Scaled", "EMA50_Scaled", "EMA100_Scaled", "EMA200_Scaled",
                "trend_ichimoku_a_Scaled", "trend_ichimoku_b_Scaled", "momentum_rsi_Scaled", "momentum_mfi_Scaled",
                "volatility_bbh_Scaled", "volatility_bbl_Scaled", "volatility_bbm_Scaled", "volatility_bbhi_Scaled", "volatility_bbli_Scaled"
                ]
trade_cost = 0


env.init_file(file_name, feature_list, trade_cost)

obv = env.reset()

# print(getstate(obv))

action_space = [-1, 0, 1]

states = []

# for o in range(10000):
#     for h in range(10000):
#         states.append((o,h))

Q = {}

# for state in states:
#     for action in action_space:
#         Q[state, action] = 0

# print("Q",Q)
# print(env.observation_space)
# print("env", env.actions)
totalrewardarr = np.zeros(shape=(EPISODES, 1400))
totalrewards = 0

for i in range(EPISODES):
    obv = env.reset()
    # print(getstate(obv))

    for j in range(1400):
        env.render(mode='human', close=False)
        # action = np.random.randint(-1, 1)

        # print(np.ndarray(action))
        # print('obv', obv)

        action = random.choice(action_space)
        # print('action', action)
        observation, reward, done, info = env.step(action)
        totalrewards += reward
        totalrewardarr[i][j] = totalrewards
        # print("observation_space",env.observation_space)

        if done:
            break

env.close()

# for i in range(EPISODES):
#     plt.figure()
#     plt.plot(totalrewardarr[i])

# plt.show()
