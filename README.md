# AerialWeb Satellite Imagery Explorer (Tool)

![Aerialweb web tool](https://lh3.googleusercontent.com/kdzFjkiK-cRc2nqGsKgiH4zhUfe_IAz_SDaIS4iSETT5Xw_IRLKZOC9S-zunawiDVvcvnlkoQV1wb012VjlUh3JDUckZolb2kOYKgm8XSpN9cDcFHucQI-DrQGFjjYABIfITVIQZjmz-8CPxWbJFXaRQBFj6QFfbqQG01Mr02RiIGBWOsH6hyatwGSpkvleENQLBDCjmLzQtC86YjAKrjmWQjfTRa46OmPJuCJJYfeuGCPy8IboX2FSqGakkI3DRS_1kA_T9B95bu98-fjhG9LF_0ES-J3nnUmUMJ4mBlCXO87FsXgLmOQjF-JsQfWGvSG-dQkol8rm7djJdQHfqoWp76--ddH-MjH3YRFpYzS4_0BJI-8GwNDUA8xvCeVEDzhPJBdi0eZ65elbN7jdtdBWNaKzrihQwzJfqRckI6Py9KNrxNr9AkxKQYT9FlElOx8uzCC70BBC9etHSoYSTq0omKAERKIn1mQ8QtmBFopyLCe4IgQmiE2aX9DuQUmNC1vGgSs6K7nDhlgIXUAmMULYWRatwc_mvfjukK5OD7C0KUS_WO_R7kYyASFfIURtqdVxI55A_lvSMPx-yWQlH3ueK_E-qlv-SynKAvdmr88nhVGTVt5wmpZLjAwHqieVbasSBPVaQcLZ_pMrXuD4ANhxZvL6QzbXjG5i3YlOXi02gj7Q9qKNSPeg5gL7eKPmWW4HahCwIpaOkO5laUoJGbYYDOA=w426-h220-no?authuser=0)

Hello, this project is a spin-off from my main project [Aerialweb](https://github.com/demiahmed/aerialweb) where I worked on utilising Sentinel2 API to query satellite imagery for my [Airport](http://metadesignlab.com/demo/aerial) project for curating high resolution open access imagery. This project is an interactive web-based interface to preview and collate large sets of aerial imagery by generating thumbnail previews using the RESTful endpoints of the S2 API.

[Live Demo](https://aerialweb.herokuapp.com) of this app

This app is made using a Flask backend and Jinja2 FE and is in the very first stages of its beta. Improved API structure, and a stable frontend are some of the future directions to this work. 

Clone this repo and add your own API keys by registering on the ESA's Sentinel and include in the `.env` file.

Feel free to play around this app and submit `merge` and `pull` requests to make this app work better. 