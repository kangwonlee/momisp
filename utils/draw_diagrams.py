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


def draw_beam(L_m, points_list, reaction_list, v_load_list=[], dist_load_list=[], moment_list=[]):
    """

    :param float L_m: length of the beam  
    :param list(dict) points_list: [{'x_m':x, 'label': txt}] 
    :param list(dict) reaction_list: [{'x_m':x}] 
    :param list(dict) v_load_list: [{'x_m':x, 'sign': +1 | -1}]
    :param list(dict) dist_load_list: [{'x_begin_m':x, 'x_end_m':x, 'text': txt}]
    :param list(dict) moment_list: [{'x_m':x, 'direction': 'ccw' | 'cw', 'open': 'right' | 'left', 'text': txt}]
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

    y_arrow = -1.5 * h_beam_m
    # 반력
    # Reaction force
    for reaction_dict in reaction_list:
        ax.arrow(float(reaction_dict['x_m']), y_arrow,
                 0, abs(y_arrow) * 0.7, head_width=0.1, head_length=abs(y_arrow) * 0.2)

    y_load = h_beam_m * 3
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

    # 모멘트
    # moment

    moment_radius_m = h_beam_m * 1.5

    draw_moment_arrows(ax, moment_list, moment_radius_m, y_load)

    ax.axis('equal')
    # Joe Kington, Emmet B, et al,. How to remove frame from matplotlib?, StackOverflow.com, 2016 Sep 16, https://stackoverflow.com/questions/14908576/
    ax.axis('off')
    plt.show()


def draw_moment_arrows(ax, moment_list, moment_radius_m, y_load):
    """

    :param AxesSubplot ax: (subplot) axis
    :param list(dict) moment_list: [{'x_m':x, 'direction': 'ccw' | 'cw', 'open': 'right' | 'left', 'text': txt}]
    :param float moment_radius_m:
    :param float y_load: text location
    :return:
    """
    style_radius_dict = {
        'ccw': moment_radius_m * 2.5,
        'cw': -moment_radius_m * 2.5,
    }

    delta_x_start_open_right = {
        'ccw': 0,
        'cw': 0,
    }

    delta_y_start_open_right = {
        'ccw': moment_radius_m * (2 ** -0.5),
        'cw': - moment_radius_m * (2 ** -0.5),
    }

    delta_x_end_open_right = delta_x_start_open_right

    delta_y_end_open_right = {
        'ccw': delta_y_start_open_right['cw'],
        'cw': delta_y_start_open_right['ccw'],
    }

    delta_x_start_open_left = {
        'ccw': delta_x_start_open_right['ccw'],
        'cw': delta_x_start_open_right['cw'],
    }

    delta_y_start_open_left = {
        'ccw': delta_y_start_open_right['cw'],
        'cw': delta_y_start_open_right['ccw'],
    }

    delta_x_end_open_left = delta_x_start_open_left

    delta_y_end_open_left = {
        'ccw': delta_y_start_open_left['cw'],
        'cw': delta_y_start_open_left['ccw'],
    }

    delta_x_start = {
        'right': delta_x_start_open_right,
        'left': delta_x_start_open_left,
    }

    delta_y_start = {
        'right': delta_y_start_open_right,
        'left': delta_y_start_open_left,
    }

    delta_x_end = {
        'right': delta_x_end_open_right,
        'left': delta_x_end_open_left,
    }

    delta_y_end = {
        'right': delta_y_end_open_right,
        'left': delta_y_end_open_left,
    }

    for moment_dict in moment_list:
        # http://matthiaseisen.com/matplotlib/shapes/arrow/#curved-arrow
        # ccw == + radius
        # cw == - radius

        direction = moment_dict.get('direction', 'ccw')
        open_dir = moment_dict.get('open', 'right')

        center_x = float(moment_dict['x_m'])
        center_y = 0

        start = (center_x + delta_x_start[open_dir][direction], center_y + delta_y_start[open_dir][direction])
        end = (center_x + delta_x_end[open_dir][direction], center_y + delta_y_end[open_dir][direction])

        connection_style_str = 'arc3, rad=%g' % style_radius_dict[direction]

        arrow = patches.FancyArrowPatch(start, end, connectionstyle=connection_style_str, mutation_scale=20)
        ax.add_patch(arrow)

        ax.text(float(moment_dict['x_m']), y_load + 0.1,
                moment_dict['text'], horizontalalignment='center')


def draw_stress_2d(sx_i, sy_i, txy_i, ax=None, angle_deg=0.0, b_label=False):
    sx, sy, txy = float(sx_i), float(sy_i), float(txy_i)

    s_bar = (sx + sy) / 2
    r = np.sqrt(((sx - sy) / 2) ** 2 + txy ** 2)

    s1 = s_bar + r
    s2 = s_bar - r
    den = max((abs(s1), abs(s2), abs(r)))

    # Nick Charton, Drawing and Animating Shapes with Matplotlib, nickcharton.net, https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
    if ax is None:
        fig, ax = plt.subplots()

    # square size
    square_size = 1.0

    # half of s
    s_h = square_size * 0.5

    c, s = get_cos_sin(angle_deg)

    # South West corner of the element square
    x_sw = - s_h
    y_sw = - s_h

    # rotate by angle_deg
    x_sw_t = x_sw * c + y_sw * (-s)
    y_sw_t = x_sw * s + y_sw * c

    # prepare the element square
    square = patches.Rectangle((x_sw_t, y_sw_t), square_size, square_size, angle=angle_deg)
    ax.add_patch(square)

    if not b_label:
        # prepare the sigma x arrow right
        draw_arrow_sigma_x_r(ax, s_h, sx / den, angle_deg)
        draw_arrow_sigma_x_l(ax, s_h, sx / den, angle_deg)
        draw_arrow_sigma_y_u(ax, s_h, sy / den, angle_deg)
        draw_arrow_sigma_y_l(ax, s_h, sy / den, angle_deg)
    else:
        # prepare the sigma x arrow right
        draw_arrow_sigma_x_r(ax, s_h, sx / den, angle_deg, sx)
        draw_arrow_sigma_x_l(ax, s_h, sx / den, angle_deg)
        draw_arrow_sigma_y_u(ax, s_h, sy / den, angle_deg, sy)
        draw_arrow_sigma_y_l(ax, s_h, sy / den, angle_deg)

    # tau arrows
    if 1e-6 < abs(txy / den):
        draw_arrow_tau(ax, s_h, txy / den, angle_deg)  # right vertical arrow
        draw_arrow_tau(ax, s_h, -txy / den, angle_deg + 90)  # top arrow
        draw_arrow_tau(ax, s_h, txy / den, angle_deg + 180)  # left vertical arrow
        draw_arrow_tau(ax, s_h, -txy / den, angle_deg + 270)  # bottom arrow

    plt.xlabel('$\\sigma$')
    plt.ylabel('$\\tau$')
    plt.grid(True)

    ax.axis('equal')
    ax.axis('off')


def draw_arrow_tau(ax, s_h, shaft_length, angle_deg, label_txt=None):
    arrow_center_x = s_h * 1.1
    arrow_center_y = 0

    c, s = get_cos_sin(angle_deg)

    arrow_start_x = arrow_center_x
    arrow_start_y = arrow_center_y - 0.5 * shaft_length

    x_start = arrow_start_x * c + arrow_start_y * (-s)
    y_start = arrow_start_x * s + arrow_start_y * c

    dx = 0.0 * c + shaft_length * (-s)
    dy = 0.0 * s + shaft_length * c

    head_width = abs(s_h) * 0.1
    head_length = head_width * 2.0

    shape = decide_right_or_left(x_start, y_start, dx, dy)

    arrow = ax.arrow(x_start, y_start,
                     dx, dy,
                     head_width=head_width, head_length=head_length,
                     fc='k', ec='k', shape=shape)

    # length of the arrow including the head
    dxe = (shaft_length + head_length) * c + 0.0 * (-s)
    dye = (shaft_length + head_length) * s + 0.0 * c

    # add an invisible plot to make sure the arrow is included in the axis
    arrow_pt = ax.plot((x_start, x_start + dxe), (y_start, y_start + dye), 'r.', alpha=0)

    # indicate stress value
    if label_txt is not None:
        plt.text(x_start + dxe, y_start + dye, str(label_txt))


def decide_right_or_left(x_start, y_start, dx, dy):
    cross = np.cross((x_start, y_start), (dx, dy))
    if 0 >= cross:
        shape = 'right'
    else:
        shape = 'left'
    return shape


def draw_arrow_sigma_x_r(ax, s_h, shaft_length, angle_deg, label_txt=None):
    arrow_angle_deg = angle_deg + 0
    c, s = get_cos_sin(arrow_angle_deg)

    # start point of the arrow
    x_start = s_h * c + 0.0 * (-s)
    y_start = s_h * s + 0.0 * c

    dx = shaft_length * c + 0.0 * (-s)
    dy = shaft_length * s + 0.0 * c

    head_width = abs(s_h) * 0.1
    head_length = head_width * 2.0

    arrow_x_r = ax.arrow(x_start, y_start, dx, dy, head_width=head_width, head_length=head_length, fc='k', ec='k')

    # length of the arrow including the head
    dxe = (shaft_length + head_length) * c + 0.0 * (-s)
    dye = (shaft_length + head_length) * s + 0.0 * c

    # add an invisible plot to make sure the arrow is included in the axis
    arrow_x_r_pt = ax.plot((x_start, x_start + dxe), (y_start, y_start + dye), 'r.', alpha=0)

    # indicate stress value
    if label_txt is not None:
        plt.text(x_start + dxe, y_start + dye, str(label_txt))


def draw_arrow_sigma_x_l(ax, s_h, shaft_length, angle_deg, label_txt=None):
    draw_arrow_sigma_x_r(ax, s_h, shaft_length, angle_deg + 180, label_txt=label_txt)


def draw_arrow_sigma_y_u(ax, s_h, shaft_length, angle_deg, label_txt=None):
    draw_arrow_sigma_x_r(ax, s_h, shaft_length, angle_deg + 90, label_txt=label_txt)


def draw_arrow_sigma_y_l(ax, s_h, shaft_length, angle_deg, label_txt=None):
    draw_arrow_sigma_x_r(ax, s_h, shaft_length, angle_deg + 270, label_txt=label_txt)


def get_cos_sin(angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return c, s


def plot_mohr_circle(sx_i, sy_i, tau_i, ax=None, b_stress=True):
    if ax is None:
        ax = plt.gca()

    # in case input needs to be converted
    sx, sy, tau = float(sx_i), float(sy_i), float(tau_i)

    s_bar = (sx + sy) * 0.5
    radius = (((sx - sy) * 0.5) ** 2 + tau ** 2) ** 0.5

    # prepare circle patch
    circle = patches.Circle((s_bar, 0), radius, fill=None)

    # add circle patch to axis
    ax.add_patch(circle)

    xlims = plt.xlim()
    if 0 < xlims[0]:
        xlims[0] = 0
    elif 0 > xlims[1]:
        xlims[1] = 0

    # indicate stress status direction
    plt.plot((0, sx, sy, 0), (-tau, -tau, tau, tau), '.-')

    if b_stress:
        normal_symbol = '\\sigma'
        shear_symbol = '\\tau'
    else:
        normal_symbol = '\\epsilon'
        shear_symbol = '\\frac{1}{2}\\gamma'

    # sigma 1
    plt.text(s_bar + radius, 0, '$%s_1$ = %g' % (normal_symbol, (s_bar + radius)), ha='center')
    # sigma 2
    plt.text(s_bar - radius, 0, '$%s_2$ = %g' % (normal_symbol, (s_bar - radius)), ha='center')
    # |tau max|
    plt.text(s_bar, radius, '$\\left|%s_{max}\\right|= %g$' % (shear_symbol, radius), ha='center')
    # primary direction
    plt.text((s_bar + sx) * 0.5, (0 - tau) * 0.5,
             '$2\\theta$ = %g(deg)' % np.rad2deg(np.arctan2(tau, (sx - sy) * 0.5)), ha='center')

    plt.axis('equal')
    plt.grid(True)
    plt.xlabel('$%s$' % normal_symbol)
    plt.ylabel('$%s$' % shear_symbol)


def plot_3d_mohr_circle_123(s1_i, s2_i, s3_i=0, ax=None):
    """

    :param float s1_i: principal stress 1
    :param float s2_i: principal stress 2
    :param float s3_i: principal stress 3
    :param AxesSubplot ax: axis to plot
    :return:
    """
    if ax is None:
        ax = plt.gca()

    # in case input needs to be converted
    s1, s2, s3 = float(s1_i), float(s2_i), float(s3_i),

    # diameters of all possible combinations of the principal stress components
    diameters_tuple = (
        (s1, s2),
        (s2, s3),
        (s3, s1),
    )

    # diameter loop
    for diameter in diameters_tuple:
        x1, x2 = diameter

        # center of the circle
        center_x = (x1 + x2) * 0.5
        center_y = 0.0

        # radius of the circle
        r = abs(x2 - center_x)

        # prepare a circle patch
        circle = patches.Circle((center_x, center_y), r, fill=False)

        # add circle patch to the axis
        ax.add_patch(circle)

    # add axis labels
    plt.xlabel('$\\sigma$')
    plt.ylabel('$\\tau$')

    plt.grid(True)
    plt.axis('equal')


def test_mohr_circle_3d():
    s123_list = (
        (50, 20, 0),
        (50, -20, 0),
        (5, 2, 1),
        (-5, -2, 0),
    )

    for k, s123 in enumerate(s123_list):
        ax = plt.subplot(2, 2, k + 1)
        s1, s2, s3 = s123
        plot_3d_mohr_circle_123(s1, s2, s3, ax=ax)

    plt.show()


def test_stress_2d():
    sx, sy, txy = 40, 20, 16
    angle_deg_list = (0.0, 30, -30, 120)

    for k, angle_deg in enumerate(angle_deg_list):
        ax = plt.subplot(2, 2, k + 1)
        draw_stress_2d(sx, sy, ((-1) ** k) * txy, ax=ax, angle_deg=angle_deg)

    plt.show()


def test_mohr_circle_2d():
    plot_mohr_circle(40, 20, 16)

    plt.show()


if __name__ == '__main__':
    test_mohr_circle_2d()
