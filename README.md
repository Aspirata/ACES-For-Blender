# Blender ACES Manager

Blender ACES Manager is a lightweight tool designed to simplify the installation and uninstallation of the ACES (Academy Color Encoding System) color management system for any Blender version. When installing ACES, the tool automatically creates a backup of Blender's original `colormanagement` folder to ensure safe and reversible changes.

## About ACES

The Academy Color Encoding System (ACES) is a standardized color management framework widely used in the film and visual effects industries. ACES ensures consistent, accurate, and natural-looking colors across different devices and workflows, making it an essential tool for professional-grade color grading and rendering.

**In plain terms**: ACES helps make colors in Blender look consistent and professional, like in big-budget movies! 🎥

## Supported ACES Versions

This tool supports the following ACES configurations:

- **ACES 1.3 Pro**  
  The ACES 1.3 version, compatible with Blender's 4.1 default color management system.  
  *Note: The source for ACES 1.3 Pro is not documented, so no download link is provided.*

- **[PixelManager v1.1.4](https://github.com/Joegenco/PixelManager/releases/tag/v.1.1.4)**  
  A collection of color management files, including ACES 1.3 and Blender 4.4's default color management system.

- **[PixelManager v2.0](https://github.com/Joegenco/PixelManager/releases/tag/v.2.0-RC3)**  
  An updated set of color management files, supporting ACES 1.3, ACES 2.0, and Blender 4.4's default color management system.

## Features

- **Easy Installation/Uninstallation**: Seamlessly install or remove ACES configurations in Blender with a single click.
- **Automatic Backups**: Safeguards Blender’s original `colormanagement` folder before applying changes.
- **Broad Compatibility**: Works with any Blender version, ensuring flexibility for users.
- **Multiple ACES Options**: Choose between ACES 1.3 Pro, PixelManager v1.1.4, or PixelManager v2.0.

## Requirements to Build

To build the Blender ACES Manager, you need the following:

- **Python**: Version 3.8 or higher (3.12 recommended)
- **PySide**: Version 6.9.1
- **PyInstaller**: Version 6.15.0

*Note*: The `build.cmd` script handles the installation of all dependencies except Python, which must be installed manually.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.