# Blender ACES Manager
I made a blender ACES Manager to easily install and uninstall ACES on any blender version. When you install ACES, a backup of the original blender colormanagement folder will be created.

## About ACES:
ACES is a color management system that is used in the film industry. It is a set of tools and standards that help to ensure that the colors in a film are consistent and look natural.

In a nutshell, it's a cool thing :D

## About ACES in this installer:
 - ACES 1.3 Pro
 It's a 1.3 version of ACES, the comes with blender's 4.1 default color management system.

 - [PixelManager v1.1.4](https://github.com/Joegenco/PixelManager/releases/tag/v.1.1.4)
 It's a bunch of color management files, including ACES 1.3 and Blender 4.4 default color management system.

 - [PixelManager v2.0](https://github.com/Joegenco/PixelManager/releases/tag/v.2.0-RC3)
  It's a bunch of color management files, including ACES 1.3, ACES 2 and Blender 4.4 default color management system.

P.S I don't remember where I downloaded ACES 1.3 Pro, so I can't provide a link.

## Requirements to Build:
 - Python 3.12
 - PySide 6.9.1
 - pyinstaller 6.15.0

Btw all of those, except for python, will be installed when you run build.cmd