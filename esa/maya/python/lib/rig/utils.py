"""Contains definition utils for rigging"""

#######################################
# imports

import maya.cmds as cmds
import pymel.core as pm

#######################################
# functionality


def create_node_by_type(node_type, **kwargs):
    """Create node by type.

    Args:
        node_type (str): Type of the node to be created
        **kwargs: Extra arguments to use in some nodes types creation.

    Returns:
        PyNode: New node of the goal and use specified.
    """

    cmds.select(clear=True)

    if node_type == "spaceLocator":
        return pm.PyNode(cmds.spaceLocator(p=(0, 0, 0))[0])

    elif node_type == "empty":
        return pm.PyNode(cmds.group(empty=True))

    elif node_type == "joint":
        return pm.PyNode(cmds.joint())

    elif node_type == "circle":
        radius = kwargs["radius"] if "radius" in kwargs else 5
        degree = kwargs["degree"] if "degree" in kwargs else 3
        sections = kwargs["sections"] if "sections" in kwargs else 8
        sweep = kwargs["sweep"] if "sweep" in kwargs else 360
        normal = kwargs["normal"] if "normal" in kwargs else (0, 1, 0)

        return pm.PyNode(cmds.circle(radius=radius, degree=degree, sections=sections, sweep=sweep, normal=normal)[0])

    elif node_type == "renderBox":
        sizeX = kwargs["sizeX"] if "sizeX" in kwargs else 2
        sizeY = kwargs["sizeY"] if "sizeY" in kwargs else 2
        sizeZ = kwargs["sizeZ"] if "sizeZ" in kwargs else 2

        new_node = pm.PyNode(cmds.createNode("renderBox"))

        new_node.attr("sizeX").set(sizeX)
        new_node.attr("sizeY").set(sizeY)
        new_node.attr("sizeZ").set(sizeZ)

        return pm.PyNode(new_node.listRelatives(parent=True, fullPath=True)[0])

    elif node_type == "PlusMinusAverage":
        return pm.PyNode(pm.shadingNode("plusMinusAverage", asUtility=True))


def align(source, target, switch=None, invert=None, offset_translation=None):
    """Aligns two nodes using matrices. If aligns axes given,
        aligns using different axis correspondence between objects.

    Args:
        source (PyNode): Node to align.
        target (PyNode): Node to use as target on the align process.
        switch (str, optional): Axes to switch orientation, inverting the third one. Valid values: "xy", "yx", "xz", "zx", "yz", "zy".
        invert (str, optional): Axis to invert. Valid values: "x", "y", "z", "xy", "yx", "xz", "zx", "yz", "zy", "xyz", ...
        offset_translation (list of int, optional): list of integers that can be used to offset the translation.
    """
    # Only if source and target are given.
    if source and target:
        # First stores the target transform matrix to apply
        align_transform = pm.xform(target, q=True, ws=True, m=True)

        if switch or invert:
            # Creates two auxiliary nodes to help in the offset transform.
            # One aligned to the world.
            # The second one, with switched or inverted axes in the matrix.
            # Parents it to the first one.
            # Aligns the first with the target given and uses the second new matrix to align the source one.

            # Aux nodes creation
            align_node_parent = pm.PyNode(pm.group(empty=True))
            align_node_parent.rename("align_node_parent")
            align_node_target = pm.PyNode(pm.group(empty=True))
            align_node_target.rename("align_node_target")

            # New matrix is the current aux target node one.
            new_matrix = pm.xform(align_node_target, q=True, ws=True, m=True)

            # If invert option is given
            if invert:
                if invert == "x":
                    new_matrix = [-1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif invert == "y":
                    new_matrix = [1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif invert == "z":
                    new_matrix = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif invert == "xy" or invert == "yx":
                    new_matrix = [-1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif invert == "xz" or invert == "zx":
                    new_matrix = [-1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif invert == "yz" or invert == "zy":
                    new_matrix = [1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif invert == "xyz" or invert == "xzy" or invert == "yxz" or invert == "yzx" or invert == "zxy" or invert == "zyx":
                    new_matrix = [-1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

            # If switch option is given
            if switch:
                if switch == "xy" or switch == "yx":
                    new_matrix = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif switch == "xz" or switch == "zx":
                    new_matrix = [0.0, 0.0, 1.0, 0.0, 0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

                elif switch == "yz" or switch == "zy":
                    new_matrix = [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

            # Applies the offset matrix to the target auxiliary node and parents it to the aux parent.
            pm.xform(align_node_target, m=new_matrix, ws=True)
            pm.parent(align_node_target, align_node_parent)

            # Aligns the aux parent to the target given and extracts the aux target current world matrix to use.
            pm.xform(align_node_parent, m=align_transform, ws=True)
            align_transform = pm.xform(align_node_target, q=True, ws=True, m=True)

            # Aux nodes delete.
            pm.delete(align_node_target)
            pm.delete(align_node_parent)

        # Applies the align transform.
        pm.xform(source, m=align_transform, ws=True)

        # If there is a translation offset applies it
        if offset_translation:
            ot = offset_translation
            pm.move(ot[0], ot[1], ot[2], source, relative=True, objectSpace=True)


def create_zero_transform_node(source_node, node_type="empty"):
    """Creates a zero transform node to be the parent of the given one and returns it.

    Args:
        source_node (PyNode): Node to create a zero transform one to be its parent.
        node_type (str, optional): Type of the zero transform node. By default "empty".

    Returns:
        PyNode: Returns the created zero node.
    """
    if source_node:
        zero_node = create_node_by_type(node_type)

        if zero_node:
            zero_node.rename(source_node.longName() + "ZT")

            align(zero_node, source_node)

            source_node_parent = source_node.listRelatives(parent=True)
            source_node_parent = source_node_parent[0] if source_node_parent else None
            if source_node_parent:
                pm.parent(zero_node, source_node_parent, absolute=True)

            pm.parent(source_node, zero_node, absolute=True)

            return zero_node

    return None


def joints_local_axis_display(joints=None, display=False, toggle=False):
    """Changes the local axis display state for joints.

    Args:
        joints (joint list, optional): List of joints to change axis display state.
        display (bool, optional): Indicates if display teh local axis or not.
        toggle (bool, optional): Indicates if must toggle the value instead of using True or False.
    """
    # If no joints, using all joints in the scene.
    if not joints:
        joints = pm.ls(type="joint", long=True)

    if joints:
        new_state = display

        # If toggle, gets the first joint state and inverts it, to use it in all the other joints.
        if toggle:
            new_state = not joints[0].getAttr("displayLocalAxis")

        # Loops the joints setting up the new state.
        for joint in joints:
            joint.setAttr("displayLocalAxis", new_state)

#######################################
# execution

if __name__ == "__main__":
    joints_local_axis_display(None, True, True)
    # align("joint_orient_002", "joint_orient_001")
    # align("joint_orient_002", "joint_orient_001", switch="yz")
    # align("joint_orient_002", "joint_orient_001", invert="x")
    # align("joint_orient_002", "joint_orient_001", invert="y")
    # align("joint_orient_002", "joint_orient_001", invert="z")
    # align("joint_orient_002", "joint_orient_001", invert="xyz")
    pass
