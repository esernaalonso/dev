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

        # To override in each specific solution. Prepare layout items with right values.

        self.master_node = self.get_node("fit", "master")
        self.master_node_shape = self.master_node.listRelatives(shapes=True)[0]
        self.master_node_shape_circle = self.master_node_shape.listConnections(source=True)[0]

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
    subtype = "chainFK"

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

        # ------------------------------------
        # FIT GOAL
        # TODO: Create auxiliar nodes to use in the anim align and conform.

        # Creation of fit goal
        if goal == "fit":
            # ------------------------------------
            # Default attributes values.
            segments = 3
            if hasattr(self, "sp_segments"):
                segments = self.sp_segments.value()

            distance = 10.0
            if hasattr(self, "dsp_len"):
                distance = self.dsp_len.value()

            segment_distance = distance/segments
            # ------------------------------------

            # ------------------------------------
            master_node = self.get_node(goal, "master")
            master_node_shape = master_node.listRelatives(shapes=True)[0]
            master_node_shape_circle = master_node_shape.listConnections(source=True)[0]

            # Locks and hides non necessary attributes.
            self.setup_channelBox_attributes(master_node_shape_circle, ["radius", "sections", "degree", "sweep"])
            # ------------------------------------

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

            # Locks and hides non necessary attributes.
            self.setup_channelBox_attributes(last_core_node, ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])

            # Position it in the distance required and parent to first core node
            utils.align(last_core_node, first_core_node, offset_translation=[0.0, distance, 0.0])
            pm.parent(last_core_node, first_core_node, absolute=True)

            # NOTE: In this case we dont add the node for now to the solution core nodes because we need to do it at the end,
            # since the branch node must be the child of this last core node.

            # Creates the zero transform node for this one.
            last_core_zero_node = self.create_zero_transform_node(last_core_node)
            self.nodes[goal]["core"].append(last_core_zero_node)
            # ------------------------------------

            # ------------------------------------
            # Creates the radius and sections, etc. connection from the main control to the last core node.
            last_core_node_shape = last_core_node.listRelatives(shapes=True)[0]
            last_core_node_shape_circle = last_core_node_shape.listConnections(source=True)[0]
            pm.connectAttr(master_node_shape_circle.attr("radius"), last_core_node_shape_circle.attr("radius"))
            pm.connectAttr(master_node_shape_circle.attr("sections"), last_core_node_shape_circle.attr("sections"))
            pm.connectAttr(master_node_shape_circle.attr("degree"), last_core_node_shape_circle.attr("degree"))
            pm.connectAttr(master_node_shape_circle.attr("sweep"), last_core_node_shape_circle.attr("sweep"))

            # Locks and hides non necessary attributes.
            self.setup_channelBox_attributes(last_core_node_shape_circle, ["radius", "sections", "degree", "sweep"])
            # ------------------------------------

            # ------------------------------------
            # Creates the node to aim the deform joints to it.
            last_core_aim_node = self.create_node_by_type("empty")

            last_core_aim_node_tag = "lastAim"
            self.rename_node(last_core_aim_node, goal, "core", last_core_aim_node_tag)
            self.set_color(last_core_aim_node, goal)
            self.add_attributes(last_core_aim_node, goal, "core", last_core_aim_node_tag)

            # Align the joint align node to the core node. Also inverts x and y.
            utils.align(last_core_aim_node, last_core_node, offset_translation=[0, 0, distance])
            pm.parent(last_core_aim_node, last_core_node, absolute=True)

            self.nodes[goal]["core"].append(last_core_aim_node)
            # ------------------------------------

            # ------------------------------------
            # Creates the connection from the distance to the aim node separation.
            last_core_aim_distance_node = self.create_node_by_type("plusMinusAverage")

            last_core_aim_distance_node_tag = "lastAimDistance"
            self.rename_node(last_core_aim_distance_node, goal, "core", last_core_aim_distance_node_tag)
            self.add_attributes(last_core_aim_distance_node, goal, "core", last_core_aim_distance_node_tag)

            pm.connectAttr(last_core_node.attr("translateY"), last_core_aim_distance_node.attr("input1D[0]"))
            pm.connectAttr(last_core_zero_node.attr("translateY"), last_core_aim_distance_node.attr("input1D[1]"))
            pm.connectAttr(last_core_aim_distance_node.attr("output1D"), last_core_aim_node.attr("translateZ"))

            # NOTE: Don't add non dag nodes to the solution node lists, beccause since they don't have parent,
            # can be confused with first core node and used wrong to get the master node. Gives listRelatives errors.
            # self.nodes[goal]["core"].append(last_core_aim_distance_node)
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
                    segment_parent_node = self.create_node_by_type("empty")

                    # Set the properties.
                    segment_parent_node_tag = ("segmentParent%03d" % i)
                    self.rename_node(segment_parent_node, goal, "core", segment_parent_node_tag)
                    self.set_color(segment_parent_node, goal)
                    self.add_attributes(segment_parent_node, goal, "core", segment_parent_node_tag)

                    # Position the segment node in the right position.
                    utils.align(segment_parent_node, first_core_node, offset_translation=[0.0, segment_distance*i, 0.0])
                    pm.parent(segment_parent_node, first_core_node, absolute=True)

                    # Creates the point constraint to maintain segment distances.
                    segment_parent_node_point_constraint = pm.PyNode(pm.pointConstraint(first_core_node, last_core_node, segment_parent_node))
                    pm.pointConstraint(first_core_node, segment_parent_node, e=True, w=(100.0/segments)*(segments - i))
                    pm.pointConstraint(last_core_node, segment_parent_node, e=True, w=(100.0/segments)*i)

                    segment_parent_node_point_constraint_tag = ("segmentParentPointConstraint%03d" % i)
                    self.rename_node(segment_parent_node_point_constraint, goal, "core", segment_parent_node_point_constraint_tag)
                    self.set_color(segment_parent_node_point_constraint, goal)
                    self.add_attributes(segment_parent_node_point_constraint, goal, "core", segment_parent_node_point_constraint_tag)

                    # Creates the aim constraint to point the last node.
                    target = last_core_node if i < segments else first_core_node
                    segment_parent_node_aim_constraint = pm.PyNode(pm.aimConstraint(target, segment_parent_node, aim=[0, 1, 0], u=[0, 0, 1], mo=True, wut="object", wuo=last_core_aim_node))

                    segment_parent_node_aim_constraint_tag = ("segmentParentAimConstraint%03d" % i)
                    self.rename_node(segment_parent_node_aim_constraint, goal, "core", segment_parent_node_aim_constraint_tag)
                    self.set_color(segment_parent_node_aim_constraint, goal)
                    self.add_attributes(segment_parent_node_aim_constraint, goal, "core", segment_parent_node_aim_constraint_tag)
                    # ------------------------------------

                    # ------------------------------------
                    # Create a segment node for each segment and an extra one for the end.
                    segment_node = self.create_node_by_type("circle", radius=1)

                    # Set the properties.
                    segment_node_tag = ("segment%03d" % i)
                    self.rename_node(segment_node, goal, "core", segment_node_tag)
                    self.set_color(segment_node, goal)
                    self.add_attributes(segment_node, goal, "core", segment_node_tag)
                    self.setup_channelBox_attributes(segment_node, ["translateY", "translateZ"])

                    # Position the segment node in the right position.
                    utils.align(segment_node, segment_parent_node)
                    pm.parent(segment_node, segment_parent_node, absolute=True)

                    # Creates the zero transform node for this one.
                    segment_zero_node = self.create_zero_transform_node(segment_node)
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the radius connection from the main control to the segments nodes.
                    segment_radius_node = self.create_node_by_type("multiplyDivide")
                    segment_radius_node.attr("input2.input2X").set(0.5)

                    segment_radius_node_tag = ("segmentRadius%03d" % i)
                    self.rename_node(segment_radius_node, goal, "core", segment_radius_node_tag)
                    self.add_attributes(segment_radius_node, goal, "core", segment_radius_node_tag)

                    # Connects the radius.
                    segment_node_shape = segment_node.listRelatives(shapes=True)[0]
                    segment_node_shape_circle = segment_node_shape.listConnections(source=True)[0]
                    pm.connectAttr(master_node_shape_circle.attr("radius"), segment_radius_node.attr("input1.input1X"))
                    pm.connectAttr(segment_radius_node.attr("output.outputX"), segment_node_shape_circle.attr("radius"))

                    pm.connectAttr(master_node_shape_circle.attr("sections"), segment_node_shape_circle.attr("sections"))
                    pm.connectAttr(master_node_shape_circle.attr("degree"), segment_node_shape_circle.attr("degree"))
                    pm.connectAttr(master_node_shape_circle.attr("sweep"), segment_node_shape_circle.attr("sweep"))

                    # Locks and hides non necessary attributes.
                    self.setup_channelBox_attributes(segment_node_shape_circle, ["radius", "sections", "degree", "sweep"])
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the node to aim the deform joints to it.
                    segment_joint_aim_node = self.create_node_by_type("empty")

                    segment_joint_aim_node_tag = ("segmentJointAim%03d" % i)
                    self.rename_node(segment_joint_aim_node, goal, "core", segment_joint_aim_node_tag)
                    self.set_color(segment_joint_aim_node, goal)
                    self.add_attributes(segment_joint_aim_node, goal, "core", segment_joint_aim_node_tag)

                    # Position the segment aim node in the right position.
                    utils.align(segment_joint_aim_node, segment_node)
                    pm.parent(segment_joint_aim_node, segment_node, absolute=True)
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the connection from the distance to the aim node separation.
                    segment_joint_aim_distance_node = self.create_node_by_type("plusMinusAverage")

                    segment_joint_aim_distance_node_tag = ("segmentJointAimDistance%03d" % i)
                    self.rename_node(segment_joint_aim_distance_node, goal, "core", segment_joint_aim_distance_node_tag)
                    self.add_attributes(segment_joint_aim_distance_node, goal, "core", segment_joint_aim_distance_node_tag)

                    # pm.connectAttr(segment_parent_node.attr("translateY"), segment_joint_aim_distance_node.attr("input1D[0]"))
                    pm.connectAttr(last_core_zero_node.attr("translateY"), segment_joint_aim_distance_node.attr("input1D[0]"))
                    pm.connectAttr(last_core_node.attr("translateY"), segment_joint_aim_distance_node.attr("input1D[1]"))
                    pm.connectAttr(segment_node.attr("translateY"), segment_joint_aim_distance_node.attr("input1D[2]"))
                    pm.connectAttr(segment_joint_aim_distance_node.attr("output1D"), segment_joint_aim_node.attr("translateZ"))

                    # NOTE: Don't add non dag nodes to the solution node lists, beccause since they don't have parent,
                    # can be confused with first core node and used wrong to get the master node. Gives listRelatives errors.
                    # self.nodes[goal]["core"].append(segment_joint_aim_distance_node)
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the node to align the deform joints to it.
                    joint_node = self.create_node_by_type("empty")

                    # Creates the align node.
                    joint_node_tag = ("segmentJoint%03d" % i)
                    self.rename_node(joint_node, goal, "core", joint_node_tag)
                    self.set_color(joint_node, goal)
                    self.add_attributes(joint_node, goal, "core", joint_node_tag)

                    # Align the joint align node to the core node. Also inverts x and y.
                    utils.align(joint_node, segment_node, invert="xy")
                    pm.parent(joint_node, segment_node, absolute=True)

                    joint_node_aim_constraint = None
                    last_joint_node_aim_constraint = None
                    if prev_joint_node:
                        # Creates the aim constraint to point the next segment.
                        joint_node_aim_constraint = pm.PyNode(pm.aimConstraint(segment_node, prev_joint_node, aim=[0, 1, 0], u=[0, 0, 1], mo=True, wut="object", wuo=last_core_aim_node))

                        joint_node_aim_constraint_tag = ("jointNodeAimConstraint%03d" % i)
                        self.rename_node(joint_node_aim_constraint, goal, "core", joint_node_aim_constraint_tag)
                        self.set_color(joint_node_aim_constraint, goal)
                        self.add_attributes(joint_node_aim_constraint, goal, "core", joint_node_aim_constraint_tag)

                        # Creates the aim constraint to point to the previous segment in the case of last part.
                        if i == segments:
                            last_joint_node_aim_constraint = pm.PyNode(pm.aimConstraint(prev_segment_node, joint_node, aim=[0, 1, 0], u=[0, 0, 1], mo=True, wut="object", wuo=last_core_aim_node))

                            last_joint_node_aim_constraint_tag = ("jointNodeAimConstraint%03d" % i)
                            self.rename_node(last_joint_node_aim_constraint, goal, "core", last_joint_node_aim_constraint_tag)
                            self.set_color(last_joint_node_aim_constraint, goal)
                            self.add_attributes(last_joint_node_aim_constraint, goal, "core", last_joint_node_aim_constraint_tag)
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the node to align the animation controls for the anim goal.
                    joint_anim_node = self.create_node_by_type("empty")

                    # Creates the anim node.
                    joint_anim_node_tag = ("segmentControl%03d" % i)
                    self.rename_node(joint_anim_node, goal, "core", joint_anim_node_tag)
                    self.set_color(joint_anim_node, goal)
                    self.add_attributes(joint_anim_node, goal, "core", joint_anim_node_tag)

                    # Align the joint anim node to the joint node.
                    utils.align(joint_anim_node, joint_node)
                    pm.parent(joint_anim_node, joint_node, absolute=True)

                    # ------------------------------------

                    # ------------------------------------
                    # Creates the node to visualize the joint direction.
                    # Creates the node to calculate the length to next joint.

                    joint_len_node = None
                    joint_len_node_point_constraint = None
                    segment_body_node = None
                    segment_body_node_point_constraint = None

                    if prev_joint_node:
                        # ------------------------------------
                        # Creates the length reference node.
                        joint_len_node = self.create_node_by_type("empty")

                        joint_len_node_tag = ("segmentJointLen%03d" % i)
                        self.rename_node(joint_len_node, goal, "core", joint_len_node_tag)
                        self.set_color(joint_len_node, goal)
                        self.add_attributes(joint_len_node, goal, "core", joint_len_node_tag)

                        # Align the body node to the joint.
                        utils.align(joint_len_node, prev_joint_node)
                        pm.parent(joint_len_node, prev_joint_node, absolute=True)

                        # Creates the point constraint to calculate the ditance to the next joint.
                        joint_len_node_point_constraint = pm.PyNode(pm.pointConstraint(joint_node, joint_len_node))

                        joint_len_node_point_constraint_tag = ("segmentJointLenPointConstraint%03d" % i)
                        self.rename_node(joint_len_node_point_constraint, goal, "core", joint_len_node_point_constraint_tag)
                        self.set_color(joint_len_node_point_constraint, goal)
                        self.add_attributes(joint_len_node_point_constraint, goal, "core", joint_len_node_point_constraint_tag)
                        # ------------------------------------

                        # ------------------------------------
                        # Creates the body node.
                        segment_body_node = self.create_node_by_type("renderBox")

                        segment_body_node_tag = ("segmentBody%03d" % i)
                        self.rename_node(segment_body_node, goal, "core", segment_body_node_tag)
                        self.set_color(segment_body_node, goal)
                        self.add_attributes(segment_body_node, goal, "core", segment_body_node_tag)

                        # Align the body node to the joint.
                        utils.align(segment_body_node, prev_joint_node)
                        pm.parent(segment_body_node, prev_joint_node, absolute=True)

                        # Creates the point constraint to maintain the ditance to the next joint.
                        segment_body_node_point_constraint = pm.PyNode(pm.pointConstraint(prev_joint_node, joint_node, segment_body_node))
                        # pm.pointConstraint(first_core_node, segment_parent_node, e=True, w=(100.0/segments)*(segments - i))
                        # pm.pointConstraint(last_core_node, segment_parent_node, e=True, w=(100.0/segments)*i)

                        segment_body_node_point_constraint_tag = ("segmentBodyPointConstraint%03d" % i)
                        self.rename_node(segment_body_node_point_constraint, goal, "core", segment_body_node_point_constraint_tag)
                        self.set_color(segment_body_node_point_constraint, goal)
                        self.add_attributes(segment_body_node_point_constraint, goal, "core", segment_body_node_point_constraint_tag)

                        # Connects the joint length to the box lenght.
                        pm.connectAttr(joint_len_node.attr("translateY"), segment_body_node.attr("sizeY"))

                        # Connects the segment radius to the box width.
                        box_radius_node = self.create_node_by_type("multiplyDivide")
                        box_radius_node.attr("input2.input2X").set(0.5)

                        box_radius_node_tag = ("segmentBoxRadius%03d" % i)
                        self.rename_node(box_radius_node, goal, "core", box_radius_node_tag)
                        self.add_attributes(box_radius_node, goal, "core", box_radius_node_tag)

                        prev_segment_node_shape = prev_segment_node.listRelatives(shapes=True)[0]
                        prev_segment_node_shape_circle = prev_segment_node_shape.listConnections(source=True)[0]

                        pm.connectAttr(prev_segment_node_shape_circle.attr("radius"), box_radius_node.attr("input1.input1X"))
                        pm.connectAttr(box_radius_node.attr("output.outputX"), segment_body_node.attr("sizeX"))
                        pm.connectAttr(box_radius_node.attr("output.outputX"), segment_body_node.attr("sizeZ"))

                        # Locks and hides non necessary attributes.
                        self.setup_channelBox_attributes(segment_body_node, ["no_attributes"])
                        # ------------------------------------
                    # ------------------------------------

                    # ------------------------------------
                    # Stores the current nodes to use in the next interation.
                    prev_segment_node = segment_node
                    prev_joint_node = joint_node
                    # ------------------------------------

                    # ------------------------------------
                    # Add the nodes to the core solution
                    self.nodes[goal]["core"].append(segment_parent_node)
                    self.nodes[goal]["core"].append(segment_parent_node_point_constraint)
                    self.nodes[goal]["core"].append(segment_parent_node_aim_constraint)
                    self.nodes[goal]["core"].append(segment_node)
                    self.nodes[goal]["core"].append(segment_zero_node)
                    self.nodes[goal]["core"].append(segment_joint_aim_node)
                    self.nodes[goal]["core"].append(joint_node)
                    self.nodes[goal]["core"].append(joint_anim_node)

                    if joint_node_aim_constraint:
                        self.nodes[goal]["core"].append(joint_node_aim_constraint)
                    if last_joint_node_aim_constraint:
                        self.nodes[goal]["core"].append(last_joint_node_aim_constraint)

                    if joint_len_node:
                        self.nodes[goal]["core"].append(joint_len_node)
                    if joint_len_node_point_constraint:
                        self.nodes[goal]["core"].append(joint_len_node_point_constraint)
                    if segment_body_node:
                        self.nodes[goal]["core"].append(segment_body_node)
                    if segment_body_node_point_constraint:
                        self.nodes[goal]["core"].append(segment_body_node_point_constraint)
                    # ------------------------------------

                # ------------------------------------
                # NOTE: In this case we add the last node to the core solutiond at the end because the branch node must be the child of this last core node.
                self.nodes[goal]["core"].append(last_core_node)

        # FIT GOAL END
        # ------------------------------------

        # ------------------------------------
        # DEFORM GOAL

        # Creation of deform goal
        if goal == "deform":
            if self.is_goal_built("fit"):
                fit_joints = self.get_nodes("fit", "core", "segmentJoint[0-9]{3,3}$")

                prev_joint_node = None
                for i in range(len(fit_joints)):
                    # ------------------------------------
                    # Creates the deform joints.
                    joint_node = self.create_node_by_type("joint")

                    joint_node_tag = ("segmentJoint%03d" % i)
                    self.rename_node(joint_node, goal, "core", joint_node_tag)
                    self.set_color(joint_node, goal)
                    self.add_attributes(joint_node, goal, "core", joint_node_tag)

                    # Align to the fit node.
                    utils.align(joint_node, fit_joints[i])

                    # Parents it to the previous joint.
                    if prev_joint_node:
                        pm.parent(joint_node, prev_joint_node, absolute=True)

                    # Stores the current node as previous for next iteration.
                    prev_joint_node = joint_node

                    # Stores the node in tbe correspondent list.
                    self.nodes[goal]["core"].append(joint_node)
                    # ------------------------------------

        # DEFORM GOAL END
        # ------------------------------------

        # ------------------------------------
        # ANIM GOAL

        # Creation of anim goal
        if goal == "anim":
            if self.is_goal_built("fit"):
                fit_joint_anim_controls = self.get_nodes("fit", "core", "segmentControl[0-9]{3,3}$")
                fit_joints = self.get_nodes("fit", "core", "segmentJoint[0-9]{3,3}$")

                prev_joint_anim_node = None

                for i in range(len(fit_joint_anim_controls)):
                    # ------------------------------------
                    # Creates the deform joints.
                    joint_anim_node = self.create_node_by_type("circle")

                    joint_anim_node_tag = ("segmentControl%03d" % i)
                    self.rename_node(joint_anim_node, goal, "core", joint_anim_node_tag)
                    self.set_color(joint_anim_node, goal)
                    self.add_attributes(joint_anim_node, goal, "core", joint_anim_node_tag)

                    # Align to the fit node.
                    utils.align(joint_anim_node, fit_joint_anim_controls[i])

                    # Parents it to the previous joint.
                    if prev_joint_anim_node:
                        pm.parent(joint_anim_node, prev_joint_anim_node, absolute=True)

                    # Stores the current node as previous for next iteration.
                    prev_joint_anim_node = joint_anim_node
                    # ------------------------------------

                    # ------------------------------------
                    # Creates the deform joints.
                    joint_node = self.create_node_by_type("joint")

                    joint_node_tag = ("segmentJoint%03d" % i)
                    self.rename_node(joint_node, goal, "core", joint_node_tag)
                    self.set_color(joint_node, goal)
                    self.add_attributes(joint_node, goal, "core", joint_node_tag)

                    # Align to the fit node.
                    utils.align(joint_node, fit_joints[i])

                    # Parents it to the anim control.
                    pm.parent(joint_node, joint_anim_node, absolute=True)
                    # ------------------------------------

                    # ------------------------------------
                    # Stores the node in tbe correspondent list.
                    self.nodes[goal]["core"].append(joint_anim_node)
                    self.nodes[goal]["core"].append(joint_node)
                    # ------------------------------------

        # ANIM GOAL END
        # ------------------------------------

    def init_ui_layout(self):
        """Inits the specific ui layout for this solution."""

        # Calls parent init.
        super(SolutionJointChainFK, self).init_ui_layout()

        self.master_node = self.get_node("fit", "master")
        self.master_node_shape = self.master_node.listRelatives(shapes=True)[0]
        self.master_node_shape_circle = self.master_node_shape.listConnections(source=True)[0]

        # To override in each specific solution. Prepare layout items with right values.
        self.dsp_len = ui.get_child(self.ui_widget, "dsp_len")
        self.sp_segments = ui.get_child(self.ui_widget, "sp_segments")
        self.pb_apply = ui.get_child(self.ui_widget, "pb_apply")

        # Update parameters.
        if self.is_goal_built("fit"):
            last_core_node = self.get_node("fit", "core", "^last$")
            last_core_zt_node = self.get_node("fit", "core", "^lastZT$")
            if last_core_node and last_core_zt_node:
                self.dsp_len.setValue(last_core_node.attr("translateY").get() + last_core_zt_node.attr("translateY").get())

            segments = self.get_nodes("fit", "core", "segment[0-9]{3,3}$")
            if segments:
                self.sp_segments.setValue(len(segments) - 1)

    def init_ui_signals(self):
        """Inits the specific ui signals for this solution."""

        # Calls parent init.
        super(SolutionJointChainFK, self).init_ui_signals()

        # To override in each specific solution. Connect the signals.

        self.pb_apply.clicked.connect(lambda: self.update_solution("fit"))

    def update_solution(self, goal, recursive=True):
        """Updates the solution with the parameters from the ui if changed.

        Args:
            goal (str): Type of goal to update.
        """
        # If goal is not fit, the way to update it is removing the goal and rebuilding it again.
        if goal in self.goals and goal != "fit":
            super(SolutionRoot, self).update_solution(goal, recursive=recursive)

        # If goal is fit.
        if goal == "fit" and self.is_goal_built(goal):
            self.remove(goal, recursive=recursive)
            if self.validate_build(goal):
                self.build(goal, recursive=recursive)

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
