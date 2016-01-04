"""Rig Manager Tool: Chicken Bones.

Attributes:
    permission (str): Indicates who has permission to execute this tool.
"""
#######################################
# imports

import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as apiUI
import sys
import os

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.icons as icons
import esa.maya.python.lib.rig.solutions_generic as solutions_generic
import esa.maya.python.lib.rig.solutions as solutions

reload(utils)
reload(ui)
reload(icons)
reload(solutions_generic)
reload(solutions)

#######################################
# attributes

permission = "artist"

#######################################
# functionality


class RigManager(QtGui.QDialog):
    """Rig Manager to handle the solution creation and also with rigging utils.

    Attributes:
        dockCtrl (dockControl): Interface control to dock the manager
        mainWidget (Widget): Manager main widget.
        opened (bool): Indicates if the Manager is open.
    """
    def __init__(self,  parent=utils.getMayaWindow()):
        """Summary

        Args:
            parent (Attribute, optional): Parent window for the manager.
        """
        super(RigManager, self).__init__(parent)

        self.setLayout(QtGui.QVBoxLayout())

        self.setObjectName('rigManager')
        allowedAreas = ['right', 'left']
        self.dockCtrl = cmds.dockControl(label='Chicken Bones Rig Manager', area='left', content=self.objectName(), allowedArea=allowedAreas)

        self.opened = True
        self.initUI()

    def initUI(self):
        """Initializes the UI"""

        # layout
        self.setLayout(QtGui.QVBoxLayout())

        # add main widget
        self.mainWidget = RigManagerMainWidget()
        self.layout().addWidget(self.mainWidget)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.show()

    def closeEvent(self, event):
        """Override of the close event to delete the dock control.

        Args:
            event (event): Close envent.
        """
        self.opened = False
        cmds.deleteUI(self.dockCtrl)


class RigManagerMainWidget(QtGui.QWidget):
    """Main Widget

    Attributes:
        header_labels (list od str): List of strings to use as labels for solution trees widget.
        solution_channel_box_layout (QGridLayout): Layout to include the channel box for this solution
        solution_description (QLabel): For showing the solution description.
        solution_manager (SolutionManager): Solution Manager Class Instance.
        solution_trees (QTreeWidget): Tree UI control to show the solutions.
        solution_widget_layout (QGridLayout): Layout to include each solution widget.
        solutionAnimIcon (QIcon): Icon for the UI.
        solutionDeformIcon (QIcon): Icon for the UI.
        solutionExportIcon (QIcon): Icon for the UI.
        solutionFitIcon (QIcon): Icon for the UI.
        solutionImportIcon (QIcon): Icon for the UI.
        solutionNewIcon (QIcon): Icon for the UI.
        solutionRemoveIcon (QIcon): Icon for the UI.
        tab_solutions_spliter (QSplitter): UI splitter.
        ui (Widget): The UI widget from the ui file.

    Deleted Attributes:
        solutions_buttons_layout (QHBoxLayout): Buttons Layout.
    """
    def __init__(self, parent=None):
        """Initializes the Widget

        Args:
            parent (Widget, optional): Parent widget.
        """
        super(RigManagerMainWidget, self).__init__(parent)

        self._editing_selection = False

        self.solution_manager = solutions.SolutionManager()

        self.initUI()

    def initUI(self):
        """Initializes the widget UI"""

        # Color vars

        # Icons

        self.solutionNewIcon = icons.getIconByName("solutionNew_16x16.png")
        self.solutionRemoveIcon = icons.getIconByName("solutionRemove_16x16.png")

        self.solutionFitIcon = self.solution_manager.get_solution_goal_icon("fit")
        self.solutionDeformIcon = self.solution_manager.get_solution_goal_icon("deform")
        self.solutionAnimIcon = self.solution_manager.get_solution_goal_icon("anim")

        self.solutionImportIcon = icons.getIconByName("solutionImport_16x16.png")
        self.solutionExportIcon = icons.getIconByName("solutionExport_16x16.png")

        # Load UI file

        self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

        # Layout

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # Solutions UI init

        self.tab_solutions_spliter = ui.get_child(self.ui, "sp_splitter")
        self.tab_solutions_spliter.setSizes([400, 250])

        ui.get_child(self.ui, "pb_solutions_new").setIcon(self.solutionNewIcon)
        ui.get_child(self.ui, "pb_solutions_delete").setIcon(self.solutionRemoveIcon)

        ui.get_child(self.ui, "pb_solutions_fit").setIcon(self.solutionFitIcon)
        ui.get_child(self.ui, "pb_solutions_deform").setIcon(self.solutionDeformIcon)
        ui.get_child(self.ui, "pb_solutions_anim").setIcon(self.solutionAnimIcon)

        ui.get_child(self.ui, "pb_solutions_import_preset").setIcon(self.solutionImportIcon)
        ui.get_child(self.ui, "pb_solutions_export_preset").setIcon(self.solutionExportIcon)

        self.solution_trees = ui.get_child(self.ui, "tr_solutions")

        self.header_labels = ["Name"] + self.solution_manager.get_solution_goals()
        self.solution_trees.setColumnCount(len(self.header_labels))
        self.solution_trees.setHeaderLabels(self.header_labels)
        # self.solution_trees.setColumnHidden(2, True)
        # self.solution_trees.setColumnWidth(0,200)
        self.solution_trees.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.solution_description = ui.get_child(self.ui, "lb_solution_desc")
        self.solution_widget_layout = ui.get_child(self.ui, "wi_solution_widget").layout()
        self.solution_channel_box_layout = ui.get_child(self.ui, "wi_channel_box").layout()

        # Fills the solution trees in the UI
        self.fill_solution_trees()

        # Solutions UI signals

        # self.solution_trees.itemSelectionChanged.connect(self.fix_solution_trees_selection)
        self.solution_trees.itemSelectionChanged.connect(self.select_solutions_nodes)
        self.solution_trees.itemSelectionChanged.connect(self.load_selected_solution_ui)

        self.solution_trees.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.solution_trees.customContextMenuRequested.connect(self.solution_trees_menu)

    def get_tree_item_level(self, item):
        """Returns the level of depth of an item in the tree.

        Args:
            item (QTreeWidgetItem): Item to get the level of depth from.

        Returns:
            int: Returns the level of depth from the given item in the tree.
        """
        level = -1

        while item:
            level += 1
            item = item.parent()

        return level

    def get_solution_trees_selected_items(self):
        """Gets all selected items in the solution trees.

        Returns:
            List of QTreeWidgetItem: Returns selected items in the solution trees.
        """
        # Gets the selected indexes
        sel_indexes = self.solution_trees.selectedIndexes()

        if not sel_indexes:
            return []
        else:
            # Collects all items related with selected indexes and returns them in an unique list.
            sel_items = []

            for index in sel_indexes:
                sel_items.append(self.solution_trees.itemFromIndex(index))

            sel_items = list(set(sel_items))

            return sel_items

    def solution_trees_menu(self, position):
        """Creates and shows a right click menu with actions to do with the solutions selected.

        Args:
            position (QPoint): To know where to show the menu in the UI.
        """
        # Creates the main menu
        menu = QtGui.QMenu(self.solution_trees)

        # Gets the selected indexes of the tree elements. This way the menu can be different depending on the selection.
        sel_items = self.get_solution_trees_selected_items()

        # If a solution is selected in the tree, try to get the correspondent in the solutions instance tree.
        selected_solution = None
        if len(sel_items) == 1:
            selected_solution = self.solution_manager.get_solution_from_ui_object(sel_items[0])

        # CREATE NEW SOLUTIONS #########################################

        # If nothing selected or one element selected, new solutions can be created.
        if not sel_items or len(sel_items) == 1:

            # New solutions sub-menu
            new_solution_menu = QtGui.QMenu("New Solution")

            # Create sub-menus for creating solution taking in count allowed children types and subtypes.
            allowed_children = self.solution_manager.get_allowed_children(selected_solution)

            for allowed_type, allowed_subtypes in allowed_children.iteritems():
                # Creates the type of solutions menu.
                type_menu = QtGui.QMenu(allowed_type)

                # For each subtype, it adds an action to the type menu.
                for allowed_subtype in allowed_subtypes:
                    new_action = QtGui.QAction(self)
                    new_action.setText(allowed_subtype)
                    new_action.triggered.connect(
                        lambda type=allowed_type, subtype=allowed_subtype, parent=selected_solution:
                        self.menu_action_execution(action="create_solution", type=type, subtype=subtype, parent=parent))
                    type_menu.addAction(new_action)

                # Adds the type of solutions menu to the new solutions menu.
                new_solution_menu.addMenu(type_menu)

            # Adds the new solutions menu to the main one.
            menu.addMenu(new_solution_menu)

        # CREATE NEW SOLUTIONS END #####################################

        # SINGLE SELECTED SOLTUTION OPERATIONS #########################

        if len(sel_items) == 1:
            # Adds a separator for the operations
            menu.addSeparator()

            # Loops different goals and add the build and remove operations.
            for goal in selected_solution.goals:
                if selected_solution.validate_build(goal) or selected_solution.validate_remove(goal):
                    # Creates the goal menu.
                    goal_menu = QtGui.QMenu(goal)

                    # If can be created (only if is not created yet and same goal parent solution is already done)
                    if selected_solution.validate_build(goal):
                        new_action = QtGui.QAction(self)
                        new_action.setText("Build")
                        new_action.triggered.connect(
                            lambda solution=selected_solution, goal=goal:
                            self.menu_action_execution(action="build_solution_goal", solution=solution, goal=goal))
                        goal_menu.addAction(new_action)

                    # If it is created, can be removed.
                    if selected_solution.validate_remove(goal):
                        new_action = QtGui.QAction(self)
                        new_action.setText("Remove")
                        new_action.triggered.connect(
                            lambda solution=selected_solution, goal=goal:
                            self.menu_action_execution(action="remove_solution_goal", solution=solution, goal=goal))
                        goal_menu.addAction(new_action)

                    # If it is created, can be conformed.
                    if selected_solution.validate_conform(goal):
                        new_action = QtGui.QAction(self)
                        new_action.setText("Conform")
                        new_action.triggered.connect(
                            lambda solution=selected_solution, goal=goal:
                            self.menu_action_execution(action="conform_solution_goal", solution=solution, goal=goal))
                        goal_menu.addAction(new_action)

                    # Adds the goal menu to the new solutions menu.
                    menu.addMenu(goal_menu)

        # SINGLE SELECTED SOLTUTION OPERATIONS END #####################

        # MULTIPLE SELECTED SOLTUTIONS OPERATIONS ######################

        if sel_items:
            # Adds a separator for the operations
            menu.addSeparator()

            # Gets the solution instances correspondent to the selected items in the tree.
            selected_solutions = [self.solution_manager.get_solution_from_ui_object(item) for item in sel_items]

            # Action to remove solutions.
            new_action = QtGui.QAction(self)
            new_action.setText("Remove Solution")
            new_action.triggered.connect(
                lambda solutions=selected_solutions:
                self.menu_action_execution(action="remove_solution", solutions=solutions))
            menu.addAction(new_action)

        # MULTIPLE SELECTED SOLTUTIONS OPERATIONS END ##################

        # Shows the menu
        menu.exec_(self.solution_trees.viewport().mapToGlobal(position))

    def menu_action_execution(self, **kwargs):
        """Executes all kind of actions from the right click menu.

        Args:
            **kwargs: Arguments for the actions.
        """

        # Creates new solutions
        if kwargs["action"] == "create_solution":

            # Solution parameters
            stype = kwargs["type"]
            ssubtype = kwargs["subtype"]
            parent = kwargs["parent"]
            ui_object = parent.ui_object if parent else None

            # Cretes the solution and adds it to the ui tree.
            solution_instance = self.solution_manager.create_solution(stype, ssubtype, parent=parent)
            self.add_solution_to_tree(solution_instance, parent_tree_node=ui_object)
            self.load_selected_solution_ui()

        # Creates solutions goals
        if kwargs["action"] == "build_solution_goal":
            solution_instance = kwargs["solution"]
            goal = kwargs["goal"]
            solution_instance.build(goal)
            self.update_solution_icons(solution_instance, recursive=True)
            self.load_selected_solution_ui()

        # Removes solutions goals
        if kwargs["action"] == "remove_solution_goal":
            solution_instance = kwargs["solution"]
            goal = kwargs["goal"]
            solution_instance.remove(goal)
            self.update_solution_icons(solution_instance, recursive=True)
            self.load_selected_solution_ui()

        # Conforms solutions goals
        if kwargs["action"] == "conform_solution_goal":
            solution_instance = kwargs["solution"]
            goal = kwargs["goal"]
            solution_instance.conform(goal)

        # Removes solutions
        if kwargs["action"] == "remove_solution":
            remove_solutions = kwargs["solutions"]
            for solution_instance in remove_solutions:
                self.remove_solution_from_tree(solution_instance)
                self.solution_manager.remove_solution(solution_instance)
            self.load_selected_solution_ui()

    def select_solutions_nodes(self):
        """Selects the selected solution selectable nodes. Usually only the fit master"""
        sel_items = self.get_solution_trees_selected_items()

        pm.select(clear=True)

        # For each solution, it selects the selectable representants
        if sel_items:
            for sel_item in sel_items:
                selected_solution = self.solution_manager.get_solution_from_ui_object(sel_item)
                if selected_solution:
                    pm.select(selected_solution.get_selectable_nodes(), add=True)

    # def fix_solution_trees_selection(self):
        # """Updates the tree selection to only allow select items in the same level."""
        # if not self._editing_selection:
        #     self._editing_selection = True
        #     last_selected_level = 0

        #     sel_items = self.solution_trees.selectedItems()
        #     if len(sel_items) > 1:
        #         last_selected = sel_items[len(sel_items) - 1]
        #         last_selected_level = self.get_tree_item_level(last_selected)

        #         for sel_item in sel_items:
        #             level = self.get_tree_item_level(sel_item)
        #             if level != last_selected_level:
        #                 sel_item.setSelected(False)

        #     self._editing_selection = False

        # # Selects the solutions nodes in the scene.
        # self.select_solutions_nodes()

    def clear_solution_ui(self):
        """Clears the layout where solution widgets are included."""

        while self.solution_widget_layout.count():
            self.solution_widget_layout.takeAt(0).widget().setParent(None)

        while self.solution_channel_box_layout.count():
            self.solution_channel_box_layout.takeAt(0).widget().setParent(None)

    def load_selected_solution_ui(self):
        """Includes the selected solution widget in the layout, the description and custom channel box."""
        # Clears the solution description label.
        self.solution_description.setText("")

        # Clears the space for the current selected solution layout. Remove the current widget in the interface.
        self.clear_solution_ui()

        # Gets the selected indexes of the tree elements. This way the menu can be different depending on the selection.
        sel_items = self.get_solution_trees_selected_items()

        # If a solution is selected in the tree, try to get the correspondent in the solutions instance tree.
        selected_solution = None
        if len(sel_items) == 1:
            selected_solution = self.solution_manager.get_solution_from_ui_object(sel_items[0])

        # Adds the widget to the ui and the description.
        if selected_solution:
            # Sets the description.
            self.solution_description.setText(selected_solution.description)

            # Sets the widget.
            solution_widget = selected_solution.get_ui(reset=True)
            self.solution_widget_layout.addWidget(solution_widget)

            # Sets the channel box.
            pm.select(clear=True)
            pm.select(selected_solution.get_channel_box_nodes())
            solution_channel_box = selected_solution.get_channel_box(reset=True)
            self.solution_channel_box_layout.addWidget(utils.mayaWindowToPySideWidget(solution_channel_box))

    def fill_solution_trees(self):
        """Fills the solution trees UI with the solutions trees"""

        self.solution_manager.fill_solution_trees()

        # Clears the current UI tree.
        self.solution_trees.clear()

        # Fills the tree with the current solutions
        for solution_root in self.solution_manager.solution_trees:
            self.add_solution_to_tree(solution_root)

    def add_solution_to_tree(self, solution_instance, parent_tree_node=None):
        """Adds the given solution instance to the tree.

        Args:
            solution_instance (Solution Instance): Solution Instance to add to the tree.
            parent_tree_node (QTreeWidgetItem, optional): Parent UI object of the new solution in the UI tree.
        """

        # New item for tree creation
        if not parent_tree_node:
            # If there is no parent it means that is a root solution.
            item = QtGui.QTreeWidgetItem(self.solution_trees, [solution_instance.name(), "", "", ""])
        else:
            # If there is parent it means that must be inserted as one of its children.
            # Calculates the index to insert the solution. See pass manager.
            # Inserts the child.
            item = QtGui.QTreeWidgetItem(None, [solution_instance.name(), "", "", ""])
            insert_index = solution_instance.get_index_in_brothers()
            parent_tree_node.insertChild(insert_index, item)

        # Stores current item as the UI object for the solution.
        solution_instance.ui_object = item

        # Item properties modification.
        item.setSizeHint(0, QtCore.QSize(-1, 20))
        item.setExpanded(True)

        # Updates the icons for the solution ui object
        self.update_solution_icons(solution_instance)

        # If the solution has children solutions, it will fill the tree recursive.
        if len(solution_instance.children_solutions) > 0:
            for ch_solution_instance in solution_instance.children_solutions:
                self.add_solution_to_tree(ch_solution_instance, parent_tree_node=item)

    def remove_solution_from_tree(self, solution_instance):
        """Adds the given solution instance removes it from the tree.

        Args:
            solution_instance (Solution Instance): Solution Instance to remove from the tree.
        """
        # If the given solution has ui object, deletes it from the tree.
        if solution_instance.ui_object:
            if solution_instance.parent_solution and solution_instance.parent_solution.ui_object:
                index = solution_instance.parent_solution.ui_object.indexOfChild(solution_instance.ui_object)
                solution_instance.parent_solution.ui_object.takeChild(index)
            else:
                index = self.solution_trees.indexOfTopLevelItem(solution_instance.ui_object)
                self.solution_trees.takeTopLevelItem(index)

    def update_solution_icons(self, solution_instance, recursive=False):
        """If solution instance is given and it has UI object, sets the icons.
            It sets the main icon for the solution and also one for each goal that is created.

        Args:
            solution_instance (Solution instance): Given solution to set the icon.
            recursive (bool, optional): Indicates if update the icons recursive in children solutions.
        """
        # If solution instance is given and it has UI object, sets the icons.
        if solution_instance:
            if solution_instance.ui_object:
                # Sets the main icon.
                solution_instance.ui_object.setIcon(0, solution_instance.icon)

                # For each goal type, sets the icon if that goal is created. Empty icon if not created.
                for index, key in enumerate(solution_instance.goals):
                    goal_icon = solution_instance.goals_icons[key] if solution_instance.is_goal_built(key) else QtGui.QIcon()
                    solution_instance.ui_object.setIcon(index+1, goal_icon)

                if recursive and solution_instance.children_solutions:
                    for child_solution in solution_instance.children_solutions:
                        self.update_solution_icons(child_solution, recursive=recursive)


def rigManagerRun():
    """Runs the tool."""

    utils.closeTool('rigManager', dock=True)
    dTool = RigManager()


def rigManagerClose():
    """Closes the tool."""
    utils.closeTool('rigManager', dock=True)

#######################################
# execution
if __name__ == "__main__":
    rigManagerRun()
