import matplotlib.pyplot as plt
import numpy as np

# Data for D = 2
data_d2 = {
    'function': ['sphere', 'sphere', 'sphere', 'rosenbrock', 'rosenbrock', 'rosenbrock', 'rastrigin', 'rastrigin', 'rastrigin'],
    'method': ['GA', 'PSO', 'SA', 'GA', 'PSO', 'SA', 'GA', 'PSO', 'SA'],
    'mean': [-450.0, -450.0, -449.9991, 390.0134, 390.0002, 413.2994, 768.6189, 768.6189, 768.6189],
    'std_dev': [0.0, 0.0, 0.0016, 0.0235, 0.0008, 26.9849, 0.0001, 0.0, 0.0],
    'best': [-450.0, -450.0, -450.0, 390.0, 390.0, 390.0, 768.6189, 768.6189, 768.6189],
    'worst': [-450.0, -450.0, -449.9951, 390.0689, 390.0029, 463.7413, 768.6192, 768.6189, 768.619]
}

# Data for D = 10
data_d10 = {
    'function': ['sphere', 'sphere', 'sphere', 'rosenbrock', 'rosenbrock', 'rosenbrock', 'rastrigin', 'rastrigin', 'rastrigin'],
    'method': ['GA', 'PSO', 'SA', 'GA', 'PSO', 'SA', 'GA', 'PSO', 'SA'],
    'mean': [-449.9997, -450.0, -391.0011, 392.3198, 425.0176, 255998.2214, 6465.1913, 6401.9100, 6615.0371],
    'std_dev': [0.0001, 0.0, 93.4342, 2.2910, 62.2730, 243193.0776, 4.8284, 0.5025, 127.0532],
    'best': [-449.9999, -450.0, -93.3914, 390.0052, 390.1067, 1679.8337, 6401.7808, 6401.7649, 6429.3994],
    'worst': [-449.9995, -450.0, -93.3914, 396.1289, 597.5602, 835868.4028, 6411.9566, 6403.7916, 6854.6334]
}

# Convert the data into a structured format
import pandas as pd

df_d2 = pd.DataFrame(data_d2)
df_d10 = pd.DataFrame(data_d10)

# Plotting function
def plot_results(df, title):
    functions = df['function'].unique()
    methods = df['method'].unique()

    fig, axes = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

    for func in functions:
        subset = df[df['function'] == func]
        x = np.arange(len(methods))
        width = 0.2

        axes[0].bar(x + width * (functions.tolist().index(func) - 1), subset['mean'], width, label=f'{func} - mean')
        axes[1].bar(x + width * (functions.tolist().index(func) - 1), subset['std_dev'], width, label=f'{func} - std dev')
        axes[2].bar(x + width * (functions.tolist().index(func) - 1), subset['best'], width, label=f'{func} - best')
        axes[2].bar(x + width * (functions.tolist().index(func) - 1), subset['worst'], width, bottom=subset['best'], label=f'{func} - worst')

    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(methods)
        ax.legend()
        ax.grid(True)

    axes[0].set_ylabel('Mean')
    axes[1].set_ylabel('Standard Deviation')
    axes[2].set_ylabel('Best/Worst')
    plt.suptitle(title)
    plt.xlabel('Methods')
    plt.show()

# Plot results for D = 2
plot_results(df_d2, 'Optimization Results for D = 2')

# Plot results for D = 10
plot_results(df_d10, 'Optimization Results for D = 10')

