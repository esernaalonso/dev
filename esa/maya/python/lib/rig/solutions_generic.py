"""Generic solutions."""

#######################################
# imports

import maya.cmds as cmds
import pymel.core as pm

import esa.maya.python.lib.rig.utils as utils
# import esa.maya.python.lib.rig.solutions as solutions
import esa.maya.python.lib.icons as icons
import esa.maya.python.lib.ui as ui

from esa.maya.python.lib.rig.solutions import Solution

reload(utils)
# reload(solutions)
# reload(solutions_ui)
reload(icons)
reload(ui)

#######################################
# constants

#######################################
# attributes

#######################################
# definitions

#######################################
# classes

# --------------------------------------
# ROOT SOLUTION


class SolutionRoot(Solution):
    """Override of Generic solution to create root solutions for any kind of rig.

    Attributes:
        description (str): Solution description.
        icon (QIcon): icon for this solution, to use in UIs.
        master_node (TYPE): Master node of the solution fit goal.
        master_node_shape (TYPE): Master node shape of the solution fit goal.
        master_node_shape_circle (TYPE): Master node shape circle input of the solution fit goal.
        node_types (dict of dicts): For each type of goal the default object type to create for each use.
        subtype (str): root. Indicates that is a root solution. It will be the root of the rig.
        type (str): generic. Indicates that is a generic solution to use in all kinds of rig.
    """
    # Solution type and subtype. Class attributes
    type = "generic"
    subtype = "root"

    # Description of this solution.
    description = "This is the Root Solution. Is used as root for the rig. Is the origin of hierarchy for the entire rig."

    # Icon for the solution.
    icon = icons.getIconByName("chemistry_16x16.png")

    # For each kind of goal the default object type to create for each use.
    # This overrides some node types for this solution.
    node_types = {
        "fit":    {"master": "circle", "core": "renderBox", "branch": "empty"},
        "deform": {"master": "empty",  "core": "empty",     "branch": "empty"},
        "anim":   {"master": "empty", "core": "renderBox", "branch": "empty"}
    }

    def __init__(self, solution_manager=None, instance_number=None):
        """Summary

        Args:
            solution_manager (SolutionManager instance, optional): Solution manger instance.
                Can be used to manage children and parent solutions and also to access utils for rig.
            instance_number (int, optional): The number of solutions of this type created. Auto-calculated by default.
        """
        super(SolutionRoot, self).__init__(solution_manager=solution_manager, instance_number=instance_number)

    def create_node_by_type(self, node_type, **kwargs):
        """Create node by type.

        Args:
            node_type (str): Type of the node to be created
            **kwargs: Extra arguments to use in some nodes types creation.

        Returns:
            PyNode: New node of the goal and use specified.
        """

        if "degree" not in kwargs:
            kwargs["degree"] = 1

        if "sections" not in kwargs:
            kwargs["sections"] = 6

        return super(SolutionRoot, self).create_node_by_type(node_type, **kwargs)

    def init_ui_layout(self):
        """Inits the specific ui layout for this solution."""

        # Calls parent init.
        super(SolutionRoot, self).init_ui_layout()

    #     # To override in each specific solution. Prepare layout items with right values.

    #     self.dsp_radius = ui.get_child(self.ui_widget, "dsp_radius")
    #     self.hsl_radius = ui.get_child(self.ui_widget, "hsl_radius")
    #     self.sp_sweep = ui.get_child(self.ui_widget, "sp_sweep")
    #     self.hsl_sweep = ui.get_child(self.ui_widget, "hsl_sweep")
    #     self.sp_sections = ui.get_child(self.ui_widget, "sp_sections")
    #     self.hsl_sections = ui.get_child(self.ui_widget, "hsl_sections")
    #     self.cbx_degree = ui.get_child(self.ui_widget, "cbx_degree")

    #     self.cbx_degree.clear()
    #     self.cbx_degree.addItem("Linear")
    #     self.cbx_degree.addItem("Cubic")

        self.master_node = self.get_node("fit", "master")
        self.master_node_shape = self.master_node.listRelatives(shapes=True)[0]
        self.master_node_shape_circle = self.master_node_shape.listConnections(source=True)[0]

    #     # Update parameters.

    #     if self.master_node_shape_circle:
    #         self.dsp_radius.setValue(self.master_node_shape_circle.attr("radius").get())
    #         self.hsl_radius.setValue(self.master_node_shape_circle.attr("radius").get())
    #         self.sp_sweep.setValue(self.master_node_shape_circle.attr("sweep").get())
    #         self.hsl_sweep.setValue(self.master_node_shape_circle.attr("sweep").get())
    #         self.sp_sections.setValue(self.master_node_shape_circle.attr("sections").get())
    #         self.hsl_sections.setValue(self.master_node_shape_circle.attr("sections").get())
    #         self.cbx_degree.setCurrentIndex(0 if self.master_node_shape_circle.attr("degree").get() < 3 else 1)

    # def init_ui_signals(self):
    #     """Inits the specific ui signals for this solution."""

    #     # Calls parent init.
    #     super(SolutionRoot, self).init_ui_signals()

    #     # To override in each specific solution. Connect the signals.

    #     self.hsl_radius.valueChanged.connect(lambda: self.dsp_radius.setValue(self.hsl_radius.value()))
    #     self.dsp_radius.valueChanged.connect(lambda: self.hsl_radius.setValue(self.dsp_radius.value()))
    #     self.hsl_sweep.valueChanged.connect(lambda: self.sp_sweep.setValue(self.hsl_sweep.value()))
    #     self.sp_sweep.valueChanged.connect(lambda: self.hsl_sweep.setValue(self.sp_sweep.value()))
    #     self.hsl_sections.valueChanged.connect(lambda: self.sp_sections.setValue(self.hsl_sections.value()))
    #     self.sp_sections.valueChanged.connect(lambda: self.hsl_sections.setValue(self.sp_sections.value()))

    #     self.dsp_radius.valueChanged.connect(lambda: self.update_solution("fit"))
    #     self.hsl_radius.valueChanged.connect(lambda: self.update_solution("fit"))
    #     self.sp_sweep.valueChanged.connect(lambda: self.update_solution("fit"))
    #     self.hsl_sweep.valueChanged.connect(lambda: self.update_solution("fit"))
    #     self.sp_sections.valueChanged.connect(lambda: self.update_solution("fit"))
    #     self.hsl_sections.valueChanged.connect(lambda: self.update_solution("fit"))
    #     self.cbx_degree.currentIndexChanged.connect(lambda: self.update_solution("fit"))

    # def update_solution(self, goal, recursive=True):
    #     """Updates the solution with the parameters from the ui if changed.

    #     Args:
    #         goal (str): Type of goal to update.
    #     """
    #     # If goal is not fit, the way to update it is removing the goal and rebuilding it again.
    #     if goal in self.goals and goal != "fit":
    #         super(SolutionRoot, self).update_solution(goal, recursive=recursive)

    #     # If goal is fit.
    #     if goal == "fit" and self.is_goal_built(goal):
    #         if not self.ui_widget.editing:
    #             self.ui_widget.editing = True

    #             # master_node = self.get_node(goal, "master")
    #             # master_node_shape = master_node.listRelatives(shapes=True)[0]
    #             # master_node_shape_circle = master_node_shape.listConnections(source=True)[0]

    #             # Update parameters.
    #             if self.master_node_shape_circle:
    #                 self.master_node_shape_circle.attr("radius").set(self.dsp_radius.value())
    #                 self.master_node_shape_circle.attr("sweep").set(self.sp_sweep.value())
    #                 self.master_node_shape_circle.attr("sections").set(self.sp_sections.value())
    #                 self.master_node_shape_circle.attr("degree").set(1 if self.cbx_degree.currentIndex() == 0 else 3)

    #             self.ui_widget.editing = False

    def init_channel_box(self, **kwargs):
        """Summary

        Args:
            **kwargs: Extra arguments for channel box.
        """
        if self.master_node_shape_circle:
            # get the nurbs circle and the attributes to show and pass it to the super function as kwargs.

            if "fixedAttrList" not in kwargs:
                kwargs["fixedAttrList"] = ["radius", "degree", "sections", "sweep"]

            if "channel_box_nodes" not in kwargs:
                kwargs["channel_box_nodes"] = [self.master_node, self.master_node_shape, self.master_node_shape_circle]

            super(SolutionRoot, self).init_channel_box(**kwargs)

# --------------------------------------
# CENTER SOLUTION


class SolutionCenter(SolutionRoot):
    """Override of Generic solution to create center solutions for any kind of rig.

    Attributes:
        allowed_parents (list of Solution classes): List of the allowed solution classes that can be this one parent
        description (str): Solution description.
        icon (QIcon): icon for this solution, to use in UIs.
        node_types (dict of dicts): For each type of goal the default object type to create for each use.
        subtype (str): root. Indicates that is a center solution. It will be the center of the rig.
        type (str): generic. Indicates that is a generic solution to use in all kinds of rig.
    """
    # Solution type and subtype. Class attributes
    type = "generic"
    subtype = "center"

    # Description of this solution.
    description = "This is the Center Solution. Is used as a mass center in a rig, usually will be the origin for the spine and pelvis systems in a biped, or hips and spine in a quadruped. Some rigs could require multiple centers. Also other independent rig solutions could hang from it."

    # Allowed parent solution types
    # If empty it means that can be used as a rig root solution.
    # If contains element "all" means that the parent can be any solution.
    allowed_parents = ["all"]

    # Icon for the solution.
    icon = icons.getIconByName("center_16x16.png")

    # For each kind of goal the default object type to create for each use.
    # This overrides some node types for this solution.
    node_types = {
        "fit":    {"master": "circle", "core": "renderBox", "branch": "empty"},
        "deform": {"master": "empty",  "core": "empty",     "branch": "joint"},
        "anim":   {"master": "empty", "core": "renderBox", "branch": "empty"}
    }

    def __init__(self, solution_manager=None, instance_number=None):
        """Summary

        Args:
            solution_manager (SolutionManager instance, optional): Solution manger instance.
                Can be used to manage children and parent solutions and also to access utils for rig.
            instance_number (int, optional): The number of solutions of this type created. Auto-calculated by default.
        """
        super(SolutionCenter, self).__init__(solution_manager=solution_manager, instance_number=instance_number)

    def create_node_by_type(self, node_type, **kwargs):
        """Create node by type.

        Args:
            node_type (str): Type of the node to be created
            **kwargs: Extra arguments to use in some nodes types creation.

        Returns:
            PyNode: New node of the goal and use specified.
        """

        if "sections" not in kwargs:
            kwargs["sections"] = 3

        if "radius" not in kwargs:
            kwargs["radius"] = 5

        if "normal" not in kwargs:
            kwargs["normal"] = (0, -1, 0)

        return super(SolutionCenter, self).create_node_by_type(node_type, **kwargs)

# --------------------------------------
# JOINT CHAIN SOLUTION
# INPROGRESS:0 Solutions Generic. Override of Generic solution to create joint chain solutions for any kind of rig. issue:3


class SolutionJointChainFK(Solution):
    """Override of Generic solution to create joint chain solutions for any kind of rig.

    Attributes:
        allowed_parents (list of Solution classes): List of the allowed solution classes that can be this one parent
        description (str): Solution description.
        icon (QIcon): icon for this solution, to use in UIs.
        node_types (dict of dicts): For each type of goal the default object type to create for each use.
        subtype (str): root. Indicates that is a center solution. It will be the center of the rig.
        type (str): generic. Indicates that is a generic solution to use in all kinds of rig.
    """
    # Solution type and subtype. Class attributes
    type = "generic"
    subtype = "chain"

    # Description of this solution.
    description = "This is a generic FK joint chain to use as required."

    # Allowed parent solution types
    # If empty it means that can be used as a rig root solution.
    # If contains element "all" means that the parent can be any solution.
    allowed_parents = ["all"]
    forbidden_parents = [SolutionRoot]

    # Icon for the solution.
    icon = icons.getIconByName("center_16x16.png")

    # For each kind of goal the default object type to create for each use.
    # This overrides some node types for this solution.
    node_types = {
        "fit":    {"master": "circle", "core": "renderBox", "branch": "empty"},
        "deform": {"master": "joint",  "core": "joint",     "branch": "joint"},
        "anim":   {"master": "empty", "core": "renderBox", "branch": "empty"}
    }

    def __init__(self, solution_manager=None, instance_number=None):
        """Summary

        Args:
            solution_manager (SolutionManager instance, optional): Solution manger instance.
                Can be used to manage children and parent solutions and also to access utils for rig.
            instance_number (int, optional): The number of solutions of this type created. Auto-calculated by default.
        """
        super(SolutionJointChainFK, self).__init__(solution_manager=solution_manager, instance_number=instance_number)

    # TODO:70 Override the store_node function to get the final node to see the distance.

    def init_ui_layout(self):
        """Inits the specific ui layout for this solution."""

        # Calls parent init.
        super(SolutionJointChainFK, self).init_ui_layout()

        self.master_node = self.get_node("fit", "master")
        self.master_node_shape = self.master_node.listRelatives(shapes=True)[0]
        self.master_node_shape_circle = self.master_node_shape.listConnections(source=True)[0]

    def create_node_by_type(self, node_type, **kwargs):
        """Create node by type.

        Args:
            node_type (str): Type of the node to be created
            **kwargs: Extra arguments to use in some nodes types creation.

        Returns:
            PyNode: New node of the goal and use specified.
        """

        if "degree" not in kwargs:
            kwargs["degree"] = 1

        if "sections" not in kwargs:
            kwargs["sections"] = 4

        if "radius" not in kwargs:
            kwargs["radius"] = 2

        return super(SolutionJointChainFK, self).create_node_by_type(node_type, **kwargs)

    def build_core(self, goal):
        """Creates the core solution attending to the goal type.

        Args:
            goal (str): Goal of the core to build.
        """

        # Creation of fit goal
        if goal == "fit":

            # Default attributes.
            # TODO:80 change them by attributes from the ui signals.
            segments = 3
            distance = 10.0
            segment_distance = distance/segments

            master_node = self.get_node(goal, "master")

            # ------------------------------------
            # Creates a node to be the parent of all core part
            first_core_node = self.create_node_by_type("empty")

            first_core_node_tag = "first"
            self.rename_node(first_core_node, goal, "core", first_core_node_tag)
            self.set_color(first_core_node, goal)
            self.add_attributes(first_core_node, goal, "core", first_core_node_tag)
            self.nodes[goal]["core"].append(first_core_node)
            # ------------------------------------

            # ------------------------------------
            # Creates a node to drive the length of the core part
            last_core_node = self.create_node_by_type("circle", radius=1.5)

            last_core_node_tag = "last"
            self.rename_node(last_core_node, goal, "core", last_core_node_tag)
            self.set_color(last_core_node, goal)
            self.add_attributes(last_core_node, goal, "core", last_core_node_tag)

            # Position it in the distance required and parent to first core node
            utils.align(last_core_node, first_core_node, offset_translation=[0.0, distance, 0.0])
            pm.parent(last_core_node, first_core_node, absolute=True)

            # Creates the zero transform node for this one.
            self.create_zero_transform_node(last_core_node)
            # ------------------------------------

            # ------------------------------------
            # Creates the node to aim the deform joints to it.
            last_core_aim_node = self.create_node_by_type("spaceLocator")

            last_core_aim_node_tag = "lastAim"
            self.rename_node(last_core_aim_node, goal, "core", last_core_aim_node_tag)
            self.set_color(last_core_aim_node, goal)
            self.add_attributes(last_core_aim_node, goal, "core", last_core_aim_node_tag)

            # Align the joint align node to the core node. Also inverts x and y.
            utils.align(last_core_aim_node, last_core_node, offset_translation=[distance, 0, 0])
            pm.parent(last_core_aim_node, last_core_node, absolute=True)
            # ------------------------------------

            # If the main core node is created successfully, continues with all the others.
            if first_core_node and last_core_node:
                # ------------------------------------
                # Variables to store prev iteration nodes.
                prev_joint_node = None
                prev_segment_node = None
                # ------------------------------------

                # Loops the number of segments.
                for i in range(segments + 1):
                    # ------------------------------------
                    # Create a segment parent node for each segment and an extra one for the end.
                    segment_parent_node = self.create_node_by_type("spaceLocator")

                    # Set the properties.
                    segment_parent_node_tag = ("segmentParent%03d" % i)
                    self.rename_node(segment_parent_node, goal, "core", segment_parent_node_tag)
                    self.set_color(segment_parent_node, goal)
                    self.add_attributes(segment_parent_node, goal, "core", segment_parent_node_tag)

                    # Position the segment node in the right position.
                    utils.align(segment_parent_node, first_core_node, offset_translation=[0.0, segment_distance*i, 0.0])
                    pm.parent(segment_parent_node, first_core_node, absolute=True)

                    # Creates the point constraint to maintain segment distances.
                    pm.pointConstraint(first_core_node, last_core_node, segment_parent_node)
                    pm.pointConstraint(first_core_node, segment_parent_node, e=True, w=(100.0/segments)*(segments - i))
                    pm.pointConstraint(last_core_node, segment_parent_node, e=True, w=(100.0/segments)*i)

                    # Creates the aim constraint to point the last node.
                    target = last_core_node if i < segments else first_core_node
                    pm.aimConstraint(target, segment_parent_node, aim=[0, 1, 0], u=[1, 0, 0], mo=True, wut="object", wuo=last_core_aim_node)
                    # ------------------------------------

                    # ------------------------------------
                    # Create a segment node for each segment and an extra one for the end.
                    segment_node = self.create_node_by_type("circle", radius=1)

                    # Set the properties.
                    segment_node_tag = ("segment%03d" % i)
                    self.rename_node(segment_node, goal, "core", segment_node_tag)
                    self.set_color(segment_node, goal)
                    self.add_attributes(segment_node, goal, "core", segment_node_tag)

                    # Position the segment node in the right position.
                    utils.align(segment_node, segment_parent_node)
                    pm.parent(segment_node, segment_parent_node, absolute=True)

                    # Creates the zero transform node for this one.
                    self.create_zero_transform_node(segment_node)
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the node to align the deform joints to it.
                    joint_node = self.create_node_by_type("joint")

                    # Creates the align node.
                    joint_node_tag = ("joint%03d" % i)
                    self.rename_node(joint_node, goal, "core", joint_node_tag)
                    self.set_color(joint_node, goal)
                    self.add_attributes(joint_node, goal, "core", joint_node_tag)

                    # Align the joint align node to the core node. Also inverts x and y.
                    utils.align(joint_node, segment_node, invert="xy")
                    pm.parent(joint_node, segment_node, absolute=True)

                    if prev_joint_node:
                        # Creates the aim constraint to point the next segment.
                        if i <= segments:
                            pm.aimConstraint(segment_node, prev_joint_node, aim=[0, 1, 0], u=[1, 0, 0], mo=True, wut="object", wuo=last_core_aim_node)

                        # Creates the aim constraint to point to the previous segment in the case of last part.
                        if i == segments:
                            pm.aimConstraint(prev_segment_node, joint_node, aim=[0, 1, 0], u=[1, 0, 0], mo=True, wut="object", wuo=last_core_aim_node)

                    # TODO: Think in a way to avoid the flip in the segments caused by the main aim node distance.
                    # Increase the distance or create more intermediate aim nodes.
                    # ------------------------------------

                    # ------------------------------------
                    # Stores the current nodes to use in the next interation.
                    prev_segment_node = segment_node
                    prev_joint_node = joint_node
                    # ------------------------------------

                    # ------------------------------------
                    # Add the nodes to the core solution
                    self.nodes[goal]["core"].append(segment_parent_node)
                    self.nodes[goal]["core"].append(segment_node)
                    self.nodes[goal]["core"].append(joint_node)
                    # ------------------------------------

                # ------------------------------------
                # Add the nodes to the core solution
                self.nodes[goal]["core"].append(last_core_node)

    def init_channel_box(self, **kwargs):
        """Summary

        Args:
            **kwargs: Extra arguments for channel box.
        """
        if self.master_node_shape_circle:
            # get the nurbs circle and the attributes to show and pass it to the super function as kwargs.

            if "fixedAttrList" not in kwargs:
                kwargs["fixedAttrList"] = ["radius", "degree", "sections", "sweep"]

            if "channel_box_nodes" not in kwargs:
                kwargs["channel_box_nodes"] = [self.master_node, self.master_node_shape, self.master_node_shape_circle]

            super(SolutionJointChainFK, self).init_channel_box(**kwargs)
#######################################
# execution

if __name__ == "__main__":
    pass
