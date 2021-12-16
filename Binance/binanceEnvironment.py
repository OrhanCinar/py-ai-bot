import pandas as pd
import numpy as np


class BinanceEnvironment():

    def __init__(self):
        self.t = 0  # time frame Id
        self.actions = ['Buy', 'Sell', 'Hold']
        self.enter_price = 0
        self.exit_price = 0
        self.buy_dateime = None
        self.sell_datetime = None
        self.completed_actions = []
        self.current_account_total = 0
        self.start_account_total = 0
        self.budget_per_trade = 0
        self.reward = 0
        self.rewards = []
        self.stop_loss = 0.01  # stop loss percentage
        self.open_position = 'None'
        self.state_size = 0

    def init(self, file_name, total_budget, budget_per_trade, render=False):

        # drive.mount('/content/gdrive')
        self.start_account_total = total_budget
        self.budget_per_trade = budget_per_trade
        self.file_name = file_name

        df_test = pd.read_csv(file_name, sep=";", nrows=100)

        float_cols = [c for c in df_test if df_test[c].dtype == "float64"]
        float32_cols = {c: np.float32 for c in float_cols}
        #print("float32_cols", float32_cols)
        self.df = pd.read_csv(file_name, sep=";", header=None,
                              engine='c', dtype=float32_cols)
        self.df.dropna(inplace=True)
        self.state_size = self.df.iloc[self.t][:-2].shape[0]+1
        self.render = render

    def get_data_frame(self):
        return self.df

    def get_actions(self):
        return self.actions

    def get_state(self):
        df = self.df.iloc[self.t][:-2]
        # print("self.state_size", self.state_size)
        # print("df.state_size", df.shape)

        state = np.append(df.to_numpy(), 0, axis=None).reshape(
            self.get_state_size(), )
#        print("state", state.shape)
        self.t += 1
        return state

    def get_state_size(self):
        return self.df.iloc[self.t][:-2].shape[0]+1

    def get_rewards(self):
        return self.rewards

    def get_rewards_sum(self):
        return sum(self.rewards)

    def get_current_price(self):
        return self.df.iloc[self.t][0]

    def step(self, action):
        stop_loss_reached = None
        current_price_diff = self.enter_price*self.stop_loss  # 170

        if current_price_diff > 0 and self.open_position == 'Sell':
            #17000 >= 17000 + 170
            stop_loss_reached = self.get_current_price() <= self.get_current_price() + \
                current_price_diff

        if current_price_diff > 0 and self.open_position == 'Buy':
            stop_loss_reached = self.get_current_price() >= self.get_current_price() - \
                current_price_diff

        #print("stop_loss_reached", stop_loss_reached, current_price_diff)

        self.calculate_reward()

        if stop_loss_reached and self.open_position == 'Sell':  # stop loss for short position
            self.exit_short()
            action_desc = 'Close Sell Stop Loss'
        elif stop_loss_reached and self.open_position == 'Buy':  # stop loss for long position
            self.exit_long()
            action_desc = 'Close Buy Stop Loss'

        elif self.open_position == 'None' and action == 'Sell':  # open short position
            action_desc = 'Open Sell'
            self.enter_short()
        elif self.open_position == 'None' and action == 'Buy':  # open long position
            action_desc = 'Open Buy'
            self.enter_long()
        elif self.open_position == 'Sell' and action == 'Buy':  # close short position with buy
            action_desc = 'Close Sell'
            self.exit_short()
        elif self.open_position == 'Buy' and action == 'Sell':  # close long position with sell
            action_desc = 'Close Buy'
            self.exit_long()
        else:
            action_desc = "NOP"

        # print(action_desc)

        done = self.df.shape[0] == self.t
        reward = self.reward

        #next_state = self.get_state()
        next_state = np.append(self.get_state().to_numpy(),
                               0, axis=None).reshape(self.get_state_size(), )

        return next_state, reward, done, {}

    def reset(self):
        self.buy_price = 0
        self.sell_price = 0
        self.buy_dateime = None
        self.sell_datetime = None
        self.completed_actions = []
        self.current_account_total = 0

    def calculate_trade(self):
        return self.budget_per_trade / self.get_current_price()

    def calculate_reward(self):
        if self.open_position == 'Buy':
            self.reward = (self.get_current_price() -
                           self.enter_price) * self.calculate_trade()
        elif self.open_position == 'Sell':
            self.reward = (self.enter_price - self.get_current_price()
                           ) * self.calculate_trade()
        self.rewards.append(self.reward)

    def enter_long(self):
        self.enter_price = self.get_current_price()
        if self.render:
            print(self.t, "- E_L:", self.open_position.ljust(6, ' '),
                  self.enter_price, self.exit_price, self.reward)
        self.exit_price = 0

        self.current_account_total -= self.calculate_trade()
        self.open_position = 'Buy'

    def exit_long(self):
        self.exit_price = self.get_current_price()
        if self.render:
            print(self.t, "- X_L:", self.open_position.ljust(6, ' '),
                  self.enter_price, self.exit_price, self.reward)
        self.enter_price = 0
        self.open_position = 'None'
        self.completed_actions.append("Buy" + str(self.enter_price))

    def enter_short(self):
        self.enter_price = self.get_current_price()
        if self.render:
            print(self.t, "- E_S:", self.open_position.ljust(6, ' '),
                  self.enter_price, self.exit_price, self.reward)
        self.exit_price = 0
        self.current_account_total += self.calculate_trade()
        self.open_position = 'Sell'

    def exit_short(self):
        self.exit_price = self.get_current_price()
        if self.render:
            print(self.t, "- X_S:", self.open_position.ljust(6, ' '),
                  self.enter_price, self.exit_price, self.reward)
        self.enter_price = 0
        self.open_position = 'None'
        self.completed_actions.append("Sell" + str(self.exit_price))

    def get_account(self):
        return self.current_account_total
