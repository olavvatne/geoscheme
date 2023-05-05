from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       edit,
                       QgsProcessingUtils,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterExpression,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing


class MergeToRegionAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    SIMPLIFY_TOLERANCE = 'SIMPLIFY_TOLERANCE'
    EXPRESSION = 'EXPRESSION'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return MergeToRegionAlgorithm()

    def name(self):
        return 'merge-to-region'

    def displayName(self):
        return self.tr('Merge to Region')

    def group(self):
        return self.tr('Geoscheme')

    def groupId(self):
        return 'geoscheme-merge-to-region'

    def shortHelpString(self):
        return self.tr("Merged filtered layer (by query) to region")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(QgsProcessingParameterExpression(
            self.EXPRESSION,
            self.tr('Expression')))

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIMPLIFY_TOLERANCE, 
                self.tr('Simplify tolerance'), 
                type=QgsProcessingParameterNumber.Double, 
                minValue=0, 
                maxValue=1.0, 
                defaultValue=0.5))
    
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback.pushInfo("Buffer")
        input_layer = QgsProcessingUtils.mapLayerFromString(parameters[self.INPUT], context)
        input_layer.setSubsetString(parameters[self.EXPRESSION])
        feedback.pushInfo(parameters[self.EXPRESSION])
        res = processing.run("native:buffer",
        {
            'INPUT': parameters[self.INPUT],
            'DISTANCE': 0.000001,
            'SEGMENTS': 1,
            'END_CAP_STYLE': 0,
            'JOIN_STYLE': 0, 
            'MITER_LIMIT': 2,
            'DISSOLVE': True,
            'OUTPUT': 'memory:'
        },
        context=context, feedback=feedback, is_child_algorithm=True)

        buffered = res['OUTPUT']
        feedback.pushInfo(buffered)

        feedback.pushInfo("Simplify")
        res2 = processing.run("native:simplifygeometries", 
        {
            'INPUT': buffered,
            'METHOD':2,
            'TOLERANCE':parameters[self.SIMPLIFY_TOLERANCE],
            'OUTPUT': parameters[self.OUTPUT]
        },
        context=context, feedback=feedback, is_child_algorithm=True)
        simplified = res2['OUTPUT']

        feedback.pushInfo(simplified)
        vl = QgsProcessingUtils.mapLayerFromString(simplified, context)
        with edit(vl):
            dpr = vl.dataProvider()
            fields = dpr.fields()
            field_index_list = []
            for f in fields:
                idx = dpr.fieldNameIndex(f.name())
                field_index_list.append(idx)
            dpr.deleteAttributes(field_index_list)
            vl.updateFields()
        return {self.OUTPUT: simplified}

