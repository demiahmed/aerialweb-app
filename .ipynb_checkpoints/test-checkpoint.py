#   <!-- <form action="{{ url_for('byAirport')}}" method="GET">
#     <select name="airport">
#     <option disabled selected value> -- select an Airport (Optional) -- </option>
#   {% for airport in airports %}
#   <option value="{{airport}}">{{airport}}</option>
#   {% endfor %}
#   </select>
# <div class="twocols">
#     <p>SizeX (m)</p>
#     <p><input type="number" step="1" name= 'xbnd' value="10000"></p>
#   </div> 
#   <p><input type="submit" value = 'Find'></p>
# </form> -->
user = 'demi12395' 
password = 'Sutd1234' 

def openDataFile1():
    import pandas as pd

    missing_values = [r"\N"]
    df = pd.read_csv(r'./data/airport-codes_csv.csv',na_values = missing_values)

    return df

def openDataFile2():
    import pandas as pd

    missing_values = [r"\N"]
    df = pd.read_csv(r'./data/airportDB.csv',na_values = missing_values)

    return df

def getAirportNamesasList():
    
    myData = openDataFile2()

    return list(myData['Name'])

def getCountryNamesasList():
    
    myData = openDataFile2()
    # #print(set(list(myData['Country'])))
    # return set(list(myData['Country']))
    cleanedCountries = [x for x in list(myData['Country']) if str(x) != 'nan']
    return sorted(set(cleanedCountries))

def getCodesByCountry(name):

    myData = openDataFile2()
    global flagCountry
    flagCountry = 1
    global countryName
    countryName = str(name)
    return list(myData.loc[myData['Country'] == str(name)]['IATA'])

def getCodesByAirport(name2):

    myData = openDataFile2()
    global flagAirport
    flagAirport = 1
    global airportName
    airportName = str(name2)

    mainDict = dict(zip(getAirportNamesasList(),myData['IATA']))
    return mainDict[str(name2)]

def getParseCoordinates(n1,n2):

    myData = openDataFile2()
    global flagCoordinates
    flagCoordinates = 1
    global coordinates
    coordinates = [[float(n1)],[float(n2)]]
    return 'Parsed {} {}'.format(coordinates[0],coordinates[1]) 

def queryByCountry(name):

    myData = openDataFile2()
    iatalist = list(myData.loc[myData['Country'] == str(name)]['IATA']) 

def getNameFromIATA(iatastr):
    myData = openDataFile2()
    mainDict = dict(zip(myData['IATA'],getAirportNamesasList()))

    if (len(iatastr)== 3):
        return mainDict[str(iatastr)]  
    else:
        return iatastr  

def getLatLonfromIATA(list,masterIATA,masterLat,masterLon):
    import numpy as np


    iatalat,iatalon,notthere = [],[],[]
    for key in list:
        if key in masterIATA:
            iatalon.append(masterLat[masterIATA.index(key)])
            iatalat.append(masterLon[masterIATA.index(key)])
        else : 
            notthere.append(key)


    latx,lony = [], []
    for i in range(0,len(list)):
        latx.append(iatalat[i])
        lony.append(iatalon[i])

    latx = np.asfarray(latx,float)
    lony = np.asfarray(lony,float)

    return latx,lony

def latLonBoxByWandH(lat,lon,ew_width,ns_height):
    import pygc

    lats, lons = [], []
    #distance in m, az (in deg), lat (in deg), long (in deg)

    res = pygc.great_circle(distance=ew_width/2, azimuth=90, latitude=lat, longitude=lon)
    lat, lon = res['latitude'], res['longitude']

    res = pygc.great_circle(distance=ns_height/2, azimuth=180, latitude=lat, longitude=lon)
    lat, lon = res['latitude'], res['longitude']
    lats.append(lat), lons.append(lon)

    res = pygc.great_circle(distance=ew_width, azimuth=270, latitude=lat, longitude=lon)
    lat, lon = res['latitude'], res['longitude']
    lats.append(lat), lons.append(lon)

    res = pygc.great_circle(distance=ns_height, azimuth=0, latitude=lat, longitude=lon)
    lat, lon = res['latitude'], res['longitude']
    lats.append(lat), lons.append(lon)

    res = pygc.great_circle(distance=ew_width, azimuth=90, latitude=lat, longitude=lon)
    lat, lon = res['latitude'], res['longitude']
    lats.append(lat), lons.append(lon)
    
    return {'lats':lats,'lons':lons}


def getAPI():
    from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 

    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

    return api

def get_link_icon(titles,icons):
    import requests
    import os
    for t,i in zip(titles,icons):
        if(os.path.isfile("static/images/" + str(t) + ".jpg")):
            print('saving time..')
            continue
        else:
            r = requests.get(i, auth=(user, password))
            with open( "static/images/" + str(t) + ".jpg", "wb") as img:
                img.write(r.content)
            img.close()

def drawBoundaries(latitude, longitude,width,height):
    import geopandas as gpd
    from pyproj import Proj, CRS,transform
    import folium
    from shapely.geometry import MultiPolygon, Polygon

    boundaries,foot =[], []

    for lat, lon in zip(latitude,longitude):

        box = latLonBoxByWandH(lat,lon,width,height)
        
        polygon_geom = Polygon(zip(box['lons'], box['lats']))
        foot.append(polygon_geom)
        crs = CRS('epsg:4326')
        polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       
        
        boundaries.append(polygon)


    Proj("epsg:4326")
    m = folium.Map([latitude[0],longitude[0]], zoom_start=12,width = "40%", height = "40%" , top='10%',left="55%", position='absolute')
    for polygon in boundaries:
        folium.GeoJson(polygon).add_to(m)
    m.save('./templates/folium.html')

    return boundaries,foot



def preprocess(batch_size, batch_number,fromD,toD, ew_width=10000, ns_height=10000,cloud = 50):
    
    try:
        ew_width = int(ew_width)
        ns_height = int(ns_height)
        batch_size = int(batch_size)
        batch_number = int(batch_number)
        fromD = str(fromD).replace('-','')
        toD = str(toD).replace('-','')
        cloud = int(cloud)
    


    except:
        print("Can't Convert")


    print("Received Inputs {}, {}, {}, {}, {}, {}, {}".format(batch_size,batch_number,fromD,toD,ew_width,ns_height,cloud))


    import os
    from zipfile import ZipFile
    import csv
    import rasterio as rio
    from rasterio.plot import show
    import rasterio.mask
    import fiona
    #import gdal
    from datetime import datetime
    from io import StringIO
    import shutil
    #from osgeo import gdal, gdal_array
    #from PIL import Image
    import json

    df0 = openDataFile1()
    list1,list2,a,b = [],[],[],[]
    for itema,itemb in zip(df0["iata_code"],df0['iso_region']):
        list1.append(itema)
        list2.append(itemb)
    
    for items in df0['coordinates']:
        a.append(items.split(',')[0])
        b.append(items.split(',')[1])

    iatalist,iatabatch= [],[]
    batch_ranges = []
    df = openDataFile2()
    allNames = []
    for items,names in zip(df['IATA'],df['Name']):
        iatabatch.append(items)
        allNames.append(names)
        
    def Remove(duplicate): 
        final_list = [] 
        for num in duplicate: 
            if num not in final_list: 
                final_list.append(num) 
        return final_list 

    iatabatch = Remove(iatabatch)
    chunk_items = len(iatabatch) - 1

    for i in range(chunk_items):
        batch_ranges.append(iatabatch[i*batch_size : (i+1)*batch_size])
        
    if 'flagCountry' in globals():
        print("flag value : {} ".format(flagCountry))

        print('Querying by Country... {}'.format(countryName))
        iatalist = getCodesByCountry(countryName)

    elif 'flagName' in globals():
        print("flag value : {} ".format(flagName))

        print('Querying by Airport for... {}'.format(airportName))
        iatalist = getCodesByAirport(airportName)


    else:
        for i in range(batch_size):
            try:
                iatalist.append(batch_ranges[batch_number -1][i])
            except:
                continue

    #try:
    #    k = int(k)
    #except ValueError as e:
    #    return e
    #else:
    if 'flagCoordinates' in globals():
        print("flag value : {} ".format(flagCoordinates))

        print('Querying Location By Coordinates for... {} {}'.format(coordinates[0],coordinates[1]))
        iatalist = ['C']
        loc_lat,loc_lon = coordinates
        

    else:
        print('Getting LatLon from IATA for ' + str(iatalist))
        loc_lat,loc_lon = getLatLonfromIATA(iatalist,list1,a,b)

    print(iatalist,loc_lat,loc_lon)

    print('Drawing spatial Boundaries...')


    polygons = drawBoundaries(loc_lat,loc_lon,ew_width,ns_height)[0]
    footprint = drawBoundaries(loc_lat,loc_lon,ew_width,ns_height)[1]
    api = getAPI()

    apiq = [] 
    qVal = {}

    for iatacode in iatalist:
        qVal[str(iatacode)] = {}
        qVal[str(iatacode)]['name'] = iatacode

    print('Querying S2...')

    for i in range(0,len(polygons)):
        apiq.append(api.query(footprint[i],
                    date = (fromD,toD),
                    platformname = 'Sentinel-2',
                    processinglevel = 'Level-2A',
                    area_relation = ('Contains'),
                    cloudcoverpercentage = (0,cloud)))
    for iatacode in iatalist:
        qVal[str(iatacode)]['numofProd'] = len(apiq[iatalist.index(iatacode)])


    products_list, products_list_sorted,images,title,titlelist,best,bestlist =[],[], [], [], [] , [],[]
    for products in apiq:
            products_list.append(api.to_geodataframe(products))
            
    #Sorting the list of products within our array of locations for minimum cloudcover
    for products in products_list:
        products_list_sorted.append(products.sort_values(['summary'],ascending = [False]))
        

    for i in range(0,len(products_list_sorted)):
            images.append(products_list_sorted[i].head(1))
            
    for items in title: 
            items[18:][:99999]
    for products in images:
        for i in range(0,len(products)):
            title.append(products.title[i])
            best.append(products.uuid[i])
        bestlist.append(best)
        titlelist.append(title)
        title,best = [], []

    for iatacode in iatalist:
        qVal[str(iatacode)]['listofTitle'] = list(products_list[iatalist.index(iatacode)]['title'])
        qVal[str(iatacode)]['listofUUID'] = list(products_list[iatalist.index(iatacode)]['uuid'])
        qVal[str(iatacode)]['listofCCP'] = list(products_list[iatalist.index(iatacode)]['cloudcoverpercentage'])
        qVal[str(iatacode)]['linkIcon'] = list(products_list[iatalist.index(iatacode)]['link_icon'])
        qVal[str(iatacode)]['dateofCapture'] = [x.date().strftime("%d %b %Y") for x in list(products_list[iatalist.index(iatacode)]['ingestiondate'])]
        qVal[str(iatacode)]['airportName'] = str(getNameFromIATA(iatacode))


    
    for iatacode in iatalist:
        get_link_icon(qVal[str(iatacode)]['listofTitle'],qVal[str(iatacode)]['linkIcon'])


    #print(qVal)
    return qVal

def downloadImages(key):

    api = getAPI()

    for items in key:
        # api.download(items, directory_path = "data")
        print('Downloading ' + items)
        dl = api.download(items, directory_path = "data")
    
    return(dl)
        # return(api.download(items, directory_path = "data"))
    # return("Downloading  " + key)

