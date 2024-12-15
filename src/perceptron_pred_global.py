def perceptron_pred_pytorch(trace, l=1, tablesize=None):
    """
    Simulates branch prediction using perceptrons with a global branch history.
    Parameters:
        trace (list): List of [branch_address, outcome] pairs from the trace file.
        l (int): Length of the global branch history register.
        tablesize (int, optional): Maximum size of the perceptron table. Defaults to None (unlimited size).
    Returns:
        num_correct (int): Number of correct predictions.
        len(p_list) (int): Number of perceptron instances created.
    """
    global_branch_history = deque([0] * l, maxlen=l)  
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

        prediction, running_sum = p_list[key].predict(global_branch_history)

        p_list[key].update_weights(prediction, outcome, global_branch_history, running_sum)

        global_branch_history.appendleft(outcome)

        if prediction == outcome:
            num_correct += 1

    return num_correct, len(p_list)  
