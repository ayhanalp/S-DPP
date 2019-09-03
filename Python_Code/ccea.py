import numpy as np
from AADI_RoverDomain.parameters import Parameters as p
import random

class Ccea:

    def __init__(self):
        self.mut_prob = p.mutation_rate
        self.epsilon = p.epsilon
        self.n_populations = p.num_rovers  # One population for each rover
        self.parent_pop_size = p.parent_pop_size
        self.offspring_pop_size = p.offspring_pop_size
        self.total_pop_size = p.parent_pop_size + p.offspring_pop_size  # Number of policies in each pop
        n_inputs = p.num_inputs; n_outputs = p.num_outputs; n_nodes = p.num_nodes
        self.policy_size = (n_inputs + 1)*n_nodes + (n_nodes + 1) * n_outputs  # Number of weights for NN
        self.pops = np.zeros((self.n_populations, self.total_pop_size, self.policy_size))
        self.parent_pop = np.zeros((self.n_populations, self.parent_pop_size, self.policy_size))
        self.offspring_pop = np.zeros((self.n_populations, self.offspring_pop_size, self.policy_size))
        self.fitness = np.zeros((self.n_populations, self.total_pop_size))
        self.team_selection = np.ones((self.n_populations, self.parent_pop_size)) * (-1)

    def reset_populations(self):  # Re-initializes CCEA populations for new run
        self.pops = np.zeros((self.n_populations, self.total_pop_size, self.policy_size))
        self.parent_pop = np.zeros((self.n_populations, self.parent_pop_size, self.policy_size))
        self.offspring_pop = np.zeros((self.n_populations, self.offspring_pop_size, self.policy_size))
        self.fitness = np.zeros((self.n_populations, self.total_pop_size))
        self.team_selection = np.ones((self.n_populations, self.parent_pop_size)) * (-1)

        for pop_index in range(self.n_populations):
            for policy_index in range(self.parent_pop_size):
                for w in range(self.policy_size):
                    weight = np.random.normal(0, 1)
                    if weight > 1.0:
                        weight = 1.0
                    if weight < -1.0:
                        weight = -1.0
                    self.parent_pop[pop_index, policy_index, w] = weight
            for policy_index in range(self.offspring_pop_size):
                for w in range(self.policy_size):
                    weight = np.random.normal(0, 1)
                    if weight > 1.0:
                        weight = 1.0
                    if weight < -1.0:
                        weight = -1.0
                    self.offspring_pop[pop_index, policy_index, w] = weight

        self.combine_pops()

    def select_policy_teams(self):  # Create policy teams for testing
        self.team_selection = np.ones((self.n_populations, self.total_pop_size)) * (-1)

        for pop_id in range(self.n_populations):
            for policy_id in range(self.total_pop_size):
                rpol = random.randint(0, (self.total_pop_size - 1))  # Select a random policy from pop
                k = 0
                while k < policy_id:  # Check for duplicates
                    if rpol == self.team_selection[pop_id, k]:
                        rpol = random.randint(0, (self.total_pop_size - 1))
                        k = -1
                    k += 1
                self.team_selection[pop_id, policy_id] = rpol  # Assign policy to team

    def mutate(self):  # Mutate policy based on probability
        for pop_index in range(self.n_populations):
            policy_index = 0
            mutate_n = int(p.percentage_mut * self.policy_size)
            if mutate_n == 0:
                mutate_n = 1
            while policy_index < self.offspring_pop_size:
                rnum = random.uniform(0, 1)
                if rnum <= self.mut_prob:
                    for w in range(mutate_n):
                        target = random.randint(0, (self.policy_size - 1))  # Select random weight to mutate
                        weight = np.random.normal(0, 1)
                        if weight > 1.0:
                            weight = 1.0
                        if weight < -1.0:
                            weight = -1.0
                        self.offspring_pop[pop_index, policy_index, target] = weight
                policy_index += 1

    def epsilon_greedy_select(self):  # Choose K solutions
        for pop_id in range(self.n_populations):
            policy_id = 0
            while policy_id < self.parent_pop_size:
                rnum = random.uniform(0, 1)
                if rnum >= self.epsilon:  # Choose best policy
                    pol_index = np.argmax(self.fitness[pop_id])
                    self.parent_pop[pop_id, policy_id] = self.pops[pop_id, pol_index].copy()
                else:
                    parent = random.randint(0, (self.total_pop_size-1))  # Choose a random parent
                    self.parent_pop[pop_id, policy_id] = self.pops[pop_id, parent].copy()
                policy_id += 1

    def down_select(self):  # Create a new offspring population using parents from top 50% of policies
        self.epsilon_greedy_select()  # Select K solutions using epsilon greedy
        self.offspring_pop = self.parent_pop.copy()  # Produce K offspring
        self.mutate()  # Mutate offspring population
        self.combine_pops()

    def combine_pops(self):
        for pop_id in range(self.n_populations):
            off_pol_id = 0
            for pol_id in range(self.total_pop_size):
                if pol_id < self.parent_pop_size:
                    self.pops[pop_id, pol_id] = self.parent_pop[pop_id, pol_id].copy()
                else:
                    self.pops[pop_id, pol_id] = self.offspring_pop[pop_id, off_pol_id].copy()
                    off_pol_id += 1
