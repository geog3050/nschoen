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
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
#import python site package
import arcpy
#import os to interact with operating system
import os
def printFeatureClassNames(workspace):
    #define the workspace (user input)
    arcpy.env.workspace = workspace
    #create variable that is a lists of the feature classes in workspace
    fcList = arcpy.ListFeatureClasses()
    #create for loop to iterate through feature classes
    for fc in fcList:
        #create variable that describes type of feature class
        fcType = arcpy.Describe(fc)
    #print the feature class with structure type: 'xxxx is a xxxxx feature class'
    print(fcType.name[:-4]+" is a "+fcType.shapeType)
        
###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    #define the workspace (user input)
    arcpy.env.workspace = workspace    
    #create variable to describe shapetype
    desc_fc = arcpy.Describe(inputFc)    
    #create for loop to iterate through fields in the feature class
    for field in fields:
        #create if statements for all numerical data in dataset (float, double, integer, and small integer)
        #print attribute name and type for all numerical data attribute names in feature class
        if desc_fc.shapeType=="Float":
            print(field.name, field.type)
        if desc_fc.shapeType=="Double":
            print(field.name, field.type) 
        if desc_fc.shapeType=="Integer":
            print(field.name, field.type)
        if desc_fc.shapeType=="SmallInteger":
            print(field.name, field.type)

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    #define the workspace (user input)
    arcpy.env.workspace = input_geodatabase
    #create output folder path (same as input geodatabase workspace)
    outFolderPath = "C:\Users\nschoen\OneDrive - University of Iowa\Documents\ArcGIS\Projects\Assignment3"
    #create output geodatabase
    output_geodatabase = "output_geodatabase"
    #create new feature class to save outputs to using the path and defined output geodatabase
    newFc = arcpy.CreateFileGDB_management(outFolderPath, output_geodatabase)
    #create for loop to iterate through feature classes in the input geodatabase
    for fc in newFc:
        #create variable that describes type of feature class 
        fcType = arcpy.Describe(newFc)
        #create if statement for if the type matches the input shape type (only features that match the shapetype)
        if fcType == shapeType:
            #use os.path.join to concatenates various path components
            out_featureclass = os.path.join(workspace, os.path.splitext(newFc)[0])
            #use copyfeatures to copy features from input feature class to the new feature class
            arcpy.CopyFeatures_management(newFc, out_featureclass)            

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

######################################################################         
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    #define the workspace (user input)
    arcpy.env.workspace = workspace
    #use get count to count number of features in feature class
    startCount = arcpy.GetCount_management(inputFc)
    # arcpy.management.AddJoin(in_layer_or_view, in_field, join_table, join_field, {join_type})
    # in_layer_or_view = inputFc
    # in_field = idFieldInputFc
    # join_table = inputTable
    # join_field = idFieldTable
    # arcpy.management.AddJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, {})
    #use arcpy.management.addjoin to to join a layer to a table based on common features
    #use KEEP_COMMON to keep only matched records
    arcpy.management.AddJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, {KEEP_COMMON})
    #create feature class to saved joined data to
    featureClass = arcpy.management.CreateFeatureclass(workspace, "featureClass.shp")
    #copy the layer into the new feature class for permanenet saved data
    finalFc = arcpy.CopyFeatures_management(inputTable,featureClass)
    #use get count again to count records in the joined shapefile (kept only matching records)
    finalCount = arcpy.GetCount_management(finalFc)
    #print the results of the joined output to show how many records matched and unmatched in the join operation
    print(finalCount+" records matched out of "+startCount+" total records.")

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')