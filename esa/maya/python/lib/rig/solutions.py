"""Definitions and classes to manage solutions."""

#######################################
# imports

from PySide import QtCore, QtGui

import maya.cmds as cmds
import pymel.core as pm

import collections
import os
import inspect
import re

import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.rig.utils as utils
import esa.maya.python.lib.icons as icons

reload(ui)
reload(utils)
reload(icons)

#######################################
# constants

#######################################
# attributes

#######################################
# definitions

#######################################
# classes

# --------------------------------------
# GENERIC SOLUTION WIDGET


class SolutionWidget(QtGui.QWidget):
    """Generic Widget Class for Solution parameters.

    Attributes:
        editing (bool): Indicates if the ui is currently being edited.
        ui (Widget): Widget loaded from a .ui file given by the solution class.
    """
    def __init__(self, parent=None, solution_class=None):
        """Inits the Widget.

        Args:
            parent (Widget, optional): The parent widget for this one.
            solution_class (Class Definition, optional): Class to use in the ui search.
        """
        super(SolutionWidget, self).__init__(parent)

        # To use in case of signals update for UIs, to avoid conflicts
        self.editing = False

        # init UI
        self.initUI(solution_class=solution_class)

    def initUI(self, solution_class=None):
        """Inits the UI of the widget.

        Args:
            solution_class (Class Definition, optional): Class to use in the ui search.
        """
        # If not class given, uses the default.
        if not solution_class:
            solution_class = Solution

        # If class is given, searches the widget ui file.
        if solution_class:
            class_file = inspect.getfile(solution_class)
            ui_file = os.path.join(os.path.dirname(class_file), (solution_class.type + "_" + solution_class.subtype + ".ui"))

            # If no ui file, gets the generic default.
            if not os.path.exists(ui_file):
                solution_class = Solution
                class_file = inspect.getfile(solution_class)
                ui_file = os.path.join(os.path.dirname(class_file), (solution_class.type + "_" + solution_class.subtype + ".ui"))

            if os.path.exists(ui_file):
                self.ui = ui.loadUiWidgetFromPyFile(ui_file, parent=self)

                # QVBoxLayout
                self.setLayout(QtGui.QVBoxLayout())
                self.layout().addWidget(self.ui)
                self.layout().setSpacing(0)
                self.layout().setContentsMargins(2, 2, 2, 2)

# --------------------------------------
# GENERIC SOLUTION


# TODO: IMPORTANT: In the align and conform process, if source and target node are circles, copy radius, segments etc.
# TODO: Change the nodes names for something shorter based in the attributes of the solution.
# TODO: Create a process to convert deform joints rotation in orientation.
class Solution(object):
    """Generic solution class to be used as template for other solutions inheritance.

    Attributes:
        allowed_parents (lists of Solution Classes): For each solution it can only be children of other classes.
            If empty, it means that any solution can be parent of this one.
        channel_box (Maya window channelBox): Maya ChannelBox window to integrate in the solution ui.
        channel_box_nodes (list of PyNodes): List of nodes to populate solution channel box.
        children_solutions (list of Solution instances): List of Solution instances that are children of this one.
        colors (dict): Colors for each goal type of nodes. Maya 2016 and after.
        colors_indexes (dict): Colors for each goal type of nodes. Maya 2015 and before.
        creatable (bool): Indicates if the solution is a creatable one or a template to be inherited by others.
        description (str): Solution description.
        goals (dict): Different type of goals in a solution.
        goals_icons (dict of icons QIcon): Default icon for each goal type.
        icon (QIcon): icon for this solution, to use in UIs.
        instance_number (int): The number of solutions of this type created. Auto-calculated by default.
        node_types (dict of dicts): For each type of goal the default object type to create for each use.
        nodes (dict of dicts of lists): Stores the goal-use nodes for the solution.
        parent_solution (Solution instance): Solution instance that is the parent of the current one.
        solution_manager (Solution Manager instance): Class instance to manage solutions (for children and parent).
        subtype (str): Subtype of the solution.
        tags (dict): Tags that can be used in the nodes for the solution. Tags are not limited to this list.
            You can use other custom tags. This are only some common used.
        type (str): Type of the solution.
        ui_object (UI object): In case the solution is handled by a UI tree, this is the UI node related with this instance.
        ui_widget (QWidget): Widget to use in the config UI.
        uses (dict): Uses for the different nodes in a solution. This are limited to the ones in the list.
    """

    # Class attributes

    # Solution type and subtype.
    type = "generic"
    subtype = "generic"

    # Description of this solution.
    description = "This is the generic solution to use in all the others as origin of inheritance."

    # Creatable indicates if the solution is a creatable one or a template to be inherited by others.
    # Example: SolutionArm will be inherited by SolutionArmRight and SolutionArmLeft. Both creatables but not the first.
    creatable = False

    # Allowed and forbidden parent solution types
    # If empty it means that can be used as a rig root solution.
    # If contains element "all" means that the parent can be any solution.
    allowed_parents = []
    forbidden_parents = []

    # Default icon for the solution.
    icon = icons.getIconByName("puzzleOne_16x16.png")

    # Prefixes of the solution goals
    goals = collections.OrderedDict([("fit", "fit"), ("deform", "deform"), ("anim", "anim")])

    # Default icon for each goal
    goals_icons = {
        "fit": icons.getIconByName("solutionFit_16x16.png"),
        "deform": icons.getIconByName("solutionDriver_16x16.png"),
        "anim": icons.getIconByName("solutionAnim_16x16.png")
    }

    # Solution types colors
    colors = {"fit": [0.910, 0.117, 0.386], "deform": [1.0, 0.761, 0.230], "anim": [0.296, 0.683, 0.312]}
    colors_indexes = {"fit": 20, "deform": 17, "anim": 19}

    # Uses for the different nodes in a solution. This are limited to the ones in the list.
    uses = {"master": "master", "core": "core", "branch": "branch"}
    tags = {"main": "main", "secondary": "secondary", "aux": "aux", "conform": "conform"}

    # For each kind of goal the default object type to create for each use.
    node_types = {
        "fit":    {"master": "circle", "core": "renderBox", "branch": "empty"},
        "deform": {"master": "joint",  "core": "joint",     "branch": "joint"},
        "anim":   {"master": "empty", "core": "renderBox", "branch": "empty"}
    }

    def __init__(self, solution_manager=None, instance_number=None):
        """Generic solution initialization.

        Args:
            solution_manager (SolutionManager instance, optional): Solution manger instance.
                Can be used to manage children and parent solutions and also to access utils for rig.
            instance_number (int, optional): The number of solutions of this type created. Auto-calculated by default.
        """

        # Master nodes of the solution goals
        # Core nodes of the solution goals
        # Branch nodes of the solution goals
        self.nodes = {
            "fit": {"master": [], "core": [], "branch": []},
            "deform": {"master": [], "core": [], "branch": []},
            "anim": {"master": [], "core": [], "branch": []},
        }

        # Indicates the created instance for this solution.
        self.instance_number = instance_number if instance_number else self.get_new_instance_number()

        # Parent solution and children solutions.
        self.parent_solution = None
        self.children_solutions = []

        # Solution Manager with Solution utils also
        self.solution_manager = solution_manager if solution_manager else SolutionManager()

        # In case the solution is handled by a UI tree, this is the UI node related with this instance.
        self.ui_object = None

        # Inits the ui widget and channel box for this solution.
        self.ui_widget = None
        self.channel_box = None
        self.init_ui()

    def validate_ui_widget(self):
        """Returns True if the ui widget can be enabled.

        Returns:
            bool: Returns True if the ui widget can be enabled, False if not.
            By default can only be enabled if the fit goal is built and there are no other goals built.
        """
        if not self.is_goal_built("fit"):
            return False
        else:
            for other_goal in self.goals:
                if other_goal != "fit":
                    if self.is_goal_built(other_goal):
                        return False

        return True

    def init_ui_widget(self):
        """Inits the specific ui widget for this solution."""
        self.ui_widget = self.solution_manager.get_solution_widget(self.__class__)

    def init_ui_layout(self):
        """Inits the specific ui layout for this solution."""

        # If widget is not created, creates it first.
        if not self.ui_widget:
            self.init_ui_widget()

        # Sets the enabled state for the ui widget, considering the goals that are built.
        self.ui_widget.setEnabled(self.validate_ui_widget())

        # NOTE: To override in each specific solution. Prepare layout items with right values.
        # Code for the layout init.

    def init_ui_signals(self):
        """Inits the specific ui signals for this solution."""

        # If widget is not created, creates it first.
        if not self.ui_widget:
            self.init_ui_widget()

        # To override in each specific solution. Connect the signals.
        # Code for the signals init.

    def init_channel_box(self, **kwargs):
        """Summary

        Args:
            **kwargs: keyword args to pass to channel box creation.
        """
        # filter the kwargs and set the objects and attributes.
        # To override in each specific solution with the specific object and attributes to be shown.

        if "fixedAttrList" not in kwargs:
            kwargs["fixedAttrList"] = [""]

        self.channel_box_nodes = kwargs["channel_box_nodes"] if "channel_box_nodes" in kwargs else []
        if "channel_box_nodes" in kwargs:
            kwargs.pop("channel_box_nodes", None)

        self.channel_box = pm.channelBox('channelBox', **kwargs)

    def init_ui(self):
        """Inits the specific ui widget for this solution."""
        if self.is_goal_built("fit"):
            self.init_ui_widget()
            self.init_ui_layout()
            self.init_ui_signals()
            self.init_channel_box()

    def get_ui(self, reset=False):
        """Returns the ui widget of this solution.

        Args:
            reset (bool, optional): Indicates if reset the UI to defaults before return it or return the current one.

        Returns:
            Widget: Returns the ui widget of this solution.
        """
        # If reset or ui_widget is none, it has to rebuild the widget first.
        if (reset or not self.ui_widget) and self.is_goal_built("fit"):
            self.init_ui()

        return self.ui_widget

    def get_channel_box(self, reset=False):
        """Summary

        Args:
            reset (bool, optional): Indicates if reset the channel box to defaults before return it or return the current one.

        Returns:
            TYPE: Returns the channel box customized for this solution.
        """
        if (reset or not self.channel_box) and self.is_goal_built("fit"):
            self.init_channel_box()

        return self.channel_box

    def get_channel_box_nodes(self, reset=False):
        """Summary

        Args:
            reset (bool, optional): Indicates if reset the channel box to defaults before return it or return the current nodes.

        Returns:
            TYPE: Returns a list of strings containing the nodes to use in the custom channel box.
        """
        if reset and self.is_goal_built("fit"):
            self.init_channel_box()

        if self.channel_box_nodes:
            return self.channel_box_nodes
        else:
            return self.get_nodes("fit", "master")

    def update_solution(self, goal, recursive=True):
        """Updates the solution with the parameters from the ui if changed.

        Args:
            goal (str): Type of goal to update.
            recursive (bool, optional): Indicates if updating the children solutions recursive.
        """

        # If goal is not fit, the way to update it is removing the goal and rebuilding it again.
        if goal != "fit":
            if self.validate_remove(goal):
                self.remove(goal, recursive=recursive)
            if self.validate_build(goal):
                self.build(goal, recursive=recursive)

        # If goal is fit, the way of updating is different for each solution, so this function needs to be overridden.
        if goal == "fit":
            pass

    def name(self):
        """Returns the solution name based on the type and subtype.

        Returns:
            string: Returns the solution name based on the type and subtype.
        """
        return self.type + "_" + self.subtype + "_" + ("%04d" % self.instance_number)

    def get_new_instance_number(self):
        """Gets the instance number that solution must have on creation. It takes in count the already existing.

        Returns:
            int: Returns the instance number that must be used if a new instance of this solution is created.
        """
        i_number = 1

        dag_nodes = pm.ls(dag=True)
        for dag_node in dag_nodes:
            if dag_node.hasAttr("stype"):
                if dag_node.getAttr("stype") == self.type and dag_node.getAttr("ssubtype") == self.subtype:
                    tmp_i_number = dag_node.getAttr("sinstance")
                    if tmp_i_number >= i_number:
                        i_number = tmp_i_number + 1

        return i_number

    def get_index_in_brothers(self):
        """Returns the index of this solution in the parent children list (brothers).

        Returns:
            int: Returns the index of this solution in the parent children list (brothers).
        """
        if self.parent_solution:
            if len(self.parent_solution.children_solutions) > 1:
                index = 0
                for brother in self.parent_solution.children_solutions:
                    if brother == self:
                        return index

                    index += 1
            else:
                return 0
        else:
            return 0

    def get_nodes(self, goal=None, use=None, tag=None):
        """Returns the nodes of the requested goal and use.

        Args:
            goal (str, optional): The type of goal we want to retrieve the nodes from.
            use (str, optional): The type of use we want to retrieve the nodes from.
            tag (str, optional): returns only the nodes that match the tag.

        Returns:
            list of PyNodes: Returns the nodes of the requested goal and use.
        """
        nodes = []

        # If only goal is given, return all nodes of this goal.
        if not use and goal in self.goals:
            nodes = []
            for current_use in self.uses:
                nodes += self.nodes[goal][current_use]

        # If only use is given, return all nodes of this use.
        if not goal and use in self.uses:
            nodes = []
            for current_goal in self.goals:
                nodes += self.nodes[current_goal][use]

        # If a goal and use are given, return that nodes.
        if goal in self.goals and use in self.uses:
            nodes = self.nodes[goal][use]

        if tag:
            nodes = [node for node in nodes if re.match(tag, node.attr("tag").get())]

        return nodes

    def get_node(self, goal, use, tag=None):
        """Returns the firs node of the requested goal and use.

        Args:
            goal (str): The type of goal we want to retrieve the node from.
            use (str): The type of use we want to retrieve the node from.
            tag (str, optional): returns only the node that matches the tag.

        Returns:
            PyNode: Returns the node of the requested goal and use.
        """
        requested_nodes = self.get_nodes(goal, use, tag)

        # if requested_nodes and tag:
        #     requested_nodes = [node for node in requested_nodes if node.attr("tag").get() == tag]

        if requested_nodes:
            return requested_nodes[0]
        else:
            return None

    def get_selectable_nodes(self):
        """Returns the selectable nodes for this solution

        Returns:
            list: Returns the selectable nodes for this solution
        """
        return self.get_nodes("fit", "master")

    def rename_node(self, node, goal, use, tag):
        """Renames the node attending to the solution type, subtype and node goal, use and tag.

        Args:
            node (PyNode): Node to rename.
            goal (str): Goal part for the name.
            use (str): Use part for the name.
            tag (str): Tag part for the name.
        """
        node.rename(self.type + "_" + self.subtype + "_" + ("%04d" % self.instance_number) + "_" + goal + "_" + use + "_" + tag)

    def set_color(self, node, goal):
        """Set the color of the node depending on the goal.

        Args:
            node (PyNode): Node to set the color.
            goal (str): Goal to know wich color use.
        """
        node.setAttr("overrideEnabled", True)
        if node.hasAttr("useOutlinerColor"):
            # Available from 2016 and after
            node.setAttr("useOutlinerColor", True)
            node.setAttr("outlinerColor", self.colors[goal])
            node.setAttr("overrideRGBColors", 1)
            node.setAttr("overrideColorRGB", self.colors[goal][0], self.colors[goal][1], self.colors[goal][2])
        else:
            # maya 2015 and older
            node.setAttr("overrideColor", self.colors_indexes[goal])

    def add_attributes(self, node, goal, use, tag):
        """Add attributes to the node attending to node goal, use and tag.

        Args:
            node (PyNode): Node to add attributes.
            goal (str): Goal to add as attribute.
            use (str): Use to add as attribute.
            tag (str): Tag to add as attribute.
        """
        pm.addAttr(node, sn="stype",        ln="solution_type",     nn="Solution Type",     ci=True, dt="string")
        pm.addAttr(node, sn="ssubtype",     ln="solution_subtype",  nn="Solution Subtype",  ci=True, dt="string")
        pm.addAttr(node, sn="sinstance",    ln="solution_instance", nn="Solution Instance", ci=True, at="short")
        pm.addAttr(node, sn="goal",         ln="goal",              nn="Solution Goal",     ci=True, dt="string")
        pm.addAttr(node, sn="use",          ln="use",               nn="Node Use",          ci=True, dt="string")
        pm.addAttr(node, sn="tag",          ln="tag",               nn="Node Tag",          ci=True, dt="string")

        node.setAttr("stype",       self.type)
        node.setAttr("ssubtype",    self.subtype)
        node.setAttr("sinstance",   self.instance_number)
        node.setAttr("goal",        goal)
        node.setAttr("use",         use)
        node.setAttr("tag",         tag)

        node.setAttr("stype",       lock=True, keyable=False)
        node.setAttr("ssubtype",    lock=True, keyable=False)
        node.setAttr("sinstance",   lock=True, keyable=False)
        node.setAttr("goal",        lock=True, keyable=False)
        node.setAttr("use",         lock=True, keyable=False)
        node.setAttr("tag",         lock=True, keyable=False)

    def setup_channelBox_attributes(self, node, attributes):
        """
        Args:
            node (PyNode): Node to setup channle box attributes
            attributes (list of string): List of strings to know which attributes setup.
        """
        utils.setup_channelBox_attributes(node, attributes)

    def get_free_branch(self, goal):
        """Method to get the solution branch node to link or align next solutions

        Args:
            goal (str): Goal of the branch to return.

        Returns:
            PyNode: Solution branch node to link or align next solutions.
        """
        branch_nodes = self.get_nodes(goal, "branch")

        if branch_nodes:
            if len(branch_nodes) == 1:
                return branch_nodes[0]
            else:
                for branch_node in branch_nodes:
                    if not branch_node.listRelatives(children=True, fullPath=True):
                        return branch_node
                return branch_nodes[0]
        else:
            return None

    def create_node_by_type(self, node_type, **kwargs):
        """Create node by type.

        Args:
            node_type (str): Type of the node to be created
            **kwargs: Extra arguments to use in some nodes types creation.

        Returns:
            PyNode: New node of the goal and use specified.
        """

        return utils.create_node_by_type(node_type, **kwargs)

    def create_node_by_goal(self, goal, use, **kwargs):
        """Create node by goal.

        Args:
            goal (str): Goal of the new node.
            use (str): Use of the new node.
            **kwargs: Extra arguments to use in some nodes types creation.

        Returns:
            PyNode: New node of the goal and use specified.
        """

        node_type = self.node_types[goal][use]
        return self.create_node_by_type(node_type, **kwargs)

    def create_zero_transform_node(self, source_node, node_type="empty"):
        """Creates a zero transform node to be the parent of the given one and returns it.

        Args:
            source_node (PyNode): Node to create a zero transform one to be its parent.
            node_type (str, optional): Type of the zero transform node. By default "empty".

        Returns:
            PyNode: Returns the created zero node.
        """
        if source_node:
            zero_node = utils.create_zero_transform_node(source_node, node_type=node_type)

            if zero_node:
                goal = source_node.attr("goal").get()
                use = source_node.attr("use").get()
                tag = source_node.attr("tag").get() + "ZT"
                self.rename_node(zero_node, goal, use, tag)
                self.set_color(zero_node, goal)
                self.add_attributes(zero_node, goal, use, tag)

                return zero_node

        return None

    def build_master(self, goal):
        """Creates the master node attending to the goal type.

        Args:
            goal (str): Goal of the master to build.
        """
        new_master_node = self.create_node_by_goal(goal, "master")
        self.nodes[goal]["master"].append(new_master_node)
        self.rename_node(new_master_node, goal, "master", self.tags["main"])

        self.set_color(new_master_node, goal)
        self.add_attributes(new_master_node, goal, "master", self.tags["main"])
        self.setup_channelBox_attributes(new_master_node, ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])

    def align_master(self, goal):
        """Align master node of the specific goal to the correspondent parent branch
            or fit goal from the same solution.

        Args:
            goal (str): Goal of the master to align.
        """
        # Is necessary to deselect all to get the right xform
        cmds.select(clear=True)

        if goal == "fit":
            # If parent solution is defined, then align to correspondent branch in parent.
            if self.parent_solution:
                align_node = self.parent_solution.get_free_branch(goal)
            else:
                # If not align to rig group.
                align_node = self.solution_manager.get_rig_group(hierarchy_node=self.get_node(goal, "master"))
        else:
            # If one of the other type of goals, align to fit
            align_node = self.get_node("fit", "master")

        if align_node:
            # align_transform = pm.xform(align_node, q=True, ws=True, m=True)
            # pm.xform(self.get_node(goal, "master"), m=align_transform, ws=True)

            utils.align(self.get_node(goal, "master"), align_node)

    def link_master(self, goal):
        """Link master node of the specific goal to the correspondent parent branch
            or fit goal from the same solution.

        Args:
            goal (str): Goal of the master to link.
        """

        if not self.parent_solution:
            parent_node = self.solution_manager.get_rig_group(hierarchy_node=self.get_node(goal, "master"))
        else:
            # Get the branch node of the parent solution and parent this to the right one in relative mode.
            parent_node = self.parent_solution.get_free_branch(goal)

            # If the master node already has a parent and this parent one of the parent solution branches, do nothing.
            if self.parent_solution:
                master_node = self.get_node(goal, "master")
                master_node_parent = master_node.listRelatives(parent=True)
                if master_node_parent and master_node_parent in self.parent_solution.get_nodes(goal, "branch"):
                    parent_node = None

        if parent_node:
            pm.parent(self.get_node(goal, "master"), parent_node, absolute=True)

    def build_branches(self, goal):
        """Creates the branch nodes attending to the goal type.

        Args:
            goal (str): Goal of the branches to build.
        """
        new_branch_node = self.create_node_by_goal(goal, "branch")
        self.nodes[goal]["branch"].append(new_branch_node)
        self.rename_node(new_branch_node, goal, "branch", self.tags["main"])

        self.set_color(new_branch_node, goal)
        self.add_attributes(new_branch_node, goal, "branch", self.tags["main"])
        self.setup_channelBox_attributes(new_branch_node, ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])

    def align_branches(self, goal):
        """Align branch nodes of the specific goal to the correspondent nodes in same solution.
            This method probably must be different in each solution type.
            This case is only for generic solution. For specific solutions must be replaced by a custom one.

        Args:
            goal (str): Goal of the branch to align.
        """
        # If there is a core created, uses the last node in the array as parent, if not uses the master.
        use = "core" if self.get_nodes(goal, "core") else "master"
        align_node = self.get_nodes(goal, use)[-1] if self.get_nodes(goal, use) else None

        for branch_node in self.get_nodes(goal, "branch"):
            # align_transform = pm.xform(align_node, q=True, ws=True, m=True)
            # pm.xform(branch_node, m=align_transform, ws=True)
            utils.align(branch_node, align_node)

    def link_branches(self, goal):
        """Link branch nodes of the specific goal to the correspondent nodes from the same solution.
            This method probably must be different in each solution type.
            This case is only for generic solution. For specific solutions must be replaced by a custom one.

        Args:
            goal (str): Goal of the branch to link.
        """
        # If there is a core created, uses the last node in the array as parent, if not uses the master.
        use = "core" if self.get_nodes(goal, "core") else "master"
        align_node = self.get_nodes(goal, use)[-1] if self.get_nodes(goal, use) else None

        for branch_node in self.get_nodes(goal, "branch"):
            pm.parent(branch_node, align_node, absolute=True)

    def build_core(self, goal):
        """Creates the core solution attending to the goal type.
            This method probably must be different in each solution type.
            This case is only for generic solution. For specific solutions must be replaced by a custom one.

        Args:
            goal (str): Goal of the core to build.
        """
        # For this kind of node in the generic solution, only for anim must be created, not for fit or deform.
        # For more complex solutions, will be necessary to create it for all goals
        if goal == "anim":
            new_core_node = self.create_node_by_goal(goal, "core")
            self.nodes[goal]["core"].append(new_core_node)
            self.rename_node(new_core_node, goal, "core", self.tags["main"])

            self.set_color(new_core_node, goal)
            self.add_attributes(new_core_node, goal, "core", self.tags["main"])

    def align_core(self, goal):
        """Align core nodes of the specific goal to the correspondent nodes in same solution.
            This method probably must be different in each solution type.
            This case is only for generic solution. For specific solutions must be replaced by a custom one.

        Args:
            goal (str): Goal of the core to align.
        """
        master_node = self.get_node(goal, "master")

        for core_node in self.get_nodes(goal, "core"):
            if goal == "fit":
                # NOTE: fit core nodes don't need to be aligned because they are created in the right position
                # during the build_core function execution, that must be overridden for each solution.

                # In case is the first core node, has to align to its master.
                if not core_node.listRelatives(parent=True) or core_node.listRelatives(parent=True)[0] == master_node:
                    utils.align(core_node, self.get_node(goal, "master"))

            elif self.is_goal_built("fit"):
                # In the other goals, must align to fit solution
                target_node = self.get_conform_target(core_node, goal, "fit")
                if target_node:
                    utils.align(core_node, target_node)
                elif not core_node.listRelatives(parent=True) or core_node.listRelatives(parent=True)[0] == master_node:
                    # In case is the first core node and has no master, has to align to its master.
                    utils.align(core_node, self.get_node(goal, "master"))

    def link_core(self, goal):
        """Link core nodes of the specific goal to the correspondent nodes from the same solution.

        Args:
            goal (str): Goal of the core to link.
        """
        for core_node in self.get_nodes(goal, "core"):
            if not core_node.listRelatives(parent=True):
                pm.parent(core_node, self.get_node(goal, "master"), absolute=True)

    def is_goal_built(self, goal):
        """Returns True if a goal is created for this solution.

        Args:
            goal (str): Goal to validate.

        Returns:
            bool: Returns True if a goal is created for this solution.
        """
        for use in self.uses:
            if self.nodes[goal][use]:
                return True

        return False

    def validate_build(self, goal):
        """Validates if the solution can be created.

        Args:
            goal (str): Goal to validate if can be built.

        Returns:
            bool: Returns if the solution can be created.
        """

        # If the goal is not created, several possibilities.
        if not self.is_goal_built(goal):

            # To build a goal that is not the fit one, the fit goal needs to be already created.
            if goal != "fit":

                # If fit goal is not created, cannot be created
                if not self.nodes["fit"]["master"]:
                    return False
                else:
                    # If the solution has a parent solution,
                    # also the parent same goal solution must be created previously.
                    if self.parent_solution:
                        return self.parent_solution.is_goal_built(goal)
                    else:
                        # If not, can be created because is a root solution or a single one.
                        return True
            else:
                # If goal is fit, can be created if the parent solution has the fit goal created.
                # If not, cannot be created.
                if self.parent_solution:
                    return self.parent_solution.is_goal_built(goal)
                else:
                    return True
        else:
            # If goal is created, cannot be created again.
            return False

    def validate_remove(self, goal):
        """Returns True if a goal can be removed.

        Args:
            goal (str): Goal to validate.

        Returns:
            bool: Returns True if a goal can be removed.
        """
        # If goal is not fit, can be removed if is created and only if fit exists.
        if goal != "fit":
            return (self.is_goal_built("fit") and self.is_goal_built(goal))
        else:
            # NOTE: Initially removing the fit goal was possible. But this could cause problems and maintenance,
            # if the fit solution is rebuilt using a deform or anim goal. So is better not allow it.

            # If goal is fit, can only be removed if there are other goals created.
            # for other_goal in self.goals:
            #     if other_goal != "fit":
            #         if self.is_goal_built(other_goal):
            #             return self.is_goal_built("fit")

            return False

    def validate_conform(self, goal):
        """Returns True if a goal can be conformed to other goal.

        Args:
            goal (str): Goal to validate.

        Returns:
            bool: Returns True if a goal can be conformed.
        """
        # If goal is not fit, can be conformed if is created and only if fit exists.
        if goal != "fit":
            return (self.is_goal_built("fit") and self.is_goal_built(goal))
        else:
            # If goal is fit, can only be conformed if there are other goals created.
            for other_goal in self.goals:
                if other_goal != "fit":
                    if self.is_goal_built(other_goal):
                        return self.is_goal_built("fit")

            return False

    def build(self, goal, recursive=True):
        """Creates the solution part of the specified goal.

        Args:
            goal (str): Goal of the solution to create.
            recursive (bool, optional): Indicates if build must be recursive in the children solutions.
        """
        if self.validate_build(goal):

            self.build_master(goal)
            self.align_master(goal)
            self.link_master(goal)

            self.build_core(goal)
            self.align_core(goal)
            self.link_core(goal)

            self.build_branches(goal)
            self.align_branches(goal)
            self.link_branches(goal)

            self.conform(goal, recursive=False)

            pm.select(clear=True)

        # Do it recursive in the children solutions.
        if recursive:
            for child_solution in self.children_solutions:
                child_solution.build(goal, recursive=recursive)

    def remove(self, goal, recursive=True):
        """Removes the solution part of the specified goal.

        Args:
            goal (str): Goal of the solution to remove.
            recursive (bool, optional): Indicates if remove must be recursive in the children solutions.
        """
        # Do it recursive in the children solutions. Must be done first to avoid errors.
        if recursive:
            for child_solution in self.children_solutions:
                child_solution.remove(goal, recursive=recursive)

        # Remove the nodes from the scene
        pm.delete(self.get_nodes(goal, "branch"))
        pm.delete(self.get_nodes(goal, "core"))
        pm.delete(self.get_nodes(goal, "master"))

        # Remove the nodes from the lists
        self.nodes[goal]["branch"] = []
        self.nodes[goal]["core"] = []
        self.nodes[goal]["master"] = []

    def get_conform_target(self, node, goal, target_goal):
        """Gets the target node to conform the given one to.

        Args:
            node (PyNode): Given node to find the equivalent target node to conform to.
            goal (str): Current goal.
            target_goal (str): Target goal to search the correspondent node in.

        Returns:
            PyNode: Returns the target node to conform the goven one to. If not found returns None.
        """
        # Converts the node in PyNode in case it is not.
        if node:
            node = pm.PyNode(node)

        # Only if node is given:
        if node:
            # all target goal nodes, where the target node must be.
            target_candidates = self.get_nodes(goal=target_goal)
            # Only if there are candidates.
            if target_candidates:

                # Gets the correspondent node in the target goal.
                target_node = None
                for t_node in target_candidates:
                    if t_node.attr("use").get() == node.attr("use").get() and t_node.attr("tag").get() == node.attr("tag").get():
                        target_node = t_node
                        break

                # If there is a target node, returns it.
                if target_node:
                    return target_node
                else:
                    # If there is no target node and the current node parent is a master, uses the master as target.
                    if node.listRelatives(parent=True) and node.listRelatives(parent=True)[0] == self.get_node(goal, "master"):
                        target_node = self.get_conform_target(self.get_node(goal, "master"), goal, target_goal)
                        if target_node:
                            return target_node

        # If no node or no matches, returns None.
        return None

    def conform_node(self, node, goal, target_goal, recursive=True):
        """Conforms the given node from one goal to the correspondent in the target goal.

        Args:
            node (PyNode): Note to conform to the correspondent one in the target goal.
            goal (str): Current goal.
            target_goal (str): Target goal to search the correspondent node in.
            recursive (bool, optional): If True indicates that all descendants must be conformed too.
        """
        # Converts the node in PyNode in case it is not.
        if node:
            node = pm.PyNode(node)

        # Only proceed if the node is given and the node is in this solution.
        if node and node in self.get_nodes(goal):
            target_node = self.get_conform_target(node, goal, target_goal)

            # If a target node is found, conforms the node to it.
            if target_node:
                # align_transform = pm.xform(target_node, q=True, ws=True, m=True)
                # pm.xform(node, m=align_transform, ws=True)
                utils.align(node, target_node)

            # If this node has children, must conform them recursive if required
            if recursive and node.listRelatives(children=True):
                for child_node in node.listRelatives(children=True):
                    self.conform_node(child_node, goal, target_goal, recursive=recursive)

    def conform(self, goal, recursive=True):
        """Conforms the solution part of the specified goal to other goal to match changes.

        Args:
            goal (str): Goal of the solution to conform.
            recursive (bool, optional): Indicates if conform must be recursive in the children solutions.
        """
        # Only can conform the given goal if it exists.
        if self.is_goal_built(goal):

            # If goal is not fit and fit is created, conform goal must be fit.
            if goal != "fit":
                target_goal = "fit" if self.is_goal_built("fit") else None
            else:
                target_goal = None

                # If goal is fit, the conform goal must be first of the other ones that is created.
                for other_goal in self.goals:
                    if other_goal != "fit":
                        if self.is_goal_built(other_goal):
                            target_goal = other_goal
                            break

            # If there is a goal to conform the given one to, does it.
            if target_goal:
                master_node = self.get_node(goal, "master")
                if master_node:
                    # It starts with the master goal and continues recursive with all descendants till the solution ends.
                    self.conform_node(master_node, goal, target_goal, recursive=recursive)

                    # If recursive, and this solution has children solutions, must conform children too.
                    if recursive and self.children_solutions:
                        for child_solution in self.children_solutions:
                            child_solution.conform(goal, recursive=recursive)

    def store_node(self, node, goal, use):
        """Stores the node in the goal and use nodes list

        Args:
            node (PyNode): Node to store
            goal (str): Goal of the node to store.
            use (str): Use of the node to store.
        """
        if node:
            node = pm.PyNode(node)

            goal = node.getAttr("goal")
            use = node.getAttr("use")

            # Add the node to the correspondent list. If the node is already stored skips it.
            if node not in self.nodes[goal][use]:
                self.nodes[goal][use].append(node)

    def store_nodes(self, root_node):
        """
        Given a node, stores it in the goal-use correspondent array. Is recursive, doing the same for children.
            Recursive stops when a child is the master of another solution

        Args:
            root_node (PyNode): Given node to store and parent of the hierarchy off all nodes to store.
        """
        current_node = pm.PyNode(root_node)

        stype = current_node.getAttr("stype")
        ssubtype = current_node.getAttr("ssubtype")
        goal = current_node.getAttr("goal")
        use = current_node.getAttr("use")

        # Only stores the node if it has the same type and subtype than the solution.
        if stype == self.type and ssubtype == self.subtype:
            self.store_node(current_node, goal, use)

            # If the node has children it stores them recursive till the solution ends.
            children = current_node.listRelatives(children=True, fullPath=True)
            for child in children:
                child = pm.PyNode(child)

                # Only calls the recursive if the next node has solution attributes
                # and is not the beginning of a new child solution.
                if child.hasAttr("stype") and child.hasAttr("ssubtype"):
                    if child.getAttr("use") != "master":
                        self.store_nodes(child)

    def fill(self, master_nodes):
        """Populates the solution with all the nodes, starting in master ones.

        Args:
            master_nodes (list PyNodes): List of master nodes to start the fill.
        """
        if master_nodes:
            self.instance_number = pm.PyNode(master_nodes[0]).getAttr("sinstance")

            for master_node in master_nodes:
                self.store_nodes(master_node)

    def set_parent_solution(self, parent_solution):
        """Sets this solution parent solution.

        Args:
            parent_solution (Solution instance): The parent solution instance to be stored.
        """
        self.parent_solution = parent_solution
        if parent_solution:
            parent_solution.add_child_solution(self)

    def add_child_solution(self, child_solution):
        """Adds a soltion to the children solutions list.

        Args:
            child_solution (Solution instance): The child solution instance to be added.
        """
        if child_solution and (child_solution not in self.children_solutions):
            self.children_solutions.append(child_solution)
            child_solution.set_parent_solution(self)

# --------------------------------------
# SOLUTION UTILS


class SolutionUtils(object):
    """Collection of utils to use in rigging solutions.

    Attributes:
        rig_group_constants (dict): Constants to help in rig groups management.
    """
    rig_group_constants = {"name": "rig_001", "pattern": "rig_*", "start": "rig_"}

    def __init__(self):
        """Initializes the Rig utils class"""
        pass

    def get_solution_goals(self):
        """Return all the possible goals for a solution.

        Returns:
            list of strings: Return all the possible goals for a solution.
        """
        return [key for key, value in Solution.goals.iteritems()]

    def get_solution_goal_icon(self, goal):
        """Returns the default icon for the given solution goal.

        Args:
            goal (str): Given goal type to get the relative icon.

        Returns:
            QIcon: Returns the default icon for the given solution goal.
        """
        return Solution.goals_icons[goal]

    def get_rig_groups(self, new=False, hierarchy_node=None):
        """Gets all rig groups in the scene that are the begining of a hierarchy. Can be new if requested.

        Args:
            new (bool, optional): Indicates if it has to create a new rig node.
            hierarchy_node (PyNode, optional): Node to use as search start for the rig group.

        Returns:
            PyNode list: Returns all rig groups starting hiearchies in the scene.
        """
        rig_groups = []
        rig_groups_names = pm.ls(self.rig_group_constants["pattern"], long=True)

        for rig_group in rig_groups_names:
            rig_groups.append(pm.PyNode(rig_group))

        if not rig_groups or new:
            rig_groups = [pm.PyNode(cmds.group(name=self.rig_group_constants["name"], empty=True))]

        return rig_groups

    def get_rig_group(self, new=False, hierarchy_node=None):
        """Returns the rig group to use in the solutions. Can be new or an existing one.

        Args:
            new (bool, optional): Indicates if it has to create a new rig node.
            hierarchy_node (PyNode, optional): Node to use as search start for the rig group.

        Returns:
            PyNode: Rig group node requested. Can be new or the one in a node hierarchy.
        """
        rig_groups = self.get_rig_groups(new=new, hierarchy_node=None)

        if hierarchy_node:
            parent = hierarchy_node

            while parent:
                parent = pm.PyNode(parent)

                if parent in rig_groups:
                    return parent
                else:
                    parent = parent.listRelatives(parent=True, fullPath=True)

        return rig_groups[0]


# --------------------------------------
# SOLUTION MANAGER

class SolutionManager(SolutionUtils):
    """This class contains functionality to handle rig solutions in a scene.

    Attributes:
        solution_classes (list of classes): All possible solutions to be created.
        solution_trees (list of Soltuion Instances): list of root solutions that also contains children solutions recursive.
    """

    def __init__(self):
        """Manager initialization"""
        super(SolutionManager, self).__init__()

        # ------------------------------------------------------------------
        # List of usable solutions
        from esa.maya.python.lib.rig.solutions_generic import SolutionRoot
        from esa.maya.python.lib.rig.solutions_generic import SolutionCenter
        from esa.maya.python.lib.rig.solutions_generic import SolutionJointChainFK

        self.solution_classes = [SolutionRoot, SolutionCenter, SolutionJointChainFK]
        # ------------------------------------------------------------------

        # List of scene root solutions.
        self.solution_trees = []

    def get_solution_widget(self, solution_class):
        """Gets a Widget instance using the ui prepared for the solution.

        Args:
            solution_class (Solution Class): Solution class to get the ui from.

        Returns:
            Widget Instance: Returns a Widget instance using the ui prepared for the solution.
        """
        # If a class is given, returns the widget for it.
        if solution_class:
            return SolutionWidget(solution_class=solution_class)
        else:
            # If not class given, the generic widget is returned
            return SolutionWidget(solution_class=Solution)

    def get_solution_types(self):
        """Returns possible solution types.

        Returns:
            list of str: List of possible solution types.
        """
        return list(set([solution_class.type for solution_class in self.solution_classes]))

    def get_solution_subtypes(self, solution_type):
        """Returns all possible solution subtypes for a given type.

        Args:
            solution_type (str): type of solutions to get all possible subtypes.

        Returns:
            list of str: List of possible solution subtypes for a given type.
        """
        return [solution_class.subtype for solution_class in self.solution_classes if solution_class.type == solution_type]

    def get_solution_class(self, solution_type, solution_subtype):
        """If the given solution_type and solution_subtype exists in one class, returns it. None if not.

        Args:
            solution_type (str): Type of the desired solution class.
            solution_subtype (str): Subtype of the desired solution class.

        Returns:
            Solution Class: If the given solution_type and solution_subtype exists in one class, returns it. None if not.
        """
        # If the given solution_type and solution_subtype exists in one class, returns it
        if solution_type and solution_subtype:
            if solution_type in self.get_solution_types():
                if solution_subtype in self.get_solution_subtypes(solution_type):
                    for solution_class in self.solution_classes:
                        if solution_class.type == solution_type and solution_class.subtype == solution_subtype:
                            return solution_class

        return None

    def get_allowed_children(self, solution_instance=None):
        """Gets all possible solutions that can be build from a current one.

        Args:
            solution_instance (Solution Instance, Optional): Solution Instance to get the allowed children solutions to construct.
                If None is given, will return the ones that can be root solutions.

        Returns:
            OrderedDict of Lists: Returns an ordered dict, each key is a solution type
                and the value is the list of possible subtypes.
        """

        # Ordered dict to store the types and subtypes.
        allowed_children = collections.OrderedDict()

        # If a solution instance is given, searches in the allowed ones.
        if solution_instance:
            for solution_class in self.solution_classes:
                if solution_class.allowed_parents:
                    if "all" in solution_class.allowed_parents or type(solution_instance) in solution_class.allowed_parents:
                        if type(solution_instance) not in solution_class.forbidden_parents:
                            if allowed_children and solution_class.type in allowed_children:
                                allowed_children[solution_class.type].append(solution_class.subtype)
                            else:
                                allowed_children[solution_class.type] = [solution_class.subtype]
        else:
            # If not solution instance given, will return the ones that can be root solutions.
            for solution_class in self.solution_classes:
                if not solution_class.allowed_parents:
                    if allowed_children and solution_class.type in allowed_children:
                        allowed_children[solution_class.type].append(solution_class.subtype)
                    else:
                        allowed_children[solution_class.type] = [solution_class.subtype]

        return allowed_children

    def get_solution_from_ui_object(self, ui_object, solutions=None):
        """Gets a solution instance from the solution trees, using a given UI object in the search.

        Args:
            ui_object (QT object): The given ui object to match the wanted solution.
            solutions (list of solutions, optional): List of solutions to do the search in.

        Returns:
            Solution Instance: Solution instance from the solution trees, using a given UI object in the search.
                Returns None if there is no match.
        """
        if ui_object:
            # Decides the solutions to use in the search.
            if not solutions:
                solutions = self.solution_trees
            elif type(solutions) != list:
                solutions = [solutions]

            # Searches in the solutions for one using the ui_object.
            for sol in solutions:
                # If the ui object is the same, returns the solution.
                if str(ui_object) == str(sol.ui_object):
                    return sol
                elif sol.children_solutions:
                    # If not, searches the children ones.
                    ui_sol = self.get_solution_from_ui_object(ui_object, sol.children_solutions)
                    if ui_sol:
                        return ui_sol

        return None

    def remove_solution(self, solution_instance, recursive=True):
        """Removes the given solution instance and all children recursive if indicated.

        Args:
            solution_instance (Solution Instance): The solution instance to remove.
            recursive (bool, optional): Indicates if al descendants must be removed as well.
        """
        # Only if there is a solution to remove.
        if solution_instance:
            # Firs is necessary, if indicated, removing the descendants, to avoid errors.
            if recursive and solution_instance.children_solutions:
                for child_solution in solution_instance.children_solutions:
                    self.remove_solution(child_solution, recursive=recursive)

        # Removes all goals of the solution.
        for goal in solution_instance.goals:
            solution_instance.remove(goal)

        # If solution has a parent, removes the current one from the parent children.
        if solution_instance.parent_solution:
            if solution_instance in solution_instance.parent_solution.children_solutions:
                solution_instance.parent_solution.children_solutions.remove(solution_instance)

        # If solution is a root solution, removes it from the trees.
        if solution_instance in self.solution_trees:
            self.solution_trees.remove(solution_instance)

    def create_solution(self, solution_type, solution_subtype, parent=None, build=True):
        """Creates the solution of the given type and subtype and returns it.

        Args:
            solution_type (str): Type of the desired solution class.
            solution_subtype (str): Subtype of the desired solution class.
            parent (Solution Instance, optional): Solution parent for the new one.
            build (bool, optional): Indicates if the solution has to be built on creation.

        Returns:
            Solution Instance: Returns the created solution instance.
        """

        # Gets the solution class to be used at creation.
        solution_class = self.get_solution_class(solution_type, solution_subtype)

        # If the combination of type and subtype exists.
        if solution_class:
            # Creates the instance
            solution_instance = solution_class()

            # If a parent solution instance is given, sets the parent.
            if parent:
                solution_instance.set_parent_solution(parent)

            # If the solution must be build on creation, it does it for the first available goal.
            if build:
                solution_goal = solution_class.goals[self.get_solution_goals()[0]]
                solution_instance.build(solution_goal)

            # If the solution has not allowed parents, it means that the solution is the start of a solution tree.
            if not solution_class.allowed_parents:
                self.solution_trees.append(solution_instance)

            return solution_instance

        return None

    def create_solution_from_master_nodes(self, master_nodes, recursive=True):
        """
        Creates a solution instance with the given master nodes.
            It uses the solution info in this nodes attributes to know the type and subtype.

        Args:
            master_nodes (PyNode list): with the master nodes of the solution.
            recursive (bool, optional): Indicates if each solution has to seach for its children solutions.

        Returns:
            Solution Instance: Returns a solution instance of the given nodes solution type.
        """
        solution_instance = None

        # Just in case they are not PyNodes
        master_nodes = [pm.PyNode(node) for node in master_nodes]

        # First of all type and subtype of the solution must be known
        solution_type = master_nodes[0].getAttr("stype")
        solution_subtype = master_nodes[0].getAttr("ssubtype")
        solution_instance_number = master_nodes[0].getAttr("sinstance")

        # Searches the solution type and subtype to use and creates the solution.
        for solution_class in self.solution_classes:
            if solution_class.type == solution_type and solution_class.subtype == solution_subtype:
                # Creates the solution.
                solution_instance = solution_class(solution_manager=self, instance_number=solution_instance_number)

                # Fills the solution with the correspondent nodes.
                solution_instance.fill(master_nodes=master_nodes)

                # If recursive, it searches the children solutions.
                if recursive:
                    solution_branch_nodes = []
                    for goal in solution_instance.goals:
                        solution_branch_nodes += solution_instance.get_nodes(goal, "branch")

                    # For the branch nodes, gets the master children nodes and catalogue them by solution type and subtype.
                    # After that, if there are more than one with same type and subtype, it means it has several
                    # children of the same solution class.
                    if solution_branch_nodes:
                        all_master_nodes = []

                        # Gets all branch children and collects them as masters for next solutions.
                        for branch_node in solution_branch_nodes:
                            children = [pm.PyNode(node) for node in branch_node.listRelatives(children=True, type="transform", fullPath=True)]

                            if children:
                                all_master_nodes += children

                        # If there are masters for new solutions
                        # Now they must be categorized by solution type and subtype. Then by independent hierarchies,
                        # because can have more than one child solution from same class.
                        if all_master_nodes:
                            master_nodes_by_solution = []
                            master_unique_name_parts = []

                            for master_node in all_master_nodes:
                                if master_node.hasAttr("stype"):
                                    # Creates a string with type, subtype and tag, that are unique
                                    # for each solution master y we don't look to the goal.
                                    unique_name_part = master_node.getAttr("stype") + "_" + master_node.getAttr("ssubtype") + "_" + ("%04d" % master_node.getAttr("sinstance"))

                                    # Stores the mater nodes that are related.
                                    # Finally they must be grouped in the list (all parallel goals for each solution).
                                    if unique_name_part not in master_unique_name_parts:
                                        master_unique_name_parts.append(unique_name_part)
                                        master_nodes_by_solution.append([master_node])
                                    else:
                                        index = master_unique_name_parts.index(unique_name_part)
                                        master_nodes_by_solution[index].append(master_node)

                            # For each group of master nodes, creates a solution from them
                            # and stores them as a child of the current one.
                            for master_nodes in master_nodes_by_solution:
                                child_solution_instance = self.create_solution_from_master_nodes(master_nodes, recursive=recursive)
                                solution_instance.add_child_solution(child_solution_instance)

        return solution_instance

    def fill_solution_trees(self):
        """
        Fills the solution trees. Searches in the scene for rig root nodes.
            Then searches recursive filling solutions.
        """
        # Cleans the current trees
        self.solution_trees = []

        # Gets all root nodes
        all_nodes = pm.ls(assemblies=True, long=True)

        # Loops the nodes and process the rig ones. Then searches the root solution.
        # Each rig node can only have one root solution.
        for node in all_nodes:
            if node.startswith(self.rig_group_constants["start"]):
                node = pm.PyNode(node)

                # Gets all children of the rig group.
                # Just in case the rig group has children that are not solution nodes or in case it hast more than
                # one root solution (that should not happen but...), it only uses the first type, subtype and
                # instance number nodes found.
                children_nodes = [pm.PyNode(child) for child in node.listRelatives(children=True, fullPath=True) if pm.PyNode(child).hasAttr("stype")]
                children_nodes = [child for child in children_nodes if child.getAttr("stype") == children_nodes[0].getAttr("stype")]
                children_nodes = [child for child in children_nodes if child.getAttr("ssubtype") == children_nodes[0].getAttr("ssubtype")]
                children_nodes = [child for child in children_nodes if child.getAttr("sinstance") == children_nodes[0].getAttr("sinstance")]

                if children_nodes:
                    # Creates the solution instance
                    solution_instance = self.create_solution_from_master_nodes(children_nodes)

                    # Is solution is created, stores it in the trees list.
                    if solution_instance:
                        self.solution_trees.append(solution_instance)

#######################################
# execution

if __name__ == "__main__":
    # sol_manager = SolutionManager()
    # SolutionWidget(solutions_generic.SolutionRoot)
    pass
