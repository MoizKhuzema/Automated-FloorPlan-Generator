import layout_1
import layout_2
import edges
import render
import squarify as sq
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # 1
    # width = 957
    # height = 876

    # 2
    # width = 1255
    # height = 903
    
    # 3
    # width = 1005
    # height = 1050

    # 4
    # width = 1030
    # height = 1245

    # 5
    width = 865
    height = 1220

    # Generating layout
    rects = layout_1.generate_layout(r'C:\Users\moizk\Desktop\Upwork\Yafei-Zhou\Squarify-Treemap\Results\exp-5\room_sizes.csv', width, height)
    
    # Generate doors and windows
    label = []
    for r in rects:
        label.append(r['label'])
    rects = rects + edges.traverse_edge('room_edges_1.csv', rects, label, width, height)

    render.render(width, height, rects)

    # Plotting result
    # sq.plot(rects, width, height, label= label)
    # plt.show()