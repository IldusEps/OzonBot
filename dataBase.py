import json

dataA4 = [[0 for i in range(0, 5)] for j in range(0, 5)]


def get_unfilled(first_rows=True):
    droping = False
    for i in range(0, 5):
        for j in range(0, 5):
            if first_rows:
                if dataA4[i][j] == 0:
                    if i != 4:
                        return i, j, droping
                    elif j < 3:
                        return i, j, droping
                    else:
                        droping = True
            else:
                if dataA4[j][i] == 0:
                    if i != 4:
                        return j, i, droping
                    elif j < 3:
                        return j, i, droping
                    else:
                        droping = True
    data_clear()
    return 0, 0, True


def data_clear():
    global dataA4
    dataA4 = [[0 for i in range(0, 5)] for j in range(0, 5)]
    data_save()


def data_save():
    with open("data.txt", "w") as file:
        json.dump(dataA4, file)


try:
    with open("data.txt", "r") as file:
        dataA4 = json.load(file)
except:
    data_save()
