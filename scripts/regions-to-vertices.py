from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       edit,
                       QgsProcessingUtils,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing

filename = '/tmp/qgis.log'
def write_log_message(message, tag, level):
    with open(filename, 'a') as logfile:
        logfile.write('{tag}({level}): {message}'.format(tag=tag, level=level, message=message))

class RegionsToVerticesAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return RegionsToVerticesAlgorithm()

    def name(self):
        return 'regions-to-vertices'

    def displayName(self):
        return self.tr('Region to Vertices')

    def group(self):
        return self.tr('Geoscheme')

    def groupId(self):
        return 'geoscheme-regions-to-vertices'

    def shortHelpString(self):
        return self.tr("Merged regions to vertices.")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback.pushInfo("Buffer")
        res = processing.run("native:buffer",
        {
            'INPUT': parameters[self.INPUT],
            'DISTANCE': -0.5,
            'SEGMENTS': 1,
            'END_CAP_STYLE': 0,
            'JOIN_STYLE': 0, 'MITER_LIMIT': 2,
            'DISSOLVE': False,
            'OUTPUT': 'memory:'
        },
        context=context, feedback=feedback, is_child_algorithm=True)

        buffered = res['OUTPUT']
        feedback.pushInfo(buffered)

        feedback.pushInfo("Extract Vertices")
        res2 = processing.run("native:extractvertices",
        {
            'INPUT': buffered,
            'OUTPUT': parameters[self.OUTPUT]
        },
        context=context, feedback=feedback, is_child_algorithm=True)
        vertices = res2['OUTPUT']

        feedback.pushInfo(vertices)
        vl = QgsProcessingUtils.mapLayerFromString(vertices, context)
        with edit(vl):
            dpr = vl.dataProvider()
            fields = dpr.fields()
            field_index_list = []
            for f in fields:
                if f.name() != "REGION":
                    idx = dpr.fieldNameIndex(f.name())
                    field_index_list.append(idx)
            dpr.deleteAttributes(field_index_list)
            vl.updateFields()
        return {self.OUTPUT: vertices}

