import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path


def render(width, height, rects):
    # Initalize graph
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot rectangles
    for rect in rects:
        if rect['label'] == 'door':
            if rect['dy'] < rect['dx']:
                verts = [[rect['x'], rect['y']], [rect['x'], rect['y'] + rect['dy'] + 70], [rect['x'] + rect['dx'] - 15, rect['y']], [rect['x'], rect['y']]]
            else:
                verts = [[rect['x'], rect['y']], [rect['x'], rect['y'] + rect['dy']], [rect['x'] + rect['dx'] + 50, rect['y']], [rect['x'], rect['y']]]
            path = Path(verts)
            patch = PathPatch(path, facecolor ='none', joinstyle= 'round')
            ax.add_patch(patch)

        elif rect['label'] == 'window':
            ax.add_patch( Rectangle((rect['x'], rect['y']),
                        rect['dx'], rect['dy'],
                        color ='#F5F5F5',
                        ec = 'black',
                        lw = 0.5) )

        else:
            if rect['label'] == 'master bedroom' or rect['label'] == 'kid bedroom' or rect['label'] == 'guest room':
                color = '#F5DEB3'
            elif rect['label'] == 'living room' or rect['label'] == 'dinner space' or rect['label'] == 'passenger':
                color ='#D2B48C'
            elif rect['label'] == 'toilet A' or rect['label'] == 'toilet B' or rect['label'] == 'balcony' or rect['label'] == 'kitchen':
                color = '#F0F8FF'
            else:
                color = '#FFA500'

            ax.add_patch( Rectangle((rect['x'], rect['y']),
                        rect['dx'], rect['dy'],
                        color = color,
                        ec = 'black',
                        lw = 5) )
            cx = rect['x'] + rect['dx']/2.0
            cy = rect['y'] + rect['dy']/2.0
            if rect['label'] == 'toilet B':
                ax.annotate(rect['label'], (cx, cy), color='black', fontsize=10, ha='center', va='center', rotation= 90)
            else:
                ax.annotate(rect['label'], (cx, cy), color='black', fontsize=10, ha='center', va='center')

    # Show figure 
    plt.xlim([-100, width + 100])
    plt.ylim([-100, height +100])
    ax.set_axis_off()
    plt.show()

    
