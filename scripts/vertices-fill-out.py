from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsVectorLayer,
                       QgsApplication,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing

filename = '/tmp/qgis.log'
def write_log_message(message, tag, level):
    with open(filename, 'a') as logfile:
        logfile.write('{tag}({level}): {message}'.format(tag=tag, level=level, message=message))

QgsApplication.messageLog().messageReceived.connect(write_log_message)


class FillOutAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FillOutAlgorithm()

    def name(self):
        return 'fill-out'

    def displayName(self):
        return self.tr('Expand')

    def group(self):
        return self.tr('Geoscheme')

    def groupId(self):
        return 'geoscheme-fill-out-regions'

    def shortHelpString(self):
        return self.tr("Takes vertices representation of regions and fills out empty space")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer'),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
      
        feedback.pushInfo("Voronoi Polygons")
        vl = QgsVectorLayer("Polygon", "temporary_points", "memory")
        res3 = processing.run("grass7:v.voronoi", 
        {
            'input':parameters[self.INPUT],
            '-l':False,'-t':False,
            'output':vl,
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER':-1,
            'GRASS_MIN_AREA_PARAMETER':0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER':0,'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':'',
            'GRASS_VECTOR_EXPORT_NOCAT':False}, context=context, feedback=feedback, is_child_algorithm=True)
       
      
        voronoi = res3['output']
        feedback.pushInfo(voronoi)
        feedback.pushInfo("Aggregate, grouped by region")
        res = processing.run("native:aggregate",
        {
            'INPUT': voronoi,
            'GROUP_BY':'"REGION"',
            'AGGREGATES':[
                {'aggregate': 'sum','delimiter': ',','input': '"fid"','length': 0,'name': 'fid','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},
                {'aggregate': 'sum','delimiter': ',','input': '"cat"','length': 0,'name': 'cat','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},
                {'aggregate': 'sum','delimiter': ',','input': '"REGION"','length': 0,'name': 'REGION','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'}],
            'OUTPUT': parameters[self.OUTPUT]
        })
        aggregate = res['OUTPUT']
        return {self.OUTPUT: aggregate}
