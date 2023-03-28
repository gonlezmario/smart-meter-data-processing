import matplotlib.pyplot as plt

# Initialize the figure and axis objects
fig, ax = plt.subplots(5, 2, figsize=(10, 10))
fig.subplots_adjust(hspace=0.5)

# Initialize the data arrays
x_data = []
y_data = [[] for i in range(10)]

# Update function to receive new data and update the plots
def update_plots(new_data):
    # Append new data to the data arrays
    x_data.append(len(x_data))
    for i in range(10):
        y_data[i].append(new_data[i])
    
    # Update the plots
    for i in range(10):
        row = i // 2
        col = i % 2
        ax[row, col].clear()
        ax[row, col].plot(x_data, y_data[i])
        ax[row, col].set_title(f"Variable {i+1}")
    
    # Draw the plots
    plt.draw()
    plt.pause(0.001)

# Example usage
# while True:
#     new_data = receive_data_from_module()  # Replace with actual function to receive data
#     update_plots(new_data)