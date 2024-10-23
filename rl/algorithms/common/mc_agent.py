from rl.algorithms.common.base_agent import BaseAgent
from rl.common.q_value_table import QValueTable
from rl.common.results_logger import ResultsLogger
import numpy as np
from typing import Tuple, List, Union


class StateActionStats:
    """
    Implements N(s, a) for Monte Carlo averaging:
    Q(s, a) <- Q(s, a) + 1/N(s, a) * (G - Q(s, a))
    In case of off-policy learning, tracks cumulative sum of importance sampling ratios.

    Args:
        state_space_shape (Tuple[int, ...]): Shape of the state space.
        action_space_shape (int): Number of actions.
    """

    def __init__(self, state_space_shape: Tuple[int, ...], action_space_shape: int) -> None:
        self.stats: np.ndarray = np.zeros(state_space_shape + (action_space_shape,))

    def get(self, state: Tuple[int, ...], action: int) -> float:
        """
        Gets the current value for a given state-action pair.

        Args:
            state (Tuple[int, ...]): The state.
            action (int): The action.

        Returns:
            float: The stats for the state-action pair (N(s, a) or C(s, a)).
        """
        return self.stats[state][action]

    def update(self, state: Tuple[int, ...], action: int) -> None:
        """
        Updates the count for a given state-action pair.

        Args:
            state (Tuple[int, ...]): The state.
            action (int): The action.
        """
        self.stats[state][action] += 1

    def update_importance_sampling(self, state: Tuple[int, ...], action: int, importance_sampling_ratio: float)-> None:
        """
        Updates the cumulative sum of importance sampling ratios.

        Args:
            state (Tuple[int, ...]): The state.
            action (int): The action.
            importance_sampling_ratio (float): The importance sampling ratio.
        """
        pass  # TODO: Implement this function


class MonteCarloAgent(BaseAgent):
    """
    Superclass for all Monte Carlo agents. Contains common methods and attributes for all Monte Carlo agents.

    Args:
        env: The environment to interact with.
        gamma (float): Discount factor for future rewards.
        epsilon (float, optional): Exploration parameter for epsilon-greedy policy.
        logger (ResultsLogger, optional): Logger for tracking results during training.
        random_seed (int, optional): Seed for reproducibility.
    """

    def __init__(
            self,
            env,
            gamma: float,
            epsilon: float = None,
            logger: ResultsLogger = None,
            random_seed: int = None
    ) -> None:
        super().__init__(env, gamma, random_seed)
        self.name: str = "Base Monte Carlo Agent"
        self.epsilon: Union[float, None] = epsilon

        self.logger: ResultsLogger = logger if logger else ResultsLogger()

        # Initialise common Monte Carlo agent attributes
        self.q_values: Union[QValueTable, None] = None
        self.policy: Union[object, None] = None

        self.returns: Union[object, None] = None
        self.state_action_stats: Union[StateActionStats, None] = None

        # TODO: shift to an environment-specific method?
        # Get env shape
        self.state_shape: Tuple[int, ...] = ()
        for space in self.env.observation_space:
            self.state_shape += (space.n,)

        self.reset()

    @staticmethod
    def _is_subelement_present(subelement: Tuple[int, ...], my_list: List[Tuple[int, ...]]) -> bool:
        """
        Checks if a subelement is present in a list of tuples.

        Args:
            subelement (Tuple[int, ...]): The subelement to check.
            my_list (List[Tuple[int, ...]]): The list to check within.

        Returns:
            bool: True if subelement is present, False otherwise.
        """
        for tpl in my_list:
            if subelement == tpl[:len(subelement)]:
                return True
        return False

    def _generate_episode(self, exploring_starts: bool = True)-> List[Tuple[Tuple[int, ...], int, float]]:
        """
        Generates an episode by interacting with the environment.

        Args:
            exploring_starts (bool, optional): If True, starts with a random action.

        Returns:
            List[Tuple[Tuple[int, ...], int, float]]:
            The generated episode consisting of (state, action, reward) tuples.
        """
        pass  # TODO: Implement this function


    def reset(self) -> None:
        """
        Resets the agent's attributes, including q-values, state-action stats, and the logger.
        """
        self.q_values = QValueTable(self.state_shape, self.env.action_space.n)
        self.state_action_stats = StateActionStats(self.state_shape, self.env.action_space.n)
        self.logger.reset()

    def act(self, state: int) -> int:
        """Choose an action based on the current state and policy."""
        raise NotImplementedError

    def learn(self, num_episodes: int = 500) -> None:
        """Train the agent over a specified number of episodes."""
        raise NotImplementedError
