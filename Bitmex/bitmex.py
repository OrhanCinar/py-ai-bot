import numpy as np
from sklearn import preprocessing
from gym.envs.registration import register, make
import gym
import random

ENV_NAME = 'bitmexEnvironment-v0'

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


def getstate(observation):
    print(observation.item(0))
    print(observation.item(1))
    myData = [10000, 9500]
    scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform([np.float32(myData)])


    print("scaled", scaled)
    # o = int(np.digitize(observation.item(0), theta_dot_space))
    # h = int(np.digitize(observation.item(1), theta_dot_space))
    # l = int(np.digitize(observation.item(2), theta_dot_space))
    # v = int(np.digitize(observation.item(3), theta_dot_space))
    # vwap = int(np.digitize(observation.item(4), theta_dot_space))
    # ema5 = int(np.digitize(observation.item(5), theta_dot_space))
    # ema10 = int(np.digitize(observation.item(6), theta_dot_space))
    # ema20 = int(np.digitize(observation.item(7), theta_dot_space))
    # ema50 = int(np.digitize(observation.item(8), theta_dot_space))
    # ema100 = int(np.digitize(observation.item(9), theta_dot_space))
    # ema200 = int(np.digitize(observation.item(10), theta_dot_space))
    # cloud_a = int(np.digitize(observation.item(11), theta_dot_space))
    # cloud_b = int(np.digitize(observation.item(12), theta_dot_space))
    # rsi = int(np.digitize(observation.item(13), theta_dot_space))
    # mfi = int(np.digitize(observation.item(14), theta_dot_space))
    # bbh = int(np.digitize(observation.item(15), theta_dot_space))
    # bbl = int(np.digitize(observation.item(16), theta_dot_space))
    # bbm = int(np.digitize(observation.item(17), theta_dot_space))
    # bb_vol_h = int(np.digitize(observation.item(18), theta_dot_space))
    # bb_vol_l = int(np.digitize(observation.item(19), theta_dot_space))

    # TimeFrame;O;H;L;C;V;VWap;OpenTime;CloseTime;EMA5;EMA10;EMA20;EMA50;EMA100;EMA200;
    # trend_ichimoku_a;trend_ichimoku_b;momentum_rsi;momentum_mfi;volatility_bbh;volatility_bbl;volatility_bbm;volatility_bbhi;volatility_bbli


    # return (o,h,l,v,vwap,ema5,ema10,ema20,ema50,ema100,ema200,cloud_a,cloud_b,rsi,mfi,bbh,bbl,bbm,bb_vol_h,bb_vol_l)
    return (0)

env=make(ENV_NAME)  # make the environment

file_name='..\\data\\indicators_light.csv'
feature_list=[
                "O",
                "H",
                "L",
                "V",
                "VWap",
                "EMA5", "EMA10", "EMA20", "EMA50", "EMA100", "EMA200",
                "trend_ichimoku_a",
                "trend_ichimoku_b",
                # "trend_visual_ichimoku_a",
                # "trend_visual_ichimoku_b",

                "momentum_rsi",
                "momentum_mfi",
                "volatility_bbh",
                "volatility_bbl",
                "volatility_bbm",
                "volatility_bbhi",
                "volatility_bbli"

                # "trend_macd",
                # "trend_macd_signal",
                # "trend_macd_diff",
                # "volume_adi",
                # "volume_obv",
                # "volume_cmf",
                # "volume_fi",
                # "volume_em",
                # "volume_vpt",
                # "volume_nvi",
                # "volatility_atr",

                # "volatility_kcc",
                # "volatility_kch",
                # "volatility_kcl",
                # "volatility_kchi",
                # "volatility_kcli",
                # "volatility_dch",
                # "volatility_dcl",
                # "volatility_dchi",
                # "volatility_dcli",

                # "trend_ema_fast",
                # "trend_ema_slow",
                # "trend_adx",
                # "trend_adx_pos",
                # "trend_adx_neg",
                # "trend_vortex_ind_pos",
                # "trend_vortex_ind_neg",
                # "trend_vortex_diff",
                # "trend_trix",
                # "trend_mass_index",
                # "trend_cci",
                # "trend_dpo",
                # "trend_kst",
                # "trend_kst_sig",
                # "trend_kst_diff",
                # "trend_aroon_up",
                # "trend_aroon_down",
                # "trend_aroon_ind",

                # "momentum_tsi",
                # "momentum_uo",
                # "momentum_stoch",
                # "momentum_stoch_signal",
                # "momentum_wr",
                # "momentum_ao",
                # "momentum_kama",
                # "others_dr",
                # "others_dlr",
                # "others_cr"

        ]
trade_cost = 0


#env.init_file(file_name, feature_list, trade_cost)

obv = env.reset()

#print(getstate(obv))

action_space = [-1, 0, 1]

states = []

# for o in range(10000):
#     for h in range(10000):
#         states.append((o,h))

Q = {}

for state in states:
    for action in action_space:
        Q[state, action] = 0

# print("Q",Q)
#print("env", env.actions)

for i in range(1):
    obv = env.reset()
    # print(getstate(obv))

    for j in range(1):
        env.render(mode='human', close=False)
        # action = np.random.randint(-1, 1)

        # print(np.ndarray(action))
        # print('obv', obv)


        action = random.choice(env.actions)
        # print('action', action)
        observation, reward, done, info = env.step(action)
        # print("observation_space",env.observation_space)

        if done:
            break

env.close()
