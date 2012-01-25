import math
import matplotlib.pyplot as mp
import numpy

def quadratic_bezier_point(p0,p1,p2,t) :
    """Returns the bezier point returned with p0, p1, and p2 as reference points
    at fraction t along curve.  Reference point arguments are length 2
    numpy arrays."""
    return (1-t)**2*p0 + 2*(1-t)*t*p1 + t**2*p2

def quadratic_bezier_curve(p0,p1,p2,n=10) :
    """Returns a set of points representing the quadratic bezier curve with
    p0, p1, and p2 as reference points.  Reference point arguments are length 2
    numpy arrays, n is the number of points making up the curve."""
    curve_pts = []
    for t in numpy.arange(0,1+1./n,1./n) :
        curve_pts.append(quadratic_bezier_point(p0,p1,p2,t))
    return curve_pts

def cubic_bezier_curve(p0,p1,p2,p3,n) :
    """Returns a set of points representing the cubic bezier curve with
    p0, p1, p2, and p3 as reference points.  p0, p1, p2, and p3 are length 2
    numpy arrays, n is the number of points making up the curve."""
    curve_pts = []
    for t in numpy.arange(0,1+1./n,1./n) :
        q_point_1 = quadratic_bezier_point(p0,p1,p2,t)
        q_point_2 = quadratic_bezier_point(p1,p2,p3,t)
        curve_pts.append((1-t)*q_point_1 + t*q_point_2)
    return curve_pts

def bezier_circle(origin,radius,n) :
    """Construct a set of points of a circle centered around *origin* using
    quadratic bezier curves functions.  *n* is the number of points desired."""

    orig_pts = numpy.array(((0,1),(1,1),(1,0)))

    rot_mat_f = lambda theta : numpy.array(((numpy.cos(theta),-numpy.sin(theta)),(numpy.sin(theta),numpy.cos(theta))))
    rotations = [0,math.pi/2,math.pi,3*math.pi/2]
    circle_pts = []
    for rot in rotations :
        rot_mat = rot_mat_f(rot)
        rot_pts = numpy.dot(orig_pts,rot_mat)
        circle_pts.extend(quadratic_bezier_curve(rot_pts[0],rot_pts[1],rot_pts[2],n/4.))
    circle_pts = [x+origin for x in circle_pts]
    return circle_pts

def trig_circle(origin,radius,n) :
    """Construct a set of points of a circle centered around *origin* using
    trigonomic functions.  *n* is the number of points desired."""

    circle_pts = []
    for t in numpy.arange(0,2*math.pi+1./n,1./n) :
        x = origin[0] + radius*numpy.cos(t)
        y = origin[1] + radius*numpy.sin(t)
        circle_pts.append((x,y))
    return circle_pts

def find_best_d(A,B,C) :
    """Determine the optimal radii, distance from circle origins, and
    coordinates where circle edges intersect for given proportions::

      - *A* is the # in class A
      - *B* is the # in class B
      - *C* is the # in class A and B

    Returns 4-tuple of (A radus, B radius, distance between, intersections).
    Intersections is a 2-tuple of 2-tuple cartesian coordinates in the
    coordinate system set by the origin of circle A is (0,0).
    """

    assert C <= A and C <= B

    # the larger class gets a area of 1,
    # the smaller class gets a area of <= 1
    # intersection gets area <= area smaller class
    max_class = float(max(A,B))
    A_area = A/max_class
    B_area = B/max_class
    C_area = C/max_class
    print A, B, C
    print A_area, B_area, C_area

    A_radius = math.sqrt(A_area/math.pi)
    B_radius = math.sqrt(B_area/math.pi)

    best_d, best_area_diff = 0., 1e5
    best_vars = []
    best_intersect_points = []
    for d in numpy.arange(0,A_radius+B_radius,0.01) :
        d_m = (A_radius+B_radius-d)
        m_1 = (d**2 - B_radius**2 + A_radius**2)/(2*d)
        try :
            h = math.sqrt(A_radius**2-m_1**2)
        except :
            # complex number, not right
            continue
        m_2 = d-m_1

        # calculate lens area
        c_1_area = A_radius**2*numpy.arccos(m_1/A_radius)-m_1*math.sqrt(A_radius**2-m_1**2)
        c_2_area = B_radius**2*numpy.arccos(m_2/B_radius)-m_2*math.sqrt(B_radius**2-m_2**2)

        computed_area = c_1_area + c_2_area

        area_diff = abs(C_area-computed_area)
        if area_diff < best_area_diff :
            best_d = d
            best_area_diff = area_diff
            best_intersect_points = ((m_1,h),(m_1,-h))

    return A_radius, B_radius, best_d, best_intersect_points

"""
# drawing circles just for fun
fig = figure(figsize=(4,4))
ax = fig.gca()
ax.set_axis_off() # turns off the box and ticks

circle_pts = bezier_circle((2,3),1,40)
x,y = zip(*circle_pts)
ax.plot(x,y,'b-')

circle_pts = trig_circle((2,3),1,40)
x,y = zip(*circle_pts)
ax.plot(x,y,'g-')
"""

def do_venn(A,B,C,plot_fn=None) :
    """Create a venn diagram figure with the specified membership numbers::

      - *A* is the # in class A
      - *B* is the # in class B
      - *C* is the # in both A and B

    If *plot_fn* is not provided, no figure is written to disk and the
    matplotlib.Axis object with the diagram drawn is returned.
    """

    A_radius, B_radius, d, intersect = find_best_d(A,B,C)

    fig_width = 0.2+A_radius+d+B_radius
    fig_height = 2*A_radius+0.2

    venn = mp.figure(figsize=(4*fig_width/fig_height,4))
    venn_ax = venn.gca()
    venn_ax.set_axis_off() # turns off the box and ticks

    A_circle = trig_circle((A_radius,A_radius),A_radius,80)
    x,y = zip(*A_circle)
    venn_ax.fill(x,y,'b-',alpha=0.8)

    B_circle = trig_circle((A_radius+d,A_radius),B_radius,80)
    x,y = zip(*B_circle)
    venn_ax.fill(x,y,'r-',alpha=0.8)

    #x,y = zip(*intersect)
    #x = [x_i+A_radius for x_i in x]
    #y = [y_i+A_radius for y_i in y]
    #venn_ax.plot(x,y,'ro')

    venn_ax.set_title('A=%d A+B=%d B=%d'%(A-C,C,B-C))
    venn_ax.axis('equal')

    if plot_fn is not None :
        venn.savefig(plot_fn)

    return venn_ax

if __name__ == '__main__' :

    do_venn(10, 10, 0)
    do_venn(10, 50, 10)
    do_venn(100, 50, 10)
    do_venn(100, 50, 40)

    show()
