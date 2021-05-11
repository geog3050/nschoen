import arcpy
import sys
import os
arcpy.env.overwriteOutput = True
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
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    #set workspace to input geodatabase
    arcpy.env.workspace = input_geodatabase
    #iterate through list of feature classes
    fcList = arcpy.ListFeatureClasses()
    #print each feature class in the feature list
    for fc in fcList:
        print(fc)
    #define variables for the spatial join
    target_features = fcPolyline
    join_features = fcPoint
    #describe the input feature classes
    desc1 = arcpy.Describe(fcPolyline)
    desc2 = arcpy.Describe(fcPoint)
    #ensure that the spatial reference systems are projected the same
    print(desc1.spatialReference.name, desc2.spatialReference.name)
    #define variables
    in_features = fcPoint
    near_features = fcPolyline    
    search_radius = "#"
    location = "LOCATION"
    angle = "NO_ANGLE"
    method = "GEODESIC"
    #use near analysis to calculate distance of facilites to nearest bike route
    arcpy.Near_analysis(in_features, near_features, search_radius, location, angle, method)
        
######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    #set workspace to input geodatabase
    arcpy.env.workspace = input_geodatabase
    #start search cursor to find nursing home values
    rows = arcpy.SearchCursor(workspace, fcPoint,
                              field = pointFieldName)
    #get values from nursing homes
    for row in rows:
        row.getValue(pointFieldValue)
    #define values for spatial analysis count
    points = fcPoint
    #define polygons for spatial analysis count
    polygons = fcPolygon
    #define the point field name for the analysis count
    pointID = pointFieldName
    #create an ouput field
    countField = os.path.join(workspace, "finalCounts")
    #calculate the frequency of the event
    expression = "recalc(!FREQUENCY!)"
    #create a code block to keep track of events
    block = """def recalc(freq):
        if freq > -1:
            return freq
        else:
            return 0"""
    #use spaital join analysis to keep track of points in the polygons
    arcpy.SpatialJoin_analysis(points, polygons, "in_memory/PointsInPolys")
    #case field will then return the count per unique ID field
    arcpy.Statistics_analysis ("in_memory/PointsInPolys", "in_memory/SS_PointsInPolys", [[pointID, "Count"]], pointID)
    #join the values to the new field
    arcpy.JoinField_management(polygons, pointID, "in_memory/SS_PointsInPolys", pointID, "FREQUENCY")
    #calculate the values for the new field
    arcpy.CalculateField_management(polygons, countField, expression, "PYTHON", block)
    #delete the old field
    arcpy.DeleteField_management(polygons, "FREQUENCY")    

######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    #set workspace to input geodatabase
    arcpy.env.workspace = workspace
    #extract disinct values of the attribute from point feature class and save to a lsit
    try:
        #set workspace to input geodatabase
        arcpy.env.workspace = workspace
        #look through the point feature specifically at the facility name
        vals = unique_values(fcPoint,pointFieldName)
        #print unique values
        print(vals)
    except Exception as e:
        print("Error: " + e.args[0])
    #iterate through list of values
    for values in vals:
        #rename values in the field with 13 characters and stripped of white spaces
        if fieldInfo.getFieldName(index) == "status":
            #create new field for the newly mangaged name
            arcpy.AddField_management(layer, "stat", "TEXT", "", "", "13", "", "NULLABLE", "NON_REQUIRED", "")
            #use the strip function to remove white spaces
            arcpy.CalculateField_management.strip(layer, "stat", "!status!", "PYTHON_9.3", "")
            #delete the old field
            arcpy.DeleteField_management(layer, "status")
    #define values for spatial analysis count
    points = fcPoint
    #define polygons for spatial analysis count
    polygons = fcPolygon
    #define the point field name for the analysis count
    pointID = pointFieldName
    #create an ouput field
    countField = layer
    #calculate the frequency of the event
    expression = "recalc(!FREQUENCY!)"
    #create a code block to keep track of events
    block = """def recalc(freq):
        if freq > -1:
            return freq
        else:
            return 0"""
    #use spaital join analysis to keep track of points in the polygons
    arcpy.SpatialJoin_analysis(points, polygons, "in_memory/PointsInPolys")
    #case field will then return the count per unique ID field
    arcpy.Statistics_analysis ("in_memory/PointsInPolys", "in_memory/SS_PointsInPolys", [[pointID, "Count"]], pointID)
    #join the values to the new field
    arcpy.JoinField_management(polygons, pointID, "in_memory/SS_PointsInPolys", pointID, "FREQUENCY")
    #calculate the values for the new field
    arcpy.CalculateField_management(polygons, countField, expression, "PYTHON", block)
    #delete the old field
    arcpy.DeleteField_management(polygons, "FREQUENCY")  
    

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')


