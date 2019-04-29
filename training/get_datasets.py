import numpy as np
import glob
import os

def get_data_for_dataset(dataset_name, mode):
    # Implement this for each dataset.
    if dataset_name == 'imagenet_video':
        datadir = os.path.join(
                os.path.dirname(__file__),
                'datasets',
                'imagenet_video')
        gt = np.load(datadir + '/labels/' + mode + '/labels.npy')
        image_paths = [datadir + '/' + line.strip()
            for line in open(datadir + '/labels/' + mode + '/image_names.txt')]

    if dataset_name == 'cfa':
        datadir = r'D:/CFA-Vehicle/data/trainTracking/data'

        gt = np.load(os.path.join(datadir, 'labels/labels.npy'))

        image_paths = sorted(glob.glob(datadir+'/**/images/*'))

    return {
            'gt' : gt,
            'image_paths' : image_paths,
            }
