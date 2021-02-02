# ==========================
# Class Definition of A2C Agent
# ==========================
import torch
import torch.nn.functional as F
import numpy as np
from collections import namedtuple
from agents.Caches.transition_cache import Transition_Cache
from agents.Networks.fcNetwork import Network

Transition = namedtuple('Transition', 'state, action, reward, done, next_state, target')

class A2CAgent():
    def __init__(self, input_dims, output_dims, network=None, **kwargs):
        # Optional arguments (kwargs)
        self.cache_size = kwargs.get("cache_size", 10000)
        self.gamma = kwargs.get("gamma", 0.98)
        self.name = kwargs.get("name", "")
        self.critic_weight = kwargs.get("critic_weight", 0.5)
        networkLayers = kwargs.get("layers", [30, 20, 10])

        # set network
        self.nn = kwargs.get('network', Network(input_dims, output_dims, lr=0.005, layers=networkLayers))

        # create new transition cache
        self.trajectories = []

    def choose_action(self, observation): 
        """
        Inputs:
            - Observation/state
        Outputs:
            - Action selected based on neural network
        """

        self.state = observation

        with torch.no_grad():
            policy, _ = self.nn(self.state)

            # calculate action based on policy returned
            a = torch.distributions.Categorical(policy)
            selected_action = a.sample()
            action = selected_action.unsqueeze(0)

            return action.detach().clone()

    def learn(self, clear_cache = True):
        """
        No required I/O.
        Function: updates the neural network based on results from collected trajectories
        """

        for trajectory in self.trajectories: # updates agent based on what it learns from each trajectory
            log_probs = []
            values = []
            targets = []

            _, last_value = self.nn(trajectory.transition_cache[-1].next_state)
            last_value = last_value.item()

            trajectory.transition_cache = self.discount_rwds(trajectory.transition_cache, last_value) # Calculates the discounted rewards

            # calculates log_probs and values for each state
            for transition in trajectory.transition_cache:
                policy, value = self.nn(transition.state)
                values.append(value)
                targets.append(torch.FloatTensor([transition.target]))
                log_probs.append(torch.distributions.Categorical(policy).log_prob(transition.action))
            
            # calculates loss
            log_probs = torch.cat(log_probs)
            values = torch.cat(values)
            targets = torch.cat(targets)
            advantages = targets - values

            actor_loss  = -(log_probs * advantages).mean()
            critic_loss = advantages.pow(2).mean()

            loss = actor_loss + 0.5 * critic_loss

            self.nn.optimizer.zero_grad()
            loss.backward()
            self.nn.optimizer.step()
            
            if clear_cache: trajectory.clear_cache() 
        
        if clear_cache: self.trajectories.clear()
    
    def store_trajectory(self, trajectory):
        """
        Inputs:
            - Trajectory (ie. list) of transitions to be stored in a transition cache
        
        No outputs.
        """

        new_cache = Transition_Cache(self.cache_size)
        for transition in trajectory: # trajectory is a list of tuples
            new_transition = Transition(state=transition[0], action=transition[1], reward=transition[2], next_state = transition[3], done=transition[4], target=-1)
            new_cache.store_transition(new_transition)
        self.trajectories.append(new_cache)

    def discount_rwds(self, transitions, last_value):
        """
        Inputs:
            - an entire trajectory
            - the value of the last state which wouldn't otherwise be included
        Outputs:
            - the same trajectory with discounted reward calculated for each transition
        """

        running_add = last_value
        for t in reversed(range(len(transitions))):
            running_add = (1 - transitions[t].done)*running_add*self.gamma + transitions[t].reward
            transitions[t] = transitions[t]._replace(target = running_add)
        return transitions