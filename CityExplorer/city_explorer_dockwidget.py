# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CityExplorerDockWidget
                                 A QGIS plugin
 QGIS plugin to visualise IUM Baseline measures
                             -------------------
        begin                : 2019-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Space Syntax Limited
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
import shutil
import csv

from info_log import *

from qgis.gui import QgsMessageBar
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal, QSize, Qt

from city_explorer_tools.utility_functions import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'city_explorer_dockwidget_base.ui'))


class CityExplorerDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    warning = pyqtSignal(str, int)
    selectionChanged = pyqtSignal(str, str, int)

    def __init__(self, layers, legend, iface, parent=None):
        """Constructor."""
        super(CityExplorerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.layers = layers
        self.iface = iface
        self.districts = getLayerByName(self.layers[0])
        self.buildings = getLayerByName(self.layers[1])
        self.streets = getLayerByName(self.layers[2])
        self.plots = getLayerByName(self.layers[3])
        self.tranform_idx = getLayerByName(self.layers[4])
        self.legend = legend
        self.districts_statistics = getLayerByName(self.layers[5])
        self.buildings_statistics = getLayerByName(self.layers[6])
        self.streets_statistics = getLayerByName(self.layers[7])

        self.chart_data = None

        # setup info icons on pushbuttons
        info_icon = QtGui.QPixmap(os.path.dirname(__file__) + "/raster/info_icon.png")

        for icon in [self.cityInfo, self.buildInfo, self.strInfo, self.vacantInfo, self.transformInfo]:
            icon.setIcon(QtGui.QIcon(info_icon))
            icon.setIconSize(QSize(18, 18))

        logo = QtGui.QPixmap(os.path.dirname(__file__) + '/raster/Space_Syntax_logo.png')
        logo = logo.scaled(100, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(logo)

        self.settings = []

        # add items to combos
        self.cpscombo.clear()
        kpi_list = [i +" index" for i in tier2.keys()]
        self.cpscombo.addItems(kpi_list)
        self.updatekpicombo()
        self.updatemodecombo()
        self.strcombo.addItems(streets)

        # enable only city index
        self.cityCheckBox.setChecked(True)
        self.districtsRadio.setChecked(True)
        self.allRadio.setChecked(True)
        self.buildCheckBox.setChecked(True)
        self.strCheckBox.setChecked(True)

        # signals to disable/enable layers
        self.cityCheckBox.stateChanged.connect(self.disable_cpscombo)
        self.buildCheckBox.stateChanged.connect(self.disable_kpicombo)
        self.strCheckBox.stateChanged.connect(self.disable_strcombo)

        # disable kpi & str combo - the signal needs the state to be changed to be called
        self.disable_kpicombo()
        self.disable_strcombo()
        self.kpi2combo.setDisabled(True)

        # signals to update combos based on selected indices (only city and building scales)
        # & to emit user input selection
        self.cpscombo.currentIndexChanged.connect(self.updatekpicombo)
        self.kpicombo.currentIndexChanged.connect(self.updatemodecombo)
        self.modecombo.currentIndexChanged.connect(self.updatemodeinput)
        self.strcombo.currentIndexChanged.connect(self.updatestrinput)
        self.kpi2combo.currentIndexChanged.connect(self.updatekpi2combo)

        # visualise additional layers
        self.vacantCheckBox.stateChanged.connect(self.make_plots_visible)
        self.transformCheckBox.stateChanged.connect(self.make_transform_idx_visible)

        # exports
        self.imageExport.clicked.connect(self.saveOutput)

        # info buttons
        self.cityInfo.clicked.connect(self.getCityInfo)
        self.strInfo.clicked.connect(self.getStreetInfo)
        self.buildInfo.clicked.connect(self.getBuildInfo)

    def updatekpicombo(self):
        #self.kpicombo.blockSignals(True)
        self.kpicombo.clear()
        kpi_list = tier2[self.cpscombo.currentText()[:-6]]
        kpi_list = ['Access to '+i if i not in ['Walkability', 'Vibrancy', 'Car dependence', 'Energy consumption'] else i for i in kpi_list]
        self.kpicombo.addItems(kpi_list) # remove word index

        #self.kpicombo.blockSignals(False)

        self.kpi2combo.blockSignals(True)
        self.kpi2combo.clear()
        try:
            self.kpi2combo.addItems(tier3[self.kpicombo.currentText()])
            if self.buildCheckBox.isChecked():
                self.kpi2combo.setDisabled(False)
            else:
                self.kpi2combo.setDisabled(True)
        except KeyError:
            self.kpi2combo.setDisabled(True)
        self.kpi2combo.blockSignals(False)

        # when cps combo changed
        user_input = self.get_district_index()

        if user_input:
            #print 'bef_emit_cps', (user_input, '', 1)
            self.selectionChanged.emit(user_input, '', 1)
        return

    def updatemodecombo(self):
        # when kpi combo changed

        selected_kpi = self.kpicombo.currentText()
        if selected_kpi == '':
            self.kpi2combo.setDisabled(True)
            return

        self.modecombo.blockSignals(True)
        self.modecombo.clear()
        try:
            self.modecombo.addItems(custom_modes[selected_kpi])
        except KeyError:
            self.modecombo.addItems(default_modes)
        self.modecombo.blockSignals(False)

        self.kpi2combo.blockSignals(True)
        self.kpi2combo.clear()
        try:
            self.kpi2combo.addItems(tier3[self.kpicombo.currentText()])
            if self.buildCheckBox.isChecked():
                self.kpi2combo.setDisabled(False)
            else:
                self.kpi2combo.setDisabled(True)
        except KeyError:
            self.kpi2combo.setDisabled(True)
        self.kpi2combo.blockSignals(False)

        user_input = self.get_building_index(), self.get_mode_time()
        if user_input != (None, None):
            #print 'bef_emit_kpi', (user_input[0], user_input[1], 2)
            self.selectionChanged.emit(user_input[0], user_input[1], 2)

        return

    def updatekpi2combo(self):
        user_input = self.get_building2_index(), self.get_mode_time()
        if user_input != (None, None):
            if user_input[0] != 'all':
                #print 'bef_emit_kpi2', (user_input[0], user_input[1], 2)
                self.selectionChanged.emit(user_input[0], user_input[1], 2)
            else:
                #print 'bef_emit_kpi2', (self.get_building_index(), user_input[1], 2)
                self.selectionChanged.emit(self.get_building_index(), user_input[1], 2)

    def updatestrinput(self):
        user_input = self.get_street_index(), ''
        if user_input != (None, None):
            #print 'bef_emit_str' , (user_input[0], user_input[1], 3)
            self.selectionChanged.emit(user_input[0], user_input[1], 3)
        return

    def updatemodeinput(self):
        user_input = self.get_building_index(), self.get_mode_time()
        if user_input != (None, None):
            #print 'bef_emit_mode', (user_input[0], user_input[1], 2)
            self.selectionChanged.emit(user_input[0], user_input[1], 2)
        return

    def disable_cpscombo(self):
        if self.cityCheckBox.isChecked():
            self.cpscombo.setDisabled(False)
            self.legend.setLayerVisible(self.districts, True)
            #self.selectionChanged.emit(self.get_district_index(), '', 2)
        else:
            self.cpscombo.setDisabled(True)
            self.legend.setLayerVisible(self.districts, False)
        return

    def disable_kpicombo(self):
        if self.buildCheckBox.isChecked():
            #print 'build'
            self.kpicombo.setDisabled(False)
            if self.kpi2combo.count() == 0:
                self.kpi2combo.setDisabled(True)
            else:
                self.kpi2combo.setDisabled(False)
                #self.selectionChanged.emit(self.get_building_index(), self.get_mode_time(), 2)
            self.modecombo.setDisabled(False)
            self.legend.setLayerVisible(self.buildings, True)
        else:
            self.kpicombo.setDisabled(True)
            self.kpi2combo.setDisabled(True)
            self.modecombo.setDisabled(True)
            self.legend.setLayerVisible(self.buildings, False)
        return

    def disable_strcombo(self):
        if self.strCheckBox.isChecked():
            self.strcombo.setDisabled(False)
            self.legend.setLayerVisible(self.streets, True)
            #self.selectionChanged.emit(self.get_street_index(), '', 2)
        else:
            self.strcombo.setDisabled(True)
            self.legend.setLayerVisible(self.streets, False)
        return

    def get_district_index(self):
        return self.cpscombo.currentText()

    def get_building_index(self):
        return self.kpicombo.currentText()

    def get_building2_index(self):
        return self.kpi2combo.currentText()

    def get_street_index(self):
        return self.strcombo.currentText()

    def get_mode_time(self):
        return self.modecombo.currentText()

    def make_plots_visible(self):
        if self.plots is None and self.vacantCheckBox.isChecked():
            self.warning.emit('Missing plots layer.', 2)
        else:
            if self.vacantCheckBox.isChecked():
                self.legend.setLayerVisible(self.plots, True)
            else:
                self.legend.setLayerVisible(self.plots, False)
        return

    def make_transform_idx_visible(self):
        if self.tranform_idx is None and self.transformCheckBox.isChecked():
            self.warning.emit('Missing transformability index layer.', 2)
        else:
            if self.transformCheckBox.isChecked():
                self.legend.setLayerVisible(self.tranform_idx, True)
            else:
                self.legend.setLayerVisible(self.tranform_idx, False)
        return

    def layerCheck(self):
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
        #print 'layer added/ removed : update layers'
        self.districts = getLayerByName(self.layers[0])
        self.buildings = getLayerByName(self.layers[1])
        self.streets = getLayerByName(self.layers[2])
        self.layerCheck()
        return

    def saveOutput(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save image as ", "image", '*.png')
        # write png file to the specified location
        shutil.copyfile(os.path.dirname(__file__) + '/city_explorer_tools/foo.png', file_name)
        return

    def setSelected(self):
        if self.allRadio.isChecked():
            self.selectedRadio.blockSignals(True)
            self.selectedRadio.setChecked(False)
            self.selectedRadio.blockSignals(False)
        else:
            sel_features = 0
            layer = None
            if self.districtsRadio.isChecked():
                layer = self.districts
            elif self.streetsRadio.isChecked():
                layer = self.streets
            elif self.buildingsRadio.isChecked():
                layer = self.buildings
            for f in layer.selectedFeatures():
                sel_features += 1
                break

            if sel_features == 1:
                self.allRadio.blockSignals(True)
                self.allRadio.setChecked(False)
                self.allRadio.blockSignals(False)
            else:
                self.allRadio.blockSignals(True)
                self.allRadio.setChecked(True)
                self.allRadio.blockSignals(False)

                self.selectedRadio.blockSignals(True)
                self.selectedRadio.setChecked(False)
                self.selectedRadio.blockSignals(False)
                self.warning.emit('No features selected!', 2)
        return

    def getSelected(self):
        if self.allRadio.isChecked():
            return False
        else:
            return True

    def saveData(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save data as ", "data", '*.csv')
        with open(file_name, mode='w') as csv_file:
            fieldnames = ['ranges', 'percentage']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for k, v in self.chart_data.items():
                writer.writerow({'ranges': k, 'percentage': v})
        return

    def getCityInfo(self):
        info_text = info_buttons[self.cpscombo.currentText()[:-6]]
        self.showInfoPopUp(info_text)
        return

    def getStreetInfo(self):
        info_text = info_buttons[self.strcombo.currentText()]
        self.showInfoPopUp(info_text)
        return

    def getBuildInfo(self):
        info_text = info_buttons[self.kpicombo.currentText()]
        self.showInfoPopUp(info_text)
        return

    def getPlotInfo(self):
        info_text = info_buttons['potential plots']
        self.showInfoPopUp(info_text)
        return

    def getTransformInfo(self):
        info_text = info_buttons['transformability index']
        self.showInfoPopUp(info_text)
        return

    def showInfoPopUp(self, info_text):

        from PyQt4 import QtGui
        info = QtGui.QMessageBox.information(self.iface.mainWindow(), '', info_text)
        return

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
