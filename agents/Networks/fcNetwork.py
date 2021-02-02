# =============================================
# Class Definition of Fully Connected Neural Network
# =============================================
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class Network(nn.Module):
    def __init__(self, input_dims, n_actions, layers = [30, 30], lr = 0.001):
        super(Network, self).__init__()
        self.input_dims = input_dims
        self.n_actions = n_actions

        self.lr = lr

        # build 2 headed network 
        fc_layers = [nn.Linear(input_dims, layers[0]), nn.ReLU()]

        for i in range(len(layers) - 1):
            fc_layers.append(nn.Linear(layers[i], layers[i + 1]))
            fc_layers.append(nn.ReLU())
        
        self.evaluator = nn.Sequential(*fc_layers)

        self.policy = nn.Linear(layers[-1], self.n_actions)
        self.value = nn.Linear(layers[-1], 1)

        # optimizer
        self.optimizer = optim.Adam(self.parameters(), lr=self.lr)

        # setup device
        # self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu:0')
        self.device = torch.device('cpu:0')
        self.to(self.device)

    def forward(self, observation):
        """
        Inputs:
            - Observation
        Outputs:
            - Extimate of the probablity distribution over action space (ie. policy), estimate of state value
        """

        state = torch.Tensor(observation).to(self.device) 
        psi = self.evaluator(state)
        
        return F.softmax(self.policy(psi)), self.value(psi)