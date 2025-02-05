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
minimum_gap = 0.2
cutoff_z = -ball_diameter*math.sin(math.radians(45))/2
wedge_range_horizontal = 2

reposition_for_printing = False

end_ball = (
    cq.Workplane("XY")
    .sphere(ball_diameter/2)
    )

# This is the visible opening, diameter for a loose fastener fit so it can
# be installed easily.
end_ball_fastener_shaft = (
    cq.Workplane("XY")
    .circle(fastener_diameter/2)
    .extrude(-ball_diameter)
    )

# In the middle of the ball is space for a hex nut that can be dropped in
# during printing.
end_ball_fastener_nut = (
    cq.Workplane("XY")
    .polygon(6, fastener_hex_width, circumscribed = True)
    .extrude(fastener_hex_thickness/2, both=True)
    )

# Beyond the nut is a somewhat cone/pagoda shaped cavity that will neck down
# to a very tight fit around the fastener. The fastener will likely cut some
# thread into this plastic but the tread isn't the point, the point is friction
# so the fastener doesn't back out too easily. This is similar in concept to
# nuts with a plastic insert, except here our metal nut is to be added during
# printing and this is the "plastic insert"
end_ball_cone = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, fastener_hex_thickness / 2))
    .polygon(6, fastener_hex_width, circumscribed = True)
    .workplane(offset = (fastener_hex_width - fastener_diameter_tight) / 4)
    .circle(fastener_diameter_tight/2)
    .loft()
    .faces(">Z").workplane()
    .circle(fastener_diameter_tight/2)
    .extrude(fastener_thread_pitch*2)
    .faces(">Z").workplane()
    .circle(fastener_diameter_tight/2)
    .workplane(offset=fastener_diameter_tight/4)
    .circle(minimum_gap)
    .loft()
    )

end_ball_assembly = (
    end_ball
    - end_ball_fastener_shaft
    - end_ball_fastener_nut
    - end_ball_cone
    )

# Create the socket surrounind the ball
ball_surround_thickness = 5
ball_surround_inner_radius = minimum_gap + ball_diameter/2
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
arm_length = 200
arm_side_outer = 16
rod_side = arm_side_outer - ball_surround_thickness
arm_side_inner = rod_side + minimum_gap * 4

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
actuating_rod_channel = (
    cq.Workplane("XZ")
    .transformed(rotate=cq.Vector(0,0,45))
    .rect(arm_side_inner, arm_side_inner)
    .extrude(-arm_length-minimum_gap*2)
    )

# Rod that transmits pushing force from mid joint to ball in socket
actuating_rod = (
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
    .sphere(minimum_gap + ball_diameter/2)
    )

# Mid joint structure
mid_joint_radius = ball_surround_outer_radius + nozzle_diameter * 2
mid_joint = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(mid_joint_radius)
    .extrude(ball_surround_outer_radius, both = True)
    )

wedge_fastener_diameter = 6.5
wedge_angle = 25
wedge_range_vertical = wedge_range_horizontal * math.tan(math.radians(wedge_angle))

# This block is used to split the upper from lower parts of the pressure wedge
# mechanism. I think its purpose can be replaced with a workplane split()
# command but I don't understand split() yet and I can't predict its behavior.
wedge_block_upper_slice = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .transformed(rotate=cq.Vector(-wedge_angle,0,0))
    .rect(ball_surround_outer_radius * 4,
          ball_surround_outer_radius * 4)
    .extrude(ball_surround_outer_radius * 4)
    )

# The wedge block is the starting point for tailoring the pressure wedge
wedge_diameter = (ball_surround_outer_radius - wedge_range_horizontal - nozzle_diameter * 4 )*2  # rod_side / math.sin(math.radians(45))
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

mid_joint_clearance_size = wedge_diameter + (minimum_gap * 4 / math.sin(math.radians(45)))
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

# Reinforce the section between end ball and mid joint
tie_length = rod_side * math.sin(math.radians(45))
tie_width = 6
tie_height = 1.8
tie_gap = 0.4 # Must be at least 1 layer height

tie = (
    cq.Workplane("YZ")
    .lineTo(tie_width,            0)
    .lineTo(tie_width-tie_height, tie_height)
    .lineTo(          tie_height, tie_height)
    .close()
    .extrude(tie_length/2, both=True)
    )

tie_clearance = (
    cq.Workplane("YZ")
    .lineTo(                                                            -minimum_gap, 0)
    .lineTo(                                      tie_height + tie_gap - minimum_gap, tie_height+tie_gap)
    .lineTo( wedge_range_horizontal + tie_width - tie_height - tie_gap + minimum_gap, tie_height+tie_gap)
    .lineTo( wedge_range_horizontal + tie_width                        + minimum_gap, 0)
    .close()
    .extrude(tie_length/2, both=True)
    )

tie_start = ball_surround_outer_radius - tie_width/2
tie_span = arm_length - ball_surround_outer_radius - mid_joint_radius - tie_width/2

# Calculate how many ties will be added. There should always be at least two,
# one at each end. If the beam is long enough, additional ties are added in
# between.
extra_ties_count = math.floor(tie_span/40)
tie_spacing = tie_span
if extra_ties_count > 0:
    tie_spacing = tie_span / (extra_ties_count+1)

for t in range(2 + extra_ties_count):
    actuating_rod = actuating_rod - tie_clearance.translate((0, tie_start + tie_spacing*t, cutoff_z))

# Assembly of center actuation rod
actuating_rod = (
    actuating_rod
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
    .edges("<Z")
    .chamfer(wedge_range_vertical/2)
    ) - (
    # Hole through the middle for fastener
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(wedge_fastener_diameter/2)
    .extrude(wedge_diameter, both=True)
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

mid_joint_trim_radius = mid_joint_radius - nozzle_diameter*2
mid_joint_trim = (
    # Volume used for trimming objects in order to fit in mid joint
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, 0))
    .circle(mid_joint_trim_radius)
    .extrude(ball_surround_outer_radius * 2)
    )

# Variation of upper block that hosts a hex head bolt.
wedge_block_hex_bolt = (
    wedge_block_upper_full_height
    - mid_joint_trim.translate((0, 0, wedge_hex_z + fastener_hex_thickness))
    - wedge_block_hex_bolt_head
    ).edges(">Z").chamfer(wedge_range_vertical/2)

# Variation of upper block that does not host a hex head, to be paired with a
# knob which will host a hex nut.
wedge_block_z = wedge_range_vertical + wedge_diameter * math.tan(math.radians(wedge_angle)) / 2
wedge_block_no_hex = (
    wedge_block_upper_full_height
    - mid_joint_trim.translate((0, 0, wedge_block_z))
    ).edges(">Z").chamfer(wedge_range_vertical/2)

# Show one or the other upper block variations during in-place visualization.
# When preparing for printing, display both in their print orientations.
if reposition_for_printing:
    show_object(
        wedge_block_hex_bolt
        .translate((ball_surround_outer_radius*2,-arm_length,0))
        .rotate((0, 0, 0), (1, 0, 0), wedge_angle),
        options={"color":"red", "alpha":0.5})
    show_object(
        wedge_block_no_hex
        .translate((-ball_surround_outer_radius*2,-arm_length,0))
        .rotate((0, 0, 0), (1, 0, 0), wedge_angle),
        options={"color":"red", "alpha":0.5})
else:
    #show_object(wedge_block_hex_bolt, options={"color":"red", "alpha":0.5})
    show_object(wedge_block_no_hex, options={"color":"red", "alpha":0.5})

# Assemble half of the arm. Print this twice for the three-jointed mechanism.
arm = (
    ball_surround_outer
    + arm_outer_shell
    + mid_joint
    - actuating_rod_channel
    - mid_joint_clearance
    - mid_joint_trim.translate((0, 0, wedge_block_z - wedge_range_vertical * 2))
    + actuating_rod
    - arm_end_ball_cavity
    )

for t in range(2 + extra_ties_count):
    arm = arm + tie.translate((0, tie_start + tie_spacing*t, cutoff_z))

# Knob parameters
knob_base_taper_height = wedge_block_z + ball_surround_outer_radius - wedge_diameter/2
knob_base_vertical_height = ball_surround_outer_radius + wedge_range_vertical*3
knob_base_radius = mid_joint_trim_radius - minimum_gap
knob_wing_radius = 35
knob_wing_thickness = 30
knob_wing_height = ball_surround_outer_radius + (knob_wing_radius - ball_surround_outer_radius)
knob_bottom = 1.8

# Clearance for the hex nut to be hosted inside nut
knob_hex_head = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, arm_length, wedge_block_z + knob_bottom))
    .polygon(6, fastener_hex_width, circumscribed = True)
    .extrude(knob_wing_height)
    )

# Revolve operation to create external volume of knob
knob = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, 0, -arm_length))
    # Base will stay intact
    .lineTo(0,                wedge_block_z, forConstruction = True)
    .lineTo(wedge_diameter/2, wedge_block_z)
    .lineTo(knob_base_radius, knob_base_taper_height)
    .lineTo(knob_base_radius, knob_base_vertical_height)
    # Top will be trimmed to form wings
    .lineTo(knob_wing_radius, knob_wing_height)
    .lineTo(0,                knob_wing_height)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
    .edges(">Z").fillet(5)
    .faces("<Z").workplane()
    .circle(fastener_diameter/2)
    .cutThruAll()
    ) - knob_hex_head

# Block to cut symmetric chunks out of the knob to create a wingnut shape
knob_removal = (
    cq.Workplane("XZ")
    .lineTo(knob_wing_thickness/2, ball_surround_outer_radius*2, forConstruction = True)
    .rect(knob_wing_radius, knob_wing_height, centered = False)
    .extrude(- arm_length - knob_wing_radius*2)
    .edges("|Y")
    .fillet(5)
    )

knob = knob - knob_removal - knob_removal.mirror("YZ")
show_object(knob, options={"color":"green","alpha":0.5})

# Complex single print object becoming likely to trigger CadQuery bugs. Ugh.
combined = end_ball_assembly + arm

# Again, chop can likely be replaced with a split() command but I have yet to figure out how
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
