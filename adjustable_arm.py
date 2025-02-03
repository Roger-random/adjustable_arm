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
Experiment into designing a 3D-printable articulated arm mechanism that has
three joints that are all tightened/loosened simultaneously with a single
knob. Frequently seen sold as "Magic Arm". Larger units are sold for holding
photography equipment in place, smaller units can be found sold as indicator
holder for machinists.
"""

import math
import cadquery as cq

# The ball for the ball-and-socket joint at the effector end

ball_diameter = 20
fastener_diameter = 6.5
fastener_diameter_tight = 6
fastener_thread_pitch = 1.2
fastener_hex_thickness = 5.7
fastener_hex_width = 11.25
nozzle_diameter = 0.4
ball_surround_gap = 0.2
cutoff_z = -ball_diameter*math.sin(math.radians(45))/2
wedge_range_horizontal = 2

reposition_for_printing = False

end_ball = (
    cq.Workplane("XY")
    .sphere(ball_diameter/2)
    )

end_ball_fastener_shaft = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0,
                                  fastener_thread_pitch + fastener_hex_thickness / 2))
    .circle(fastener_diameter/2)
    .extrude(-ball_diameter)
    )

end_ball_fastener_nut = (
    cq.Workplane("XY")
    .polygon(6, fastener_hex_width, circumscribed = True)
    .extrude(fastener_hex_thickness/2, both=True)
    )

end_ball_assembly = (
    end_ball
    - end_ball_fastener_shaft
    - end_ball_fastener_nut
    )

# Create the socket surrounind the ball
ball_surround_thickness = 5
ball_surround_inner_radius = ball_surround_gap + ball_diameter/2
ball_surround_outer_radius = ball_surround_thickness + ball_diameter/2
ball_surround_inner_45 = ball_surround_inner_radius/math.sqrt(2)
ball_surround_outer_45 = ball_surround_outer_radius/math.sqrt(2)

ball_surround_outer = (
    cq.Workplane("YZ")
    .sphere(ball_surround_thickness + ball_diameter/2)
    )

# Cut a cone so the end lug can swivel around freely in a 90 degree cone
lug_clearance = (
    cq.Workplane("YZ")
    .lineTo(fastener_diameter/2, 0)
    .lineTo(-ball_diameter, ball_diameter + fastener_diameter/2)
    .lineTo(-ball_diameter, 0)
    .close()
    .revolve(360, (0,0,0), (1,0,0))
    )
ball_surround_outer = ball_surround_outer - lug_clearance

# Build the arm connecting to the ball joint
arm_length = 50
arm_side_outer = ball_surround_outer_45*2
rod_side = arm_side_outer - ball_surround_thickness
arm_side_inner = rod_side + ball_surround_gap * 4

# Outer shell will link the ball-and-socket to center (mid) joint
arm_outer_shell = (
    cq.Workplane("XZ")
    .transformed(rotate=cq.Vector(0,0,45))
    .rect(arm_side_outer, arm_side_outer)
    .extrude(-arm_length)
    .edges("|Y")
    .fillet(ball_surround_thickness/2)
    )

# Channel inside for rod that transmits pushing force from mid joint to
# ball in socket
arm_actuating_rod_channel = (
    cq.Workplane("XZ")
    .transformed(rotate=cq.Vector(0,0,45))
    .rect(arm_side_inner, arm_side_inner)
    .extrude(-arm_length-ball_surround_gap*2)
    )

# Rod that transmits pushing force from mid joint to ball in socket
arm_actuating_rod = (
    cq.Workplane("XZ")
    .transformed(rotate=cq.Vector(0,0,45))
    .transformed(offset=cq.Vector(0, 0, -wedge_range_horizontal))
    .rect(rod_side, rod_side)
    .extrude(wedge_range_horizontal - arm_length)
    .edges("|Y")
    )

# The actual "socket" part of ball and socket
arm_end_ball_cavity = (
    cq.Workplane("YZ")
    .sphere(ball_surround_gap + ball_diameter/2)
    )

# Mid joint structure
mid_joint = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(ball_surround_outer_radius + nozzle_diameter * 2)
    .extrude(ball_surround_outer_radius, both = True)
    )

wedge_fastener_diameter = 6.5
wedge_angle = 25
wedge_range_vertical = wedge_range_horizontal / math.tan(math.radians(wedge_angle))

wedge_block_upper_slice = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .transformed(rotate=cq.Vector(-wedge_angle,0,0))
    .rect(ball_surround_outer_radius * 4,
          ball_surround_outer_radius * 4)
    .extrude(ball_surround_outer_radius * 4)
    )

wedge_diameter = rod_side / math.sin(math.radians(45))
wedge_block_mid = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(wedge_diameter/2)
    .extrude(ball_surround_outer_radius, both=True)
    )

# TODO: Combine shapes into a single 2D wire that is extruded, instead of
# combining via three extrusions.
wedge_block_lower_fastener_slot = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(wedge_fastener_diameter/2)
    .extrude(ball_surround_outer_radius, both = True)
    ) + (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length + wedge_range_horizontal, 0))
    .circle(wedge_fastener_diameter/2)
    .extrude(ball_surround_outer_radius, both = True)
    ) + (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length + wedge_range_horizontal/2, 0))
    .rect(wedge_fastener_diameter, wedge_range_horizontal)
    .extrude(ball_surround_outer_radius, both = True)
    )

mid_joint_clearance_size = wedge_diameter + ball_surround_gap * 2
mid_joint_clearance = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(mid_joint_clearance_size/2)
    .extrude(ball_surround_outer_radius, both = True)
    ) + (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length - wedge_range_horizontal/2, 0))
    .rect(mid_joint_clearance_size, wedge_range_horizontal)
    .extrude(ball_surround_outer_radius, both = True)
    ) + (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length - wedge_range_horizontal, 0))
    .circle(mid_joint_clearance_size/2)
    .extrude(ball_surround_outer_radius, both = True)
    )

arm_actuating_rod = (
    arm_actuating_rod
    + wedge_block_mid
    - wedge_block_upper_slice
    - wedge_block_lower_fastener_slot
    )

# Wedge that will push on the actuating rod in its full size. Expected to be
# trimmed for different application: one on near side of knob to carry its
# pressure, and one on far side of knob hosting a hex bolt head.
wedge_block_upper_full_height = (
    wedge_block_mid
    .intersect(wedge_block_upper_slice)
    ) - (
    # Hole through the middle for fastener
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(wedge_fastener_diameter/2)
    .extrude(wedge_diameter/2, both=True)
    )

wedge_hex_z = (
    # Minimum Z
    fastener_hex_width * math.tan(math.radians(wedge_angle)) / 2
    # Plus a nonzero big of plastic to support the hex bolt at minimum point
    + 1.2
    )

wedge_block_hex_bolt_head = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, wedge_hex_z))
    .transformed(rotate=cq.Vector(0, 0, 30))
    .polygon(6, fastener_hex_width, circumscribed = True)
    .extrude(fastener_hex_thickness)
    )

mid_joint_trim = (
    # Volume above the top of hex head.
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, wedge_hex_z + fastener_hex_thickness))
    .circle(ball_surround_outer_radius)
    .extrude(ball_surround_outer_radius * 2)
    )

wedge_block_hex_bolt = (
    wedge_block_upper_full_height
    - mid_joint_trim
    - wedge_block_hex_bolt_head
    )

if reposition_for_printing:
    show_object(
        wedge_block_hex_bolt
        .translate((ball_surround_outer_radius*2,-arm_length,0))
        .rotate((0, 0, 0), (1, 0, 0), wedge_angle),
        options={"color":"red", "alpha":0.5})
else:
    show_object(wedge_block_hex_bolt, options={"color":"red", "alpha":0.5})

# Assemble half of the arm. Print this twice for the three-jointed mechanism.
arm = (
    ball_surround_outer
    + arm_outer_shell
    + mid_joint
    - arm_actuating_rod_channel
    - mid_joint_clearance
    - mid_joint_trim.translate((0,0,-wedge_range_vertical))
    + arm_actuating_rod
    - arm_end_ball_cavity
    )


"""
knob_height = 20
knob_bottom = 0.6

knob_hex_head = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(
        0,
        arm_length,
        mid_joint_ramp_height/2 + mid_joint_ramp_vertical_offset + knob_bottom))
    .polygon(6, 11, circumscribed = True)
    .extrude(knob_height)
    )

knob = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(
        0,
        arm_length,
        mid_joint_ramp_height/2 + mid_joint_ramp_vertical_offset))
    .polygon(12,
        mid_joint_diameter - mid_joint_shell_perimeter*2,
        circumscribed = False)
    .circle(mid_joint_fastener_diameter/2)
    .extrude(knob_height)
    .faces(">Z")
    .fillet(2)
    ) - knob_hex_head

show_object(knob, options={"color":"green","alpha":0.5})
"""

combined = end_ball_assembly + arm

chop = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0,0,cutoff_z))
    .rect(arm_length*3,arm_length*3)
    .extrude(-ball_surround_outer_radius)
    )
if reposition_for_printing:
    show_object((combined - chop).translate((0,0,-cutoff_z)), options={"color":"blue", "alpha":0.5})
else:
    show_object(combined - chop, options={"color":"blue", "alpha":0.5})

# 2345678901234567890123456789012345678901234567890123456789012345678901234567890
