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
Clamp a 1/4"-20 bolt head onto the spindle of a Bridgeport knee mill so we can
attach an indicator to tram the head.
"""

import math
import cadquery as cq

def bridgeport_spindle_clamp(
        radius,
        ring_height = 10,
        ring_thickness = 8, # Keep this a multiple of nozzle diameter
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
    ).faces(">Z").edges("|Y").fillet(5)


    hex_head_connection_x = radius + ring_thickness/2
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
        .lineTo(radius                 , -ring_height/2, forConstruction = True)
        .lineTo(radius + ring_thickness, -ring_height/2)
        .lineTo(radius + ring_thickness,  ring_height/2)
        .lineTo(radius                 , ring_height/2)
        .close()
        .revolve(360, (0,0,0), (0,1,0))
    ).faces("|Z").chamfer(2)

    slot_width = 2
    tab_width = slot_width + 8
    tab_length = 20
    tab = (
        cq.Workplane("XY")
        .rect(tab_width, tab_length)
        .extrude(ring_height/2, both=True)
        # Hole for fastener
        .faces(">X").workplane()
        .lineTo(-tab_length/2,0)
        .circle(3.5/2)
        .extrude(-tab_width, both=True, combine='cut')
    )

    slot = (
        cq.Workplane("XY")
        .rect(slot_width, tab_length*2)
        .extrude(ring_height/2, both=True)
    )

    tab_slot_offset = (0, -radius - tab_length/2 - ring_thickness/2, 0)
    clip = (
        ring
        + hex_head_connection
        + hex_head.translate((
            0,
            hex_head_connection_x
            + hex_head_connection_length,
            hex_head_side/2 + ring_height/2))
        + tab.translate(tab_slot_offset)
    )

    clip = clip - slot.translate(tab_slot_offset)

    return clip

if show_object:
    show_object(bridgeport_spindle_clamp(radius=48/2), options={"color":"blue", "alpha":0.5})
