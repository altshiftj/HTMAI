import csv

f = open('cell_fire.csv', 'w', newline='')
writer = csv.writer(f)

def initialize_csv():
    header = ['layer', 'thought count', 'cell', 'column', 'x', 'y', 'head direction', 'linear_speed', 'angular_velocity']
    writer.writerow(header)


def write_activecell_to_csv(tm, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    active_cells = tm.getActiveCells().sparse
    for i in range(len(active_cells)):
        column = tm.columnForCell(active_cells[i])
        data = [layer_name, thought_count, active_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        writer.writerow(data)
    return

def write_predcell_to_csv(tm, sdr, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    predictive_cells = sdr.sparse
    for i in range(len(predictive_cells)):
        column = tm.columnForCell(predictive_cells[i])
        data = [layer_name, thought_count, predictive_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        writer.writerow(data)
    return

def write_winnercell_to_csv(tm, layer_name, thought_count, x, y, head_direction, linear_speed, angular_velocity):
    winner_cells = tm.getWinnerCells().sparse
    for i in range(len(winner_cells)):
        column = tm.columnForCell(winner_cells[i])
        data = [layer_name, thought_count, winner_cells[i], column, x, y, head_direction, linear_speed, angular_velocity]
        writer.writerow(data)
    return