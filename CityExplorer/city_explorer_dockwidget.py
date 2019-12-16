# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CityExplorerDockWidget
                                 A QGIS plugin
 QGIS plugin to visualise IUM Baseline measures
                             -------------------
        begin                : 2019-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Ioanna Kolovou
        email                : i.kolovou@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from log import *

from qgis.gui import QgsMessageBar
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal, QSize, Qt

from city_explorer_tools.utility_functions import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'city_explorer_dockwidget_base.ui'))


class CityExplorerDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    warning = pyqtSignal(str, int)
    selectionChanged = pyqtSignal(str, str, str, str)

    def __init__(self, layers, parent=None):
        """Constructor."""
        super(CityExplorerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.layers = layers
        self.districts = getLayerByName(self.layers[0])
        self.buildings = getLayerByName(self.layers[1])
        self.streets = getLayerByName(self.layers[2])

        # setup info icons on pushbuttons
        info_icon = QtGui.QPixmap(os.path.dirname(__file__) + "/raster/info_icon.png")
        self.cityInfo.setIcon(QtGui.QIcon(info_icon))
        self.cityInfo.setIconSize(QSize(18, 18))

        self.buildInfo.setIcon(QtGui.QIcon(info_icon))
        self.buildInfo.setIconSize(QSize(18, 18))

        self.strInfo.setIcon(QtGui.QIcon(info_icon))
        self.strInfo.setIconSize(QSize(18, 18))

        self.vacantInfo.setIcon(QtGui.QIcon(info_icon))
        self.vacantInfo.setIconSize(QSize(18, 18))

        self.transformInfo.setIcon(QtGui.QIcon(info_icon))
        self.transformInfo.setIconSize(QSize(18, 18))

        logo = QtGui.QPixmap(os.path.dirname(__file__) + '/raster/Space_Syntax_logo.png')
        logo = logo.scaled(100, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(logo)

        self.settings = []

        # add items to combos
        self.updatecpscombo()
        self.updatekpicombo()
        self.updatemodecombo()
        self.strcombo.addItems(streets)

        # enable only city index
        self.cityCheckBox.setChecked(True)
        self.buildCheckBox.setChecked(False)
        self.strCheckBox.setChecked(False)

        # signals to disable/enable layers
        self.cityCheckBox.stateChanged.connect(self.disable_cpscombo)
        self.buildCheckBox.stateChanged.connect(self.disable_kpicombo)
        self.strCheckBox.stateChanged.connect(self.disable_strcombo)

        # disable kpi & str combo - the signal needs the state to be changed to be called
        self.disable_kpicombo()
        self.disable_strcombo()

        # signals to update combos based on city indices
        self.cpscombo.currentIndexChanged.connect(self.updatekpicombo)
        self.kpicombo.currentIndexChanged.connect(self.updatemodecombo)

    def get_settings(self):

        # TODO get districts list
        # get vacant plots
        # get districts, streets, buildings, modes
        cps = self.get_district_index()
        kpi = self.get_building_index()
        mode = self.get_mode_time()
        street = self.get_street_index()
        return cps, kpi, mode, street

    def updatecpscombo(self):
        self.cpscombo.clear()
        kpi_list = kpis.keys()
        self.cpscombo.addItems(kpi_list[::-1])
        cps, kpi, mode, street = self.get_settings()
        self.selectionChanged.emit(cps, kpi, mode, street)
        return

    def updatekpicombo(self):
        self.kpicombo.clear()
        self.kpicombo.addItems(tier2[self.cpscombo.currentText()])
        cps, kpi, mode, street = self.get_settings()
        self.selectionChanged.emit(cps, kpi, mode, street)
        return

    def updatemodecombo(self):
        self.modecombo.clear()
        selected_kpi = self.kpicombo.currentText()
        if selected_kpi == '':
            return
        self.modecombo.addItems(modes[selected_kpi])
        cps, kpi, mode, street = self.get_settings()
        self.selectionChanged.emit(cps, kpi, mode, street)
        return

    def disable_cpscombo(self):
        if self.cityCheckBox.isChecked():
            self.cpscombo.setDisabled(False)
        else:
            self.cpscombo.setDisabled(True)
        return

    def disable_kpicombo(self):
        if self.buildCheckBox.isChecked():
            print 'build'
            self.kpicombo.setDisabled(False)
            self.modecombo.setDisabled(False)
        else:
            self.kpicombo.setDisabled(True)
            self.modecombo.setDisabled(True)
        return

    def disable_strcombo(self):
        if self.strCheckBox.isChecked():
            self.strcombo.setDisabled(False)
        else:
            self.strcombo.setDisabled(True)
        return

    def get_district_index(self):
        return self.cpscombo.currentText()

    def get_building_index(self):
        return self.kpicombo.currentText()

    def get_street_index(self):
        return self.strcombo.currentText()

    def get_mode_time(self):
        return self.modecombo.currentText()

    #TODO
    def get_districts(self):
        return

    def layerCheck(self):
        # TODO Disable buttons when layer not present
        missing_layers = []
        if self.districts is None:
            missing_layers.append('districts')
        if self.buildings is None:
            missing_layers.append('buildings')
        if self.streets is None:
            missing_layers.append('streets')
        if len(missing_layers) > 0:
            self.warning.emit('Missing layers: ' + ', '.join(missing_layers), 2)  # QgsMessageBar.CRITICAL
        return

    def updateLayers(self):
        print 'layer added/ removed : update layers'
        self.districts = getLayerByName(self.layers[0])
        self.buildings = getLayerByName(self.layers[1])
        self.streets = getLayerByName(self.layers[2])
        self.layerCheck()
        return

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()


