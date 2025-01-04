# ACES-For-Blender
I made an installation and uninstallation script for Blender ACES

## How to use:
 - Download the latest [release](https://github.com/Aspirata/ACES-For-Blender/releases)
 - Run the ACES Installer.exe
 - Select the mode (install or uninstall)
 - Select the blender instance folder or specify the path to the blender colormanagement folder
 - When installing, select the ACES version (PixelManager or 1.3 Pro)
 - Enjoy!

 P.S The installer will automatically backup the original color management system in case you want to revert it.

## About ACES:
ACES is a color management system that is used in the film industry. It is a set of tools and standards that help to ensure that the colors in a film are consistent and look natural.

In a nutshell, it's a cool thing :D

## About ACES in this installer:
 - 1.3 Pro
 It's a 1.3 version of ACES, the comes with blender's 4.1 default color management system.
 - [PixelManager](https://github.com/Joegenco/PixelManager)
 It's a bunch of color management files, including ACES 1.3 and Blender 4.4 default color management system.

Btw this install script can be used for any color space, but I only use ACES, so only ACES here :3

P.S I don't remember where I downloaded the original ACES 1.3 Pro files, so I can't provide a link.

## Dependencies:
 - Python 3.10+ (It may work on older versions, but idk lol fr)
 - PyQt6
