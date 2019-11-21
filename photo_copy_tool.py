#python 3.7.3
import argparse
from datetime import datetime
import logging
import os
from pathlib import Path
import shutil
import re
import sys

import pyexiv2

#########################################

def valid_path(mypath: str):
    if pattern.match(mypath).end() == len(mypath):
        return mypath
    else:
        msg = 'not a valid path: '.format(mypath) 
        raise argparse.ArgumentTypeError(msg)

def get_files_in_source(source_path: Path) -> list:
    try:
        files_in_source = []
        for root, dirs, files in os.walk(source_path):
            files_in_source.extend(files)
            break
        return files_in_source
    except OSError:
        logger.info('files in '+source_path+' could not be read')
        return []

def create_logger(logger_name: str, dest_folder: str, name_file: str) -> logging.Logger:
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(dest_folder+name_file+'.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def copy_photos(filename: str, source_folder: str, dest_folder: str):
    try:
        metadata = pyexiv2.ImageMetadata(source_folder+filename)
        metadata.read()
        tag = metadata['Exif.Image.DateTime']
        creation_date = tag.value.date()
        
        del metadata
        del tag
        
        folder_name = str(creation_date)

        new_directory = dest_folder + folder_name + '/'

        try:
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)
            else:
                logger.info('folder '+new_directory+' already exists!')
        except:
            logger.info('folder '+new_directory+' could not be created!')

        try:
            if not os.path.isfile(new_directory+filename):
                shutil.copy2(source_folder+filename, new_directory)
            else:
                logger.info('file '+filename+' already exists')
        except:
            logger.info('file '+filename+' could not be moved')
    except:
        logger.info('file '+filename+' could not be copied')


#########################################

pattern = re.compile("((?:[^\/]*\/)*)")

parser = argparse.ArgumentParser(description = 'photo copy tool')
parser.add_argument('sourcefolder',
    type = valid_path,
    help = 'the folder the photos will be copied from'
    )
parser.add_argument('destinationfolder', 
    type = valid_path, 
    help = 'the folder the photos will be copied to'
    )

args = parser.parse_args()

source_folder = args.sourcefolder # '/home/daniel/Documents/python/copytool/testfiles/'
dest_folder = args.destinationfolder # '/home/daniel/Pictures/'

logger = create_logger('photo copy tool', dest_folder, 'copy')

files_source = get_files_in_source(Path(source_folder))

for photo in files_source:
    print(photo)
    copy_photos(photo, source_folder , dest_folder)


