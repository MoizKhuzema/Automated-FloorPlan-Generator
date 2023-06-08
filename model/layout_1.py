import networkx as nx


def generate_layout(G, width, height):
    # Setting boundary
    total_w = G.nodes['toilet B']['Width'] * G.nodes['toilet B']['Height']
    total_w = G.nodes['master bedroom']['Width'] + G.nodes['living room']['Width'] + (total_w / G.nodes['master bedroom']['Width']) + G.nodes['dinner space']['Width']
    if total_w > width:
        diff = total_w - width
        for i in ['living room', 'master bedroom']:
            total = G.nodes[i]['Width'] * G.nodes[i]['Height']
            G.nodes[i]['Width'] -= diff/3
            G.nodes[i]['Height'] = total / G.nodes[i]['Width']

    passange_x = 0

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

                if (y + G.nodes[a]['Height']) > (((height / 2) - (h / 2)) + h - 50):
                    left_flag = 1
                    y = ((height / 2) - (h / 2)) + G.nodes['living room']['Height']
                else:
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
               if (x + G.nodes[a]['Width']) > passange_x:
                   passange_x = x + G.nodes[a]['Width']
               
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

    dinner = []
    master = []
    living = []
    kid = []
    guest = []
    for rect in rects:
        if rect['label'] == 'dinner space':
            dinner = rect
        elif rect['label'] == 'master bedroom':
            master = rect
        elif rect['label'] == 'guest room':
            guest = rect
        elif rect['label'] == 'living room':
            living = rect
        elif rect['label'] == 'kid bedroom':
            kid = rect

    # Adjusting kid bedroom
    total = kid['dx'] * kid['dy']
    if 'guest room' in G.nodes():
        if guest['x'] == living['x']:
            total = kid['dx'] * kid['dy']
            kid['dx'] = master['dx']
            kid['dy'] = master['dy']
            kid['x'] = living['x'] - kid['dx']
        elif kid['x'] == living['x'] and 'toilet A' not in G.nodes():
            kid['dx'] = living['dx']
            kid['dy'] = total / kid['dx']

    # Adjusting dinner space
    total = dinner['dx'] * dinner['dy']
    if (dinner['x'] + dinner['dx']) == (living['x'] + living['dx']):
        dinner['x'] = living['x']
        dinner['dx'] = living['dx']

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
    if passange_x == 0:
        passange_x = living['x'] + living['dx'] + 300
    rects.append(
        {
            'label': 'elevator',
            'x': passange_x,
            'y': ((height / 2) - (h / 2) + G.nodes['living room']['Height']) - (G.nodes['elevator']['Height'] / 2),
            'dx': G.nodes['elevator']['Width'],
            'dy': G.nodes['elevator']['Height']
        }
    )
    G.remove_edge('elevator', 'living room')

    # Adding passenger
    rects.append(
        {
            'label': 'passenger',
            'x': (width / 2) - (w / 2) + G.nodes['living room']['Width'],
            'y': ((height / 2) - (h / 2) + G.nodes['living room']['Height']) - (G.nodes['elevator']['Height'] / 2),
            'dx': passange_x - ((width / 2) - (w / 2) + G.nodes['living room']['Width']),
            'dy': (G.nodes['elevator']['Height'] / 2)
        }
    )

    # Adding toilet B
    total = G.nodes['toilet B']['Width'] * G.nodes['toilet B']['Height']
    rects.append(
        {
            'label': 'toilet B',
            'y': (height / 2) - (h / 2),
            'dy': G.nodes['master bedroom']['Height'],
            'dx': total / G.nodes['master bedroom']['Height'],
            'x': (width / 2) - (w / 2) - G.nodes['master bedroom']['Width'] - (total / G.nodes['master bedroom']['Height'])
        }
    )
    G.remove_edge('master bedroom', 'toilet B')

    # Adding kitchen
    i = 0
    dinner_flag = 0
    while rects[i]['label'] != 'dinner space':
        i += 1
    total = G.nodes['kitchen']['Width'] * G.nodes['kitchen']['Height']
    if right_flag == 0 and rects[i]['x'] == living['x']:
        rects.append(
            {
                'label': 'kitchen',
                'x': dinner['x'] + dinner['dx'],
                'dy': dinner['dy'],
                'dx': total/dinner['dy'],
                'y': dinner['y']
            }
        )
        dinner_flag = 1
    else:
        rects.append(
                {
                    'label': 'kitchen',
                    'x': rects[i]['x'],
                    'dx': dinner['dx'],
                    'dy': total / dinner['dx'],
                    'y': rects[i]['y'] - (total / dinner['dx'])
                }
            )
    G.remove_edge('dinner space', 'kitchen')

    # # Adding toilet A
    # if G.edges():
    #     i = 0
    #     while rects[i]['label'] != 'guest room':
    #         i += 1
    #         if i > len(rects):
    #             break
    #     if i <= len(rects) and rects[i]['x'] == (width / 2) - (w / 2):
    #         if guest['x'] == living['x']:
    #             total = G.nodes['toilet A']['Height'] * G.nodes['toilet A']['Width']
    #             rects.append(
    #                 {
    #                     'label': 'toilet A',
    #                     'x': guest['x'] + guest['dx'],
    #                     'y': ((height / 2) - (h / 2) + G.nodes['living room']['Height']),
    #                     'dy': guest['dy'],
    #                     'dx': total / guest['dy']
    #                 }
    #             )
    #         else:
    #             rects.append(
    #                 {
    #                     'label': 'toilet A',
    #                     'x': rects[i]['x'] + rects[i]['dx'],
    #                     'y': rects[i]['y'],
    #                     'dy': G.nodes['toilet A']['Height'],
    #                     'dx': G.nodes['toilet A']['Width']
    #                 }
    #             )
    #     else:
    #         total = G.nodes['toilet A']['Height'] * G.nodes['toilet A']['Width']
    #         rects.append(
    #             {
    #                 'label': 'toilet A',
    #                 'x': kid['x'] + kid['dx'],
    #                 'y': ((height / 2) - (h / 2) + G.nodes['living room']['Height']),
    #                 'dy': kid['dy'],
    #                 'dx': total / kid['dy']
    #             }
    #         )

    return rects, dinner_flag