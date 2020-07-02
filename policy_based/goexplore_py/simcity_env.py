import gym
from gym_city.envs.env import MicropolisEnv
from atari_reset.atari_reset.wrappers import MyWrapper
from collections import OrderedDict
from typing import Tuple
import numpy as np

class MySimCity(MyWrapper):
    max_steps = 200
    screen_width = 36
    screen_height = 36
    x_repeat = 1
    #FIXME: should probably be up to simcity env itself
    param_bounds = OrderedDict({
            'res_pop': (0, 750),
            'com_pop': (0, 100),
            'ind_pop': (0, 100),
           #'traffic': (0, 5000),
           #'mayor_rating': (0, 100)
           #'num_plants': (0, 100),
            })

    @staticmethod
    def get_attr_max(name):
        return MySimCity.param_bounds[name][1]



    def __init__(self,
                 env,
                 cell_representation=None):
        super(MySimCity, self).__init__(env)
        self.env.unwrapped.seed(0)
        self.state = []
        self.cur_steps = 0
        self.total_steps = 0
        self.cur_score = 0
        MySimCity.env = env
        MySimCity.screen_width = self.MAP_X
        MySimCity.screen_height = self.MAP_Y
        self.env_name = 'Micropolis'
        self.cell_representation = cell_representation
        self.done = 0

    def step(self, action) -> Tuple[np.ndarray, float, bool, dict]:
        print('STEP START')
        unprocessed_state, reward, done, lol = self.env.step(action)
        self.state.append(unprocessed_state)
        self.state.pop(0)
        self.cur_steps += 1
        self.total_steps += 1

        if self.cur_steps >= MySimCity.max_steps:
            done = True

        self.pos_from_simcity()

        self.cur_score += reward

        if done:
            self.res_pop = 0
            self.com_pop = 0
            self.ind_pop = 0
            self.done = 1
        self.pos = self.cell_representation(self)

        print('DONE STEP')
        return unprocessed_state, reward, done, lol

    def reset(self) -> np.ndarray:
        unprocessed_state = self.env.reset()
       #self.state = [convert_state(unprocessed_state)]
        self.cur_score = 0
        self.cur_steps = 0
        self.pos = None
        self.pos_from_simcity()
        self.pos = self.cell_representation(self)
        print('self pos', self.cell_representation(self))
        self.done = 0
        return unprocessed_state

    def pos_from_simcity(self):
        self.res_pop = self.metrics['res_pop']
        self.com_pop = self.metrics['com_pop']
        self.ind_pop = self.metrics['ind_pop']
        

    def __getattr__(self, e):
        return getattr(self.env, e)

    def get_my_simcity(self):
        return self

    def get_pos(self):
        assert self.pos is not None
        return self.pos

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, ob):
        self.__dict__ = ob

