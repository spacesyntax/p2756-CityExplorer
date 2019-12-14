
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


from ..log import colour_scales, ranges, labels
ranges = [
    [0,0],
    [0, 0.2],
    [0.2, 0.4],
    [0.4, 0.6],
    [0.6, 0.8],
    [0.8, 1]
]
labels = ['0', '0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']

def applySymbologyFixedDivisions(layer, field):
    rangeList = []
    for i, range  in enumerate(ranges[field]):
        rangeList.append(makeSymbologyForRange(layer, range[0], ranges[1], '0', QColor("#0000ff")))

    rangeList.append(makeSymbologyForRange(layer, 0, 0.2, '0-0.2', QColor("#00ffff")))
    rangeList.append(makeSymbologyForRange(layer, 0.2, 0.4, '0.2-0.4', QColor("#00ff50")))
    rangeList.append(makeSymbologyForRange(layer, 0.4, 0.6, '0.4-0.6', QColor("#ffff00")))
    rangeList.append(makeSymbologyForRange(layer, 0.6, 0.8, '0.6-0.8', QColor("#ffa000")))
    rangeList.append(makeSymbologyForRange(layer, 0.8, 1, '0.8-1', QColor("#ff0000")))

    renderer = QgsGraduatedSymbolRendererV2(field, rangeList)
    for i in renderer.symbols():
        i.symbolLayer(0).setOutlineColor(QColor("#ffffff"))
        i.symbolLayer(0).setBorderWidth(0.000001)
        #i.symbolLayer(0).setOutputUnit(1)
    renderer.setMode(QgsGraduatedSymbolRendererV2.Custom)
    layer.setRendererV2(renderer)
    return renderer