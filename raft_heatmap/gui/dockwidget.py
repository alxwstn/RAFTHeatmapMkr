#! python3
"""Dockwidget for RAFT heatmap plugin."""

# standard
import os

from qgis.core import Qgis

# PyQGIS
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from raft_heatmap.toolbelt import PlgLogger

# project
from ..category_enum import PinCategories

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "dockwidget.ui"))


class RaftDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()
    csvSelected = pyqtSignal(str)
    heatMapDisplaySelected = pyqtSignal()
    pinDisplaySelected = pyqtSignal()
    pinsFiltered = pyqtSignal(list)

    def __init__(self, parent=None):
        """Constructor."""
        super(RaftDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.log = PlgLogger().log
        # Connect signals and slots
        # Qgis.PyQt.QgsFileWidget
        self.QgsFileWidget.fileChanged.connect(self.__signal_QgsFileWidget_fileChanged)
        # PyQt5.QtWidgets.QRadioButton
        self.showHeatMap.toggled.connect(self.__showHeatmap_toggled)
        self.pinConfigBox.setEnabled(False)
        self._checkboxes = {}  # key -> checkbox
        self._build_checkboxes()

    def _build_checkboxes(self):
        for cat in PinCategories:
            cb = QtWidgets.QCheckBox(cat.value, self)
            cb.setChecked(True)
            cb.stateChanged.connect(self.__filterPins_itemschanged)
            self.checkboxLayout.addWidget(cb)
            self._checkboxes[cat.name] = cb

    def selected_keys(self):
        return [key for key, cb in self._checkboxes.items() if cb.isChecked()]

    def reset_pin_categories(self):
        for cb in self._checkboxes.values():
            cb.setChecked(True)

    def reset_radio_buttons(self):
        self.showHeatMap.setChecked(False)
        self.showPins.setChecked(True)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def __signal_QgsFileWidget_fileChanged(self):
        if os.path.exists(self.QgsFileWidget.filePath()):
            self.csvSelected.emit(self.QgsFileWidget.filePath())
            # trigger fitlering when a new file is selected
            self.__filterPins_itemschanged()
            self.pinConfigBox.setEnabled(True)
        else:
            self.log(
                message="Selected file does not exist: {}".format(
                    self.QgsFileWidget.filePath()
                ),
                log_level=Qgis.MessageLevel.Warning,
                push=False,
            )
            self.pinConfigBox.setEnabled(False)
            self.csvSelected.emit(None)

        self.reset_pin_categories()
        self.reset_radio_buttons()

    def __showHeatmap_toggled(self):
        if self.showHeatMap.isChecked():
            self.heatMapDisplaySelected.emit()
        if self.showPins.isChecked():
            self.pinDisplaySelected.emit()

    def __filterPins_itemschanged(self):
        self.log(
            message="filtered pins fired: {}".format(self.selected_keys()),
            log_level=Qgis.MessageLevel.Info,
            push=False,
        )
        self.pinsFiltered.emit(self.selected_keys())
