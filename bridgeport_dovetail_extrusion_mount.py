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
Mount a 2" x 2" extrusion beam onto the ram dovetail of a Bridgeport mill

https://www.mcmaster.com/products/extrusions/t-slotted-framing-and-fittings~/t-slotted-framing-rail-profile~quad/system-of-measurement~inch/t-slotted-framing-rails-4/quad-rail-profile-style~quad/rail-width~2/
"""

# Original estimate values
estimated_dovetail_base_width = 133.35
dovetail_height = 25
estimated_dovetail_top_width = estimated_dovetail_base_width - dovetail_height*2

# Bridgeport dovetail is not 45 degrees! Adjust as per measurement against
# a test print with incorrect 45 degree dovetail.
lr_shift_adjustment = 2.5
adjusted_dovetail_base_width = estimated_dovetail_base_width + 10 - 6 - lr_shift_adjustment
adjusted_dovetail_top_width = estimated_dovetail_top_width + 10 - lr_shift_adjustment

# Placeholder built from measured dimensions of Bridgeport mill ram dovetail.
# Might be off by a tiny bit so design will need to be flexible.
def dovetail_placeholder():
    dovetail_half = (
        cq.Workplane("YZ")
        .lineTo(adjusted_dovetail_base_width/2, 0)
        .lineTo(adjusted_dovetail_top_width/2, dovetail_height)
        .lineTo(0, dovetail_height)
        .close()
        .extrude(35, both=True)
    ).faces("<Z").edges(">Y").chamfer(2)

    return (
        dovetail_half
        + dovetail_half.mirror("XZ")
    )

def extrusion_beam_placeholder():
    return (
        cq.Workplane("XZ")
        .rect(50.8, 50.8)
        .extrude(100, both=True)
    ).translate((0,0,-25.4))

def test_fit_plate_01():
    test_dovetail_base_width = 133.35
    beam_top_corner_x = test_dovetail_base_width/2 + 5
    plate_claw_thickness = 20
    plate_claw_height = 25

    test_beam_height = 20

    plate_half = (
        cq.Workplane("YZ")
        .lineTo(beam_top_corner_x, 0)
        .lineTo(beam_top_corner_x - plate_claw_height                       , plate_claw_height)
        .lineTo(beam_top_corner_x - plate_claw_height + plate_claw_thickness, plate_claw_height)
        .lineTo(beam_top_corner_x                     + plate_claw_thickness, 0)
        .lineTo(beam_top_corner_x                                           , -test_beam_height)
        .lineTo(0                                                           , -test_beam_height)
        .close()
        .extrude(6)
    )

    plate = plate_half + plate_half.mirror("XZ")

    return plate.translate((25.4,0,0))

if show_object:
    show_object(dovetail_placeholder(), options={"color":"red", "alpha":0.5})
    show_object(extrusion_beam_placeholder(), options={"color":"red", "alpha":0.5})
    show_object(test_fit_plate_01(), options={"color":"green", "alpha":0.5})
