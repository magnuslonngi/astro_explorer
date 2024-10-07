from astropy.visualization.lupton_rgb import make_lupton_rgb
from astropy import units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astroquery.skyview import SkyView
import cv2
import threading
import time
import os

timeout_duration = 300
stop_event = threading.Event()
radius = 0.3 * u.degree
offset = 1.712 * u.degree
output_folder = './Exoplanets/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_planet_images(planet_list_file='found_and_filtered_exoplanets.txt'):
    
    def verify_thread_status(thread_to_check):
        if thread_to_check.is_alive():
            print("Process took too long and timed out! Stopping the process...")
            stop_event.set()
            thread_to_check.join() 
            return True
        else:
            print("Process has ended.")
            return False

    def get_images(pos, survey, radius, image_list): 
        start_time = time.time() 
        try:
            skyview_fits = SkyView.get_images(position=pos, survey=f"{survey}", radius=radius, pixels=5000, scaling='Log') 
            image_list.append(skyview_fits[0][0])
        except Exception as e: 
            print(e)
            stop_event.set()
        finally:
            elapsed_time = time.time() - start_time
            print(f"Download finished in {elapsed_time:.2f} seconds")

    try:
        with open(planet_list_file, 'r') as file:
            positions = [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"File not found or an error occurred: {e}")
        raise  

    for position in positions:  
        try:
            fits_image = SkyCoord.from_name(position)
        except Exception as e:
            print(f"The exoplanet {position} is not found.")
            print(e)
            continue

        print(f"Downloading {position} data")
        filename = os.path.join(output_folder, f'{position.replace(" ", "_")}.png')
                    
        gri_images = [] 

        g_image_thread = threading.Thread(target=get_images, args=(fits_image, "SDSSg", radius, gri_images))   
        r_image_thread = threading.Thread(target=get_images, args=(fits_image, "SDSSr", radius, gri_images))   
        i_image_thread = threading.Thread(target=get_images, args=(fits_image, "SDSSi", radius, gri_images))   

        g_image_thread.start()
        r_image_thread.start()
        i_image_thread.start()

        g_image_thread.join(timeout_duration)
        r_image_thread.join(timeout_duration)
        i_image_thread.join(timeout_duration)

      
        thread_status = [
            verify_thread_status(g_image_thread),
            verify_thread_status(r_image_thread),
            verify_thread_status(i_image_thread)
        ]

        if any(thread_status):  
            print(f"Skipping {position} due to timeout or error.")
            continue

        try:

            g, r, i = [np.clip(image.data, 0, np.percentile(image.data, 99.9)) for image in gri_images]

            g = g / np.max(g)
            r = r / np.max(r)
            i = i / np.max(i)

            rgb = make_lupton_rgb(i, r, g, stretch=1, Q=10)
            rgb = cv2.flip(rgb, 0)  


            cv2.imwrite(filename, rgb)
            print(f"Image saved as {filename}")

        except Exception as e:
            print(f"Error processing images for {position}: {e}")

