**Perceptron-Based Branch Prediction in Modern Processors**

Project Overview
This project explores an innovative perceptron-based branch predictor to enhance the efficiency of modern processors by minimizing pipeline stalls and improving prediction accuracy. Unlike traditional predictors, the perceptron-based approach dynamically adapts to program-specific branching patterns, leveraging machine learning techniques to identify complex relationships in branch behavior.

The project evaluates the perceptron model against conventional predictors like GShare and compares the impact of Global History Registers and Local History Registers on prediction accuracy.

Methodology

1. Data Collection
Branch traces were generated using Intel’s Pin Tool for algorithms such as:
Insertion Sort
Quick Sort
Merge Sort
Factorial
Fibonacci
Prime Number Calculation
2. Perceptron Predictor Design
Integrated Global History Registers as inputs to the perceptron model to capture branching patterns over a configurable history length.
Computed the weighted sum of branch history bits and bias to predict branch outcomes as Taken or Not Taken.
Updated weights iteratively using the perceptron learning rule to improve accuracy over time.
3. Comparative Analysis
Compared the Perceptron Predictor with the GShare Predictor for accuracy and misprediction rates.
Assessed the effect of increasing history register lengths on prediction accuracy.
