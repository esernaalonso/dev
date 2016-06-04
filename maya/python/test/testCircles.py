import pymel.core as pm


def get_circles():
    circle_nodes = []

    all_nodes = pm.ls(type="transform")

    for node in all_nodes:
        node = pm.PyNode(node)
        shapes = node.listRelatives(shapes=True)

        if shapes:
            for shape in shapes:
                connections = shape.listConnections(source=True)

                if connections:
                    for connection in connections:
                        print connection
                        print str(type(connection))
                        if str(type(connection)) == "<class 'pymel.core.nodetypes.MakeNurbCircle'>":
                            circle_nodes.append(node)

    return circle_nodes

circles = get_circles()
print "=================================================="
for circle in circles:
    print circle
print "=================================================="
