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
Attach a ring LED circuit board of specified diameter to a 1/4"-20 bolt head
"""

import math
import cadquery as cq

def ring_led_clip(
        radius=30,
        ring_height = 4,
        ring_thickness = 8, # Keep this a multiple of nozzle diameter
        clip_angular_length = 60 # Each clip occupies this number of degrees of arc
        ):
    bolt_head_diameter = 11
    bolt_head_thickness = 4.25
    bolt_shaft_diameter = 6.5

    hex_head_side = 18

    hex_head_thickness = bolt_head_thickness+2
    hex_head = (
        cq.Workplane("XZ")
        .rect(hex_head_side, hex_head_side)
        .circle(bolt_shaft_diameter/2)
        .extrude(hex_head_thickness)
        .faces("<Y")
        .polygon(6, bolt_head_diameter, circumscribed = True)
        .extrude(-bolt_head_thickness, combine='cut')
    )

    hex_head_connection_x = radius + ring_thickness - math.tan(math.asin((hex_head_side/2)/radius))*(hex_head_side/4)
    hex_head_connection_length = 10 + hex_head_thickness
    hex_head_connection = (
        cq.Workplane("YZ")
        .lineTo(hex_head_connection_x,                               ring_height/2, forConstruction = True)
        .lineTo(hex_head_connection_x,                              -ring_height/2)
        .lineTo(hex_head_connection_x + hex_head_connection_length, -ring_height/2)
        .lineTo(hex_head_connection_x + hex_head_connection_length,  ring_height/2)
        .close()
        .extrude(hex_head_side/2, both = True)
    )

    ring = (
        cq.Workplane("YZ")
        .lineTo(radius, 0, forConstruction = True)
        .lineTo(radius + ring_thickness, 0)
        .lineTo(radius + ring_thickness, ring_height/2)
        .lineTo(radius, ring_height/2)
        .close()
        .revolve(240+clip_angular_length, (0,0,0), (0,1,0))
    )

    claw = (
        cq.Workplane("YZ")
        .lineTo(radius, 0, forConstruction = True)
        .lineTo(radius-ring_height/2, ring_height/2)
        .lineTo(radius,ring_height/2)
        .close()
        .revolve(clip_angular_length, (0,0,0), (0,1,0))
    )

    clip_half = (
        ring.rotate((0,0,0),(0,0,1),   -120 - clip_angular_length/2)
        + claw.rotate((0,0,0),(0,0,1),      - clip_angular_length/2)
        + claw.rotate((0,0,0),(0,0,1),  120 - clip_angular_length/2)
        + claw.rotate((0,0,0),(0,0,1), -120 - clip_angular_length/2)
    )

    clip = (
        clip_half
        + clip_half.mirror("XY")
        + hex_head_connection
        + hex_head.translate((
            0,
            hex_head_connection_x
            + hex_head_connection_length,
            hex_head_side/2))
    )

    clip = clip.edges(">Y").edges("|Z").fillet(2)
    clip = clip.edges(">Z[1]").fillet(5)
    clip = clip.edges(">Y").edges(">Z").fillet(2)
    return clip

if show_object:
    show_object(ring_led_clip(60), options={"color":"blue", "alpha":0.5})
