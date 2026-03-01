import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def save_model_performance_charts(y_test, y_pred, artifacts_path="artifacts"):
    """Generates and saves visual proofs of model accuracy."""
    os.makedirs(artifacts_path, exist_ok=True)
    
    # 1. Actual vs Predicted Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, color='blue')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price (Lakhs)')
    plt.ylabel('Predicted Price (Lakhs)')
    plt.title('Actual vs Predicted Real Estate Prices')
    plt.savefig(os.path.join(artifacts_path, "accuracy_plot.png"))
    
    # 2. Error Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot((y_test - y_pred), kde=True, color='green')
    plt.title('Residual (Error) Distribution')
    plt.savefig(os.path.join(artifacts_path, "error_distribution.png"))