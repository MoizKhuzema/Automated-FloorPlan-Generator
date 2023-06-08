import pandas as pd


def generate_door(rect_a, rect_b, room_b):
    doors = []
    if rect_a['dy'] == rect_b['y'] or rect_a['y'] == rect_b['dy'] or rect_a['y'] == (rect_b['y'] + rect_b['dy']) or rect_b['y'] == (rect_a['y'] + rect_a['dy']):
        print(rect_a)
        diff = (rect_a['dx'] / 2) + rect_a['x']
    elif rect_a['y'] == rect_b['y'] and rect_a['dy'] == rect_b['dy']:
        diff = (rect_a['dy'] / 2) + rect_a['y']
    elif rect_a['y'] == rect_b['y'] and rect_a['dy'] > rect_b['dy']:
        diff = (rect_b['dy'] / 2) + rect_b['y']
    elif rect_a['y'] == rect_b['y'] and rect_a['dy'] < rect_b['dy']:
        diff = (rect_a['dy'] / 2) + rect_a['y']
    elif (rect_a['dy'] + rect_a['y']) == (rect_b['dy'] + rect_b['y']) and rect_a['y'] > rect_b['y']:
        diff = (rect_a['dy'] / 2) + rect_a['y']
    elif (rect_a['dy'] + rect_a['y']) == (rect_b['dy'] + rect_b['y']) and rect_a['y'] < rect_b['y']:
        diff = (rect_b['y'] / 2) + rect_b['y']
    elif rect_a['y'] < rect_b['y']:
        diff = (((rect_a['y'] + rect_a['dy']) - rect_b['y']) / 2) + rect_b['y']
    elif rect_a['y'] > rect_b['y']:
        diff = (((rect_b['y'] + rect_b['dy']) - rect_a['y']) / 2) + rect_a['y']

    #  if room b is to the left of room a
    if rect_b['x'] < rect_a['x'] and rect_a['y'] != rect_b['dy'] and rect_a['dy'] != rect_b['y']:
        doors.append(
            {
                'label': 'door',
                'x': rect_a['x'] - 10,
                'y': diff - 40,
                'dy': 80,
                'dx': 20
            }
        )
    # if room b is to the right of room a
    elif rect_b['x'] > rect_a['x'] and rect_a['y'] != rect_b['dy'] and rect_a['dy'] != rect_b['y']:
        doors.append(
            {
                'label': 'door',
                'x': rect_a['x'] + rect_a['dx'] - 10,
                'y': diff - 40,
                'dy': 80,
                'dx': 20
            }
        )
    # if room b is above room a
    elif rect_b['y'] == rect_a['dy']:
        doors.append(
            {
                'label': 'door',
                'x': diff - 40,
                'y': rect_a['y'] + rect_a['dy'] - 10,
                'dy': 20,
                'dx': 80
            }
        )
    # if room b is below room a
    else:
        doors.append(
            {
                'label': 'door',
                'x': diff - 40,
                'y': rect_a['y'] - 10,
                'dy': 20,
                'dx': 80
            }
        )
    
    return doors


def generate_window(rect_a, width, height):
    windows = []
    # if room b is above room a
    if (rect_a['y'] + rect_a['dy']) > height - 10:
        windows.append(
            {
                'label': 'window',
                'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                'y': rect_a['y'] + rect_a['dy'] - 10,
                'dy': 20,
                'dx': 120
            }
        )
    #  if room b is to the left of room a
    elif rect_a['x'] == 0:
        windows.append(
            {
                'label': 'window',
                'x': -10,
                'y': (rect_a['dy'] / 2) + rect_a['y'] - 60,
                'dy': 120,
                'dx': 20
            }
        )
    # if room b is to the right of room a
    elif (rect_a['x'] + rect_a['dx']) == width:
        windows.append(
            {
                'label': 'window',
                'x': rect_a['x'] + rect_a['dx'] - 10,
                'y': (rect_a['dy'] / 2) + rect_a['y'] - 60,
                'dy': 120,
                'dx': 20
            }
        )
    # if room b is below room a
    else:
        windows.append(
            {
                'label': 'window',
                'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                'y': - 10,
                'dy': 20,
                'dx': 120
            }
        )
    
    return windows


def traverse_edge(filepath, rects, label, width, height):
    # load edge data
    edges = pd.read_csv(filepath, names=['a', 'b'])

    # door edges
    door_edges = edges.head(9)
    for idx in door_edges.index:
        if (door_edges.loc[idx])['a'] not in label:
            door_edges.drop(idx, inplace= True)
            continue
        elif (door_edges.loc[idx])['b'] not in label:
            door_edges.drop(idx, inplace= True)

    # window edges
    window_edges = edges.tail(8)
    for idx in window_edges.index:
        if (window_edges.loc[idx])['a'] not in label:
            window_edges.drop(idx, inplace= True)
            continue
        elif (window_edges.loc[idx])['b'] != 'outside':
            window_edges.drop(idx, inplace= True)

    doors = []
    windows = []

    for i in door_edges.index:
        room_a, room_b = door_edges.loc[i].tolist()

        # Wierd bug for this case
        if (room_b == 'dinner space'):
            for rect in rects:
                if rect['label'] == 'kitchen':
                    rect_a = rect
                elif rect['label'] == room_b:
                    rect_b = rect
            doors = doors + generate_door(rect_a, rect_b, room_b)
            continue
        
        # Generate doors
        for rect in rects:
            if rect['label'] == room_a:
                rect_a = rect
            elif rect['label'] == room_b:
                rect_b = rect
                break
        doors = doors + generate_door(rect_a, rect_b, room_b)

    # Generate windows
    for i in range(len(window_edges)):
        room_a, room_b = window_edges.iloc[i].tolist()
        for rect in rects:
            if rect['label'] == room_a:
                rect_a = rect
            elif rect['label'] == room_b:
                rect_b = rect 
                break 
        windows = windows + generate_window(rect_a, width, height)

    # Generate front door
    for rect in rects:
        if rect['label'] == 'elevator':
            rect_a = rect
    front_door =  [
        {
            'label': 'door',
            'x': ((rect_a['dx']) / 2) + rect_a['x'] - 40,
            'y': rect_a['y'] - 10,
            'dx': 80,
            'dy': 20
        }
    ]
         
    return rects + doors + windows + front_door

