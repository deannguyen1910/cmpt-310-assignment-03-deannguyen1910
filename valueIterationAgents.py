# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            values = self.values.copy() # it is fetched every state (not whole table) ... so make a temp Value to create the table we doing
            for state in self.mdp.getStates():
                self.values[state] = float(self.computeValueFromQValues(state, values))

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        value = 0.0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            value += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
        return float(value)
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        if self.mdp.isTerminal(state):
            return None

        value, saveAction = -float('inf'), None
        for action in self.mdp.getPossibleActions(state):
            temp = self.computeQValueFromValues(state, action)
            if value < temp:
                value, saveAction = temp, action

        return saveAction
        util.raiseNotDefined()

    def computeQValueFromValues2(self, state, action, values):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        value = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            value += prob * (self.mdp.getReward(state, action, nextState) + self.discount * values[nextState])
        return value
        util.raiseNotDefined()

    def computeValueFromQValues(self, state, values):
        """
        Return max Q Value
        """
        #self.values[state] = -float('inf')
        tempvalue = -float('inf')

        for action in self.mdp.getPossibleActions(state):
            temp = self.computeQValueFromValues2(state, action, values)
            tempvalue = max(tempvalue, temp)
        if tempvalue == -float('inf'):
            tempvalue = 0.0
        return float(tempvalue)

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            state = self.mdp.getStates()[i %  len(self.mdp.getStates())]
            action = self.computeActionFromValues(state)
            if action == None:
                self.values[state] = 0.0
            else:
                self.values[state] = float(self.computeQValueFromValues(state, action))


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def getNextStates(self, state, predecessors):
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
            for nextState, prob in nextStates:
                if prob > 0:
                    predecessors[nextState].append(state)

    def predecessorsOfAllStates(self, states):
        predecessors = util.Counter()
        for state in states: 
            predecessors[state] = list()
        for state in states:
            self.getNextStates(state, predecessors)
        return predecessors
    
    def buildPriorityQueue(self, states):
        q = util.PriorityQueue()
        for state in states:
            diff = abs(self.values[state] - self.computeValueFromQValues(state, self.values))
            q.push(state, -diff)

        return q

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        predecessors = self.predecessorsOfAllStates(states)
        
        q = self.buildPriorityQueue(states)
        
        for i in range(self.iterations):
            if q.isEmpty():
                return
            state = q.pop()
            self.values[state] = self.computeValueFromQValues(state, self.values)
            for predecessor in predecessors[state]:
                diff = abs(self.values[predecessor] - self.computeValueFromQValues(predecessor, self.values))
                if diff > self.theta:
                    q.update(predecessor, -diff)