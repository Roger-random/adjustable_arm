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
Clip a 3/8" indicator shaft to a 1/4"-20 hex bolt head.
"""

def indicator_holder():
    bolt_head_diameter = 11
    bolt_head_thickness = 4.25
    bolt_shaft_diameter = 6.5

    head_block_side = 15
    head_block_thickness = bolt_head_thickness + 2

    head_block = (
        cq.Workplane("YZ")
        .rect(head_block_side, head_block_side)
        .circle(bolt_shaft_diameter/2)
        .extrude(head_block_thickness)
        .faces("<X")
        .polygon(6, bolt_head_diameter, circumscribed=True)
        .extrude(bolt_head_thickness, combine='cut')
    )

    nozzle_diameter = 0.4
    slit_width = 1
    indicator_shaft_diameter = 9.45
    indicator_block_width = indicator_shaft_diameter + nozzle_diameter*4
    indicator_block_length = indicator_shaft_diameter * 3
    indicator_block_height = head_block_side
    indicator_shaft_position = indicator_block_length/2 - indicator_shaft_diameter * 1.25

    indicator_block = (
        cq.Workplane("XY")
        .rect(indicator_block_length, indicator_block_width)
        .extrude(indicator_block_height/2, both=True)
        # Cut hole for indicator shaft
        .faces(">X")
        .transformed(offset=cq.Vector((-indicator_shaft_position, 0, 0)))
        .circle(indicator_shaft_diameter/2)
        .cutThruAll()
        # Cut slit for indicator shaft
        .faces(">X")
        .transformed(offset=cq.Vector((- indicator_block_length/2 + indicator_shaft_diameter, 0, 0)))
        .rect(indicator_shaft_diameter*2, slit_width,)
        .cutThruAll()
    )

    indicator_fastener = (
        cq.Workplane("XZ")
        .transformed(offset=cq.Vector((-indicator_block_length/2 + 3.5, 0, 0)))
        .circle(3.5/2)
        .extrude(indicator_block_width, both=True)
    )

    indicator_block = indicator_block - indicator_fastener

    combined = head_block + indicator_block.translate(
        (head_block_thickness - indicator_block_length/2,
         head_block_side/2 + indicator_block_width/2, 0))

    # Cosmetic fillets
    combined = combined.faces("|X").faces(">X[2]").edges(">Y").fillet(1)
    combined = combined.faces(">Y").edges(">X").fillet(head_block_thickness)
    combined = combined.faces("<Y").edges("|Z").fillet(1)

    return combined

if show_object:
    show_object(indicator_holder(), options={"color":"blue", "alpha":0.5})
