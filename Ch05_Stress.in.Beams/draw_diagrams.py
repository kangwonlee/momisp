import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches


def rect_section():
    # Matthias Elsen, Draw rectangles with matplotlib, Python Patterns, 2015, https://matthiaseisen.com/pp/patterns/p0203/
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    width = 0.5
    height = 1.0

    center = np.array((0.5, 0.5))
    corner_sw = center + (-0.5) * np.array((width, height))
    corner_ne = center + 0.5 * np.array((width, height))

    ax1.add_patch(
        patches.Rectangle(
            corner_sw, width, height
        )
    )

    # https://stackoverflow.com/questions/25761717/matplotlib-simple-and-two-head-arrows
    # http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.annotate.html#matplotlib.axes.Axes.annotate
    offset = height * 0.25
    plt.annotate(s='$b$',
                 xy=(corner_sw[0], offset + center[1]),
                 xytext=(corner_ne[0], offset + center[1] * 0.9625),
                 arrowprops=dict(arrowstyle='<->')
                 )

    plt.annotate(s='$h$',
                 xy=(center[0], corner_sw[1]),
                 xytext=(center[0] * 0.9625, corner_ne[1] / 0.975),
                 arrowprops=dict(arrowstyle='<->')
                 )

    offset_x = width * 0.25
    plt.annotate(s='$\\frac{h}{2}$',
                 xy=(offset_x + center[0], center[1]),
                 xytext=(offset_x + center[0] * 0.9625, corner_ne[1] / 0.955),
                 arrowprops=dict(arrowstyle='<->')
                 )

    overhang_x = width * 0.25
    plt.plot((corner_sw[0] - overhang_x, corner_ne[0] + overhang_x),
             (center[1], center[1]), 'k-.')

    # Matplotlib development team, Text properties and layout, matplotlib User's Guide, https://matplotlib.org/users/text_props.html
    ax1.set_axis_off()
    plt.show()


def rect_section_c():

    # Matthias Elsen, Draw rectangles with matplotlib, Python Patterns, 2015, https://matthiaseisen.com/pp/patterns/p0203/
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    width = 0.5
    height = 1.0

    center = np.array((0.5, 0.5))
    corner_sw = center + (-0.5) * np.array((width, height))
    corner_ne = center + 0.5 * np.array((width, height))

    ax1.add_patch(
        patches.Rectangle(
            corner_sw, width, height
        )
    )

    # https://stackoverflow.com/questions/25761717/matplotlib-simple-and-two-head-arrows
    # http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.annotate.html#matplotlib.axes.Axes.annotate
    offset = height * 0.25
    plt.annotate(s='$b$', 
                 xy=(corner_sw[0], offset + center[1]), 
                 xytext=(corner_ne[0], offset + center[1]*0.9625 ),
                 arrowprops=dict(arrowstyle='<->')
                )

    overhang_x = width * 0.25
    offset = height * (-0.25)
    plt.plot((corner_sw[0]-overhang_x, corner_ne[0]+overhang_x), 
             (offset + center[1], offset + center[1]), 'k-.')
    plt.text(corner_ne[0] + overhang_x + 0.01, offset + center[1] - .01, 'c')

    plt.annotate(s='$h$', 
                 xy=(center[0], corner_sw[1]), 
                 xytext=(center[0]*0.9625, corner_ne[1]/0.975),
                 arrowprops=dict(arrowstyle='<->')
                )

    offset_x = width * 0.25
    plt.annotate(s='$\\frac{h}{2}$', 
                 xy=(offset_x + center[0], center[1]), 
                 xytext=(offset_x + center[0]*0.9625, corner_ne[1]/0.955),
                 arrowprops=dict(arrowstyle='<->')
                )

    overhang_x = width * 0.125
    plt.plot((corner_sw[0] - overhang_x, corner_ne[0] + overhang_x), 
             (center[1], center[1]), 'k-.')

    # Matplotlib development team, Text properties and layout, matplotlib User's Guide, https://matplotlib.org/users/text_props.html
    ax1.set_axis_off()  
    plt.show()