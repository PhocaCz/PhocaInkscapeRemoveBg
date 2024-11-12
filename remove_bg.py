#! /usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Jan Pavelka https://www.phoca.cz
# Version: 1.0

import sys
import os
import re
import subprocess
import math
import inkex
import tempfile
from distutils.spawn import find_executable
from subprocess import PIPE, Popen
from inkex.command import call
inkex.localization.localize

from lxml import etree
import base64

from rembg import new_session, remove
from PIL import Image, ImageEnhance, ImageChops, ImageOps
import subprocess

import warnings

class RemoveBackgroundLayer(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--tab")
        self.arg_parser.add_argument("--model",                 action="store", type=str,             dest="model",                  default="u2net")

        self.arg_parser.add_argument("--post_process_mask",  action="store", type=inkex.Boolean,   dest="post_process_mask",  default=True)

        self.arg_parser.add_argument("--alpha_matting",  action="store", type=inkex.Boolean,   dest="alpha_matting",  default=True)

        self.arg_parser.add_argument("--alpha_matting_foreground_threshold",                action="store", type=int,             dest="alpha_matting_foreground_threshold",                default="240")

        self.arg_parser.add_argument("--alpha_matting_background_threshold",                action="store", type=int,             dest="alpha_matting_background_threshold",                default="10")

        self.arg_parser.add_argument("--alpha_matting_erode_size",                action="store", type=int,             dest="alpha_matting_erode_size",                default="40")

        self.arg_parser.add_argument("--debug",  action="store", type=inkex.Boolean,   dest="debug",  default=False)

    def objects_to_paths(self, elements, replace=True):
        for node in list(elements.values()):
            elem = node.to_path_element()
            if replace:
                node.replace_with(elem)
                elem.set('id', node.get('id'))
            elements[elem.get('id')] = elem

    def select_area(self):
        opt = self.options
        x0 = y0 = y1 = x0 = None
        scale       = self.svg.unittouu('1px')
        # convert objects to path to not wrongly count the selection.bounding.box()
        self.objects_to_paths(self.svg.selected, True)
        bbox        = self.svg.selection.bounding_box()

        x0 = math.ceil(bbox.left/scale)
        x1 = math.ceil(bbox.right/scale)
        y0 = math.ceil(bbox.top/scale)
        y1 = math.ceil(bbox.bottom/scale)
        points = [x0, y0, x1, y1]
        return points

    def effect(self):
        opt                         = self.options

        with tempfile.TemporaryDirectory() as temp_dir:

            # inkex.utils.debug(temp_dir)
            self.options.temp_file      = temp_dir + "/phocaRemoveBgInput.png"
            self.options.source_file    = opt.input_file
            self.options.dest_file      = temp_dir + "/phocaRemoveBgOutput.png"
            self.options.dpi            = '300'

            self.remove_bg()

    def remove_bg(self):

        opt = self.options
        # inkex.utils.debug(opt.model)

        if not opt.debug:
            warnings.filterwarnings("ignore", category=ResourceWarning, message=".*TemporaryDirectory.*")

        # https://gitlab.com/inkscape/inkscape/-/issues/4163
        os.environ["SELF_CALL"] = "true"

        filename, file_extension = os.path.splitext(opt.dest_file)

        selected_objects = self.svg.selected
        for obj_id, obj in selected_objects.items():
            imageObjectId = obj.get('id')
            imageObject = obj

        # Create PNG with inkscape
        cmd = ['inkscape']
        # cmd.append("-C")
        # inkscape --export-type=png --export-filename=test2.png --export-id=path7 --export-id-only --export-background-opacity=0 test.svg

        if len(self.svg.selected) == 0:
            inkex.errormsg(_('Please select some image object'))
            sys.exit()

        #c = self.select_area()
        #cmd.append("--export-area ")
        #cmd.append("{}:{}:{}:{}".format(c[0], c[1], c[2], c[3]))

        cmd.append("--export-type=png" )
        #cmd.append("\"{}\"".format('png'))

        # cmd.append("--export-dpi=" + format(opt.dpi))
        #cmd.append("\"{}\"".format(opt.dpi))
        cmd.append("--export-filename=" + "\"" + format(opt.temp_file) + "\"")
        #cmd.append("\"{}\"".format(opt.temp_file))

        cmd.append("--export-id=" + "\"" + format(imageObjectId) + "\"")
        #cmd.append("\"{}\"".format(imageObjectId))

        cmd.append("--export-id-only")

        cmd.append("--export-background-opacity=0")
        #cmd.append("\"{}\"".format(0))

        cmd.append("\"{}\"".format(opt.source_file))
        cmd = ' '.join(cmd)
        # inkex.utils.debug(f"Path: {cmd}")
        # stdout=subprocess.DEVNULL,
        if (opt.debug):
            p = subprocess.Popen(cmd, shell=True)
        else:
            p = subprocess.Popen(cmd, shell=True, stderr=subprocess.DEVNULL)
        #inkex.utils.debug(f"Path: {cmd}")
        p.wait()

        imageTemp = Image.open(opt.temp_file)
        session = new_session(opt.model)

        # inkex.utils.debug(opt.alpha_matting_erode_size)
        imageWithoutBg = remove(imageTemp, session=session, post_process_mask=opt.post_process_mask, alpha_matting=opt.alpha_matting, alpha_matting_foreground_threshold=opt.alpha_matting_foreground_threshold, alpha_matting_background_threshold=opt.alpha_matting_background_threshold, alpha_matting_erode_size=opt.alpha_matting_erode_size)

        imageWithoutBg.save(opt.dest_file)

        with open(opt.dest_file, "rb") as png_file:
            png_data = png_file.read()
            png_base64 = base64.b64encode(png_data).decode('utf-8')

        x = float(imageObject.get('x', '0'))
        y = float(imageObject.get('y', '0'))
        width = float(imageObject.get('width', '100'))
        height = float(imageObject.get('height', '100'))

        imageToPaste = etree.Element(inkex.addNS('image', 'svg'))
        #imageToPaste = inkex.Image()
        imageToPaste.set(inkex.addNS('href', 'xlink'), f"data:image/png;base64,{png_base64}")
        imageToPaste.set('x', str(x))
        imageToPaste.set('y', str(y))
        imageToPaste.set('width', str(width))
        imageToPaste.set('height', str(height))

        parent = imageObject.getparent()
        parent.remove(imageObject)
        parent.append(imageToPaste)

        #inkex.utils.debug(opt.model)
        #inkex.errormsg("\n\n========================================\n")
        #inkex.errormsg(_('Background removed with model:') + ' ' + format(opt.model))
        #inkex.errormsg("\n========================================\n\n")
        #sys.exit()
        return


if __name__ == "__main__":
    RemoveBackgroundLayer().run()
