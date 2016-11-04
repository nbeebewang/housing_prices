


####################################################################################
########  If you're not Nicasia, comment this out ##################################
####################################################################################
import sys
sys.path.append("/anaconda/lib/python2.7/site-packages")
####################################################################################



from urllib2 import urlopen
import requests 
import numpy as np 
import pandas as pd 
import string 
from bs4 import BeautifulSoup
import urllib
from pyzillow import pyzillow
import inspect


Nicasia_Zillow_ID = "X1-ZWz1figcd74yyz_73nhl"
MeiYin_Zillow_ID = 'X1-ZWz1fifootsb9n_6msnx'
Marina_Zillow_ID = "X1-ZWz19i20n69ukr_77v70"

###################################################################
########  Choose a zillow id from above to use ####################
###################################################################

zillow_id = Nicasia_Zillow_ID


####################################################################################
########  To save time, comment out all but the desired borough ####################
####################################################################################
bk = pd.read_csv("nyc_pluto_16v1/BK.csv")
bx = pd.read_csv("nyc_pluto_16v1/BX.csv")
mn = pd.read_csv("nyc_pluto_16v1/MN.csv")
qn = pd.read_csv("nyc_pluto_16v1/QN.csv")
si = pd.read_csv("nyc_pluto_16v1/SI.csv")
####################################################################################



### get all attributes that can be extracted

_, dictvals = inspect.getmembers(pyzillow.GetDeepSearchResults)[2]
dictvals = (str(dictvals))

zillow_attribute_keys = []
keys_as_list = dictvals.split("{")[2].split(",")
for elt in keys_as_list:
    keyname = elt.split("\'")[1] 
    if keyname[0] != "_":
        zillow_attribute_keys.append(keyname)
        


##################################################################
########  CHANGE THIS TO THE CORRECT BOROUGH  ####################
##################################################################

address_list = bk['Address'].values
zips = bk['ZipCode'].values
res_status = bk['UnitsRes'].values

##################################################################


column_names = zillow_attribute_keys


#############################################
########  Name the file  ####################
#############################################
f = open('thing.csv', 'w')
#############################################

for elt in column_names:
    f.write(elt + ",")
f.write("\n")



data = []
zillow_data = pyzillow.ZillowWrapper(Nicasia_Zillow_ID)


for i in range(len(address_list)): 
    
    # elt==elt removes all NaNs bc NaNs dont equal themselves but everything else should
    # also removing all values that dont start with a number (eg when only a street is provided in the address)
    # remove all rows for which res_status > 0
    if address_list[i] == address_list[i] and address_list[i][0].isdigit() and int(res_status[i]) > 0:
        address = address_list[i].replace(" ", "-")
    else:
        address = None

    if zips[i] == zips[i]:
        zipcode = str(int(zips[i]))
    else:
        zipcode = None 


    if address and zipcode:
        try:
            result =  zillow_data.get_deep_search_results(address, zipcode)
        except:
            pass

        if result:
            data = pyzillow.GetDeepSearchResults(result)
            for key in zillow_attribute_keys:
                mycode = "if data." + key + ":\n f.write(data." + key + " + ',') \nelse:\n f.write(',')"
                exec(mycode)
        f.write("\n")
    if i % 1000 == 0:
        print i

f.close()


