import os
import time
import sys
sys.path.append(os.getcwd())
from frame_selection_.main import main as fs_main

from inference_.main import ImagePipeline

def main(config = {
                    'input_video': "C:/Users/RW154JK/OneDrive - EY/Desktop/v1/videos/mini.mp4",
                    'output_folder': "C:/Users/RW154JK/OneDrive - EY/Desktop/v1/app_output",
                    'model': 'yolov5s'
                    }
         ):
    start = time.time()
    fs_main(config['input_video'], 'fs_output')
    fs_output_folder = f'{config["input_video"].split(".")[0]}/fs_output'


    image_pipeline = ImagePipeline(fs_output_folder, 
                                    '.jpeg', 
                                    config['output_folder'], 
                                    config['model'])

    image_pipeline.preprocess()
    image_pipeline.forward()
    print(f'Finished after {time.time() - start} seconds.')
    
if __name__ == "__main__":
    main()