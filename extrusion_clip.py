"""
MIT License

Copyright (c) 2025 Roger Cheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Clip a 1/4"-20 bolt to an aluminum extrusion beam, target is the 30mm x 30mm
beam used by Prusa Resarch for MK3 and MK4 line of printers.

https://github.com/prusa3d/Original-Prusa-i3/blob/MK3S/Frame/Extrusions.pdf
"""

import math
import cadquery as cq

# All coordinates below are drawn relative to the center of extrusion beam
# as (0,0) so most dimensions are divided in half for easier coordinate math.
extrusion_size_half = 15 # 30mm x 30mm extrusion but coordinate
extrusion_channel_entrance_half = 4
extrusion_channel_lip = 2

# Perimeter thickness should be:
# 1. Thin enough to be flexible for installation
# 2. Thick enough to be grip reliably
# 3. Multiple of nozzle diameter for easy printing
perimeter_thickness = 1.6
clip_length = 40

extra_gap = 0.1

# Profile for the clip itself. Top side hooks into the extrusion rail. Bottom
# has only a lip because hooks on both sides would be impossible to install.
# Bottom also has a small protrusion that I hope helps with uninstallation
perimeter_inner = extrusion_size_half
perimeter_outer = perimeter_inner + perimeter_thickness

lip_addon_x = extrusion_channel_entrance_half - perimeter_thickness/2

def perimeter_feature(length):
    return (
        cq.Workplane("XY")
        .lineTo(perimeter_thickness/2, 0, forConstruction = True)
        .radiusArc((-perimeter_thickness/2, 0), perimeter_thickness/2)
        .lineTo(-perimeter_thickness/2, length)
        .radiusArc((perimeter_thickness/2, length), perimeter_thickness/2)
        .close()
        .extrude(clip_length/2, both=True)
    )

clip_side = (
    perimeter_feature(extrusion_size_half*2 + perimeter_thickness + extra_gap*2)
    .translate(( extrusion_size_half + perimeter_thickness/2 + extra_gap,
                -extrusion_size_half - perimeter_thickness/2 - extra_gap, 0))
)

clip_top = (
    perimeter_feature(
        extrusion_size_half
        - extrusion_channel_entrance_half
        + perimeter_thickness
        + extra_gap)
    .rotate((0,0,0),(0,0,1), -90)
    .translate((extrusion_channel_entrance_half - perimeter_thickness/2,
                perimeter_inner + extra_gap  + perimeter_thickness/2))
)
clip_bottom = clip_top.mirror("XZ")

lip_top = (
    perimeter_feature(
        extrusion_channel_lip
        + perimeter_thickness/2
        + extra_gap)
    .translate((extrusion_channel_entrance_half - perimeter_thickness/2,
                perimeter_inner - extrusion_channel_lip))
)
lip_bottom = (
    perimeter_feature(extrusion_channel_lip/2 + extra_gap)
    .translate((extrusion_channel_entrance_half - perimeter_thickness/2,
                -perimeter_inner - extra_gap - perimeter_thickness/2))
)

hook_size = 1
top_hook = (
    perimeter_feature(hook_size)
    .rotate((0,0,0),(0,0,1), -135)
    .translate((lip_addon_x,  perimeter_inner - extrusion_channel_lip))
)

lever_size = 5
bottom_removal_lever = (
    perimeter_feature(lever_size)
    .rotate((0,0,0),(0,0,1), 135)
    .translate((lip_addon_x, -perimeter_inner - perimeter_thickness/2 - extra_gap))
)

clip_perimeter = clip_side + clip_top + clip_bottom + lip_top + lip_bottom + top_hook + bottom_removal_lever

show_object(clip_perimeter, options={"color":"blue", "alpha":0.5})
