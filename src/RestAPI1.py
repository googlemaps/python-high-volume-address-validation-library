from av_result_parser import av_result_parser_class
from flask import Flask
from flask_restful import Resource, Api
#from main import HighVolumeAVMain 
import googlemaps
import config_loader

app = Flask(__name__)
api = Api(app)
port = 5100

#config =config_loader.Config()
#Create a client of the googleMaps client library

#gmaps = googlemaps.Client(key=config.api_key)

#av_result_parser_load=av_result_parser_class()

@app.route('/high-volume-validate', methods=['GET', 'POST'])
def high_volume_validate():
   return "HELLO WORLD"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
 