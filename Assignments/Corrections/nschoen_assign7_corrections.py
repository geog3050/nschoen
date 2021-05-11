import os
import sys    
import arcpy
from arcpy import env   
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

##################################################################################################### 
# 100 Points Total
#
# Given a linear shapefile (roads) and a point shapefile representing facilities(schools),
# this function should generate either a time-based (1-,2-,3- minute) or road network distance-based (200-, 400-, 600-, .. -2000 meters)
# concentric service areas around facilities and save the results to a layer file on an output geodatabase.
# Although you are not required to map the result, make sure to check your output service layer feature.
# The service area polygons can be used to visualize the areas that do not have adequate coverage from the schools. 

# Each parameter is described below:

# inFacilities: The name of point shapefile (schools)     
# roads: The name of the roads shapefile
# workspace: The workspace folder where the shapefiles are located. 

# Below are suggested steps for your program. More code may be needed for exception handling
# and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. 
# 2- Check all possible cases where inputs can be in wrong type, different projections, etc. 
# 3- Create a geodatabase using arcpy and import all initial shapefiles into feature classes. All your processes and final output should be saved into the geodatabase you created. Therefore, set the workspace parameter to the geodatabase once it is created.
# 4- Using the roads linear feature class, create and build a network dataset. Check the Jupyter notebook shared on ICON,
#    which covers the basics of how to create and build a network dataset from scratch. 
# 5- Use arcpy's MakeServiceAreaLayer function in the link below:
#    https://pro.arcgis.com/en/pro-app/tool-reference/network-analyst/make-service-area-layer.htm
#    Specify the following options while creating the new service area layer. Please make sure to read all the parameters needed for the function. 
#       If you use "length" as impedance_attribute, you can calculate concentric service areas using 200, 400, 600, .. 2000 meters for break values.
#       Feel free to describe your own break values, however, make sure to include at least three of them. 
#       Generate the service area polygons as rings, so that anyone can easily visualize the coverage for any given location if needed.
#       Use overlapping polygons to determine the number of facilities (schools) that cover a given location.
#       Use hierarchy to speed up the time taken to create the polygons.
#       Use the following values for the other parameters:
#       "TRAVEL_FROM", "DETAILED_POLYS", "MERGE"
#################################################################################################################### 
def calculateNetworkServiceArea(inFacilities, roads, workspace):
    #allow overwrite table on
    arcpy.env.overwriteOutput = True    
    #set new workspace as the input workspace
    arcpy.env.workspace = workspace 
    #check that the projections of feature classes align
    spatial_ref1 = arcpy.Describe(inFacilities).spatialReference
    spatial_ref2 = arcpy.Describe(roads).spatialReference
    if spatial_ref1.name != spatial_ref2.name:
        print(inFacilities + " needs to be projected as " + roads + " to match the coordinate system of the clip feature class.")
        print(inFacilities + " is projected as " + spatial_ref1.name + " and " + roads + " is projected as " + spatial_ref2.name)
    else:
        print("The coordinate systems for both layers match.")    
    #check that the feature classes are the correct type
    #roads should be polyline shapefile
    #facilties (schools) should be a point file
    #use try to identify errors in the types of data  
    try:
        #use the describe function to determine the element data type
        desc_inFacilities = arcpy.Describe(inFacilities)
        desc_roads = arcpy.Describe(roads)
        if desc_inFacilities.shapeType != "Point":
            print("Error shapeType: ", inFacilities, "needs to be a point type!")
            sys.exit(1)
        if desc_roads.shapeType != "Polyline":
            print("Error shapeType: ", roads, "needs to be a polyline type!")
            sys.exit(1)     
        #define folder pathway
        folder = workspace
        #create geodatabase name
        out_name = "myGeodatabase.gdb"
        #Create a geodatabase using arcpy 
        arcpy.CreateFileGDB_management(folder, out_name)
        #pass input shapefiles into feature class in geodatabase
        inFeatures = inFacilities
        inFeatures2 = roads
        outLocation = "myGeodatabase.gdb"
        outLocation2 = "myGeodatabase.gdb"
        outFeatureClass = "inFacilities"
        outFeatureClass2 = "roads"
        #pass input facitilies into geodatabase
        arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, 
                                            outFeatureClass)
        #pass input roads into geodatabase
        arcpy.FeatureClassToFeatureClass_conversion(inFeatures2, outLocation2, 
                                            outFeatureClass2)
        #test for existence of the geodatabse
        if arcpy.Exists(myGeodatabase):
            #set workspace to user input geodatabase
            arcpy.env.workspace = myGeodatabase
            print("Environment workspace is set to: ", myGeodatabase)
        else:
            print("Workspace", myGeodatabase, "does not exist!")
            sys.exit(1)  
        #set variable for the road network
        roads_shp = folder + roads
        #describe the road shapefile 
        desc = arcpy.Describe(roads_shp)
        #check to make sure that network analysis extension is enabled
        arcpy.CheckOutExtension("network")
        #create new featuredataset
        arcpy.CreateFeatureDataset_management(arcpy.env.workspace, "featuredataset", desc.spatialReference)
        #copy features to the new dataset
        arcpy.CopyFeatures_management(roads_shp, "featuredataset/roads")
        #create network dataset in an exisiting feature dataset 
        arcpy.na.CreateNetworkDataset("featuredataset", "roads_ND", ["roads"])
        #constructs the network connectivity and also attribute information of a network dataset
        arcpy.BuildNetwork_na("featuredataset/roads_ND")
        #use make serivce area layer
        #define variables
        network = os.path.join(myGeodatabase, "inFacilities", "roads_ND")
        layer_name = "schoolRoadNetwork"
        impedance = "distanceAway"
        #set variables for 600, 1200, and 1800 meters
        #generate polygons as rings
        #use this function to set analysis properties of the netwrok service area and determine accessibility to schools based on roads
        result_object = arcpy.na.MakeServiceAreaLayer(network, layer_name,
                                    impedance, "TRAVEL_FROM", "200 400 600 800 1000 1200 1400 1600 1800 2000",
                                    "DETAILED_POLYS", "MERGE", "RINGS")
    
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')


