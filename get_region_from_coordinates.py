import shapefile



########### Example use of this code:

# path_to_shape_file = '/Users/nbw/Dropbox/CS_109_Project/crime_UNFORMATTED/nypp_16b/nypd_pres'
# regions_dict = generate_regions_to_points_dict(path_to_shape_file, "Precinct")
# get_region_from_latlong_and_shapefile(40.768814, -73.931085, regions_dict)
# #	--> returns 114






#################################################################################################
####### Inputs:
#######     - path to shapefile
#######		- name of the attribute we want as our name of each region
####### Returns:
#######		- dict mapping region names to shape polygons 

def generate_regions_to_points_dict(shapefile_path, region_attribute_name):
    sf = shapefile.Reader(shapefile_path)
    shapes = sf.shapes()
    records = sf.records()
    fields = sf.fields
    
    # Make sure region_attribute_name exists in the shapefile
    found = False
    for i in range(1, len(fields)):
        if fields[i][0] == region_attribute_name:
            attribute_key = i-1
            found = True
    if not found:
        print "Region attribute not found. Available attributes:"
        for i in range(1, len(fields)):
            print str(fields[i][0]) + "\t",
        return     

    
    regions_to_points_dict = {}
    for i in range(len(records)):
        regions_to_points_dict[records[i][attribute_key]] = shapes[i].points
    return regions_to_points_dict
 



#################################################################################################
####### Code from: http://www.ariel.com.au/a/python-point-int-poly.html
####### Inputs:
####### 	- x value
#######		- y value
#######		- polygon: list of (x,y) pairs corresponding to the perimeter/corners of a polygon
####### Returns: true if x,y is in the specified polygon

def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside




#################################################################################################
####### Inputs:
#######     - latitude
#######		- longitude 
#######     - regions_to_points_dict - keys are region names, values are lists of points outlining the region
#######								- see "generate_regions_to_points_dict" method to create one of these dicts
####### Returns:
#######		- region the latitude,longitude input falls inside 

def get_region_from_latlong_and_shapefile(latitude, longitude, regions_to_points_dict):
    for key in regions_to_points_dict.keys():
        if point_inside_polygon(longitude, latitude, regions_to_points_dict[key]):
            return key
    print "region not found"
    return



