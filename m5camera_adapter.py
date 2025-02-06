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
Clip a M5CAMERA to a 1/4"-20 hex bolt head, using the M5CAMERA's mounting
points compatible with studless LEGO beams.
"""

lego_pin_length = 15.25
lego_pin_hole_diameter = 4.85
lego_pin_lip_diameter = 6.22
lego_pin_lip_depth = 1

def lego_pin():
    center = (
        cq.Workplane("XY")
        .circle(lego_pin_hole_diameter/2)
        .extrude(lego_pin_length/2)
    )

    top_lip = (
        cq.Workplane("XY")
        .circle(lego_pin_lip_diameter/2)
        .extrude(lego_pin_lip_depth)
    )

    bottom_lip = top_lip.translate((0,0,lego_pin_length/2 - lego_pin_lip_depth))

    return center + top_lip + bottom_lip


def camera_adapter():
    bolt_head_diameter = 11
    bolt_head_thickness = 4.25
    bolt_shaft_diameter = 6.5
    pin_spacing_half = 32.2 / 2

    block = (
        cq.Workplane("XY")
        .rect(bolt_head_diameter*2, 45)
        .circle(bolt_shaft_diameter/2)
        .extrude(lego_pin_length/2)
        .edges("|Z").fillet(bolt_head_diameter-1)
        .faces("|X").chamfer(1)
        .faces(">Z").workplane()
        .polygon(6, bolt_head_diameter, circumscribed=True)
        .extrude(-bolt_head_thickness, combine='cut')
    )

    return (
        block
        -lego_pin().translate((0,  pin_spacing_half, 0))
        -lego_pin().translate((0, -pin_spacing_half, 0))
    )

if show_object:
    show_object(camera_adapter(), options={"color":"blue", "alpha":0.5})
