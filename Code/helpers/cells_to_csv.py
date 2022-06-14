import csv

f = open('cell_fire.csv', 'w', newline='')
writer = csv.writer(f)

def initialize_csv(layer):
    f = open(f'{layer}_cell_fire.csv', 'w', newline='')
    header = ['thought count','cell', 'column', 'x', 'y', 'head direction']
    writer.writerow(header)


def write_to_csv(tm, thought_count, x, y, head_direction):
    active_cells = tm.getActiveCells().sparse
    for i in range(len(active_cells)):
        column = tm.columnForCell(active_cells[i])
        data = [thought_count, active_cells[i], column, x, y, head_direction]
        writer.writerow(data)
    return