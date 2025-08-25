# [Readme RU](README.md)

# Blender ACES Manager

Blender ACES Manager is a simple program for managing ACES in Blender.

## What is ACES

**ACES (Academy Color Encoding System)** is a standardized color management system widely used in the film and visual effects industries. ACES ensures consistent, accurate, and natural-looking colors across different devices and workflows, making it an essential tool for professional-grade color grading and rendering.

**Simply put**: ACES makes the image look better, just like in Hollywood movies.

## Preinstalled ACES Versions

- **ACES 1.3 Pro**  
  ACES 1.3 version, compatible with Blender 4.1’s default color management system.  
  *Note: the source of ACES 1.3 Pro is not documented, so no download link is provided.*

- **[PixelManager v2.0](https://github.com/Joegenco/PixelManager/releases/tag/v.2.0-RC4)**  
  An updated set of color management files with support for ACES 1.3, ACES 2.0, and Blender 4.4’s default color management system.

You can build the program with any ACES or other color managers — just place them in the **ACES** folder.

## Features

- **Easy installation and removal of ACES**
- **Automatic backup of Blender’s original color management system**
- **Compatibility with current Blender versions (3.6+)**

## Build Dependencies

- **Python**: version 3.8 or higher (3.12 recommended)  
- **PySide**: version 6.9.1  
- **Nuitka**: version 2.7.12  
- **ordered-set**: version 4.1.0  
- **zstandard**: version 0.23.0  

*P.S.*: The `build.cmd` script will install all dependencies except Python.

## License

This project is distributed under the MIT License. See more details [here](LICENSE).
