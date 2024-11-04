# Phoca - Inkscape Remove Background (AI)

Inkscape extension for removing background in raster images


Phoca - Inkscape Remove Background (AI) extension is an Inkscape extension to help you easily remove backgrounds from raster images using AI and the remg library



See more info here: [Inkscape - Save As (Save As JPG, Save As WEBP, Save as AVIF, Save As PNG) Extension](https://www.phoca.cz/blog/1303-inkscape-save-as-save-as-jpg-save-as-webp-save-as-avif-save-as-png-extension)


Tested with Inkscape version 1.4

See video:

[https://youtu.be/a3KBT9g1pus](https://youtu.be/a3KBT9g1pus)

![Phoca - Inkscape Save As Extension](https://i.imgur.com/DODK5ku.png)

![Phoca - Inkscape Save As Options](https://i.imgur.com/CA3EwMm.png)

### How to install

Just follow Inkscape guides for installing Inkscape extensions (download the [ZIP package](https://www.phoca.cz/download/category/127-inkscape-save-as) and unzip it to Inkscape extension folder and restart Inkscape)

Inkscape extension folder you can find here: Inkscape - Edit - Preferences - System - Inkscape extensions

### Usage

- Make sure you have your remb library environment set up correctly on your computer, see Be aware section below
- Select raster image, click on Raster - Remove Image Background. Set options and click on Apply button
- Then the selected image should have its background removed using AI

### Be aware
- This extensions requires rembg and PIL library installed on your system, see: https://github.com/danielgatis/rembg
- This extension is for experienced users who have set up and tested the rembg library on their computer
- Removing image backgrounds using AI models can be a very challenging process. Therefore, it is a good idea to have your environment set up correctly and try first to remove the background of an image using the rembg library directly in the console
