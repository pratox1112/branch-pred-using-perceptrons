class PerceptronPyTorch(nn.Module):
    """
    Implements a perceptron for branch prediction using PyTorch.
    Attributes:
        N: Length of the branch history register.
    Methods:
        predict(branch_history): Predicts the branch outcome.
        update_weights(prediction, actual, branch_history, running_sum): Updates perceptron weights.
    """
    def __init__(self, N):
        super(PerceptronPyTorch, self).__init__()
        self.N = N
        self.linear = nn.Linear(N, 1, bias=True)
        nn.init.zeros_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)
        self.threshold = 2 * N + 14

    def predict(self, branch_history):
        """
        Predicts the outcome of a branch based on the branch history.
        Parameters:
            branch_history (deque): A deque representing recent branch outcomes.
        Returns:
            prediction (int): Predicted branch outcome (-1 for not taken, 1 for taken).
            running_sum (float): The perceptron output value (confidence score).
        """
        input_tensor = torch.tensor(list(branch_history), dtype=torch.float32).unsqueeze(0)
        running_sum = self.linear(input_tensor).item()
        prediction = -1 if running_sum < 0 else 1
        return prediction, running_sum

    def update_weights(self, prediction, actual, branch_history, running_sum):
        """
        Updates perceptron weights if the prediction is incorrect or confidence is low.
        Parameters:
            prediction (int): Predicted branch outcome (-1 or 1).
            actual (int): Actual branch outcome (-1 or 1).
            branch_history (deque): Recent branch outcomes used as input.
            running_sum (float): The perceptron output value.
        """
        if (prediction != actual) or (abs(running_sum) < self.threshold):
            input_tensor = torch.tensor(list(branch_history), dtype=torch.float32).unsqueeze(0)
            actual_tensor = torch.tensor([actual], dtype=torch.float32)
            with torch.no_grad():
                self.linear.weight += actual_tensor * input_tensor
                self.linear.bias += actual_tensor
