def read_trace_from_file(file_path):
    """
    Reads a branch trace file and parses branch addresses and outcomes.
    Parameters:
        file_path (str): Path to the branch trace file.
    Returns:
        trace (list): A list of [branch_address, outcome] pairs.
    """
    trace = []
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    print(f"Warning: Line {line_number} is malformed: '{line}'")
                    continue
                branch_address, outcome_str = parts
                try:
                    outcome = int(outcome_str)
                    if outcome not in (0, 1):
                        print(f"Warning: Line {line_number} has invalid outcome '{outcome}': '{line}'")
                        continue
                except ValueError:
                    print(f"Warning: Line {line_number} has non-integer outcome '{outcome_str}': '{line}'")
                    continue
                trace.append([branch_address, outcome])
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except IOError as e:
        print(f"IOError while reading file '{file_path}': {e}")
    return trace
