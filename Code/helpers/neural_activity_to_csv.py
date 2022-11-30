import csv

# region Location Recording
location_csv = open('cell_fire_locations.csv', 'w', newline='')
location_writer = csv.writer(location_csv)

def write_activecell_to_csv(tm, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    active_cells = tm.getActiveCells().sparse
    for i in range(len(active_cells)):
        column = tm.columnForCell(active_cells[i])
        data = [layer_name, thought_count, active_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        location_writer.writerow(data)
    return

def write_predcell_to_csv(tm, sdr, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    predictive_cells = sdr.sparse
    for i in range(len(predictive_cells)):
        column = tm.columnForCell(predictive_cells[i])
        data = [layer_name, thought_count, predictive_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        location_writer.writerow(data)
    return

def write_winnercell_to_csv(tm, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    winner_cells = tm.getWinnerCells().sparse
    for i in range(len(winner_cells)):
        column = tm.columnForCell(winner_cells[i])
        data = [layer_name, thought_count, winner_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        location_writer.writerow(data)
    return
# endregion

# region Activity Recording
activity_csv = open('neural_activity.csv', 'w', newline='')
activity_writer = csv.writer(activity_csv)

def initialize_neural_activity_location_csv():
    header = ['layer', 'thought count', 'cell', 'column', 'x', 'y', 'head direction', 'linear_speed', 'angular_velocity']
    location_writer.writerow(header)

def write_neural_activity_csv(tm):
    active_segments = tm.getActiveCells.size()
    activity_writer.writerow(header)


# endregion

