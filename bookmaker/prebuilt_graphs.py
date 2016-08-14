from blur.markov import graph, nodes

from bookmaker import custom_nodes


def indenter():
    """
    Build and return a markov graph for indentation value behavior.

    Picking along this ``Graph`` will yield values in 72 DPI units.

    Returns:
        blur.markov.graph.Graph: A markov graph representing
            the change in indentation value from one line to the next.
            All values are in 72-dpi points.
    """
    # All values in 72-dpi points
    stay = nodes.Node(0)
    short_right = custom_nodes.SoftFloatNode([(1, 20), (3, 3), (6, 1)])
    short_left = custom_nodes.SoftFloatNode([(-1, 20), (-3, 3), (-6, 1)])
    far_right = custom_nodes.SoftFloatNode([(8, 5), (85, 25),
                                            (110, 1), (170, 10)])
    far_left = custom_nodes.SoftFloatNode([(-8, 5), (-85, 25),
                                           (-110, 1), (-170, 10)])

    stay.add_link(stay, 40)
    stay.add_link(short_right, 3)
    stay.add_link(short_left, 3)
    stay.add_link(far_right, 10)
    stay.add_link(far_left, 10)

    short_right.add_link(stay, 60)
    short_right.add_link(short_right, 100)
    short_right.add_link(short_left, 50)
    short_right.add_link(far_right, 10)
    short_right.add_link(far_left, 10)

    short_left.add_link(stay, 60)
    short_left.add_link(short_right, 30)
    short_left.add_link(short_left, 100)
    short_left.add_link(far_right, 20)

    far_right.add_link(stay, 10)

    far_left.add_link(stay, 30)

    return graph.Graph([stay, short_right, short_left, far_right, far_left])


def text_pause_or_write():
    """
    Build and return a network with two states: 1 (write) and 0 (don't write).

    Returns:
        blur.graph.Graph: A markov graph representing
            the state of writing vs. not writing
    """
    dense_write = nodes.Node(1)
    write = nodes.Node(1)
    light_write = nodes.Node(1)
    light_rest = nodes.Node(0)
    rest = nodes.Node(0)
    dense_rest = nodes.Node(0)

    dense_write.add_link(dense_write, 1000)
    dense_write.add_link(light_write, 15)
    dense_write.add_link(light_rest, 1)

    write.add_link(dense_write, 1)
    write.add_link(write, 50)
    write.add_link(light_write, 4)
    write.add_link(light_rest, 12)

    light_write.add_link(write, 4)
    light_write.add_link(light_write, 10)
    light_write.add_link(light_rest, 8)

    light_rest.add_link(dense_rest, 1)
    light_rest.add_link(light_rest, 5)
    light_rest.add_link(light_write, 14)

    rest.add_link(rest, 5)
    rest.add_link(dense_rest, 6)
    rest.add_link(light_write, 30)

    dense_rest.add_link(dense_rest, 30)
    dense_rest.add_link(rest, 2)
    dense_rest.add_link(light_write, 2)

    return graph.Graph([dense_write, write, light_write,
                        light_rest, rest, dense_rest])
