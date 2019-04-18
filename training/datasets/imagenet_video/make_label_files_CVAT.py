import cv2
import numpy as np
import glob
import xml.etree.ElementTree as ET
import time
import random
import os
import sys
import argparse
from tqdm import tqdm

basedir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(
    basedir,
    os.path.pardir,
    os.path.pardir,
    os.path.pardir)))


from re3_utils.util import drawing
from re3_utils.util.im_util import get_image_size

DEBUG = False

def main(args):

    data_dir = args.data_dir
    #wildcard = '/*/*/' if label_type == 'train' else '/*/'
    #dataset_path = 'data/ILSVRC2015/'
    #annotationPath = dataset_path + 'Annotations/'
    #imagePath = dataset_path + 'Data/'

#    if not DEBUG:
#        if not os.path.exists(os.path.join('labels', label_type)):
#            os.makedirs(os.path.join('labels', label_type))
#        imageNameFile = open('labels/' + label_type + '/image_names.txt', 'w')

    videos = sorted(glob.glob(data_dir+'/**'))
    #print("videos: {}".format(videos))

    bboxes = []
    imNum = 0
    #totalImages = len(glob.glob(annotationPath + 'VID/' + label_type + wildcard + '*.xml'))
    #print('totalImages', totalImages)

    for vv,video in enumerate(videos):
        #labels = sorted(glob.glob(video + '*.xml'))
        #images = [label.replace('Annotations', 'Data').replace('xml', 'JPEG') for label in labels]
        video_name = video.split('/')[-1]
        images = sorted(glob.glob(os.path.join(video, 'images/*')))

        # for CVAT the labels are all in a single xml file
        labels = ET.parse(os.path.join(video, video_name+'.xml'))

        trackColor = dict()
        for ii,imageName in enumerate(tqdm(images)):
            if not DEBUG:
                # Leave off initial bit of path so we can just add parent dir to path later.
                #imageNameFile.write(imageName + '\n')
                pass
            #label = labels[ii]
            labelTree = labels.getroot()
            imgSize = get_image_size(images[ii])
            area = imgSize[0] * imgSize[1]
            if DEBUG:
                print('Image: {}     Index: {}'.format(imageName.split('/')[-1], ii))
                #image = cv2.imread(images[ii])
            #print('Image: {}     Index: {}'.format(imageName.split('/')[-1], ii))
            for track in labelTree.findall('track'):
                cls = track.attrib['label']
                #assert cls in classes
                classInd = 0
                trackID = int(track.attrib['id'])
                #loop over all boxes in the track ID
                for box in track.findall('box'):
                    # find the box that corresponds to the current frame number
                    if int(box.attrib['frame']) != ii:
                        continue

                    #print("Found box in frame {} with trackID {}".format(ii, trackID))
                    occl = int(box.attrib['occluded'])
                    #bbox = obj.find('bndbox')
                    bbox = [int(float(box.attrib['xtl'])),
                            int(float(box.attrib['ytl'])),
                            int(float(box.attrib['xbr'])),
                            int(float(box.attrib['ybr'])),
                            vv, trackID, imNum, classInd, occl]

                    if DEBUG:
                        print('name', obj.find('name').text, '\n')
                        print(bbox)
                        if trackID not in trackColor:
                            trackColor[trackId] = [random.random() * 255 for _ in range(3)]
                        drawing.drawRect(image, bbox[:4], 3, trackColor[trackId])
                    bboxes.append(bbox)
            if DEBUG:
                cv2.imshow('image', image)
                cv2.waitKey(1)

            imNum += 1

    bboxes = np.array(bboxes)
    # Reorder by video_id, then track_id, then video image number so all labels for a single track are next to each other.
    # This only matters if a single image could have multiple tracks.
    order = np.lexsort((bboxes[:,6], bboxes[:,5], bboxes[:,4]))
    bboxes = bboxes[order,:]
    if not DEBUG:
        save_dir = os.path.join(data_dir, 'labels')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        np.save(os.path.join(save_dir, 'labels.npy'), bboxes)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-d","--data_dir", help='base directory for all data.')
    p.add_argument("-t", "--type", choices=['train','test','val'], default='train', help="One of 'train', 'test', or 'val'.")
    args = p.parse_args()
    main(args)
#    main('val')
