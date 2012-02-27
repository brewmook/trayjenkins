from PySide import QtGui

class QtGuiFactory(object):

    def QMenu(self, parentWidget):
        """
        @type parentWidget: PySide.QtGui.Widget
        """
        return QtGui.QMenu(parentWidget)
