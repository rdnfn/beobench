"""Code for CVXPY based optimal solution."""


from typing import Dict, List
import cvxpy as cp


class EpisodeProblem:
    """Problem of environment episode."""

    def __init__(
        self,
        constraints: List,
        objective: cp.Objective,
        parameters: Dict,
        actions: Dict,
    ) -> None:
        """Problem of environment episode.

        Args:
            constraints (List): list of CVXPY constraints
            objective (cp.Objective): objective of optimisation
            parameters (Dict): parameters that change per episode
                (e.g. solar traces)
            actions (Dict): dictionary of variable representing agent actions
        """
        self.problem = cp.Problem(objective, constraints)
        self.parameters = parameters
        self.actions = actions

    def solve(self, parameters: Dict = None) -> List:

        # Setting the parameters values (this can be episode specific data)
        if parameters is not None:
            for param_name in parameters.keys():
                self.parameters[param_name].value = parameters[param_name]

        self.problem.solve()

        # Extracting action values from variable values in solution
        action_values = {
            action_name: action.value
            for (
                action_name,
                action,
            ) in self.actions.items()
        }
        return action_values
