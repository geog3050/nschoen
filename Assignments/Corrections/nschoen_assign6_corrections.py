import arcpy
from arcpy import env
from arcpy.sa import *

###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Natalie Schoen", "nschoen"])

###################################################################### 
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    #Create folder for the data folder
    folder = geodatabase
    #Set the workspace as the folder
    arcpy.env.workspace = folder
    #create file in the geodatabase
    arcpy.CreateFileGDB_management(folder, geodatabase)
    #set new workspace as the geodatabase
    arcpy.env.workspace = geodatabase
    #set input table
    inTable = folder + csvFile
    #set output table
    outTable = "yearly"
    # Set the expression, with help from the AddFieldDelimiters function, to select the appropriate field delimiters for the data type
    expression = arcpy.AddFieldDelimiters(arcpy.env.workspace)
    #export table to new geodatabase
    arcpy.TableToTable_conversion(inTable, arcpy.env.workspace, outTable, expression) 

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    #set new workspace as the geodatabase
    arcpy.env.workspace = workspace
    #allow overwrite table on
    arcpy.env.overwriteOutput = True
    #Generate an input feature later using inTable
    yearly_points = "yearly_points"
    #Convert the projection of the input feature layer to match the coordinate system of the clip feature class.
    #create spaitial reference ID
    spatial_ref1 = arcpy.Describe(inTable).spatialReference
    spatial_ref2 = arcpy.Describe(inClipFc).spatialReference
    if spatial_ref1.name != spatial_ref2.name:
        print(inTable + " needs to be projected as " + spatial_ref2 + " to match the coordinate system of the clip feature class.")
    else:
        print("The coordinate systems for both layers match.")
    #create new point feature class based on lat long values
    # xField: The field that contains the longitude values
    # yField: The field that contains the latitude values    
    arcpy.management.XYTableToPoint(inTable, yearly_points, xField, yField)
    #Check and enable the spatial analyst extension for kriging
    try:
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            # raise a custom exception
            raise LicenseError
    except LicenseError:
        print("Spatial Analyst license is unavailable")
    from arcpy.sa import *
    #Use KrigingModelOrdinary function to interpolate
    #define the value field
    field = valueField
    outKriging = Kriging(yearly_points, field, '#', cellSize)
    #Save the output
    outKriging.save("valueField")
    #begin clipping code
    #clip the interpolated kriging raster
    #define input clipped feature directory
    inputClipped = folder + inClipFc
    #covert flipped features
    arcpy.FeatureClassToFeatureClass_conversion(inputClipped, 
                                                arcpy.env.workspace, 
                                                "inputClipped")
    #create variable to define the input
    descInput = arcpy.Describe("inputClipped")
    #create the boundaries for the clipped feature
    rectangle = str(descInput.extent.XMin) + " " + str(descInput.extent.YMin) + " " + str(descInput.extent.XMax) + " " + str(descInput.extent.YMax)
    print(rectangle)
    #use clip management to clip the interpolated feature to the clipped area
    arcpy.Clip_management("valueField", rectangle, "#", "#", "#", "ClippingGeometry", 
                          "MAINTAIN_EXTENT")
    outInt = Int("valueField")
    #Save the output 
    outInt.save("valueFieldCI")    
    

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')