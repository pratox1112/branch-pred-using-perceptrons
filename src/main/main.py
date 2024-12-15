def main():
    """
    Main function to process multiple datasets and plot results.
    """
    file_paths = [
        r'C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\factorial.txt',
        r'C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\fibonacci.txt',
        r'C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\insertionsort.txt',
        r'C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\mergesort.txt',
        r'C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\prime.txt',
        r'C:\Users\prato\OneDrive\Desktop\EECE7205 - Fundamentals of CompE\Project\Trace files\quicksort.txt'
    ]

    max_l = 50  # Maximum value of l to test
    results = {}

    # Process each dataset
    for file_path in file_paths:
        dataset_name = file_path.split('\\')[-1].split('.')[0]
        l_values, accuracies, times = process_trace(file_path, max_l)
        if l_values:
            results[dataset_name] = {
                'l_values': l_values,
                'accuracies': accuracies,
                'times': times
            }

    # Plot accuracy comparisons
    plt.figure(figsize=(12, 8))
    for dataset_name, data in results.items():
        plt.plot(data['l_values'], data['accuracies'], marker='o', label=f'{dataset_name} Accuracy')
    plt.title('Accuracy vs. Branch History Length for Multiple Datasets')
    plt.xlabel('Branch History Length')
    plt.ylabel('Accuracy (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()
