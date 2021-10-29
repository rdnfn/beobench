"""Core functions of beogym."""
import gym
import beogym


class Agent:
    def __init__(self) -> None:
        pass


class Env(gym.Env):
    """Beogym environment interface."""

    def __init__(self) -> None:
        """Beogym environment interface."""
        super().__init__()

        # Variable to be set when implementing this interface

        # Add markdown description of problem definition
        self.problem_description = None

        # OPTIONAL: add CVXPY problem definition
        self.cvxpy_problem: beogym.cvxpy.EnvProblem = None

    def _create_cvxpy_def(self) -> dict:
        """Create a CVXPY problem definition. To be implemented optionally.

        Returns:
            dict: dictionary with all parts of CVXPY problem definition.
        """

        variables = {}
        constraints = []
        objective = None
        # Subset of variables that describe the actions over an episode
        actions = None

        cvxpy_def = {
            "variables": variables,
            "actions": actions,
            "constraints": constraints,
            "objective": objective,
        }

        return cvxpy_def

    def evaluate(self, agent: Agent) -> dict:
        """Evaluation function of agent on this environment.

        Args:
            agent (Agent): agent to evaluate

        Raises:
            NotImplementedError

        Returns:
            dict: dictionary with evaluation metrics
        """

        raise NotImplementedError
