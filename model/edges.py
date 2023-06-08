import pandas as pd


def generate_door(rect_a, rect_b, room_b):
    doors = []
    if (rect_a['dy'] + rect_a['y']) == rect_b['y'] or rect_a['y'] == (rect_b['dy'] + rect_b['y']):
        if (rect_a['dx'] > rect_b['dx']):
            diff = (rect_b['dx'] / 2) + rect_b['x']
        else:
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
        diff = (rect_b['dy'] / 2) + rect_b['y']
    elif rect_a['y'] < rect_b['y']:
        diff = (((rect_a['y'] + rect_a['dy']) - rect_b['y']) / 2) + rect_b['y']
    elif rect_a['y'] > rect_b['y']:
        diff = (((rect_b['y'] + rect_b['dy']) - rect_a['y']) / 2) + rect_a['y']

    #  if room b is to the left of room a
    if rect_b['x'] < rect_a['x'] and rect_a['y'] != (rect_b['y'] + rect_b['dy']) and (rect_a['y'] + rect_a['dy']) != rect_b['y']:
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
    elif rect_b['x'] > rect_a['x'] and rect_a['y'] != (rect_b['y'] + rect_b['dy']) and (rect_a['y'] + rect_a['dy']) != rect_b['y']:
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
    elif rect_b['y'] == (rect_a['y'] + rect_a['dy']):
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


def generate_window(rect_a, passage, filepath, dinner_flag):
    windows = []

    if rect_a['label'] == 'toilet B':
        if filepath == 'doors_1.csv':
            windows.append(
                {
                    'label': 'window',
                    'x': rect_a['x'] - 10,
                    'y': (rect_a['dy'] / 2) + rect_a['y'] - 60,
                    'dy': 120,
                    'dx': 20
                }
            )
        else:
            windows.append(
                {
                    'label': 'window',
                    'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                    'y': rect_a['y'] - 10,
                    'dy': 20,
                    'dx': 120
                }
            )
    elif rect_a['label'] == 'kid bedroom':
        windows.append(
            {
                'label': 'window',
                'x': rect_a['x'] - 10,
                'y': (rect_a['dy'] / 2) + rect_a['y'] - 60,
                'dy': 120,
                'dx': 20
            }
        )
    elif rect_a['label'] == 'toilet A':
        windows.append(
            {
                'label': 'window',
                'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                'y': rect_a['y'] + rect_a['dy'] - 10,
                'dy': 20,
                'dx': 120
            }
        )
    elif rect_a['label'] == 'guest room':
        if (rect_a['y'] + rect_a['dy']) == passage['y']:
            windows.append(
                {
                    'label': 'window',
                    'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                    'y': rect_a['y'] - 10,
                    'dy': 20,
                    'dx': 120
                }
            )
        else:
            windows.append(
                {
                    'label': 'window',
                    'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                    'y': rect_a['y'] + rect_a['dy'] - 10,
                    'dy': 20,
                    'dx': 120
                }
            )
    elif rect_a['label'] == 'dinner space':
        if filepath == 'doors_1.csv':
            if dinner_flag:
                windows.append(
                    {
                        'label': 'window',
                        'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                        'y': rect_a['y'] + rect_a['dy'] - 10,
                        'dy': 20,
                        'dx': 120
                    }
                )
            else:
                windows.append(
                    {
                        'label': 'window',
                        'x': rect_a['x'] + rect_a['dx'] - 10,
                        'y': (rect_a['dy'] / 2) + rect_a['y'] - 60,
                        'dy': 120,
                        'dx': 20
                    }
                )
        else:
            if dinner_flag:
                pass
            else:
                windows.append(
                    {
                        'label': 'window',
                        'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                        'y': rect_a['y'] + rect_a['dy'] - 10,
                        'dy': 20,
                        'dx': 120
                    }
                )
    elif rect_a['label'] == 'kitchen':
        if filepath == 'doors_1.csv':
            if dinner_flag:
                windows.append(
                    {
                        'label': 'window',
                        'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                        'y': rect_a['y'] + rect_a['dy'] - 10,
                        'dy': 20,
                        'dx': 120
                    }
                )
            else:
                windows.append(
                    {
                        'label': 'window',
                        'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                        'y': rect_a['y'] - 10,
                        'dy': 20,
                        'dx': 120
                    }
                )
        else:
            windows.append(
                {
                    'label': 'window',
                    'x': (rect_a['dx'] / 2) + rect_a['x'] - 60,
                    'y': rect_a['y'] + rect_a['dy'] - 10,
                    'dy': 20,
                    'dx': 120
                }
            )
        
    return windows


def traverse_edge(filepath, rects, label, dinner_flag):
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
        doors = doors + generate_door(rect_a, rect_b, room_b)

    # Generate windows
    passage = []
    for rect in rects:
        if rect['label'] == 'passenger':
            passage = rect
    for i in range(len(window_edges)):
        room_a, room_b = window_edges.iloc[i].tolist()
        for rect in rects:
            if rect['label'] == room_a:
                rect_a = rect
            elif rect['label'] == room_b:
                rect_b = rect 
                break 
        windows = windows + generate_window(rect_a, passage, filepath, dinner_flag)

    # Generate front door
    for rect in rects:
        if rect['label'] == 'elevator':
            rect_a = rect
    front_door =  [
        {
            'label': 'door',
            'x': rect_a['x'] - 10,
            'y': rect_a['y'] + (rect_a['dy'] / 4) - 40,
            'dx': 20,
            'dy': 80
        }
    ]
         
    return rects + doors + windows + front_door

