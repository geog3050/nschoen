#import packages
import arcpy
import sys
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
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcpolygon, attribute, geodatabase = "assignment2.gdb"):
    #create output file with the same name as existing file by overwriting it
    arcpy.env.overwriteOutput = True      
    #test for existence of data types
    if arcpy.Exists(geodatabase):
        #set workspace to user input geodatabase
        arcpy.env.workspace = geodatabase
        print("Environment workspace is set to: ", geodatabase)
    else:
        print("Workspace", geodatabase, "does not exist!")
        sys.exit(1)
    #use try to identify errors in the types of data  
    try:
        #use the describe function to determine the element data type
        desc_fcpolygon = arcpy.Describe(fcpolygon)
        if desc_fcpolygon.shapeType != "Polygon":
            print("Error shapeType: ", fcpolygon, "needs to be a polygon type!")
            sys.exit(1)
        print(desc1.spatialReference.name, desc2.spatialReference.name)      
    spatial_ref = arcpy.Describe(fcpolygon).spatialReference
    #identify input coordinate system unit of measurement
    if desc.spatialReference.linearUnitName != "miles":
        print("Error: coordinate system unit measurement needs to be in miles!")
    #if the spatial reference is unknown
    if spatial_ref.name == "Unknown":
        print("{} has an unknown spatial reference".format(fc))
    #if spatial reference is a geographic projection
    if spatial_ref.name == "WGS84" or "NAD83":
        print("{} has a geographic projection as spatial reference!".format(fc))
    # Otherwise, print out the feature class name and spatial reference
    else:
        print("{} : {}".format(fc, spatial_ref.name))
    #Calculate the area of each polygon in square miles and append to a new column
    arcpy.AddField_management(areaColumn, "density", "DOUBLE")
    #new field is equal to old field divided by the normalizing field
    arcpy.management.CalculateField(fcpolygon, "density_sqm", attribute/areaColumn,"PYTHON_9.3")      
    #Calculate area in square miles to new column
    arcpy.CalculateGeometryAttributes_management(areaColumn, [["density_sqm", "AREA_GEODESIC"]], "MILES_US")

###################################################################### 
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase = "assignment2.gdb"):
    #test for existence of data types
    if arcpy.Exists(geodatabase):
        #set workspace to user input geodatabase
        arcpy.env.workspace = geodatabase
        print("Environment workspace is set to: ", geodatabase)
    else:
        print("Workspace", geodatabase, "does not exist!")
        sys.exit(1)
        #use try to identify errors in the types of data  
    try:
        #use the describe function to determine the element data type
        desc_fcLine = arcpy.Describe(fcLine)
        desc_fcClipPolygon = arcpy.Describe(fcClipPolygon)
        if desc_fcLine.shapeType != "Polyline":
            print("Error shapeType: ", fcLine, "needs to be a polyline type!")
            sys.exit(1)
        if desc_fcClipPolygon.shapeType != "Polygon":
            print("Error name: ", fcClipPolygon, "needs to be a polygon type!")
            sys.exit(1)
    #Transform the projection of one to other if the line and polygon shapefiles have different projections
    if desc_fcLine.spatialReference.name != desc_fcClipPolygon.spatialReference.name:
            print("Coordinate system error: Spatial reference of", fcLine, "and", fcClipPolygon, "should be the same.")
            sys.exit(1)            
    #identify input coordinate system unit of measurement
    if desc.spatialReference.linearUnitName != "miles":
        print("Error: coordinate system unit measurement needs to be in miles!")
    #create output file with the same name as existing file by overwriting it
    arcpy.env.overwriteOutput = True
    #list feature classes
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
        print(fc)
    #define variables
    fcLine = river_network.shp
    fcClipPolygon = states.shp
    polygonIDFieldName = Iowa
    clipPolygonID = rivers
    #id or name field that could uniquely identify a feature in the polygon feature class
    arcpy.AddField_management(polygonIDFieldName, "geoid", "TEXT")
    #Create update cursor for feature class 
    with arcpy.da.UpdateCursor(fcClipPolygon, ["Field1", "geoid"]) as cursor:
        # update geoid using Field1
        for row in cursor:
            field1_list = row[0].split(", ")
            greater_list = field1_list[-1].split("> ")
            geoid_str = ""
            for item in greater_list:
                colon_list = item.split(":")
                geoid_str += colon_list[1]
            #print(geoid_str)
            row[1] = geoid_str
            cursor.updateRow(row)
    arcpy.AddField_management(polygonIDFieldName, "length", "DOUBLE")
    #select attributes
    arcpy.Select_analysis(fcLine, fcClipPolygon, clipPolygonID)
    #clips the linear feature class by the selected polygon boundary,
    arcpy.Clip_analysis(clipPolygonID, bufferOutput, clipPolygonID)
    #calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon
    arcpy.CalculateGeometryAttributes_management(polygonIDFieldName, [["length", "LENGTH_GEODESIC"]], "MILES_US")
 

######################################################################
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase = "assignment2.gdb"):
    #set workspace
    arcpy.env.workspace = geodatabase
    #create output file with the same name as existing file by overwriting it
    arcpy.env.overwriteOutput = True
    #Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
    unit = desc.spatialReference.linearUnitName
    if distanceUnit != unit:
        print("Error: ", fcPoint, "needs to be measured in ", unit)
    #If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
    if desc.spatialReference.linearUnitName == "degrees":
        totalCount = 0
        counts = []
        with arcpy.da.SearchCursor("fcPoint", ["Value", "Count"]) as cursor:
            for row in cursor:
                totalCount += row[1]
                counts.append([row[0], row[1]])
            for ele in counts:
                total = (ele[0], ele[1]/totalCount*area)
    #use spatial join to get features within an area and add count to field
    out_feature_class = arcpy.management.AddField(fcPoint, outFc, "SHORT")
    #buffer to get distance
    arcpy.analysis.Buffer(fcPoint, distance, out_feature_class, {distanceUnit})
        
                
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
