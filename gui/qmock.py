from PySide import QtGui


class QtGuiFactory(object):

    def QAction(self, text, parent, **kwargs):
        """
        @rtype: Pyside.QtGui.QAction
        """

    def QListWidgetItem(self, icon, name):
        """
        @type icon: PySide.QtGui.QIcon
        @type name: str
        """
        return QtGui.QListWidgetItem(icon, name)

    def QMenu(self, parentWidget):
        """
        @type parentWidget: PySide.QtGui.Widget
        """
        return QtGui.QMenu(parentWidget)
