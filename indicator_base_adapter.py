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
Crude adapter to mount 3D printed adjustable arm on the magnetic base of a
non-magic-arm style indicator holder with two fasteners I found that fit.

Doing this right means getting on a lathe to create a shaft that has the two
appropriate threads and remove 3D printed plastic from the process
"""

import math
import cadquery as cq

block_height = 12.5

block = (
    cq.Workplane("XY")
    .rect(30,40)
    .extrude(block_height)
    ).edges("Z").fillet(3)

base_fastener_clear = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0,-7.5,0))
    .circle(4)
    .extrude(block_height)
)

arm_fastener_shaft = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 7.5,0))
    .circle(3.25)
    .extrude(block_height)
)

arm_fastener_hex = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 7.5,0))
    .polygon(6, 12, circumscribed=True)
    .extrude(4.2)
)

block_assembly = (
    block
    -base_fastener_clear
    -arm_fastener_shaft
    -arm_fastener_hex
).faces(">Z or <Z").chamfer(1)

show_object(block_assembly, options={"color" : "#ABCDEF", "alpha" : 0.5})
