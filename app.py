from flask import Flask, send_from_directory, render_template, request, jsonify
from test import * 
import time
import folium
import json
import os
from dbConnection import *


# get env variables
keyString = os.environ.get("MONGO_KEY") 

# client = MongoClient(keyString)
# print('Connected to DB')
# db = client["aerialweb"]
# collection = db["search-cache"]
# fs = gridfs.GridFS(db)


sessionToken = time.strftime('%Y%m%d%H%M%S')
airportsList = getAirportNamesasList()
countriesList = getCountryNamesasList()
# print(sorted(countriesList))

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSON_AS_ASCII'] = False

def bindDataToThumb(dataFull):
    data = dataFull["data"]
    thumbs = dataFull["thumb"]

    for key in data:
        data[key]["thumb"] = thumbs[list(data.keys()).index(key)]

    return data

def getDataFromForm(type):

    x = request.form['xbnd']
    y = request.form['ybnd']
    s = request.form['fromDate']
    e = request.form['toDate']
    c = request.form['cloud']

    if type == "by_airport":
        pri0 = request.form['airport']
        pri1 = None

        return [pri0,pri1,x,y,s,e,c]
    elif type == "by_country":
        pri0 = request.form['country']
        pri1 = 1
        pri2 = 1

        return [pri0,pri1,pri2,x,y,s,e,c]

    elif type == "by_coordinates" :
        pri0 = request.form['latitude']
        pri1 = request.form['longitude']
        pri2 = 1
        pri3 = 1

        return [pri0,pri1,pri2,pri3, x,y,s,e,c]
    elif type == "by_traffic" :
        pri0 = request.form['sz']
        pri1 = request.form['nm']

        return [pri0,pri1,x,y,s,e,c]
    


    #return(pri0,pri1,x,y,s,e,c)

def dumpJSON(cat,x, y, s, e, c, apiResponse, airName = 'null',countName = 'null',coord0 = 'null',coord1 = 'null',batsize = 'null',batnumb = 'null'):


    params = {}
    params['category'] = cat
    params['xbnd'] = x
    params['ybnd'] = y
    params['fromDate'] = s
    params['toDate'] = e
    params['cloud'] = c
    params['res'] = apiResponse



    if cat == "by_airport":
        params['airportName'] = airName
        collection.insert_one(params)
        # with open(f"data/{airName}_{sessionToken}.json", 'w') as f:
        #     json.dump(params, f)
    elif cat == "by_country":
        params['country'] = countName
        collection.insert_one(params)
        # with open(f"data/{countName}_{sessionToken}.json", 'w') as f:
        #     json.dump(params, f)
    elif cat == "by_coordinates" :
        params['latitude'] = coord0
        params['longitude'] = coord1
        collection.insert_one(params)
        # with open(f"data/{str(coord0)}c{str(coord1)}_{sessionToken}.json", 'w') as f:
        #     json.dump(params, f)
    elif cat == "by_traffic" :
        params['sz'] = batsize
        params['nm'] = batnumb
        collection.insert_one(params)
        # with open(f"data/{str(batnumb)}n{str(batsize)}_{sessionToken}.json", 'w') as f:
        #     json.dump(params, f)










#Download by airport name Page
@app.route('/by_airport',methods=["POST", "GET"])
def by_airport():
    if request.method =="POST":
        type = "by_airport" 
        # name,nulled,xBound,yBound,start,end,cl = getDataFromForm(type) 
        # dumpJSON(type,xBound,yBound,start,end,cl,airName = name)
        formData = request.get_json()
        print(formData)
        name, xBound, yBound, start, end, cl = formData['name'],formData['xBound'], formData['yBound'], formData['start'], formData['end'],formData['cl']




        print("Name was selected")
        p = getCodesByAirport(name)
        print(name,p)


        # data = render_template("picker.html", result =preprocess(1,airportsList.index(name)+1,start,end,xBound,yBound,cl),airports=airportsList,countries=countriesList)
        result = preprocess(1,airportsList.index(name)+1,start,end,xBound,yBound,cl)
        data = {
            "data": result[1]
            }
        dataForDB = {
            "data": result[0]
            }

        # bound = bindDataToThumb(data)
        dumpJSON(type, xBound, yBound, start,end,cl,dataForDB["data"],airName=p)
        # with open(f"data/test.json", 'w') as f:
        #     json.dump(data, f)
        return jsonify(data)

    
    return render_template("by_airport.html", airports = airportsList)

#Download by Country airport Page
@app.route('/by_country',methods=["POST", "GET"])
def by_country():
    if request.method =="POST":
        type = "by_country" 
        # country,size,num,xBound,yBound,start,end,cl = getDataFromForm(type) 

        formData = request.get_json()
        print(formData)
        country, xBound, yBound, start, end, cl = formData['country'],formData['xBound'], formData['yBound'], formData['start'], formData['end'],formData['cl']

        # Dumping JSON of request made
  




        print("Country was selected")
        p = getCodesByCountry(country)
        print(p)

        result = preprocess(1,1,start,end,xBound,yBound,cl)
        data = {
            "data": result[1]
            }
        dataForDB = {
            "data": result[0]
            }
        dumpJSON(type,xBound,yBound,start,end,cl,dataForDB["data"], countName = country)
        return jsonify(data)


    
    return render_template("by_country.html", countries = countriesList)

#Download by Coordinates Page
@app.route('/by_coordinates',methods=["POST", "GET"])
def by_coordinates():
    if request.method =="POST":
        type = "by_coordinates" 
        # lat,lon,size,num,xBound,yBound,start,end,cl = getDataFromForm(type) 

        formData = request.get_json()
        print(formData)
        lat, lon, xBound, yBound, start, end, cl = formData['lat'],formData['lon'],formData['xBound'], formData['yBound'], formData['start'], formData['end'],formData['cl']






        print("Latlong was selected")
        p = getParseCoordinates(lat,lon)
        print(p)

        # Dump JSON
        result = preprocess(1,1,start,end,xBound,yBound)
        data = {
            "data": result[1]
            }
        dataForDB = {
            "data": result[0]
            }

        dumpJSON(type,xBound,yBound,start,end,cl,dataForDB["data"],cl, coord0 = lat, coord1 = lon)
        return jsonify(data)


    
    return render_template("by_coordinates.html")

#Download by Passenger Traffic Page    
@app.route('/by_traffic',methods=["POST", "GET"])
def by_traffic():
    if request.method =="POST":
        type = "by_traffic" 
        # size,num,xBound,yBound,start,end,cl = getDataFromForm(type) 

 

        formData = request.get_json()
        print(formData)
        size, num, xBound, yBound, start, end, cl = formData['size'],formData['num'],formData['xBound'], formData['yBound'], formData['start'], formData['end'],formData['cl']


        # p = getSizeNum()

        result = preprocess(size,num,start,end,xBound,yBound,cl )

        data = {
            "data": result[1]
            }
        dataForDB = {
            "data": result[0]
            }

        # Dump JSON
        dumpJSON(type,xBound,yBound,start,end,cl, dataForDB["data"], batsize = size, batnumb = num)
        return jsonify(data)

    
    return render_template("by_traffic.html")
        

@app.route('/map',methods=["GET"])
def map():
    return render_template("folium_target.html")



@app.route("/", methods=["POST", "GET"])
def main():


    folium.Map([0,0], zoom_start=1, width = "40%", height = "40%" , top='10%',left="55%", position='absolute').save('./templates/folium.html')

    if request.method =="POST":

        try:
            name = request.form['airport']
            print(name)
        except:
            # print("Name wasn't selected")
            name = 0
        try:
            country = request.form['country']
            # print(country)
        except:
            # print("Country wasn't selected")
            country = 0
        try:
            lat = request.form['latitude']
            lon = request.form['longitude']
            # print(country)
        except:
            # print("Country wasn't selected")
            lat,lon = 0,0
        size = request.form['sz']
        num = request.form['nm']
        lat = request.form['latitude']
        lon = request.form['longitude']
        xBound = request.form['xbnd']
        yBound = request.form['ybnd']
        start = request.form['fromDate']
        end = request.form['toDate']
        cl = request.form['cloud']

        # print(name + "XXXX\n",size,num,xBound,yBound,start,end,cl)
        params = {}


        params['name'] = name
        params['country'] = country
        params['latitude'] = lat
        params['longitude'] = lon
        params['sz'] = size
        params['nm'] = num
        params['xbnd'] = xBound
        params['ybnd'] = yBound
        params['fromDate'] = start
        params['toDate'] = end
        params['cloud'] = cl



        if isinstance(name,str) :
            print("Name was selected")
            p = getCodesByAirport(name)
            print(name,p)
            return render_template("index.html", result =preprocess(1,airportsList.index(name)+1,start,end,xBound,yBound,cl),airports = airportsList,countries = countriesList)
        elif isinstance(country,str):
            print("Country was selected")
            p = getCodesByCountry(country)
            print(p)
            return render_template("index.html", result =preprocess(size,num,start,end,xBound,yBound,cl),airports=airportsList,countries = countriesList)
        elif lat == '' and lon == '':
        # elif isinstance(lat,str) and isinstance(lon,str):
            print("Latlong was selected")
            p = getParseCoordinates(lat,lon)
            print(p)
            return render_template("index.html", result =preprocess(size,num,start,end,xBound,yBound,cl),airports=airportsList,countries = countriesList)
        # if isinstance(name,str) or isinstance(country,str):
        #     if isinstance(name,str):
        #         print("Name was selected")
        #         p = getCodesByAirport(name)
        #         print(name,p)
        #         return render_template("index.html", result =preprocess(1,airportsList.index(name)+1,start,end,xBound,yBound,cl),airports = airportsList,countries = countriesList)
        #     else:
        #         print("Country was selected")
        #         p = getCodesByCountry(country)
        #         print(p)
        #         return render_template("index.html", result =preprocess(size,num,start,end,xBound,yBound,cl),airports=airportsList,countries = countriesList)


        # elif country:

            # return render_template("index.html", result = preprocess(1,airportsList.index(name)+1,start,end,xBound,yBound,cl))
        else:
            return render_template("index.html", result =preprocess(size,num,start,end,xBound,yBound,cl),airports = airportsList,countries=countriesList)

    else:
        return render_template("index.html",result = {},airports=airportsList,countries=countriesList)

@app.route("/download", methods=["POST", "GET"])
def download():
    uuid = request.args.get('uniqueID')
    uuid = uuid.split(',')
    print(uuid)

    with open("data/" + sessionToken + ".json") as f:
        params = json.load(f)
    
    downloadImages(uuid)
    

    return render_template('download.html')
    # return render_template('download.html',result = preprocess(size,num,start,end,xBound,yBound,cl),content = downloadImages(uuid),airports=airportsList,countries = countriesList)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True,port=1000)