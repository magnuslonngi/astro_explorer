#Iniciador de procesos para la extracion de imagenes y creacion de la cubicacion de dicha 

from look_filter_module import check_explonets_and_save
#from plano import process_planet_images
from cubemap_module import generate_mapping_data
from data_obtainer_module import process_images
from Image_obtainer_module import process_planet_images
import glob
import os
from PIL import Image
import numpy as np
import cv2

#check_explonets_and_save('output_exoplanets.txt')

#process_planet_images('found_and_filtered_exoplanets.txt')
def apply_cubemap_to_generated_images(image_directory, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    image_paths = glob.glob(os.path.join(image_directory, "*.png")) 
    
    if len(image_paths) == 0:
        print("No images were found in the specified directory.")
        return

    for img_path in image_paths:
        print(f"Processing the image: {img_path}")

        imgIn = Image.open(img_path)
        inSize = imgIn.size

        map_x_32, map_y_32 = generate_mapping_data(inSize[0])


        cubemap = cv2.remap(np.array(imgIn), map_x_32, map_y_32, cv2.INTER_LINEAR)


        imgOut = Image.fromarray(cubemap)

        output_filename = os.path.join(output_directory, os.path.basename(img_path).replace(".png", "_cubic.png").replace(".jpg", "_cubic.jpg"))
        imgOut.save(output_filename)
        print(f"Cube image saved as: {output_filename}")
    
    print("Cubic processing completed for all images.")

input_directory='./planet_images/'
output_directory='./images_cube/'
apply_cubemap_to_generated_images(input_directory, output_directory)


image_dir = "./images_cube/"
json_path = "planet_data.json"
process_images(image_dir, json_path)
