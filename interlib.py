def above_below(value: float, value_list: list):
    for i in range(len(value_list)):
        if float(value_list[i]) < float(value) < float(value_list[i + 1]):
            below = float(value_list[i])
            above = float(value_list[i + 1])
    return below, above


def corresponding_ab(value, list1, list2):
    for i in range(len(list1)):
        if float(list1[i]) < float(value) < float(list1[i + 1]):
            below = float(list2[i])
            above = float(list2[i + 1])
    return below, above


def find_index(value, value_list):
    for i in range(len(value_list)):
        if value == value_list[i]:
            return i


def interpolate(x, x1, x2, y1, y2):
    m = (y2 - y1) / (x2 - x1)
    y = y1 + m * (x - x1)
    return y


def interpolist(x, x_1, x_2, y_list_1, y_list_2):
    y_list = []
    for i in range(len(y_list_1)):
        y_list.append(interpolate(x, x_1, x_2, y_list_1[i], y_list_2[i]))
    return y_list
