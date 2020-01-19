# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CityExplorer
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QFileDialog
# Initialize Qt resources from file resources.py
import resources
import csv


# Import the code for the DockWidget
from city_explorer_dockwidget import CityExplorerDockWidget
import os.path

from city_explorer_tools.apply_symbology import *
from city_explorer_tools.draw_histogram import *

class CityExplorer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CityExplorer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Nur-Sultan 2030 Masterplan Explorer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CityExplorer')
        self.toolbar.setObjectName(u'CityExplorer')

        #print "** INITIALIZING CityExplorer"

        self.pluginIsActive = False
        self.dockwidget = None

        self.iface = iface
        self.legend = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CityExplorer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CityExplorer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Nur-Sultan Explorer'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING CityExplorer"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        self.dockwidget.warning.disconnect(self.giveMessage)
        self.dockwidget.selectionChanged.disconnect(self.updateVisuals)
        self.legend.itemAdded.disconnect(self.dockwidget.updateLayers)
        self.legend.itemRemoved.disconnect(self.dockwidget.updateLayers)

        # disconnects from dockwidget
        self.dockwidget.cityCheckBox.stateChanged.disconnect(self.dockwidget.disable_cpscombo)
        self.dockwidget.buildCheckBox.stateChanged.disconnect(self.dockwidget.disable_kpicombo)
        self.dockwidget.strCheckBox.stateChanged.disconnect(self.dockwidget.disable_strcombo)
        self.dockwidget.cpscombo.currentIndexChanged.disconnect(self.dockwidget.updatekpicombo)
        self.dockwidget.kpicombo.currentIndexChanged.disconnect(self.dockwidget.updatemodecombo)

        self.dockwidget.vacantCheckBox.stateChanged.disconnect(self.dockwidget.make_plots_visible)
        self.dockwidget.transformCheckBox.stateChanged.disconnect(self.dockwidget.make_transform_idx_visible)

        self.dockwidget.districtsRadio.toggled.disconnect(self.updateCityChart)
        self.dockwidget.buildingsRadio.toggled.disconnect(self.updateBuildChart)
        self.dockwidget.streetsRadio.toggled.disconnect(self.updateStrChart)

        self.dockwidget.imageExport.clicked.disconnect(self.dockwidget.saveOutput)

        self.dockwidget.allRadio.clicked.disconnect(self.refreshChart)
        self.dockwidget.selectedRadio.clicked.disconnect(self.refreshChart)

        self.dockwidget.dataExport.clicked.disconnect(self.dockwidget.saveData)


        # signals to update combos based on selected indices (only city and building scales)

        self.dockwidget.modecombo.currentIndexChanged.disconnect(self.dockwidget.updatemodeinput)
        self.dockwidget.strcombo.currentIndexChanged.disconnect(self.dockwidget.updatestrinput)
        self.dockwidget.kpi2combo.currentIndexChanged.disconnect(self.dockwidget.updatekpi2combo)

        # info buttons
        self.dockwidget.cityInfo.clicked.connect(self.dockwidget.getCityInfo)
        self.dockwidget.strInfo.clicked.connect(self.dockwidget.getStreetInfo)
        self.dockwidget.buildInfo.clicked.connect(self.dockwidget.getBuildInfo)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD CityExplorer"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Nur-Sultan 2030 Masterplan Explorer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def giveMessage(self, message, level):
        # Gives warning according to message
        self.iface.messageBar().pushMessage("City Explorer: ", "%s" % (message), level, duration=5)
        return

    def updateVisuals(self, user_input1, user_input2, tier):

        ium_field = IUMField(user_input1, user_input2, tier)
        print 'col_name', ium_field.ium_column

        layer = None
        if tier == 1:
            layer = self.dockwidget.districts
        elif tier == 2:
            layer = self.dockwidget.buildings
        elif tier == 3:
            layer = self.dockwidget.streets

        # map visualisation
        if layer:
            applySymbologyFixedDivisions(layer, ium_field)
            layer.triggerRepaint()

        # update legend

        # update zoom only when specific districts are selected

        # update chart only if the tier matches

        if (tier == 1 and self.dockwidget.districtsRadio.isChecked()) or \
                (tier == 2 and self.dockwidget.buildingsRadio.isChecked()) or \
                (tier == 3 and self.dockwidget.streetsRadio.isChecked()):

            output_path, self.dockwidget.chart_data = drawHistogram(self.iface, layer, ium_field, self.dockwidget.getSelected())
            chart = QPixmap(output_path)
            chart = chart.scaled(300, 300, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            self.dockwidget.chartView.setPixmap(chart)

        return

    def updateCityChart(self):
        if self.dockwidget.districtsRadio.isChecked():
            layer = self.dockwidget.districts
            ium_field = IUMField(self.dockwidget.get_district_index(), '', 1)
            output_path, self.dockwidget.chart_data = drawHistogram(self.iface, layer, ium_field, self.dockwidget.getSelected())
            chart = QPixmap(output_path)
            chart = chart.scaled(300, 300, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            self.dockwidget.chartView.setPixmap(chart)
        return

    def updateStrChart(self):
        if self.dockwidget.streetsRadio.isChecked():
            layer = self.dockwidget.streets
            ium_field = IUMField(self.dockwidget.get_street_index(), '', 3)
            output_path, self.dockwidget.chart_data = drawHistogram(self.iface, layer, ium_field, self.dockwidget.getSelected())
            chart = QPixmap(output_path)
            chart = chart.scaled(300, 300, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            self.dockwidget.chartView.setPixmap(chart)
        return

    def updateBuildChart(self):
        if self.dockwidget.buildingsRadio.isChecked():
            layer = self.dockwidget.buildings
            if self.dockwidget.kpi2combo.isEnabled() and self.dockwidget.get_building2_index() != 'all':
                ium_field = IUMField(self.dockwidget.get_building2_index(), self.dockwidget.get_mode_time(), 2)
            else:
                ium_field = IUMField(self.dockwidget.get_building_index(), self.dockwidget.get_mode_time(), 2)
            output_path, self.dockwidget.chart_data = drawHistogram(self.iface, layer, ium_field, self.dockwidget.getSelected())
            chart = QPixmap(output_path)
            chart = chart.scaled(300, 300, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            self.dockwidget.chartView.setPixmap(chart)
        return

    def updateChart(self):
        if self.dockwidget.districtsRadio.isChecked():
            self.updateCityChart()
        elif self.dockwidget.streetsRadio.isChecked():
            self.updateStrChart()
        elif self.dockwidget.buildingsRadio.isChecked():
            self.updateBuildChart()
        return

    def refreshChart(self):
        print 'refresh'
        self.dockwidget.setSelected()
        self.updateChart()
        return

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING CityExplorer"

            self.legend = self.iface.legendInterface()

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = CityExplorerDockWidget(['city_scale', 'building_scale', 'street_scale', 'potential_plots', 'transformability_index',
                                                          'city_scale_summary_stats', 'building_scale_summary_stats', 'street_scale_summary_stats_nach', 'street_scale_summary_stats_int' ], self.legend, self.iface)

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # connects
            self.dockwidget.warning.connect(self.giveMessage)
            self.legend.itemAdded.connect(self.dockwidget.updateLayers)
            self.legend.itemRemoved.connect(self.dockwidget.updateLayers)
            self.dockwidget.selectionChanged.connect(self.updateVisuals)

            self.dockwidget.districtsRadio.setChecked(True)
            self.dockwidget.districtsRadio.toggled.connect(self.updateCityChart)
            self.dockwidget.buildingsRadio.toggled.connect(self.updateBuildChart)
            self.dockwidget.streetsRadio.toggled.connect(self.updateStrChart)

            self.dockwidget.allRadio.clicked.connect(self.refreshChart)
            self.dockwidget.selectedRadio.clicked.connect(self.refreshChart)

            self.dockwidget.dataExport.clicked.connect(self.dockwidget.saveData)

            # check layers on loading the widget
            self.dockwidget.layerCheck()

            # show the dockwidget
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
            self.updateCityChart()
