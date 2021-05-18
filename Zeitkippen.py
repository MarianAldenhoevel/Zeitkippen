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
import logging
import os
import sys
import time
import datetime
import ffmpeg

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
video_metadata = ffmpeg.probe(args.inputfile)
video_metadata = video_metadata['streams'][0]

# Get dimensions, clamping to even numbers because browsers don't like to
# display other video.
videox = int(video_metadata['width']) // 2 * 2
videoy = int(video_metadata['height']) // 2 * 2
videot = int(video_metadata['nb_frames']) // 2 *2 
videoframerate = video_metadata['r_frame_rate']

logger.info('Video format detected: width={0}pixel, height={1}pixel, {2} frames at framerate={3}'.format(
    videox,
    videoy,
    videot,
    videoframerate)
)

# logger.debug(json.dumps(video_metadata, indent = 4))

# Read Video.
data, _ = (
    ffmpeg
    .input(args.inputfile)
    .output('pipe:', format = 'rawvideo', pix_fmt = 'rgb24')
    .run(capture_stdout = True)
)

# Make numpy-array from it. Reshaping into the correct dimensions.
video = numpy.frombuffer(data, numpy.uint8).reshape([-1, videoy, videox, 3])
data = None

ffmpeg_output_options = {
    'movflags': 'faststart',
    'pix_fmt': 'yuv420p'
}

# Create folders for exported images and videos. They will be created next to the input video with fixed names.
outputfolder = os.path.dirname(args.inputfile)

xyfolder = outputfolder + '/xy'
if not os.path.exists(xyfolder):
    os.makedirs(xyfolder)

xtfolder = outputfolder + '/xt'
if not os.path.exists(xtfolder):
    os.makedirs(xtfolder)

ytfolder = outputfolder + '/yt'
if not os.path.exists(ytfolder):
    os.makedirs(ytfolder)

# XY: This should recreate the original frames and video
nframes = videot
logger.info('Dumping {0} xy-frames.'.format(nframes))
for t in range(nframes):
    if (t%100 == 0) or (t == nframes-1):
        logger.debug('Processing xy-frame #{0}.'.format(t))

    frame = video[t,:,:]
    image = Image.fromarray(frame)
        
    image.save(xyfolder + '/{0:04d}.png'.format(t))

    if (t == 0):
        image.save(xyfolder + '/first.png')

    if (t == nframes-1):
        image.save(xyfolder + '/last.png')

(
ffmpeg
    .input(xyfolder + '/%04d.png', framerate = videoframerate)
    .output(
        outputfolder + '/xy.mp4', 
        **ffmpeg_output_options
    )
    .run()
)

# XT
nframes = videoy
logger.info('Dumping {0} xt-frames.'.format(nframes))
for y in range(nframes):
    if (y%100 == 0) or (y == nframes-1):
        logger.debug('Processing xt-frame #{0}.'.format(y))

    frame = video[0:videot,y,:]
    image = Image.fromarray(frame)
        
    image.save(xtfolder + '/{0:04d}.png'.format(y))

    if (y == 0):
        image.save(xtfolder + '/first.png')

    if (y == nframes-1):
        image.save(xtfolder + '/last.png')

(
ffmpeg
    .input(xtfolder + '/%04d.png', framerate = videoframerate)
    .output(
        outputfolder + '/xt.mp4', 
        **ffmpeg_output_options
    )
    .run()
)

# YT    
nframes = videox
logger.info('Dumping {0} yt-frames.'.format(nframes))
for x in range(nframes):
    if (x%100 == 0) or (x == nframes-1):
        logger.debug('Processing yt-frame #{0}.'.format(x))

    frame = video[0:videot,:,x]
    image = Image.fromarray(frame)
        
    image.save(ytfolder + '/{0:04d}.png'.format(x))
    
    if (x == 0):
        image.save(ytfolder + '/first.png')

    if (x == nframes-1):
        image.save(ytfolder + '/last.png')

(
ffmpeg
    .input(ytfolder + '/%04d.png', framerate = videoframerate)
    .output(
        outputfolder + '/yt.mp4', 
        **ffmpeg_output_options
    )
    .run()
)
    