import networkx as nx


def generate_layout(G, width, height):
    # Setting boundary
    total_w = G.nodes['toilet B']['Width'] * G.nodes['toilet B']['Height']
    total_w = (G.nodes['master bedroom']['Width'] * 2) + G.nodes['living room']['Width'] + (total_w / G.nodes['master bedroom']['Width'])

    if total_w > width:
        diff = total_w - width
        for i in ['living room', 'master bedroom']:
            total = G.nodes[i]['Width'] * G.nodes[i]['Height']
            G.nodes[i]['Width'] -= diff/3
            G.nodes[i]['Height'] = total / G.nodes[i]['Width']


    passange_y = 200

    # Center living room
    w = G.nodes['living room']['Width']
    h = G.nodes['living room']['Height']
    rects = [
        {
            'label': 'living room',
            'x': (width / 2) - (w / 2),
            'y': (height / 2) - (h / 2),
            'dx': w,
            'dy': h 
        }
    ]

    # Add rooms connected to living room
    x = (width / 2) - (w / 2)
    y = (height / 2) - (h / 2)
    left_flag = 0
    right_flag = 0
    top_flag = 0
    bottom_flag = 0
    for a, b in G.edges():
        if a == 'elevator' or b == 'elevator':
            continue
        if a == 'balcony' or b == 'balcony':
            continue
        if a == 'kid bedroom' or b == 'kid bedroom':
            continue
        if a == 'living room' or b == 'living room':
            if a == 'living room':
                a = b
                b = 'living room'

            # Add room left of living room
            if not left_flag:
                G.remove_edge(a, b)
                rects.append(
                    {
                        'label': a,
                        'x': x - G.nodes[a]['Width'],
                        'y': y,
                        'dx': G.nodes[a]['Width'],
                        'dy': G.nodes[a]['Height']
                    }
                )

                if a == 'guest room' or 'guest room' not in G.nodes():
                    left_flag = 1
                    y = ((height / 2) - (h / 2)) + G.nodes['living room']['Height']
                    x = (width / 2) - (w / 2)
                else:
                    x -= G.nodes[a]['Width']
                    y += G.nodes[a]['Height']
                continue
        
            # Adding rooms to the top
            if not top_flag:
               if (x + G.nodes[a]['Width']) <= ((width / 2) - (w / 2) + w):
                G.remove_edge(a, b)
                rects.append(
                        {
                            'label': a,
                            'x': x,
                            'y': y,
                            'dx': G.nodes[a]['Width'],
                            'dy': G.nodes[a]['Height']
                        }
                    )
                x += G.nodes[a]['Width']
                continue
               
               else:
                    if x == (width / 2) - (w / 2):
                       rects.append(
                            {
                                'label': a,
                                'x': x - (G.nodes[a]['Width'] - G.nodes['living room']['Width']),
                                'y': y,
                                'dx': G.nodes[a]['Width'],
                                'dy': G.nodes[a]['Height']
                            }
                        )
                       G.remove_edge(a, b)
                       top_flag = 1
                       x = (width / 2) - (w / 2) + G.nodes['living room']['Width']
                       y = ((height / 2) - (h / 2) + G.nodes['living room']['Height']) - (G.nodes['elevator']['Height'] / 2)
                       continue
                    top_flag = 1
                    x = (width / 2) - (w / 2) + G.nodes['living room']['Width']
                    y = ((height / 2) - (h / 2) + G.nodes['living room']['Height']) - (G.nodes['elevator']['Height'] / 2)

            # Adding rooms to the right
            if not right_flag:
               G.remove_edge(a, b)
               rects.append(
                    {
                        'label': a,
                        'x': x,
                        'y': y - G.nodes[a]['Height'],
                        'dx': G.nodes[a]['Width'],
                        'dy': G.nodes[a]['Height']
                    }
                )
               
               if (y - G.nodes[a]['Height']) < ((height / 2) - (h / 2) + 50):
                    right_flag = 1
                    y = (height / 2) - (h / 2)
               else:
                    y -= G.nodes[a]['Height']
               continue

            # Adding rooms to the bottom
            if not bottom_flag:
               G.remove_edge(a, b)
               rects.append(
                    {
                        'label': a,
                        'x': x - G.nodes[a]['Width'],
                        'y': y - G.nodes[a]['Height'],
                        'dx': G.nodes[a]['Width'],
                        'dy': G.nodes[a]['Height']
                    }
                )
               
               if (x - G.nodes[a]['Width']) < ((width / 2) - (w / 2) + (G.nodes['balcony']['Width'] / 2)):
                    bottom_flag = 1
               else:
                    x -= G.nodes[a]['Width']
               continue

    # Adding balcony
    if bottom_flag:
        total = G.nodes['balcony']['Width'] * G.nodes['balcony']['Height']
        rects.append(
            {
                'label': 'balcony',
                'x': (width / 2) - (w / 2) - (G.nodes['master bedroom']['Width']),
                'dx': G.nodes['master bedroom']['Width'],
                'dy': total / G.nodes['master bedroom']['Width'],
                'y': ((height / 2) - (h / 2)) - (total / G.nodes['master bedroom']['Width'])
            }
        )
    else:
        rects.append(
            {
                'label': 'balcony',
                'x': (width / 2) - (w / 2) - (G.nodes['balcony']['Width'] / 2),
                'y': (height / 2) - (h / 2) - G.nodes['balcony']['Height'],
                'dx': G.nodes['balcony']['Width'],
                'dy': G.nodes['balcony']['Height']
            }
        )
    G.remove_edge('balcony', 'living room')
    G.remove_edge('master bedroom', 'balcony')

    # Adding elevator
    rects.append(
        {
            'label': 'elevator',
            'x': ((width / 2) - (w / 2)) + G.nodes['living room']['Width'],
            'y': ((height / 2) - (h / 2) + G.nodes['living room']['Height']) - (G.nodes['elevator']['Height'] / 2),
            'dx': G.nodes['elevator']['Width'],
            'dy': G.nodes['elevator']['Height']
        }
    )
    G.remove_edge('elevator', 'living room')

    # Adding toilet B
    total_toilet = G.nodes['toilet B']['Width'] * G.nodes['toilet B']['Height']
    rects.append(
        {
            'label': 'toilet B',
            'y': (height / 2) - (h / 2),
            'dy': G.nodes['master bedroom']['Height'],
            'dx': total_toilet / G.nodes['master bedroom']['Height'],
            'x': (width / 2) - (w / 2) - G.nodes['master bedroom']['Width'] - (total_toilet / G.nodes['master bedroom']['Height'])
        }
    )
    G.remove_edge('master bedroom', 'toilet B')

    # Adding kid bedroom
    total = G.nodes['kid bedroom']['Width'] * G.nodes['kid bedroom']['Height']
    rects.append(
        {
            'label': 'kid bedroom',
            'y': (height / 2) - (h / 2),
            'dy': G.nodes['master bedroom']['Height'],
            'dx': total / G.nodes['master bedroom']['Height'],
            'x': ((width / 2) - (w / 2)) - (total_toilet / G.nodes['master bedroom']['Height']) - G.nodes['master bedroom']['Width'] - (total / G.nodes['master bedroom']['Height'])
        }
    )
    G.remove_edge('kid bedroom', 'living room')

    # Adjusting Guest room
    guest = []
    master = []
    living = []
    elevator = []
    dinner = []
    for rect in rects:
        if rect['label'] == 'guest room':
            rect['y'] += passange_y
            rect['dy'] += passange_y
            guest = rect
        elif rect['label'] == 'master bedroom':
            master = rect
        elif rect['label'] == 'living room':
            living = rect
        elif rect['label'] == 'elevator':
            elevator = rect
        elif rect['label'] == 'dinner space':
            dinner = rect

    # Adding kitchen
    i = 0
    flag = 0
    while rects[i]['label'] != 'dinner space':
        i += 1
    total = G.nodes['kitchen']['Width'] * G.nodes['kitchen']['Height']
    if len(guest): 
        if rects[i]['dy'] - (guest['y'] - rects[i]['y']) > 0:
            rects.append(
                    {
                        'label': 'kitchen',
                        'y': guest['y'],
                        'dy': rects[i]['dy'] - (guest['y'] - rects[i]['y']),
                        'dx': total / rects[i]['dy'],
                        'x': rects[i]['x'] - (total / rects[i]['dy'])
                    }
                )
            if rects[-1]['x'] < (guest['x'] + guest['dx']):
                rects[-1]['dx'] -= (guest['x'] + guest['dx'] - rects[-1]['x'])
                rects[-1]['x'] = rects[i]['x'] - rects[-1]['dx']
        else:
            rects.append(
                    {
                        'label': 'kitchen',
                        'y': guest['y'],
                        'dy': guest['dy'],
                        'dx': total / guest['dy'],
                        'x': rects[i]['x'] - (total / guest['dy'])
                    }
                )
            flag = 1     
            rects[i]['dy'] += 200
    else:
        y_adj = (living['y'] + living['dy']) - (master['y'] + master['dy'])
        rects.append(
                {
                    'label': 'kitchen',
                    'x': rects[i]['x'] - G.nodes['kitchen']['Width'],
                    'y': rects[i]['y'] + (200 - y_adj),
                    'dx': G.nodes['kitchen']['Width'],
                    'dy': G.nodes['kitchen']['Height']
                }
            )
    G.remove_edge('dinner space', 'kitchen')
    elevator['y'] = rects[i]['y'] + (rects[i]['dy'] / 2)
    elevator['x'] = rects[i]['x'] + rects[i]['dx']

    # Adding passenger
    kid = []
    kitchen = []
    for rect in rects:
        if rect['label'] == 'kid bedroom':
            kid = rect
        elif rect['label'] == 'kitchen':
            kitchen = rect
    rects.append(
        {
            'label': 'passenger',
            'x': kid['x'],
            'y': master['y'] + master['dy'],
            'dy': passange_y,
            'dx': living['x'] - kid['x']
        }
    )
    
    # Adjust Guest Room
    if len(guest):
        total = guest['dx'] * guest['dy']
        guest['x'] = kid['x']
        if 'toilet A' in G.nodes():
            if ((kitchen['x'] - kid['x']) - G.nodes['toilet A']['Width']) < kid['dx']:
                guest['dx'] += kitchen['x'] - (guest['x'] + guest['dx'])
            else:
                guest['dx'] = (kitchen['x'] - kid['x']) - G.nodes['toilet A']['Width']
        else:
            guest['dx'] = (kitchen['x'] - kid['x'])
        guest['dy'] = total / guest['dx']
        if flag == 1:
            kitchen['dy'] = guest['dy']

    # Adjust Kitchen
    dinner_flag = 0
    if len(guest):
        if kitchen['dy'] < 150 and len(guest) != 0:
            kitchen['dy'] = guest['dy']
    else:
        kitchen['x'] = dinner['x']
        kitchen['y'] = dinner['y'] + dinner['dy']
        kitchen['dx'] = dinner['dx']
        dinner_flag = 1

    # Adding toilet A
    toilet = []
    for rect in rects:
        if rect['label'] == 'toilet B':
            toilet = rect 
    if 'toilet A' in G.nodes():
        if len(guest):
            if ((rects[-2]['x']) - (guest['x'] + guest['dx'])) >= 100:
                total = G.nodes['toilet A']['Width'] * G.nodes['toilet A']['Height']
                rects.append(
                    {
                        'label': 'toilet A',
                        'x': guest['x'] + guest['dx'],
                        'y': guest['y'],
                        'dx': (rects[-2]['x']) - (guest['x'] + guest['dx']),
                        'dy': kitchen['dy']
                    }
                )
            else:
                total = G.nodes['toilet A']['Width'] * G.nodes['toilet A']['Height']
                rects.append(
                    {
                        'label': 'toilet A',
                        'y':  kid['y'] + (kid['dy'] / 2),
                        'dy': passange_y + (kid['dy'] / 2),
                        'dx': total / (passange_y + (kid['dy'] / 2)),
                        'x': rects[-1]['x'] - (total / (passange_y + (kid['dy'] / 2)))
                    }
                )
            
        else:
            total = G.nodes['toilet A']['Width'] * G.nodes['toilet A']['Height']
            rects.append(
                {
                    'label': 'toilet A',
                    'y':  kid['y'] + (kid['dy'] / 2),
                    'dy': passange_y + (kid['dy'] / 2),
                    'dx': total / (passange_y + (kid['dy'] / 2)),
                    'x': rects[-1]['x'] - (total / (passange_y + (kid['dy'] / 2)))
                }
            )

    return rects, dinner_flag