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

def Horz_Vert():
    print("Creating sample video: Horz_Vert")

    imageX = 400
    imageY = 400
    framecount = 400

    base = 120
    height = 120

    folder = basefolder + '\\_Horz_Vert'
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

    x = -height / 2 
    dx = imageX / framecount

    y = -height / 2
    dy = imageY / framecount

    for frame in range(framecount):
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        draw.polygon([
            (x + frame*dx,          imageY/2 - base/2),
            (x + frame*dx + height, imageY/2),
            (x + frame*dx,          imageY/2 + base/2)
            ], 
            fill = (0,0,255), outline = (0,0,0)
        )

        draw.polygon([
            (imageX/2 - base/2, y + frame*dy),
            (imageX/2,          y + frame*dy + height),
            (imageX/2 + base/2, y + frame*dy)
            ], 
            fill = (0,255,0), outline = (0,0,0)
        )

        frame = numpy.array(im)
        writer.writeFrame(frame)

    writer.close()

def Abstract():
    print("Creating sample video: Abstract")
    
    imageX = 600
    imageY = 300
    framecount = 150

    folder = basefolder + '\\_Abstract'
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

def Oscillation():
    print("Creating sample video: Oscillation")
    
    imageX = 400
    imageY = 400
    framecount = 400

    folder = basefolder + '\\_Oscillation'
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

    circleR = 30

    colors = [
        (255,  0,  0),
        (  0,255,  0),
        (  0,  0,255),
        (255,255,  0),
        (  0,255,255),
        (255,  0,255)
    ]

    osccount = 6

    dx = imageX/osccount
    dt = 2*math.pi/framecount
        
    for frameindex in range(framecount):
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im, 'RGBA')

        t = -math.pi/4 + frameindex * dt
        for osc in range(osccount): 
            x = osc*dx + dx/2
            y = imageY/2 + imageY/2 * math.sin((osc + 1) * t)
            
            color = colors[osc % len(colors)]
            
            points = []
            vertexcount = osc+3 # Start at a triangle
            for vertexindex in range(vertexcount):
                a = vertexindex * math.pi * 2 / vertexcount
                points.append((x + circleR*math.sin(a), y + circleR*math.cos(a)))

            draw.polygon(points, fill=color, outline=(0,0,0))

        frame = numpy.array(im)
        writer.writeFrame(frame)

    writer.close()


def Rotation():
    print("Creating sample video: Rotation")
    
    imageX = 400
    imageY = 400
    framecount = 400

    folder = basefolder + '\\_Rotation'
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

    circleR = 20

    colors = [
        (255,  0,  0),
        (  0,255,  0),
        (  0,  0,255),
        (255,255,  0),
        (  0,255,255),
        (255,  0,255)
    ]

    osccount = 6

    dt = 2*math.pi/framecount
        
    for frameindex in range(framecount):
        im = Image.new('RGB', (imageX, imageY), (255, 255, 255))
        draw = ImageDraw.Draw(im, 'RGBA')

        t = -math.pi/4 + frameindex * dt
        r = 1.5*circleR
        for osc in range(osccount): 
            phi = (osccount-osc) * t

            color = colors[osc % len(colors)]
            
            draw.line([imageX/2, imageY/2, imageX/2 + imageX*math.sin(phi), imageY/2 + imageY*math.cos(phi)], color, 2)

        for osc in range(osccount): 
            phi = (osccount-osc) * t
            x = imageX/2 + r*math.sin(phi)
            y = imageX/2 + r*math.cos(phi)
            
            color = colors[osc % len(colors)]
            
            points = []
            vertexcount = osc+3 # Start at a triangle
            for vertexindex in range(vertexcount):
                a = vertexindex * math.pi * 2 / vertexcount
                points.append((x + circleR*math.sin(a), y + circleR*math.cos(a)))

            draw.polygon(points, fill=color, outline=(0,0,0))

            r = r + 1.5*circleR

        frame = numpy.array(im)
        writer.writeFrame(frame)

    writer.close()

# MAIN:

print(basefolder)
if not os.path.exists(basefolder):
    os.makedirs(basefolder)

Horz_Vert()
Abstract()
Oscillation()
Rotation()