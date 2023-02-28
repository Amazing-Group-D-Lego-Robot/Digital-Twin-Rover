import pandas as pd


class Predictor:
    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract prediction function that takes a current state and instruction then returns a dataframe containing
        predicted 100 states. The predicted states should be a prediction of what applying the instruction to the
        current_state will cause, for example:

            instruction =/
                "move_in_x 10"
            current_state =/
                x_pos   y_pos   z_pos
                0       0       10
            return =/
                x_pos   y_pos   z_pos
                0.1     0       10
                0.2     0       10
                ...
                9.9     0       10
                10      0       10

        The method may utilise a storage variable (such as self.MLP_weights, or otherwise) to inform the prediction. If
        it does, this should be defined and initialised in the __init__ function.

        :param instruction: string containing the instruction
        :param current_state: dataframe with one entry describing the currents state
        :return: a series of predictions in the form of entries in a pandas dataframe
        """
        return pd.DataFrame()
