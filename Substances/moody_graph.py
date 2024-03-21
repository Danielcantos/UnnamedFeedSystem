import numpy as np
import matplotlib.pyplot as plt

def moody_chart():
    Re = np.logspace(1, 8, 400)  # Generate a range of Reynolds numbers
    epsilon_D = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]  # Typical relative roughnesses
    f_values = []

    # Calculate f values for each Re and epsilon/D
    for e_d in epsilon_D:
        f_values.append(0.25 / (np.log10((e_d / 3.7) + (5.74 / (Re ** 0.9))) ** 2))

    # Plot the Moody chart
    plt.figure(figsize=(10, 6))
    for i, e_d in enumerate(epsilon_D):
        plt.plot(Re, f_values[i], label=f"ε/D = {e_d:.0e}")

    plt.xscale('log')
    plt.xlabel('Reynolds Number')
    plt.ylabel('Friction Factor (f)')
    plt.title('Moody Chart')
    plt.ylim(0.008, 0.1)  # Limit f values for better readability
    plt.grid(True)
    plt.legend()
    plt.show()

moody_chart()
