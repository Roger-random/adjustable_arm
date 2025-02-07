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
3D-printed insert to help a 1/4"-20 hex bolt fit snugly within the channel of
an aluminum extrusion beam.

https://www.mcmaster.com/products/extrusions/t-slotted-framing-and-fittings~/t-slotted-framing-rail-profile~quad/system-of-measurement~inch/t-slotted-framing-rails-4/quad-rail-profile-style~quad/rail-width~2/
"""

import math
import cadquery as cq

def rail_insert():
    bolt_head_diameter = 11

    insert_length = 30

    channel_width = 17
    channel_height = 5.25

    # Surprise: workplane has no trapezoid function. Oh well, I can draw my own.
    trapezoid_profile_half = (
        cq.Workplane("XZ")
        .lineTo(channel_width/2, 0)
        .lineTo(channel_width/2 - channel_height, channel_height)
        .lineTo(0, channel_height)
        .close()
        .extrude(insert_length/2, both=True)
    )

    trapezoid_profile = trapezoid_profile_half + trapezoid_profile_half.mirror("YZ")

    trapezoid_profile = trapezoid_profile.faces("<Z").edges("|Y").fillet(1)
    trapezoid_profile = trapezoid_profile.faces("|Z").chamfer(1)

    rail_insert = (
        trapezoid_profile.faces("<Z").workplane()
        .polygon(6, bolt_head_diameter, circumscribed=True)
        .cutThruAll()
    )

    return rail_insert

if show_object:
    show_object(rail_insert(), options={"color":"blue", "alpha":0.5})
