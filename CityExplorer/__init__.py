# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CityExplorer
                                 A QGIS plugin
 QGIS plugin to visualise IUM Baseline measures 
                             -------------------
        begin                : 2019-11-14
        copyright            : (C) 2020 by Space Syntax Limited
        email                : i.kolovou@spacesyntax.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CityExplorer class from file CityExplorer.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .city_explorer import CityExplorer
    return CityExplorer(iface)
