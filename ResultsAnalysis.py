from navigation_logics import RESULTS_FILE
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define constants for column names
ASTAR__ZERO_H = 0
ASTAR__ARIAL_DIST_H = 1
ASTAR__DIJKSTRA_H = 2
QLEARNING = 3

NUM_OF_ALGOS = 4

MEAN_SHIFT = NUM_OF_ALGOS
MIN_SHIFT = 2 * NUM_OF_ALGOS
MAX_SHIFT = 3 * NUM_OF_ALGOS

def read_results():
    # reads the CSV file
    file_path = RESULTS_FILE
    df = pd.read_csv(file_path)

    # get results
    y_values = []
    # results of changing traffic
    for i in range(NUM_OF_ALGOS):
        y_values.append(df[str(i)])

    # results of mean traffic
    for i in range(NUM_OF_ALGOS):
        y_values.append(df[str(i + MEAN_SHIFT)])

    # results of min traffic
    for i in range(NUM_OF_ALGOS):
        y_values.append(df[str(i + MIN_SHIFT)])

    # result of max traffic
    for i in range(NUM_OF_ALGOS):
        y_values.append(df[str(i + MAX_SHIFT)])

    return y_values


def create_graph(y_values):
    x_values = np.arange(len(y_values[ASTAR__ZERO_H]))
    line_width = 50

    # plot changing traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H] - 1*line_width, label='A star - Zero heuristic', color='cornflowerblue')
    plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H] - 0.5*line_width, label='A star - Arial dist heuristic', color='lightgreen')
    plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H], label='A star - Dijkstra heuristic', color='lightcoral')
    plt.plot(x_values, y_values[QLEARNING] + 0.5*line_width, label='Q learning', color='mediumpurple')

    # plot min traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H + MIN_SHIFT] - 1 * line_width, color='cornflowerblue', linestyle='--')
    plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H + MIN_SHIFT] - 0.5 * line_width, color='lightgreen', linestyle='--')
    plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H + MIN_SHIFT], color='lightcoral', linestyle='--')
    plt.plot(x_values, y_values[QLEARNING + MIN_SHIFT] + 0.5 * line_width, color='mediumpurple', linestyle='--')

    # plot max traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H + MAX_SHIFT] - 1 * line_width, color='cornflowerblue', linestyle='--')
    plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H + MAX_SHIFT] - 0.5 * line_width, color='lightgreen', linestyle='--')
    plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H + MAX_SHIFT], color='lightcoral', linestyle='--')
    plt.plot(x_values, y_values[QLEARNING + MAX_SHIFT] + 0.5 * line_width, color='mediumpurple', linestyle='--')

    # plot mean traffic data
    # plt.plot(x_values, y_values[ASTAR__ZERO_H + MEAN_SHIFT] - 1 * line_width, color='cornflowerblue', linestyle='dotted')
    # plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H + MEAN_SHIFT] - 0.5 * line_width, color='lightgreen', linestyle='dotted')
    # plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H + MEAN_SHIFT], color='lightcoral', linestyle='dotted')
    # plt.plot(x_values, y_values[QLEARNING + MEAN_SHIFT] + 0.5 * line_width, color='mediumpurple', linestyle='dotted')

    # Add labels and title
    plt.xlabel('')
    plt.ylabel('')
    plt.title('')


    # Set x-axis ticks to integers only
    plt.xticks(ticks=x_values)

    # Display the legend and grid
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

y_values = read_results()
create_graph(y_values)