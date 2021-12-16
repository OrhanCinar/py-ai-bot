import pandas as pd
import numpy as np
import gym
import Binance.binanceEnvironment as b

env = gym.make('CartPole-v1')

state_size = env.observation_space.shape[0]
action_size = env.action_space.n
state = env.reset()

# print("cartpole state_size", state_size)
# print("cartpole state", state)
# print("cartpole state type", state.shape)

env = b.BinanceEnvironment()
env.init("data\\test.csv", total_budget=100.0,
         budget_per_trade=5.0, render=True)
#state_binance = env.get_state()

print(env.get_data_frame().iloc[0, -1:])


# print("binance state", state_binance)
# print("binance state type", state_binance.shape)

# x = state_binance.reshape(11, )

# print("x state", x[0])
# print("x state type", x.shape)

#df = env.get_data_frame()

#print("binance df", df)
