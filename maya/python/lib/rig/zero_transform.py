"""Contains definition utils for rigging"""

#######################################
# imports

import maya.cmds as cmds
import pymel.core as pm

import esa.maya.python.lib.rig.utils as utils

reload(utils)

#######################################
# functionality


def create_node(source_node, node_type="empty"):
    """Creates a zero transform node to be the parent of the given one and returns it.

    Args:
        source_node (PyNode): Node to create a zero transform one to be its parent.
        node_type (str, optional): Type of the zero transform node. By default "empty".

    Returns:
        PyNode: Returns the created zero node.
    """
    if source_node:
        # Creates the node
        zero_node = utils.create_node_by_type(node_type)

        if zero_node:
            # Renames it as ZT node
            zero_node.rename(source_node.longName() + "ZT")

            # Aligns it to the current one.
            utils.align(zero_node, source_node)

            # If source node has a parent, this will be the ZT node parent
            source_node_parent = source_node.listRelatives(parent=True)
            source_node_parent = source_node_parent[0] if source_node_parent else None
            if source_node_parent:
                pm.parent(zero_node, source_node_parent, absolute=True)

            # Source node parent now will be the ZT node
            pm.parent(source_node, zero_node, absolute=True)

            return zero_node

    return None


def get_node(source_node):
    """Returns the zero transform node if exists.

    Args:
        source_node (PyNode): Node to search the zero transform parent node.

    Returns:
        PyNode: Returns the zero node.
    """
    if source_node:
        source_node = pm.PyNode(source_node)

        # Searchs in the parent to see if it is a ZT node.
        zero_node = None
        parent = source_node.listRelatives(parent=True)
        if parent:
            if parent[0].shortName() == (source_node.shortName() + "ZT"):
                zero_node = parent[0]

        if zero_node:
            return zero_node

    return None


def set_current(source_node):
    """Stores the current transform to the zero transform values.

    Args:
        source_node (PyNode): Node to store the zero transform.
    """
    if source_node:
        source_node = pm.PyNode(source_node)

        zero_node = get_node(source_node)

        # If it has a ZT parent node, stores the source node transform
        if zero_node:
            utils.align(zero_node, source_node)
            apply(source_node)


def apply(source_node):
    """Applies the zero transform values.

    Args:
        source_node (PyNode): Node to apply zero transform.
    """
    if source_node:
        source_node = pm.PyNode(source_node)

        zero_node = get_node(source_node)

        # If it has a ZT parent node, resets the source node transform
        if zero_node:
            reset_attributes = {"translateX": 0, "translateY": 0, "translateZ": 0, "rotateX": 0, "rotateY": 0, "rotateZ": 0, "scaleX": 1, "scaleY": 1, "scaleZ": 1}
            for key, value in reset_attributes.iteritems():
                source_node.attr(key).set(value)


#######################################
# execution

if __name__ == "__main__":
    sel = pm.ls(selection=True)
    for sel_obj in sel:
        set_current(sel_obj)
    pass
