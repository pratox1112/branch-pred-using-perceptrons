def perceptron_pred_pytorch(trace, l=1, tablesize=None):
    """
    Simulates branch prediction using perceptrons.
    Parameters:
        trace (list): List of [branch_address, outcome] pairs from the trace file.
        l (int): Length of the branch history register.
        tablesize (int, optional): Maximum size of the perceptron table. Defaults to None (unlimited size).
    Returns:
        num_correct (int): Number of correct predictions.
        len(p_list) (int): Number of perceptron instances created.
    """
    branch_histories = defaultdict(lambda: deque([0] * l, maxlen=l))
    p_list = {}
    num_correct = 0

    for br in trace:
        branch_address = br[0]
        outcome = 1 if br[1] else -1

        if tablesize:
            index = hash(branch_address) % tablesize
            key = index
        else:
            key = branch_address

        if key not in p_list:
            p_list[key] = PerceptronPyTorch(l)

        local_history = branch_histories[branch_address]
        prediction, running_sum = p_list[key].predict(local_history)
        p_list[key].update_weights(prediction, outcome, local_history, running_sum)
        local_history.appendleft(outcome)

        if prediction == outcome:
            num_correct += 1

    return num_correct, len(p_list)
