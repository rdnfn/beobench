"""Module with core functions of beobench."""
import gym


class Agent:
    def __init__(self) -> None:
        pass


class Env(gym.Env):
    """beobench environment interface."""

    def __init__(self) -> None:
        """beobench environment interface."""
        super().__init__()

        # Variable to be set when implementing this interface

        # Add markdown description of problem definition
        self.problem_description = None

    @property
    def cvxpy_def(self) -> dict:
        """Get a CVXPY problem definition. To be implemented optionally.

        Returns:
            dict: dictionary with all parts of CVXPY problem definition.
        """

        if not hasattr(self, "_cvxpy_def"):

            # CHANGE: add your problem definition by setting all the
            # vars (variables, constraints, objective, actions) below.
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

            self._cvxpy_def = cvxpy_def

        return self._cvxpy_def

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
