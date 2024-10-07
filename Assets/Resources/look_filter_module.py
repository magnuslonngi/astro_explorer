from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.sdss import SDSS
import astropy.units as u
from astroquery.skyview import SkyView

def check_explonets_and_save(filename="found_and_filtered_exoplanets.txt"):

    exoplanets = NasaExoplanetArchive.query_criteria(table="pscomppars", select="pl_name, ra, dec")
    total_planets = len(exoplanets)

    print(f"Total number of exoplanets found in the NASA Exoplanet Archive: {total_planets}\n")

    with open("found_and_filtered_exoplanets.txt", "w") as file:
        for i, exoplanet in enumerate(exoplanets, start=1):
            name = exoplanet['pl_name']
            sky_coord = exoplanet['sky_coord']

            print(f"Checking exoplanet {i}/{total_planets}: {name}")

            xid = SDSS.query_region(sky_coord, radius=3*u.arcmin, spectro=True)

            if xid:
                try:
                    skyview_data = SkyView.get_image_list(position=name, survey="SDSSg")
                except Exception as e:
                    print(e)
                else:
                    if skyview_data:
                        file.write(name + "\n")
                        print(f"Exoplanet {name} found in SDSS and got the data.")
                    else:
                        print(f"No SDSS data found for: {name}")
                        print("\n" + "-"*50 + "\n")
            else:
                print(f"Exoplanet {name} not found in SDSS.")

            print("\n" + "-"*50 + "\n")

    print("Finished checking exoplanets. Names of found and filtered exoplanets and are saved in 'found_exoplanets.txt'.")
