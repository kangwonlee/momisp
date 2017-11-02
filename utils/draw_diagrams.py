import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


def rect_section():
    ax1, width, height, corner_sw, corner_ne, center = rect_section_base()

    show_diagram(ax1)


def show_diagram(ax1):
    # Matplotlib development team, Text properties and layout, matplotlib User's Guide, https://matplotlib.org/users/text_props.html
    ax1.set_axis_off()
    plt.show()


def rect_section_base(centroid_overhang=0.25):
    # Matthias Elsen, Draw rectangles with matplotlib, Python Patterns, 2015, https://matthiaseisen.com/pp/patterns/p0203/
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    # size of the section
    width = 0.5
    height = 1.0
    # coordinates of the section
    center = np.array((0.5, 0.5))
    corner_sw = center + (-0.5) * np.array((width, height))
    corner_ne = center + 0.5 * np.array((width, height))
    # draw a rectangle
    ax1.add_patch(
        patches.Rectangle(
            corner_sw, width, height
        )
    )
    # indicate dimensions : b, h, h/2
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
    # rotational axis at the centroid
    overhang_x = width * centroid_overhang
    plt.plot((corner_sw[0] - overhang_x, corner_ne[0] + overhang_x),
             (center[1], center[1]), 'k-.')
    return ax1, width, height, corner_sw, corner_ne, center


def rect_section_c():

    centroid_overhang = 0.125

    ax1, width, height, corner_sw, corner_ne, center = rect_section_base(centroid_overhang)

    # add a new rotation axis c
    overhang_x = width * 0.25
    offset = height * (-0.25)
    plt.plot((corner_sw[0]-overhang_x, corner_ne[0]+overhang_x), 
             (offset + center[1], offset + center[1]), 'k-.')
    plt.text(corner_ne[0] + overhang_x + 0.01, offset + center[1] - .01, 'c')

    show_diagram(ax1)


def draw_beam(L_m, points_list, reaction_list, v_load_list=[], dist_load_list=[]):
    """

    :param float L_m: length of the beam  
    :param list(dict) points_list: [{'x_m':x, 'label': txt}] 
    :param list(dict) reaction_list: [{'x_m':x}] 
    :return: 
    """

    # input argument cleansing
    L_m = float(L_m)

    # Nick Charton, Drawing and Animating Shapes with Matplotlib, nickcharton.net, https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
    fig, ax = plt.subplots()

    h_beam_m = L_m / 20.0

    beam_patch = plt.Rectangle((0, 0), L_m, h_beam_m)
    ax.add_patch(beam_patch)

    y_text = -1

    for point_dict in points_list:
        ax.text(float(point_dict['x_m']), y_text, point_dict['text'])

    y_arrow = -0.5
    # 반력
    # Reaction force
    for reaction_dict in reaction_list:
        ax.arrow(float(reaction_dict['x_m']), y_arrow,
                 0, abs(y_arrow) * 0.7, head_width=0.1, head_length=abs(y_arrow) * 0.2)

    y_load = h_beam_m * 2
    # 집중하중 P
    # Concentrated shear force load P
    for v_load_dict in v_load_list:
        # arrow heading upward
        if 0 < v_load_dict['sign']:
            ax.arrow(float(v_load_dict['x_m']), h_beam_m + 0.1,
                     0, abs(y_arrow) * 0.7, head_width=0.1, head_length=abs(y_arrow) * 0.2)
        # arrow heading downward
        elif 0 > v_load_dict['sign']:
            ax.arrow(float(v_load_dict['x_m']), y_load,
                     0, - abs(y_arrow) * 0.7, head_width=0.1, head_length=abs(y_arrow) * 0.2)

    # 분포하중 w0
    # Distributed load w0
    for dist_load_dict in dist_load_list:
        x_load_m_array = np.linspace(float(dist_load_dict['x_begin_m']),
                                     float(dist_load_dict['x_end_m']), 10 + 1)
        y_load_m_array = np.ones_like(x_load_m_array) * y_load
        u_load_m_array = np.zeros_like(x_load_m_array)
        v_load_m_array = np.ones_like(x_load_m_array) * (h_beam_m * -1)

        ax.quiver(x_load_m_array, y_load_m_array,
                  u_load_m_array, v_load_m_array)

        ax.text((float(dist_load_dict['x_begin_m']) + float(dist_load_dict['x_end_m'])) * 0.5, y_load + 0.1,
                dist_load_dict['text'], horizontalalignment='center')

    ax.axis('equal')
    # Joe Kington, Emmet B, et al,. How to remove frame from matplotlib?, StackOverflow.com, 2016 Sep 16, https://stackoverflow.com/questions/14908576/
    ax.axis('off')
    plt.show()