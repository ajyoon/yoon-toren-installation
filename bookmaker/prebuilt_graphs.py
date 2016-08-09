from blur.markov import graph, nodes

from bookmaker import custom_nodes


def indenter():
    """
    Build and return a markov graph for indentation value behavior.

    Picking along this ``Graph`` will yield values in 72 DPI units.

    Returns:
        blur.markov.graph.Graph: A markov graph representing
            indentation values
    :return: instance of chance.network.Network
    """
    n1 = nodes.Node(0)
    n2 = custom_nodes.SoftFloatNode([(1, 20), (3, 3), (11, 1)])
    n3 = custom_nodes.SoftFloatNode([(-1, 20), (-3, 3), (-11, 1)])
    n4 = custom_nodes.SoftFloatNode([(14, 5), (85, 25), (110, 1), (170, 10)])
    n5 = custom_nodes.SoftFloatNode([(-14, 5), (-85, 25),
                                     (-110, 1), (-170, 10)])

    n1.add_link(n1, 40)
    n1.add_link(n2, 3)
    n1.add_link(n3, 3)
    n1.add_link(n4, 10)
    n1.add_link(n5, 10)

    n2.add_link(n1, 60)
    n2.add_link(n2, 100)
    n2.add_link(n3, 50)
    n2.add_link(n4, 10)
    n2.add_link(n5, 10)

    n3.add_link(n1, 60)
    n3.add_link(n2, 30)
    n3.add_link(n3, 100)
    n3.add_link(n4, 20)

    n4.add_link(n1, 10)

    n5.add_link(n1, 30)

    return graph.Graph([n1, n2, n3, n4, n5])


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
