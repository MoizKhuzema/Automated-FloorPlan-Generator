from Task_1.graph import create_graph
from Task_1.layout_2 import generate_layout
from Task_1.edges import traverse_edge
from Task_1.render import render


def Task1(width, height, file):
    # max dimensions
    width = width
    height = height

    # generate graph
    filename = file
    G = create_graph(filename)

    # generate layout
    rects, dinner_flag = generate_layout(G, width, height)
    label = []
    for r in rects:
        label.append(r['label'])
    
    # generate doors
    rects = traverse_edge(r'C:\Users\moizk\Desktop\Upwork\Yafei-Zhou\FloorPlanGenerator\Task_1\doors_2.csv', rects, label, dinner_flag)
    # render(width, height, rects)

    return rects


def Task2():
    pass


if __name__ == '__main__':
    # rects = Task1(1500, 1500, r'C:\Users\moizk\Desktop\Upwork\Yafei-Zhou\FloorPlanGenerator\Task_1\Results\exp-1\room_sizes.csv')
    rects = [{'label': 'living room', 'x': 500.0, 'y': 500.0, 'dx': 500.0, 'dy': 500.0}, 
    {'label': 'master bedroom', 'x': 112.70999999999998, 'y': 500.0, 'dx': 387.29, 'dy': 387.29}, 
    {'label': 'guest room', 'x': -326.2201040563918, 'y': 1087.29, 'dx': 413.1169512878373, 'dy': 390.6787157894862}, 
    {'label': 'dinner space', 'x': 500.0, 'y': 1000.0, 'dx': 316.23, 'dy': 316.23}, 
    {'label': 'balcony', 'x': 200.0, 'y': 333.33000000000004, 'dx': 600.0, 'dy': 166.67}, 
    {'label': 'elevator', 'x': 816.23, 'y': 1158.115, 'dx': 255.0, 'dy': 480.0}, 
    {'label': 'toilet B', 'y': 500.0, 'dy': 387.29, 'dx': 77.45678948591492, 'x': 35.253210514085055}, 
    {'label': 'kid bedroom', 'y': 500.0, 'dy': 387.29, 'dx': 361.4733145704769, 'x': -326.2201040563918}, 
    {'label': 'kitchen', 'y': 1087.29, 'dy': 228.94000000000005, 'dx': 158.1031527685545, 'x': 341.89684723144546}, 
    {'label': 'passenger', 'x': -326.2201040563918, 'y': 887.29, 'dy': 200, 'dx': 826.2201040563918}, 
    {'label': 'toilet A', 'x': 86.89684723144552, 'y': 1087.29, 'dx': 254.99999999999994, 'dy': 228.94000000000005}, 
    {'label': 'door', 'x': 266.355, 'y': 877.29, 'dy': 20, 'dx': 80}, 
    {'label': 'door', 'x': 102.70999999999998, 'y': 653.645, 'dy': 80, 'dx': 20}, 
    {'label': 'door', 'x': 266.355, 'y': 490.0, 'dy': 20, 'dx': 80}, 
    {'label': 'door', 'x': 710.0, 'y': 490.0, 'dy': 20, 'dx': 80}, 
    {'label': 'door', 'x': -185.48344677115335, 'y': 877.29, 'dy': 20, 'dx': 80}, 
    {'label': 'door', 'x': -159.66162841247314, 'y': 1077.29, 'dy': 20, 'dx': 80}, 
    {'label': 'door', 'x': 174.3968472314455, 'y': 1077.29, 'dy': 20, 'dx': 80}, 
    {'label': 'door', 'x': 490.0, 'y': 1161.76, 'dy': 80, 'dx': 20}, 
    {'label': 'window', 'x': 360.94842361572273, 'y': 1306.23, 'dy': 20, 'dx': 120}, 
    {'label': 'window', 'x': 598.115, 'y': 1306.23, 'dy': 20, 'dx': 120}, 
    {'label': 'window', 'x': 154.3968472314455, 'y': 1306.23, 'dy': 20, 'dx': 120}, 
    {'label': 'window', 'x': -336.2201040563918, 'y': 633.645, 'dy': 120, 'dx': 20}, 
    {'label': 'window', 'x': -179.66162841247314, 'y': 1467.9687157894862, 'dy': 20, 'dx': 120},
    {'label': 'window', 'x': 13.981605257042517, 'y': 490.0, 'dy': 20, 'dx': 120}, 
    {'label': 'door', 'x': 806.23, 'y': 1238.115, 'dx': 20, 'dy': 80}]

    # drop entries where label is door
    idx = []
    balcony = 0
    for i in range(len(rects)):
        if rects[i]['label'] == 'door' or rects[i]['label'] == 'window':
            idx.append(i)
        if rects[i]['label'] == 'balcony':
            balcony = rects[i]
            idx.append(i)

    for i in range(len(idx)):
        rects.pop(idx[i] - i)

    # Sort by values of x
    new_rects = sorted(rects, key=lambda d: d['x'])
    
    # Creating front-view
    for i in range(len(new_rects)):
        
    
    