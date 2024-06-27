# Python Script: Merge Intersecting Lines
# Author: Chad Ramos
# This script tool merges input line features where they intersect (within a given search distance)
# based on the problem and solution at https://community.esri.com/t5/arcgis-pro-questions/how-to-merge-intersecting-line-segments/m-p/1066880
# This does not preserve any attribute data from the input features

# import modules
import arcpy
from arcpy import analysis
from arcpy import management


# set parameters
featureClass=arcpy.GetParameterAsText(0) #input feature layer
buffDist=arcpy.GetParameterAsText(1) #search distance for intersect
MergeIntLines=arcpy.GetParameterAsText(2) #output feature layer


####################################################
#set the environment overwrite to true so that we can rewrite the backup weekly
arcpy.env.overwriteOutput=True


####################################################
#Buffer input lines by search distance
arcpy.AddMessage("buffering input lines...")
buffDist1="{} feet".format(buffDist)
buff1=arcpy.analysis.Buffer(featureClass,"buff1.shp",buffDist1)

#Dissolve the buffer, no multipart and no unsplit
arcpy.AddMessage("dissolving buffer...")
buffDiss1=arcpy.Dissolve_management(buff1,"buffDiss1.shp","","","SINGLE_PART","DISSOLVE_LINES")


#add field and calculate ID
arcpy.AddMessage("adding ID field to dissolved buffer...")
oidField1=arcpy.Describe(buffDiss1).oidFieldName
arcpy.AddMessage(oidField1)
calculation='!{}!'.format(oidField1) #dont forget to add !! surrounding OID field name
arcpy.AddMessage("calc expression: {}".format(calculation))
arcpy.management.CalculateField(buffDiss1,'ID',calculation,"PYTHON3","",'LONG')

#spatial join and add ID back to lines
arcpy.AddMessage("creating spatial join...")
spatialJoin1=arcpy.analysis.SpatialJoin(featureClass,buffDiss1,"spatialJoin1.shp")


#dissolve spatial join on new ID field
arcpy.AddMessage("dissolving spatial join...")
arcpy.management.Dissolve(spatialJoin1,MergeIntLines,"ID","",True)

arcpy.AddMessage("complete")

