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

def queryProducts(latitude,longitude,iatas,fromDate,toDate,cloudcover,w,h):

    import geopandas as gpd
    import pyproj
    import folium
    from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt 
    from shapely.geometry import MultiPolygon, Polygon



    polygons,footprint =[], []

    for lat, lon in zip(latitude,longitude):

        box = latLonBoxByWandH(latitude,longitude,w,h)
        
        polygon_geom = Polygon(zip(box['lons'], box['lats']))
        footprint.append(polygon_geom)
        crs = {'init': 'epsg:4326'}
        polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       
        
        polygons.append(polygon)


    pyproj.Proj("+init=epsg:4326")
    m = folium.Map([latitude[0],longitude[0]], zoom_start=12,width = "40%", height = "40%" , top='10%',left="55%", position='absolute')
    for polygon in polygons:
        folium.GeoJson(polygon).add_to(m)
    m.save('./templates/folium.html')

    user = 'demi12395' 
    password = 'Sutd1234' 

    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

    apiq = [] 

    qVal = {}

    for i in range(0,len(polygons)):
        apiq.append(api.query(footprint[i],
                    date = (fromDate,toDate),
                    platformname = 'Sentinel-2',
                    processinglevel = 'Level-2A',
                    area_relation = ('Contains'),
                    cloudcoverpercentage = (0,cloudcover)))
    for i in range(len(apiq)):
        qVal[str(iatas[i])] = len(apiq[i])
    
    return qVal