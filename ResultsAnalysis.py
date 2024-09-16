from navigation_logics import RESULTS_FILE, QLEARNING_RESULT_FILE
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define constants for column names
ASTAR__ZERO_H = 0
ASTAR__ARIAL_DIST_H = 1
ASTAR__DIJKSTRA_H = 2
ASTAR__COMBINATION_H = 3
ASTAR__NONADMISSIBLE_H = 4
QLEARNING = 5

NUM_OF_ALGOS = 6

MEAN_SHIFT = NUM_OF_ALGOS
MIN_SHIFT = 2 * NUM_OF_ALGOS
MAX_SHIFT = 3 * NUM_OF_ALGOS
RUNTIME_SHIFT = 4 * NUM_OF_ALGOS

NUM_OF_QLEARNERS = 6

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

    # result of running time
    for i in range(NUM_OF_ALGOS):
        y_values.append(df[str(i + RUNTIME_SHIFT)])

    return y_values

def read_Q_learners_results():
    # reads the CSV file
    file_path = QLEARNING_RESULT_FILE
    df = pd.read_csv(file_path)

    # get results
    y_values = []
    # results of changing traffic
    for i in range(NUM_OF_QLEARNERS):
        y_values.append(df[str(i)])

    # result of running time
    for i in range(NUM_OF_QLEARNERS):
        y_values.append(df[str(i + NUM_OF_QLEARNERS)])

    return y_values


def create_runtime_sample_grpah(y_values):
    x_values = np.arange(len(y_values[ASTAR__ZERO_H]))
    line_width = 0
    # plot changing traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H + RUNTIME_SHIFT] - 1.5 * line_width, label='A star - Zero heuristic',
             color='cornflowerblue')
    plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H + RUNTIME_SHIFT] - 1 * line_width, label='A star - Arial dist heuristic',
             color='lightgreen')
    plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H + RUNTIME_SHIFT] - 0.5 * line_width, label='A star - Dijkstra heuristic',
             color='orangered')
    plt.plot(x_values, y_values[ASTAR__COMBINATION_H + RUNTIME_SHIFT], label='A star - Combination heuristic',
             color='orange')
    plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H + RUNTIME_SHIFT] + 0.5 * line_width, label='A star - Non-admissible heuristic',
             color='hotpink')
    plt.plot(x_values, y_values[QLEARNING + RUNTIME_SHIFT] + 1 * line_width, label='Q learning', color='mediumpurple')

    plt.yscale('log')

    # labels and title
    plt.xlabel('sample')
    plt.ylabel('Running Time (seconds in log scale)')
    plt.title('Running Time per Algorithm')

    # x-axis ticks to integers only
    plt.xticks(ticks=np.arange(0, len(x_values), 10))

    # display the legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()


def create_Q_learners_runtime_sample_grpah(y_values):
    x_values = np.arange(len(y_values[0]))

    # plot changing traffic data
    plt.plot(x_values, y_values[0 + NUM_OF_QLEARNERS], label='learning rate 0.4',
             color='cornflowerblue')
    plt.plot(x_values, y_values[1 + NUM_OF_QLEARNERS], label='learning rate 0.5',
             color='lightgreen')
    plt.plot(x_values, y_values[2 + NUM_OF_QLEARNERS], label='learning rate 0.6',
             color='orangered')
    plt.plot(x_values, y_values[3 + NUM_OF_QLEARNERS], label='learning rate 0.7',
             color='orange')
    plt.plot(x_values, y_values[4 + NUM_OF_QLEARNERS], label='learning rate 0.8',
             color='hotpink')
    plt.plot(x_values, y_values[5 + NUM_OF_QLEARNERS], label='learning rate 0.9',
             color='mediumpurple')

    plt.yscale('log')

    # labels and title
    plt.xlabel('sample')
    plt.ylabel('Running Time (seconds in log scale)')
    plt.title('Running Time per Q learning Parameter')

    # x-axis ticks to integers only
    plt.xticks(ticks=np.arange(0, len(x_values), 5))
    # display the legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()
def create_cost_sample_graph(y_values):
    x_values = np.arange(len(y_values[ASTAR__ZERO_H]))
    line_width = 0

    # plot changing traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H] - 1.5*line_width, label='changing traffic', color='cornflowerblue')
    # plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H] - 1*line_width, label='A star - Arial dist heuristic', color='lightgreen')
    # plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H] - 0.5*line_width, label='A star - Dijkstra heuristic', color='orangered')
    # plt.plot(x_values, y_values[ASTAR__COMBINATION_H], label='A star - Combination heuristic', color='orange')

    # plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H] + 0.5*line_width, label='A star - Non-admissible heuristic', color='hotpink')
    # plt.plot(x_values, y_values[QLEARNING] + 1*line_width, label='Q learning', color='mediumpurple')
    # plt.plot(x_values, y_values[ASTAR__ZERO_H] - 1.5 * line_width, label='A star - Admissible heuristics',
    #          color='cornflowerblue')

    # plot min traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H + MIN_SHIFT] - 1.5*line_width, color='cornflowerblue', linestyle='dotted', label='min traffic')
    # plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H + MIN_SHIFT] - 1*line_width, color='lightgreen', linestyle='dotted')
    # plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H + MIN_SHIFT] - 0.5*line_width, color='orangered', linestyle='dotted')
    # plt.plot(x_values, y_values[ASTAR__COMBINATION_H + MIN_SHIFT], color='orange', linestyle='dotted')
    # plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H + MIN_SHIFT] + 0.5*line_width, color='hotpink', linestyle='dotted')
    # plt.plot(x_values, y_values[QLEARNING + MIN_SHIFT] + 1*line_width, color='mediumpurple', linestyle='dotted')

    # # plot max traffic data
    plt.plot(x_values, y_values[ASTAR__ZERO_H + MAX_SHIFT] - 1.5*line_width, color='cornflowerblue', linestyle='--', label='max traffic')
    # plt.plot(x_values, y_values[ASTAR__ARIAL_DIST_H + MAX_SHIFT] - 1*line_width, color='lightgreen', linestyle='--')
    # plt.plot(x_values, y_values[ASTAR__DIJKSTRA_H + MAX_SHIFT] - 0.5*line_width, color='orangered', linestyle='--')
    # plt.plot(x_values, y_values[ASTAR__COMBINATION_H + MAX_SHIFT], color='orange', linestyle='--')
    # plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H + MAX_SHIFT] + 0.5*line_width, color='hotpink', linestyle='dotted')
    # plt.plot(x_values, y_values[QLEARNING + MAX_SHIFT] + 1*line_width, color='mediumpurple', linestyle='dotted')

    plt.yscale('log')
    # labels and title
    plt.xlabel('sample')
    plt.ylabel('Cost (time until arrival, log scael)')
    plt.title('A-Star Admissible Heuristic Cost')

    # Set x-axis ticks to integers only
    plt.xticks(ticks=np.arange(0, len(x_values), 10))

    # Display the legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()

def create_min_max_graph(y_values):
    x_values = np.arange(len(y_values[ASTAR__ZERO_H]))
    line_width = 0

    # plot changing traffic data
    # plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H] + 0.5*line_width, label='changing traffic', color='hotpink')
    plt.plot(x_values, y_values[QLEARNING] + 1*line_width, label='changing traffic', color='mediumpurple')

    # plot min traffic data
    # plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H + MIN_SHIFT] + 0.5*line_width, color='hotpink', linestyle='dotted', label='min traffic')
    plt.plot(x_values, y_values[QLEARNING + MIN_SHIFT] + 1*line_width, color='mediumpurple', linestyle='dotted', label='min traffic')

    # # plot max traffic data
    # plt.plot(x_values, y_values[ASTAR__NONADMISSIBLE_H + MAX_SHIFT] + 0.5*line_width, color='hotpink', linestyle='--', label='max traffic')
    plt.plot(x_values, y_values[QLEARNING + MAX_SHIFT] + 1*line_width, color='mediumpurple', linestyle='--', label='max traffic')

    plt.yscale('log')
    # labels and title
    plt.xlabel('sample')
    plt.ylabel('Cost (time until arrival, log scale)')
    plt.title('Q Learning Cost')

    # Set x-axis ticks to integers only
    plt.xticks(ticks=np.arange(0, len(x_values), 10))

    # Display the legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()

def create_Q_learners_cost_sample_graph(y_values):
    x_values = np.arange(len(y_values[0]))

    # plot changing traffic data
    plt.plot(x_values, y_values[0], label='learning rate 0.4',
             color='cornflowerblue')
    plt.plot(x_values, y_values[1], label='learning rate 0.5',
             color='lightgreen')
    plt.plot(x_values, y_values[2], label='learning rate 0.6',
             color='orangered')
    plt.plot(x_values, y_values[3], label='learning rate 0.7',
             color='orange')
    plt.plot(x_values, y_values[4], label='learning rate 0.8',
             color='hotpink')
    plt.plot(x_values, y_values[5], label='learning rate 0.9',
             color='mediumpurple')
    plt.yscale('log')
    # labels and title
    plt.xlabel('sample')
    plt.ylabel('Cost (time until arrival, log scale)')
    plt.title('Cost per Q Learning Parameter')

    # Set x-axis ticks to integers only
    plt.xticks(ticks=np.arange(0, len(x_values), 5))

    # Display the legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()


# GENERAL ALGOS
y_values = read_results()
# create_cost_sample_graph(y_values)
# create_min_max_graph(y_values)
create_runtime_sample_grpah(y_values)

# Q LEARNERS
# y_values = read_Q_learners_results()
# create_Q_learners_cost_sample_graph(y_values)
# create_Q_learners_runtime_sample_grpah(y_values)