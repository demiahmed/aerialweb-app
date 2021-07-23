from flask import Flask, redirect, url_for, render_template, request, jsonify
from test import * 
import time
import folium
import json
sessionToken = time.strftime('%Y%m%d%H%M%S')
airportsList = getAirportNamesasList()
countriesList = getCountryNamesasList()
# print(sorted(countriesList))

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

def dumpJSON(cat,x, y, s, e, c, airName = 'null',countName = 'null',coord0 = 'null',coord1 = 'null',batsize = 'null',batnumb = 'null'):


    params = {}
    params['category'] = cat


    if cat == "by_airport":
        params['airportName'] = airName
    elif cat == "by_country":
        params['country'] = countName
    elif type == "by_coordinates" :
        params['latitude'] = coord0
        params['longitude'] = coord1
    elif type == "by_traffic" :
        params['sz'] = batsize
        params['nm'] = batnumb

    params['xbnd'] = x
    params['ybnd'] = y
    params['fromDate'] = s
    params['toDate'] = e
    params['cloud'] = c

    with open("data/" + sessionToken + ".json", 'w') as f:
        json.dump(params, f)




app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

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

        return jsonify({"data": preprocess(1,airportsList.index(name)+1,start,end,xBound,yBound,cl)})

    
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
        dumpJSON(type,xBound,yBound,start,end,cl,countName = country)




        print("Country was selected")
        p = getCodesByCountry(country)
        print(p)
        return jsonify({"data" :preprocess(1,1,start,end,xBound,yBound,cl)})

    
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

        # Dump JSON
        dumpJSON(type,xBound,yBound,start,end,cl)




        print("Latlong was selected")
        p = getParseCoordinates(lat,lon)
        print(p)
        return jsonify({"data": preprocess(1,1,start,end,xBound,yBound,cl)})

    
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

        # Dump JSON
        dumpJSON(type,xBound,yBound,start,end,cl)
        p = getSizeNum()

        return jsonify({"data":preprocess(size,num,start,end,xBound,yBound,cl)})

    
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

        with open("data/" + sessionToken + ".json", 'w') as f:
            json.dump(params, f)

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




if __name__ == "__main__":
    app.run(debug=True,port=1000)