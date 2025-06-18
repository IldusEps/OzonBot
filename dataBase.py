import json

dataA4 = [[0 for i in range(0, 5)] for j in range(0, 5)]


def get_unfilled():
    for i in range(0, 5):
        for j in range(0, 5):
            if dataA4[i][j] == 0:
                if i != 4:
                    return i, j
                elif j < 3:
                    return i, j
    data_clear()
    return 0, 0


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
