import time
import os
import os.path
from .extracting_candidate_frames import *
from .clustering_with_hdbscan import *
import matplotlib.pyplot as plt

def main(input_video = "videos/hallway.mp4",
         output_folder = 'fs_output'):
    start_time = time.time()



    print('file execution started for input video {}'.format(input_video))
    vd = FrameExtractor()

    imgs, imgs_idx = vd.extract_candidate_frames(input_video)
    final_images = ImageSelector()
    imgs_final, imgs_final_idx = final_images.select_best_frames(imgs, imgs_idx)
    # graph(imgs_final_idx)
    output_destination = input_video.rsplit(".", 1)[0] + '/' + output_folder
    print(output_destination)
    os.makedirs(output_destination, exist_ok=True)
    for img, i in zip(imgs_final, imgs_final_idx):
        vd.save_frame_to_disk(
            img,
            file_path=os.path.join(output_destination),
            file_name="test_" + str(i),
            file_ext=".jpeg",
        )
    print("--- {a} seconds to extract key frames from {b}---".format(a=(time.time() - start_time),b=input_video))
    return imgs_idx

def graph(imgs_idx):
    fig = plt.figure(figsize=(5,1))
    plt.hist(np.array(imgs_idx)/max(imgs_idx), bins=max(imgs_idx))
    fig.savefig('saved_imgs.png')

if __name__ == "__main__":
    main()