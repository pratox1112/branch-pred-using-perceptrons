def process_trace(file_path, max_l):
    """
    Process a single trace file, run the perceptron predictor for different l values,
    and return the results as lists.
    """
    trace = read_trace_from_file(file_path)
    print(f"Processing {file_path}")
    print(f"Total branches in trace: {len(trace)}\n")
    
    if len(trace) == 0:
        print("No valid branch data found. Skipping this dataset.")
        return None, None, None

    l_values = []
    accuracies = []
    times = []

    for i in range(1, max_l + 1):
        start_time = time.time()
        num_correct, num_p = perceptron_pred_pytorch(trace, l=i, tablesize=None)
        end_time = time.time()
        duration = end_time - start_time
        accuracy = (num_correct / len(trace)) * 100 if len(trace) > 0 else 0

        l_values.append(i)
        accuracies.append(accuracy)
        times.append(duration)

        print(f"i:{i} --> (Accuracy: {accuracy:.2f}%, Time: {duration:.4f} seconds)")

    return l_values, accuracies, times


