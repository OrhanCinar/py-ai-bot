import numpy as np
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

env = make(ENV_NAME)  # make the environment

file_name = '..\\data\\indicators.csv'
feature_list = [
                "O",
                "H",
                "L",
                "V",
                "VWap",
                "EMA5", "EMA10", "EMA20", "EMA50", "EMA100", "EMA200",
                "trend_ichimoku_a",
                "trend_ichimoku_b",
                "trend_visual_ichimoku_a",
                "trend_visual_ichimoku_b",

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

env.init_file(file_name, feature_list, trade_cost)


for i in range(10):
    obv = env.reset()
    for j in range(400000):
        env.render(mode='human', close=False)
        # action = np.random.randint(-1, 1)

        # print(np.ndarray(action))
        # print('obv', obv)
       
        action = [random.choice(env.actions) for ob in obv][0]
        # print('action', action)
        observation, reward, done, info= env.step(action)

        if done:
            break

env.close()
