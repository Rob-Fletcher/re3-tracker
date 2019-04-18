import cv2
import os
from tqdm import tqdm
import argparse



def main(args):

    output_path = args.video.replace('.mp4', '/images')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    vid = cv2.VideoCapture(args.video)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Length of video: {}".format(length))

    for frame in tqdm(range(length-1)):
        success, image = vid.read()
        if success:
            cv2.imwrite(os.path.join( output_path, "frame{:06d}.jpg".format(frame)), image)
        else:
            print("Could not extract frame")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-v","--video", help='Video to extract frames for.')
    args = p.parse_args()
    main(args)
