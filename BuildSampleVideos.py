#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Build synthetic stock samples for the Zeitkippen system.
'''

import math
import numpy
from PIL import Image, ImageDraw
import skvideo.io
import os

basefolder = os.path.dirname(os.path.realpath(__file__)) + '\\html\\data'

def ball_y():
    print("Creating sample video: Ball-y")

    imageX = 300
    imageY = 300

    circleD = 50
    circleY = -circleD

    folder = basefolder + '\\Ball-y'
    if not os.path.exists(folder):
        os.makedirs(folder)

    outfile = folder + '\\input.mp4'
    writer = skvideo.io.FFmpegWriter(
        outfile,
        outputdict={
            '-vcodec': 'libx264', 
            '-b': '30000000'
        }
    )

    while circleY < imageY+circleD:
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        draw.ellipse((150-circleD/2, circleY, 150+circleD/2, circleY+circleD), fill=(0, 0, 255), outline=(0, 0, 0))

        frame = numpy.array(im)
        writer.writeFrame(frame)

        circleY += 2

    writer.close()


def ball_x():
    print("Creating sample video: Ball-x")

    imageX = 300
    imageY = 300

    circleD = 50
    circleX = -circleD

    folder = basefolder + '\\Ball-x'
    if not os.path.exists(folder):
        os.makedirs(folder)

    outfile = folder + '\\input.mp4'
    writer = skvideo.io.FFmpegWriter(
        outfile,
        outputdict={
            '-vcodec': 'libx264', 
            '-b': '30000000'
        }
    )

    while circleX < imageX+circleD:
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        draw.ellipse((circleX, circleX+circleD, 150-circleD/2, 150+circleD/2), fill=(0, 0, 255), outline=(0, 0, 0))

        frame = numpy.array(im)
        writer.writeFrame(frame)

        circleX += 2

    writer.close()

def ball_xy():
    print("Creating sample video: Ball-xy")

    imageX = 300
    imageY = 300

    circleD = 50
    circleXY = -circleD

    folder = basefolder + '\\Ball-xy'
    if not os.path.exists(folder):
        os.makedirs(folder)

    outfile = folder + '\\input.mp4'
    writer = skvideo.io.FFmpegWriter(
        outfile,
        outputdict={
            '-vcodec': 'libx264', 
            '-b': '30000000'
        }
    )

    while circleXY < imageX+circleD:
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        draw.ellipse((circleXY, circleXY, circleXY+circleD/2, circleXY+circleD/2), fill=(0, 0, 255), outline=(0, 0, 0))

        frame = numpy.array(im)
        writer.writeFrame(frame)

        circleXY += 2

    writer.close()

def Abstract():
    print("Creating sample video: Abstract")
    
    imageX = 600
    imageY = 300
    framecount = 150

    folder = basefolder + '\\Abstract'
    if not os.path.exists(folder):
        os.makedirs(folder)

    outfile = folder + '\\input.mp4'
    writer = skvideo.io.FFmpegWriter(
        outfile,
        outputdict={
            '-vcodec': 'libx264', 
            '-b': '30000000'
        }
    )

    for frameindex in range(framecount):
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im, 'RGBA')

        y = 0
        dy = 1
        while y < imageY:
            colindex = math.trunc((frameindex/framecount)*255)
            color = (colindex, 255-colindex, 0)
            draw.rectangle([0, y, imageX+1, y+dy], fill=color, outline=color)
            y += dy*2
            dy = dy*1.2

        x = 0
        dx = 1
        while x < imageX-dx:
            colindex = math.trunc((frameindex/framecount)*255)
            color = (0, colindex, 255-colindex, 128)
            draw.rectangle([x, 0, x+dx, imageY+1], fill=color, outline=color)
            x += dx*2
            dx = dx*1.3

        frame = numpy.array(im)
        writer.writeFrame(frame)

    writer.close()

# MAIN:

print(basefolder)
if not os.path.exists(basefolder):
    os.makedirs(basefolder)

#ball_x()
#ball_y()
#ball_xy()

Abstract()
