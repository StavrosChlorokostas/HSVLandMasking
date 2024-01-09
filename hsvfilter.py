import json
from jsonschema import validate, Draft202012Validator, ValidationError
import os

# custom data structure to hold the values of the HSV filter
class HSVfilter:
    
    #constants
    schema = {
        "type": "object",
        "properties": {
            "hMin": {"type": "integer","minimum": 0,"maximum": 179},
            "sMin": {"type": "integer","minimum": 0,"maximum": 255},
            "vMin": {"type": "integer","minimum": 0,"maximum": 255},
            "hMax": {"type": "integer","minimum": 0,"maximum": 179},
            "sMax": {"type": "integer","minimum": 0,"maximum": 255},
            "vMax": {"type": "integer","minimum": 0,"maximum": 255},
            "sAdd": {"type": "integer","minimum": 0,"maximum": 255},
            "sSub": {"type": "integer","minimum": 0,"maximum": 255},
            "vAdd": {"type": "integer","minimum": 0,"maximum": 255},
            "vSub": {"type": "integer","minimum": 0,"maximum": 255},
            "clahe": {"type": "integer","minimum": 0,"maximum": 1},
            "blur": {"type": "integer","minimum": 0,"maximum": 20},
            "close": {"type": "integer","minimum": 0,"maximum": 20},
            "object": {"type": "integer","minimum": 0,"maximum": 25000},
            "hole": {"type": "integer","minimum": 0,"maximum": 25000}
        }
    }

    def __init__(self, hMin=0, sMin=0, vMin=0, hMax=179, sMax=255, vMax=255, sAdd=0,
                 sSub=0, vAdd=0, vSub=0, Clahe=0, Blur=0, Close=0, Object=0, Hole=0):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub
        self.clahe = Clahe
        self.blur = Blur
        self.close = Close
        self.object = Object
        self.hole = Hole

    def save_to_file(self, output_folder):

        output_file = os.path.join(output_folder,'hsv_parameters_from_GUI.json')
        hsv_parameters = {
            "hMin" : self.hMin,
            "sMin" : self.sMin,
            "vMin" : self.vMin,
            "hMax" : self.hMax,
            "sMax" : self.sMax,
            "vMax" : self.vMax,
            "sAdd" : self.sAdd,
            "sSub" : self.sSub,
            "vAdd" : self.vAdd,
            "vSub" : self.vSub,
            "clahe" : self.clahe,
            "blur" : self.blur,
            "close" : self.close,
            "object" : self.object,
            "hole" : self.hole
        }

        with open(output_file, "w") as outfile: 
            json.dump(hsv_parameters, outfile)
        
        outfile.close()
    
    
    def import_from_file(self,json_file):
        try:
            with open(json_file) as hsv_json:
                hsv_dict = json.load(hsv_json)
        except TypeError:
            print("ERROR: HSV filter parameters have not been provided. Please include the path to a valid json file to the 'hsvparams' variable (-hsv) or use GUI mode (-guimode) to create one manually. Type --help for more information. Exiting...")
            quit()
        except FileNotFoundError:
            print("ERROR: The directory passed in 'hsvparams' cannot be found. Exiting...")
            quit()
        
        try:
            validate(hsv_dict,self.schema)
        except ValidationError:
            print("ERROR: Invalid JSON passed in 'hsvparams'. Detailed errors below:\n")
            v = Draft202012Validator(self.schema)
            errors = sorted(v.iter_errors(hsv_dict), key=lambda e: e.path)
            for error in errors:
                print(error)
            quit()

        self.hMin = hsv_dict['hMin']
        self.sMin = hsv_dict['sMin']
        self.vMin = hsv_dict['vMin']
        self.hMax = hsv_dict['hMax']
        self.sMax = hsv_dict['sMax']
        self.vMax = hsv_dict['vMax']
        self.sAdd = hsv_dict['sAdd']
        self.sSub = hsv_dict['sSub']
        self.vAdd = hsv_dict['vAdd']
        self.vSub = hsv_dict['vSub']
        self.clahe = hsv_dict['clahe']
        self.blur = hsv_dict['blur']
        self.close = hsv_dict['close']
        self.object = hsv_dict['object']
        self.hole = hsv_dict['hole']
