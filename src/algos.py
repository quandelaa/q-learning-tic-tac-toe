from board import TTTGame
from random import random, choice

class TTTBot:
    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        old_q = self.get_q_val(old_state, action)
        best_new_action = self.best_future_action(new_state)

        self.update_q_value(old_state, action, old_q, reward, best_new_action)

    def get_q_val(self, state, action):
        q = self.q.get((tuple(state), action))

        return q if q is not None else 0
    
    def best_future_action(self, state):
        availables = TTTGame.available_actions(state)

        if not availables:
            return 0
        
        best_q = -100

        for action in availables:
            q = self.q.get((tuple(state), action))

            if q is None:
                q = 0

            if q > best_q:
                best_q = q
        
        return best_q
    
    def update_q_value(self, state, action, old_q, reward, best_reward):

        self.q[(tuple(state), action)] = old_q + self.alpha * ((reward + best_reward) - old_q)

    def choose_action(self, state, q_state, use_epsilon=False):
        availables = TTTGame.available_actions(state)

        best_q = -100
        best_action = None

        for action in availables:
            q = self.q.get((tuple(q_state), action))

            if q is None:
                q = 0

            if q > best_q:
                best_q = q
                best_action = action

        if not use_epsilon:
            return best_action
        
        if self.epsilon > random():
            try:
                return tuple(choice(availables))
            except IndexError:
                return best_action
        else:
            return best_action
