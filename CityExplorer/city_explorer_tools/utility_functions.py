
from qgis.core import  QgsMapLayerRegistry
import math


def getLayerByName(name):
    layer = None
    for i in QgsMapLayerRegistry.instance().mapLayers().values():
        if i.name() == name:
            layer = i
    return layer


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100