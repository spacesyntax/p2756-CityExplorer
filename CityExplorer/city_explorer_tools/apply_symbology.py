
from qgis.core import QgsSymbolV2, QgsMarkerSymbolV2, QgsLineSymbolV2, QgsFillSymbolV2, QGis, QgsRendererRangeV2, QgsGraduatedSymbolRendererV2
from PyQt4.QtGui import *


def validatedDefaultSymbol(geometryType):
    symbol = QgsSymbolV2.defaultSymbol(geometryType)
    if symbol is None:
        if geometryType == QGis.Point:
            symbol = QgsMarkerSymbolV2()
        elif geometryType == QGis.Line:
            symbol = QgsLineSymbolV2()
        elif geometryType == QGis.Polygon:
            symbol = QgsFillSymbolV2()
    return symbol


def makeSymbologyForRange(layer, min, max, title, color):
    symbol = validatedDefaultSymbol(layer.geometryType())
    symbol.setColor(color)
    range = QgsRendererRangeV2(min, max, symbol, title)
    return range


# field is an IUMField class object
def applySymbologyFixedDivisions(layer, field):

    colors = field.get_colour_scale()
    ranges = field.get_values_ranges()
    labels = field.get_style_labels()
    column_name = field.ium_column
    #print colors, ranges, labels

    rangeList = []
    for i, range  in enumerate(ranges):
        rangeList.append(makeSymbologyForRange(layer, range[0], range[1], labels[i], QColor(colors[i])))
    renderer = QgsGraduatedSymbolRendererV2(column_name, rangeList)
    for i in renderer.symbols():
        i.symbolLayer(0).setOutlineColor(QColor("#ffffff"))
        try:
            i.symbolLayer(0).setBorderWidth(0.000001)
        except AttributeError: # if line layer
            pass
        #i.symbolLayer(0).setOutputUnit(1)
    renderer.setMode(QgsGraduatedSymbolRendererV2.Custom)
    layer.setRendererV2(renderer)
    return renderer