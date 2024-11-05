# Phoca - Inkscape Remove Background (AI)

Inkscape extension for removing background in raster images

Phoca - Inkscape Remove Background (AI) extension is an Inkscape extension to help you easily remove backgrounds from raster images using AI and the remg library

See more info here: [Inkscape - Remove Image Background (AI) Extension ](https://www.phoca.cz/blog/1342-inkscape-remove-image-background-ai-extension)

Tested with Inkscape version 1.4

See video:

[https://youtu.be/Ryelh_9TUdA](https://youtu.be/Ryelh_9TUdA)

![Phoca - Inkscape Save As Extension](https://i.imgur.com/8YZhu2b.png)

![Phoca - Inkscape Save As Options](https://i.imgur.com/KhXItaH.png)

![Phoca - Inkscape Save As Options](https://i.imgur.com/iJvN9Wc.png)

### How to install

Just follow Inkscape guides for installing Inkscape extensions (download the [ZIP package](https://www.phoca.cz/download/126-inkscape/136-inkscape-remove-background) and unzip it to Inkscape extension folder and restart Inkscape)

Inkscape extension folder you can find here: Inkscape - Edit - Preferences - System - Inkscape extensions

### Usage

- Make sure you have your Rembg library environment set up correctly on your computer, see Be aware section below.
- Select raster image, click on Raster - Remove Image Background. Set options and click on Apply button.
- Then the selected image should have its background removed using AI.

### Be aware
- This extensions requires Rembg and PIL libraries (and their dependencies) installed on your system, see: [Rembg](https://github.com/danielgatis/rembg)
- This extension is for experienced users who have set up and tested the Rembg - a Python library on their computer.
- Removing image backgrounds using AI models can be a very challenging process. Therefore, it is a good idea to have your environment set up correctly and try first to remove the background of an image using the Rembg library directly in the console.
