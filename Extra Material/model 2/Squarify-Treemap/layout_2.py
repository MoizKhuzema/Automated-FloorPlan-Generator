import squarify as sq
import pandas as pd
import matplotlib.pyplot as plt


def absolute(rects):
    for rect in rects:
        rect['x'] = abs(rect['x'])
        rect['y'] = abs(rect['y'])
        rect['dy'] = abs(rect['dy'])
        rect['dx'] = abs(rect['dx'])
    return rects


def generate_private(rect, private):
    # points of origin
    x = 0
    y = 0
    width = rect['dx']
    height = rect['dy']

    # Adding rooms
    size = []
    master_toilet = private.loc[private['Rooms'] == 'toilet B']
    private.drop(private.index[private['Rooms'] == 'toilet B'][0], inplace= True)
    for i in range(len(private)):
        if private.iloc[i, 0] == 'master bedroom':
            total_size = (private.iloc[i, 1] * private.iloc[i, 2]) + (master_toilet.iloc[0, 1] * master_toilet.iloc[0, 2])
            size.append(total_size)
        else:
            size.append(private.iloc[i, 1] * private.iloc[i, 2])

    normed = sq.normalize_sizes(size, width, height)
    temp = sq.squarify(normed, x, y, width, height)
    temp = absolute(temp)
    
    # Optimizing Balcony Layout
    total_size = temp[2]['dx'] * temp[2]['dy']
    temp[2]['dx'] = width
    temp[2]['dy'] = total_size/width
    temp[2]['x'] = 0
    temp[2]['y'] = 0
    temp[2]['label'] = 'balcony A'

    # Optimizing KidBD Layout
    total_size = temp[1]['dx'] * temp[1]['dy']
    temp[1]['dx'] = width
    temp[1]['dy'] = total_size/width
    temp[1]['x'] = 0
    temp[1]['label'] = 'kid bedroom'

    # Optimizing MasterBD Layout 
    total_size = temp[0]['dx'] * temp[0]['dy']
    temp[0]['y'] = temp[2]['dy']
    temp[0]['dy'] = height - temp[1]['dy'] - temp[2]['dy']
    temp[0]['x'] = (master_toilet.iloc[0, 1] * master_toilet.iloc[0, 2])/temp[0]['dy']
    temp[0]['dx'] = width - temp[0]['x']
    temp[0]['label'] = 'master bedroom'
    temp[1]['y'] = temp[0]['y'] + temp[0]['dy']

    # Adding Toilet to MasterBD
    if (master_toilet.iloc[0, 1] * master_toilet.iloc[0, 2])/temp[0]['dy'] != 0:
        toilet = [
            {
                'label': 'toilet B',
                'dy': temp[0]['dy'],
                'dx': temp[0]['x'],
                'y': temp[2]['dy'],
                'x': 0
            }
        ]
        rect = temp + toilet
    else:
        rect = temp
    
    return rect


def generate_public(rect, public, elevator, adjusted_x, adjusted_y, passage_y, norm_y):
    # points of origin
    x = 0
    y = 0
    width = rect['dx']
    height = rect['dy']

    # Adding rooms
    size = []
    row = []
    for i in range(len(public)):
        if public.iloc[i, 0] == 'living room':
            remaining_size = (public.iloc[i, 1] * public.iloc[i, 2]) - (elevator.iloc[0, 1] * (norm_y - elevator.iloc[0, 2]))
            size.append(abs(remaining_size))
        elif public.iloc[i, 0] == 'toilet A':
            row.append(public.iloc[i])
        else:
            size.append(public.iloc[i, 1] * public.iloc[i, 2])
    public.drop(public.index[public['Rooms'] == row[0][0]], inplace= True)
    normed = sq.normalize_sizes(size, width, height)
    temp = sq.squarify(normed, x, y, width, height)
    
    if public.loc[public['Rooms'] == 'guest room']['Width'].values[0] != 0.0:
        # Optimizing dinner space
        total_size = temp[2]['dx'] * temp[2]['dy']
        temp[2]['y'] = adjusted_y
        temp[2]['x'] = adjusted_x
        temp[2]['dx'] = width
        temp[2]['dy'] = total_size / temp[2]['dx']
        temp[2]['label'] = 'dinner space'

        # Optimizing living room
        total_size =  temp[1]['dx'] * temp[1]['dy']
        temp[1]['x'] = adjusted_x
        temp[1]['y'] = temp[2]['dy'] + temp[2]['y']
        temp[1]['dx'] = width
        temp[1]['dy'] = total_size / temp[1]['dx']
        temp[1]['label'] = 'living room' 

        # Optimizing guest room
        total_size =  temp[0]['dx'] * temp[0]['dy']
        temp[0]['y'] = temp[1]['dy'] + temp[1]['y']
        if temp[0]['y'] >= norm_y:
            temp[0]['y'] = norm_y - temp[0]['dy']
            temp[1]['dy'] -= (temp[1]['dy'] - temp[0]['y'])
        temp[0]['y'] = temp[1]['y'] + temp[1]['dy']
        temp[0]['x'] = adjusted_x
        temp[0]['dx'] = width
        temp[0]['dy'] = total_size / temp[0]['dx']
        temp[0]['label'] = 'guest room'

        # Checking leftover space
        if temp[0]['y'] + temp[0]['dy'] < norm_y:
            temp[1]['dy'] += norm_y - (temp[0]['y'] + temp[0]['dy'])
            temp[0]['y'] = temp[1]['dy'] + temp[1]['y']

        # Adding corri
        if passage_y > temp[1]['y'] + temp[1]['dy']:
            temp[1]['dy'] += passage_y - (temp[1]['y'] + temp[1]['dy']) + 100
            temp[0]['y'] = temp[1]['dy'] + temp[1]['y']
            temp[0]['dy'] -= passage_y - (temp[1]['y'] + temp[1]['dy']) + 100

    else:

        # Optimizing dinner space
        temp[2]['y'] = 0
        temp[2]['x'] = adjusted_x
        temp[2]['label'] = 'dinner space' 

        # Optimizing living room
        temp[1]['y'] = temp[2]['dy'] + temp[2]['y']
        temp[1]['x'] = adjusted_x
        temp[1]['dx'] = temp[2]['dx']
        if temp[1]['y'] >= norm_y:
            temp[1]['y'] = norm_y - temp[1]['dy']
            temp[2]['dy'] -= (temp[2]['dy'] - temp[1]['y'])
        temp[1]['label'] = 'living room'
        temp = temp[1:]

    # Plot fixed
    total_size = row[0][1] * row[0][2]
    row_x = elevator['Width'].values[0]
    row_y = total_size / row_x
    if row[0]['Width'] == 0.0:
        fixed = [
            {
                'label': 'living room',
                'x': adjusted_x + temp[1]['dx'],
                'y': 0,
                'dy': norm_y - elevator['Height'].values[0],
                'dx': elevator['Width'].values[0]
            }
        ]
    else:
        fixed = [
            {
                'label': 'toilet A',
                'x': adjusted_x + temp[1]['dx'],
                'y': 0,
                'dy': row_y,
                'dx': row_x
            },
            {
                'label': 'living room',
                'x': adjusted_x + temp[1]['dx'],
                'y': row_y,
                'dy': norm_y - row_y - elevator['Height'].values[0],
                'dx': elevator['Width'].values[0]
            }
        ]

    rect = temp + fixed
    return rect


def generate_service(rect, norm_y, adjusted_x, service):
    # points of origin
    x = 0
    y = 0
    width = rect['dx']
    height = rect['dy']

    # Adding rooms
    size = []
    for i in range(len(service)):
        if service.iloc[i, 1] != 0.0:
            size.append(service.iloc[i, 1] * service.iloc[i, 2])

    normed = sq.normalize_sizes(size, width, height)
    temp = sq.squarify(normed, x, y, width, height)
    temp = absolute(temp)

    if len(temp) == 2:
        # Optimizing laundry
        total = temp[1]['dx'] * temp[1]['dy']
        temp[1]['y'] = 0
        temp[1]['x'] = adjusted_x
        temp[1]['dx'] = width / 2
        temp[1]['dy'] = total / temp[1]['dx']
        temp[1]['label'] = 'laundry'

        # Optimizing kitchen
        temp[0]['y'] = 0
        temp[0]['x'] = temp[1]['dx'] + temp[1]['x']
        temp[0]['dx'] = width / 2
        temp[0]['dy'] = temp[1]['dy']
        temp[0]['label'] = 'kitchen'
    else:
       # Optimizing kitchen
        total = temp[0]['dx'] * temp[0]['dy']
        temp[0]['y'] = 0
        temp[0]['x'] = adjusted_x
        temp[0]['dx'] = width
        temp[0]['dy'] = total / temp[0]['dx']
        temp[0]['label'] = 'kitchen' 

    return temp


def generate_rooms(rects, height, elevator, private, public, service):
    new_rects = [rects[0]]

    # Generate Private
    new_rects = new_rects + generate_private(rects[1], private) 
    adjusted_y = 0
    for r in new_rects:
        if r['label'] == 'balcony A':
            adjusted_x = r['dx']
        elif r['label'] == 'kid bedroom':
            passenge_y = r['y']
    # Generate Service
    new_rects += generate_service(rects[2], height, adjusted_x, service)
    for r in new_rects:
        if r['label'] == 'kitchen':
            adjusted_y = r['dy']
    # Generate Public
    new_rects += generate_public(rects[3], public, elevator, adjusted_x, adjusted_y, passenge_y, height)
    return new_rects


def generate_layout(filepath, norm_x, norm_y, x_origin=0, y_origin=0):
    # load room data
    df = pd.read_csv(filepath)
    df.fillna(0, inplace=True)

    # divide rooms into private, public, service
    # fixed contains: part of living room
    elevator = df.loc[df['Rooms'] == 'elevator']
    private = df.loc[df['Rooms'].isin(['balcony A', 'master bedroom', 'toilet B', 'kid bedroom'])]  
    public = df.loc[df['Rooms'].isin(['living room', 'dinner space', 'toilet A', 'guest room'])]
    service = df.loc[df['Rooms'].isin(['kitchen', 'laundry'])]

    # total size of each division (in sq meter)
    size_private = sum(private['Width'] * private['Height'])
    size_public = sum(public['Width'] * public['Height'])
    size_fixed = (norm_y - elevator['Height'].values[0]) * elevator['Width'].values[0]
    toilet = public[public['Rooms'] == 'toilet A']['Width'].values[0] * public[public['Rooms'] == 'toilet A']['Height'].values[0]
    size_public = size_public - (size_fixed - toilet)
    size_service = sum(service['Width'] * service['Height'])

    # points of origin
    x = x_origin
    y = y_origin
    width = norm_x - elevator['Width'].values[0]
    height = norm_y

    # Adding elevator to plot
    rect = [
        {
            "label": 'elevator',
            "dy": elevator['Height'].values[0],
            "dx": elevator['Width'].values[0],
            "x": width,
            "y": height - elevator['Height'].values[0]
        }
    ]

    # Adding private/public/service to plot
    size = [size_private, size_service, size_public]
    normed = sq.normalize_sizes(size, width, height)
    temp = sq.squarify(normed, x, y, width, height)
    
    # Optimizing Private area layout
    total = temp[0]['dy'] * temp[0]['dx']
    temp[0]['dy'] = height
    temp[0]['dx'] = total / temp[0]['dy']

    # Optimizing Service area layout
    total = temp[2]['dy'] * temp[2]['dx']
    temp[2]['x'] = temp[0]['dx']
    temp[2]['dx'] = width - temp[0]['dx']
    temp[2]['dy'] = total / temp[2]['dx']
    temp[2]['y'] = norm_y - temp[2]['dy']

    # Optimizing Public area layout
    total = temp[1]['dy'] * temp[1]['dx']
    temp[1]['x'] = temp[0]['dx']
    temp[1]['y'] = 0
    temp[1]['dx'] = temp[2]['dx']
    temp[1]['dy'] = norm_y - temp[2]['dy']
    
    rect = rect + temp
    return generate_rooms(rect, height, elevator, private, public, service)

    # if (total/temp[2]['dx']) < (norm_y - temp[1]['dy']):
    #     temp[1]['dy'] = total/temp[1]['dx']
    # else:
    #     temp[1]['dy'] = total/temp[1]['dx']
    #     adjustment = temp[1]['y'] - (height - temp[1]['dy'])
    #     temp[1]['y'] = height - temp[1]['dy']
    #     temp[0]['dy'] -= (temp[0]['dy'] - temp[1]['y'])
    #     if adjustment < (temp[2]['dx'] / 2):
    #         temp[0]['dx'] += adjustment
    #         temp[1]['dx'] += adjustment
    #     temp[2]['x'] = temp[0]['dx']
    #     temp[2]['dx'] = width - temp[0]['dx']

    # Normalizing to total size
    # if temp[0]['dy'] + temp[1]['dy'] < norm_y:
    #     leftover_a = norm_y - temp[0]['dy'] - temp[1]['dy']
    #     temp[0]['dy'] += leftover_a/2
    #     temp[1]['dy'] += leftover_a/2
    #     temp[1]['y'] = temp[0]['dy']
    
    # Adding remaining space as unknown
    # unknown = []
    # if temp[2]['dy'] < norm_y:
    #     unknown = [
    #         {
    #             "label": 'unknown',
    #             'x': temp[2]['x'],
    #             'y': temp[2]['dy'],
    #             'dx': temp[2]['dx'],
    #             'dy': norm_y - temp[2]['dy'] 
    #         }
    #     ]