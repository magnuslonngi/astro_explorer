from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy.coordinates import SkyCoord
import json
from pathlib import Path
import os
from PIL import Image


def get_exoplanet_info(position, path):
    path = Path(path)
    
    if not path.is_file():
        with open(path, "w") as outfile:
            try:
                json_starter = {
                    "exoplanets": []
                }
                
                json_starter = json.dumps(json_starter)
                outfile.write(json_starter)
            except Exception as e:
                print(e)
    
    # Check if file exists       
    
    archive = NasaExoplanetArchive()
    result = archive.query_object_async(position)
    fits_image = SkyCoord.from_name(position)
    info = NasaExoplanetArchive.query_criteria(table="pscomppars", select=f"pl_name, pl_orbper, discoverymethod, disc_year, disc_pubdate, disc_facility, disc_telescope, disc_instrument", where=f"pl_name like '{position}'")

    if len(result) > 0:
        exoplanet_name = f"{result['pl_name'][0]}"  # Nombre del exoplaneta
        exoplanet_orbital_period = f"{result['pl_orbper'][0]}"  # Periodo orbital (días)
        exoplanet_disc_method = f"{result["discoverymethod"][0]}"  
        exoplanet_disc_year = f"{result["disc_year"][0]}" 
        exoplanet_disc_pubdate = f"{result["disc_pubdate"][0]}" 
        exoplanet_disc_facility = f"{result["disc_facility"][0]}" 
        exoplanet_disc_telescope = f"{result["disc_telescope"][0]}" 
        exoplanet_disc_instrument = f"{result["disc_instrument"][0]}" 
                
            # Data to be written
        exoplanet_json_data = {
            "name": exoplanet_name,
            "data": {   
                "pl_orbper": exoplanet_orbital_period,
                "discoverymethod": exoplanet_disc_method,
                "disc_year": exoplanet_disc_year,
                "disc_pubdate": exoplanet_disc_pubdate,
                "disc_facility": exoplanet_disc_facility,
                "disc_telescope": exoplanet_disc_telescope,
                "disc_instrument": exoplanet_disc_instrument
            }
        }
        
        json_object = json.dumps(exoplanet_json_data, indent=4)

        with open(path,'r+') as outfile:
            data = json.load(outfile)
            print(data)
            data["exoplanets"].append(exoplanet_json_data)
            outfile.seek(0)
            json.dump(data, outfile, indent=4)
    else:
        return "No se encontraron resultados para el exoplaneta especificado."


image_dir = "./GeneratedImages/cubic"

def process_images(image_dir, json_path):
    for filename in os.listdir(image_dir):
        if filename.endswith('.png'):  # Filter image files
            planet_name = filename.replace("_cubic.png", "")
            planet_name = planet_name.replace("_", " ")       
            image_path = os.path.join(image_dir, filename)  # Full path to the image   
            get_exoplanet_info(planet_name, "./planet_data.json")