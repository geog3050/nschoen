def calculateRoadSegmentsInPolygon(inputGeodatabase, featureClassA, featureClassB):
   #OBJECTIVE: calculate the total length of road segments in meters from featureClassB (a polyline feature class) in featureClassA (a polygon feature class)
   #import packages
   import arcpy
   import sys
   #create output file with the same name as existing file by overwriting it
   arcpy.env.overwriteOutput = True
   #set workspace to user input geodatabase
   arcpy.env.workspace = inputGeodatabase
   #add a new field to feature class B to keep track of how many line segments are in each polygon
   arcpy.AddField_management(featureClassB, "total_length", "DOUBLE")
   #define output for intersect analysis
   intersection = "B_Intersects_A"
   #calculate geometric intersection of features
   arcpy.Intersect_analysis([featureClassB, featureClassA], intersection)
   #calculate total length in meters in the intersected feature class
   arcpy.CalculateGeometryAttributes_management(intersection, [["total_length", "LENGTH_GEODESIC"]], "METERS")
   #calculate the summary stats for the field
   summary = arcpy.Statistics_analysis(featureClassB, intersection, "SUM", "total_length")