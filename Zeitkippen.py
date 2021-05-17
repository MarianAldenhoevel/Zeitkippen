#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    This is the main module of the Zeitkippen video processor.

    Copyright (c) 2021 Marian Aldenhövel
'''

import argparse
import json
import math
import numpy
from PIL import Image
from scipy.interpolate import interp1d
import skvideo.io
import logging
import os
import sys
import time
import datetime

# Conversion function for argparse booleans
def str2bool(v):
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
    return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    return False
  else:
    raise argparse.ArgumentTypeError('Boolean value expected.')

# Setup command line parser
parser = argparse.ArgumentParser(description = 'Create videos with transposed dimensions.')

parser.add_argument('-ll', '--log-level',
    action = 'store',
    default = 'INFO',
    help ='Set the logging output level to CRITICAL, ERROR, WARNING, INFO or DEBUG (default: %(default)s)',
    dest ='log_level',
    metavar = 'level'
)

parser.add_argument('-if', '--input-file',                          
    action = 'store',
    dest = 'inputfile',  
    required = True,              
    help = 'name of input file with video readable by sk-video/ffmpeg'
)

parser.add_argument('-sf', '--save-frames',
    action = 'store',
    default = False,
    type = str2bool,
    help = 'Save the individual frames as PNG images (default: %(default)s)',
    dest = 'saveframes',
    metavar = 'flag'
  )

args = parser.parse_args()

args.inputfile = os.path.abspath(args.inputfile)
args.log_level_int = getattr(logging, args.log_level, logging.INFO)

# Setup logging
fh = logging.FileHandler(os.path.splitext(os.path.realpath(__file__))[0] + '.log')
fh.setLevel(args.log_level_int)

ch = logging.StreamHandler()
ch.setLevel(args.log_level_int)

ch.setFormatter(logging.Formatter('({thread}) [{levelname:7}] {name} - {message}', style='{'))
fh.setFormatter(logging.Formatter('{asctime} ({thread}) [{levelname:7}] {name} - {message}', style='{'))

root = logging.getLogger()
root.addHandler(ch)
root.addHandler(fh)
root.setLevel(logging.DEBUG)

logger = logging.getLogger('main')

# Probe input file.
logger.info('Probing file \'{0:s}\'.'.format(args.inputfile))

# Dump video metadata at appropriate verbosity-levels
video_metadata = skvideo.io.ffprobe(args.inputfile)

logger.info('Video format detected: width={0}pixel, height={1}pixel, {2} frames at framerate={3}'.format(
    video_metadata['video']['@width'],
    video_metadata['video']['@height'],
    video_metadata['video']['@nb_frames'],
    video_metadata['video']['@r_frame_rate']))

# logger.debug(json.dumps(video_metadata, indent = 4))

# Open input file as generator to read each frame in turn.
inputparameters = {}
outputparameters = {}
reader = skvideo.io.FFmpegReader(args.inputfile,
    inputdict=inputparameters,
    outputdict=outputparameters)

# Create folders for exported images and videos. They will be created next to the input video with fixed names.
outputfolder = os.path.dirname(args.inputfile)

xyfolder = outputfolder + '\\xy'
if not os.path.exists(xyfolder):
    os.makedirs(xyfolder)

xtfolder = outputfolder + '\\xt'
if not os.path.exists(xtfolder):
    os.makedirs(xtfolder)

ytfolder = outputfolder + '\\yt'
if not os.path.exists(ytfolder):
    os.makedirs(ytfolder)

try:
    # Initialize array of all the pixels of the video.
    frames = numpy.empty((
        int(video_metadata['video']['@nb_frames']),
        int(video_metadata['video']['@height']),
        int(video_metadata['video']['@width']),
        3),
        dtype='uint8'
    )
    
    # Iterate through the frames to fill the pixel array.
    frame_index = 0
    for frame in reader.nextFrame():
        if (frame_index%100 == 0):
            logger.debug('Reading frame #{0}.'.format(frame_index))
        
        # Save xy-Frame (normal)
        #image = Image.fromarray(frame)
        #image.save(xyfolder + '\\{0:04d}.png'.format(frame_index))
        frames[frame_index] = frame
        frame_index = frame_index + 1

    logger.info('Read {0} frames.'.format(frame_index))

    # This should recreate the original frames and video
    writer = skvideo.io.FFmpegWriter(outputfolder+'\\xy.mp4')
    try:
        nframes = frames.shape[0]
        logger.info('Dumping {0} xy-frames.'.format(nframes))
        for t in range(nframes):
            if (t%100 == 0) or (t == nframes-1):
                logger.debug('Processing xy-frame #{0}.'.format(t))

            frame = frames[t,:,:]
            if (args.saveframes) or (t == 0) or (t == nframes-1):
                image = Image.fromarray(frame)
                
                if args.saveframes:
                    image.save(xyfolder + '\\{0:04d}.png'.format(t))

                if (t == 0):
                    image.save(xyfolder + '\\first.png')

                if (t == nframes-1):
                    image.save(xyfolder + '\\last.png')

            writer.writeFrame(frame)
    finally:
        writer.close()

    writer = skvideo.io.FFmpegWriter(outputfolder+'\\xt.mp4')
    try:
        nframes = frames.shape[1]
        logger.info('Dumping {0} xt-frames.'.format(nframes))
        for y in range(nframes):
            if (y%100 == 0) or (y == nframes-1):
                logger.debug('Processing xt-frame #{0}.'.format(y))

            frame = frames[:,y,:]
            if (args.saveframes) or (y == 0) or (y == nframes-1):
                image = Image.fromarray(frame)
                
                if args.saveframes:
                    image.save(xtfolder + '\\{0:04d}.png'.format(y))
        
                if (y == 0):
                    image.save(xtfolder + '\\first.png')

                if (y == nframes-1):
                    image.save(xtfolder + '\\last.png')

            writer.writeFrame(frame)
    finally:
        writer.close()

    writer = skvideo.io.FFmpegWriter(outputfolder+'\\yt.mp4')
    try:
        nframes = frames.shape[2]
        logger.info('Dumping {0} yt-frames.'.format(nframes))
        for x in range(nframes):
            if (x%100 == 0) or (x == nframes-1):
                logger.debug('Processing yt-frame #{0}.'.format(x))

            frame = frames[:,:,x]
            if (args.saveframes) or (x == 0) or (x == nframes-1):
                image = Image.fromarray(frame)
                
                if args.saveframes:
                    image.save(ytfolder + '\\{0:04d}.png'.format(x))
                
                if (x == 0):
                    image.save(ytfolder + '\\first.png')

                if (x == nframes-1):
                    image.save(ytfolder + '\\last.png')

            writer.writeFrame(frame)
    finally:
        writer.close()        
            
finally:
    logger.info('Closing input file.')
    reader.close()