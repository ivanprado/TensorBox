#!/usr/bin/env python

import argparse
import os
from os.path import join
import xml.etree.ElementTree as ET
import json
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

def main():
    '''
    Converts XML with Annotations from XML VOC format to TensorBox json format.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--annotations-folder', required=True, type=str, help="Folder with XML annotation files")
    parser.add_argument('--image-list-file', required=True, type=str, help="File with list of image names without extension")
    parser.add_argument('--image-path', required=True, type=str, help="Path to prepend to images")
    args = parser.parse_args()


    assert os.path.isdir(args.annotations_folder), "Folder {} does not exists or is not a folder.".format(args.annotations_folder)
    assert os.path.isfile(args.image_list_file), "File {} does not exists or is not a file.".format(args.image_list_file)

    with open(args.image_list_file) as f:
        imgnames = f.readlines()
        imgnames = [x.strip() for x in imgnames]

    D = []
    for imgname in imgnames:
        annofile = join(args.annotations_folder, imgname + ".xml")
        imgfile = join(args.annotations_folder, imgname + ".xml")
        assert os.path.isfile(annofile), "File {} does not exists".format(annofile)
        tree = ET.parse(annofile)
        root = tree.getroot()
        IMG = {'image_path': join(args.image_path, imgname + "jpg"),
               'rects': []}
        for object in root.iter("bndbox"):
            RECTS = {}
            RECTS["x1"] = float(object.find("xmin").text)
            RECTS["x2"] = float(object.find("xmax").text)
            RECTS["y1"] = float(object.find("ymin").text)
            RECTS["y2"] = float(object.find("ymax").text)
            IMG['rects'].append(RECTS)
        D.append(IMG)
    # pp.pprint(D)
    print json.dumps(D, indent=4, separators=(',', ': '), sort_keys=True)

if __name__ == '__main__':
    main()


