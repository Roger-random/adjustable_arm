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
Attach a simple round platform to a 1/4"-20 hex bolt head
"""

def round_platform(radius=30):
    bolt_head_diameter = 11
    bolt_head_thickness = 4.25
    bolt_shaft_diameter = 6.5

    hex_head_side = 18

    flat = (
        cq.Workplane("XY")
        .circle(radius)
        .extrude(1.2)
    )

    hex_head = (
        cq.Workplane("XZ")
        .rect(hex_head_side, hex_head_side)
        .circle(bolt_shaft_diameter/2)
        .extrude(bolt_head_thickness+2)
        .faces("<Y")
        .polygon(6, bolt_head_diameter, circumscribed=True)
        .extrude(-bolt_head_thickness, combine='cut')
    )

    platform = flat + hex_head.translate((0, +radius, hex_head_side/2))

    # Cosmetic fillets
    platform = platform.faces(">Z").edges("|Y").fillet(bolt_head_diameter/2)
    platform = platform.faces(">Z").edges("|X").fillet(1)
    platform = platform.faces("<Z[1]").edges("%Line").fillet(2)
    platform = platform.faces("<Z[1]").chamfer(0.6)

    return platform

if show_object:
    show_object(round_platform(), options={"color":"blue", "alpha":0.5})