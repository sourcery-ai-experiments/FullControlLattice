from math import cos, sin, pi, atan, sqrt, acos, radians

import fullcontrol as fc
import lab.fullcontrol as fclab

output = 'visualize'  # 'visualize' or 'gcode'


# design parameters

lattice_id = 'M1'
# Lattice Type (www.tinyurl.com/lattice-research) - Lattice structure sub-family, as identified in the journal paper investigating these structures (www.tinyurl.com/lattice_paper)
# default value: M1 ; options: 'M1', 'M2', 'M3', 'M4'

alpha = 30
# Star-Polygon Angle (Degrees) - Angle of star-polygon corners
# default value: 30 ; guideline range: 15 to 150

seg_length = 4.33
# Strut Length (mm) - Length of each lattice strut
# default value: 4.33 ; guideline range: 1 to 50

units_x = 10
# Length (Unit Cells) - Number of units cells along the length of the lattice
# default value: 10 ; guideline range: 4 to 15

units_y = 3
# Width (Unit Cells) - Number of units cells in the width direction - the actual value may be more than this to ensure neat printing between layers
# default value: 3 ; guideline range: 1 to 5

EW = 0.5
# Extrusion Width (mm) - Width of printed lines (i.e. width of each lattice strut) - recommended value: 1-1.5x nozzle diameter
# default value: 0.5 ; guideline range: 0 to 100

EH = 0.2
# Extrusion Height (mm) - Height of printed lines (i.e. layer thickness) - recommended value: 0.25-0.5x nozzle diameter
# default value: 0.2 ; guideline range: 0.01 to 5

layers = 2
# Layers -
# default value: 2 ; guideline range: 1 to 5

start_x = 30
# X Start (mm) - Approximate start-point of lattice in X
# default value: 30 ; guideline range: -1000000 to 1000000

start_y = 30
# Y Start (mm) - Approximate start-point of lattice in Y
# default value: 30 ; guideline range: -1000000 to 1000000

# generate the design (make sure you've run the above cells before running this cell)

layers = int(layers)

rows = units_y

if lattice_id == 'M1':
    steplist_repeating_unit = []
    # define the repeating unit (set of lines = Points)
    steplist_repeating_unit.append(fc.Point(x=0, y=0, z=0))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(-alpha/2)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(-60+alpha/2)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(120-alpha/2)))

    # calculate offsets for repeating the repeating unit
    repeat_offset_x = steplist_repeating_unit[3].x # offset for repeating in x along a line
    row_offset_x = -(steplist_repeating_unit[2].x-steplist_repeating_unit[1].x)  # offset in x for every other row
    row_offset_y = -(steplist_repeating_unit[1].y+steplist_repeating_unit[2].y) # offset in y between rows

    # repeat unit to make a full row, printing to the end and back
    steplist_row_1 = fc.move(steplist_repeating_unit, fc.Vector(x=repeat_offset_x), copy=True, copy_quantity=units_x)
    steplist_row_2 = fclab.reflectXYpolar_list(steplist_row_1, fc.Point(x=0,y=0), 0)

    # repeat the row, with a constant offset in y and alternating offset in x
    steplist_lattice = []
    rows = (units_y*2)-1
    for i in range(rows):
        x_offset_now = row_offset_x if i%2 == 1 else 0
        steplist_lattice.extend(fc.move(steplist_row_1+steplist_row_2, fc.Vector(x=x_offset_now, y=row_offset_y*i)))

elif lattice_id == 'M2':
    dev_angle = (atan((1-cos(radians(alpha)))/(sqrt(3)+sin(radians(alpha))))*180/pi)

    steplist_repeating_unit = []
    # define the repeating unit for row 1 (set of lines = Points)
    steplist_repeating_unit.append(fc.Point(x=0, y=0, z=0))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle+90-alpha)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle+30)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle-150-alpha)))
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2], seg_length, radians(dev_angle+30-alpha)))  # travel line 4#
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle-150)))  # travel line 5#
    steplist_repeating_unit.append(fc.Extruder(on=True))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2], seg_length, radians(dev_angle-90)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle-30)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle+30)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle+90)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle+150)))
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2], seg_length, radians(dev_angle-30)))  # travel line 11#
    steplist_repeating_unit.append(fc.Extruder(on=True))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2], seg_length, radians(dev_angle+150-alpha)))
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2], seg_length, radians(dev_angle-30-alpha)))  # travel line 13#
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1], seg_length, radians(dev_angle-90)))  # travel line 14#
    steplist_repeating_unit.append(fc.Extruder(on=True))

    # calculate offsets for repeating the repeating unit
    repeat_offset_x = steplist_repeating_unit[19].x
    row_offset_x = (steplist_repeating_unit[16].x-steplist_repeating_unit[8].x)
    row_offset_y = (steplist_repeating_unit[3].y-steplist_repeating_unit[9].y)

    # repeat unit to make row 1
    steplist_row_1 = fc.move(steplist_repeating_unit, fc.Vector(x=repeat_offset_x), copy=True, copy_quantity=units_x)

    # Start row 2
    steplist_repeating_unit_back = []
    steplist_repeating_unit_back_start_x = steplist_repeating_unit[1].x+(units_x*repeat_offset_x)+row_offset_x
    steplist_repeating_unit_back_start_y = steplist_repeating_unit[1].y+row_offset_y

    # define the repeating unit for row 2(set of lines = Points)
    steplist_repeating_unit_back.append(fc.Point(x=steplist_repeating_unit_back_start_x, y=steplist_repeating_unit_back_start_y))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle-90-alpha)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle+90)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle+150-alpha)))
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2], seg_length, radians(dev_angle-30-alpha)))  # travel line 4#
    steplist_repeating_unit_back.append(fc.Extruder(on=True))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2], seg_length, radians(dev_angle+150)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle-150-alpha)))
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2], seg_length, radians(dev_angle+30-alpha)))  # travel line 7#
    steplist_repeating_unit_back.append(fc.Extruder(on=True))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2], seg_length, radians(dev_angle-150)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle-90)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle-30)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle+30)))
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2], seg_length, radians(dev_angle+90)))  # travel line 12#
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle+150)))  # travel line 13#
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1], seg_length, radians(dev_angle-150)))  # travel line 14#
    steplist_repeating_unit_back.append(fc.Extruder(on=True))

    # repeat unit to make row 2
    steplist_row_2 = fc.move(steplist_repeating_unit_back, fc.Vector(x=-repeat_offset_x), copy=True, copy_quantity=units_x)
    steplist_lattice = fc.move(steplist_row_1+steplist_row_2, fc.Vector(y=2*row_offset_y), copy=True, copy_quantity=units_y)

elif lattice_id == 'M3':
    steplist_repeating_unit = []
    # define the repeating unit for row 1 (set of lines = Points)
    steplist_repeating_unit.append(fc.Point(x=0, y=0, z=0))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(120)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(0)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(180-alpha)))    #highest: end point of strut 3
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(-alpha)))      #travel line 4#
    steplist_repeating_unit.append(fc.Extruder(on=True))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(-120)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(60-alpha)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(-120)))       #lowest: end point of strut 7
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(0)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(120)))
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(-60)))     #travel line 10#
    steplist_repeating_unit.append(fc.Extruder(on=True))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(120-alpha)))
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(-60)))     #travel line 12#
    steplist_repeating_unit.append(fc.Extruder(on=True))

    rotation_angle = -atan((steplist_repeating_unit[15].y-steplist_repeating_unit[1].y)/(steplist_repeating_unit[15].x-steplist_repeating_unit[1].x))
    steplist_repeating_unit = fc.move_polar(steplist_repeating_unit, steplist_repeating_unit[1], 0, rotation_angle)

    # calculate offsets for repeating the repeating unit
    repeat_offset_x = (steplist_repeating_unit[17].x-steplist_repeating_unit[0].x)
    row_offset_y = (steplist_repeating_unit[3].y-steplist_repeating_unit[9].y)
    steplist_repeating_unit_back_start_x = (steplist_repeating_unit[3].x-steplist_repeating_unit[9].x) + (units_x+1)*repeat_offset_x

    # repeat unit to make row 1
    steplist_row_1 = fc.move(steplist_repeating_unit, fc.Vector(x=repeat_offset_x), copy=True, copy_quantity=units_x)

    steplist_repeating_unit_back = []
    steplist_repeating_unit_back.append(steplist_repeating_unit[0])
    steplist_repeating_unit_back.append(steplist_repeating_unit[2])
    steplist_repeating_unit_back.append(steplist_repeating_unit[3])
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(steplist_repeating_unit[2])
    steplist_repeating_unit_back.append(fc.Extruder(on=True))
    steplist_repeating_unit_back.append(steplist_repeating_unit[1])
    steplist_repeating_unit_back.append(steplist_repeating_unit[0])
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(steplist_repeating_unit[1])
    steplist_repeating_unit_back.append(fc.Extruder(on=True))
    steplist_repeating_unit_back.append(fc.move(steplist_repeating_unit[10], fc.Vector(x=-repeat_offset_x)))
    steplist_repeating_unit_back.append(fc.move(steplist_repeating_unit[11], fc.Vector(x=-repeat_offset_x)))
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(fc.move(steplist_repeating_unit[10], fc.Vector(x=-repeat_offset_x)))
    steplist_repeating_unit_back.append(fc.Extruder(on=True))
    steplist_repeating_unit_back.append(fc.move(steplist_repeating_unit[9], fc.Vector(x=-repeat_offset_x)))
    steplist_repeating_unit_back.append(fc.move(steplist_repeating_unit[8], fc.Vector(x=-repeat_offset_x)))
    steplist_repeating_unit_back.append(fc.move(steplist_repeating_unit[0], fc.Vector(x=-repeat_offset_x)))
    steplist_repeating_unit_back = fc.move(steplist_repeating_unit_back,fc.Vector(x=steplist_repeating_unit_back_start_x,y=row_offset_y))

    # repeat unit to make row 2
    steplist_row_2 = fc.move(steplist_repeating_unit_back, fc.Vector(x=-repeat_offset_x), copy=True, copy_quantity=units_x+1)
    steplist_lattice = fc.move(steplist_row_1+steplist_row_2, fc.Vector(y=2*row_offset_y), copy=True, copy_quantity=units_y)

elif lattice_id == 'M4':
    if alpha == 150: alpha=120 # fixes issue with alpha > 135
    dev_angle =  abs(acos((-sqrt(1+sin(2*radians(alpha))))/((sqrt(3-2*cos(radians(alpha))+2*sin(radians(alpha))))))*180/pi)

    steplist_repeating_unit = []
    # define the repeating unit for row 1 (set of lines = Points)
    steplist_repeating_unit.append(fc.Point(x=0, y=0, z=0))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(90-dev_angle)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(270-dev_angle-alpha)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(180-dev_angle)))    #highest: end point of strut 3
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(-dev_angle)))      #travel line 4#
    steplist_repeating_unit.append(fc.Extruder(on=True))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(180-dev_angle-alpha)))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(90-dev_angle-alpha)))   #lowest: end point of strut 6
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(-dev_angle-alpha)))
    steplist_repeating_unit.append(fc.Extruder(on=False))
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-2],seg_length,radians(-90-dev_angle-alpha)))  #travel line 8#
    steplist_repeating_unit.append(fc.polar_to_point(steplist_repeating_unit[-1],seg_length,radians(-180-dev_angle-alpha))) #travel line 9#
    steplist_repeating_unit.append(fc.Extruder(on=True))

    # calculate offsets for repeating the repeating unit
    repeat_offset_x = (steplist_repeating_unit[12].x-steplist_repeating_unit[0].x) # offset for repeating in x along a line
    row_offset_y = (steplist_repeating_unit[3].y-steplist_repeating_unit[8].y) # offset in y between rows (end of line 3 - end of line 7)

    # repeat unit to make row 1
    steplist_row_1 = fc.move(steplist_repeating_unit, fc.Vector(x=repeat_offset_x), copy=True, copy_quantity=units_x)

    steplist_repeating_unit_back = []
    steplist_repeating_unit_back_start_x = steplist_row_1[-2].x+(steplist_repeating_unit[1].x-steplist_repeating_unit[0].x)
    steplist_repeating_unit_back_start_y = row_offset_y-(steplist_repeating_unit[7].y-steplist_repeating_unit[8].y-(steplist_repeating_unit[5].y-steplist_repeating_unit[7].y))
    # define the repeating unit for row 2(set of lines = Points)
    steplist_repeating_unit_back.append(fc.Point(x=steplist_repeating_unit_back_start_x, y=steplist_repeating_unit_back_start_y))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1],seg_length,radians(-90-dev_angle)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1],seg_length,radians(90-dev_angle-alpha)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1],seg_length,radians(-dev_angle-alpha)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1],seg_length,radians(-90-dev_angle-alpha)))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1],seg_length,radians(180-dev_angle)))
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2],seg_length,radians(-dev_angle)))   #travel line 6#
    steplist_repeating_unit_back.append(fc.Extruder(on=True))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2],seg_length,radians(180-dev_angle-alpha)))
    steplist_repeating_unit_back.append(fc.Extruder(on=False))
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-2],seg_length,radians(90-dev_angle-alpha)))    #travel line 8#
    steplist_repeating_unit_back.append(fc.polar_to_point(steplist_repeating_unit_back[-1],seg_length,radians(-dev_angle-alpha)))  #travel line 9#
    steplist_repeating_unit_back.append(fc.Extruder(on=True))

    steplist_row_2 = fc.move(steplist_repeating_unit_back, fc.Vector(x=-repeat_offset_x), copy=True, copy_quantity=units_x)

    if units_y%2 != 0: units_y += 1
    row_pairs = int(units_y/2)
    steplist_lattice = fc.move(steplist_row_1+steplist_row_2, fc.Vector(y=2*row_offset_y), copy=True, copy_quantity=row_pairs)

# add three sacrificial printed lines to return to start point neatly, ready to being the next layer under steady-state conditions
steplist_lattice.extend([fc.Point(x=-repeat_offset_x),fc.Point(y=0),fc.Point(x=0)])

if output == 'visualize':
    # the visual preview becomes very slow when there are lots of lines. Remove travel to make it show more quickly
    steplist_lattice = fc.points_only(steplist_lattice)

# make lots of layers
steplist_multilayer = fc.move(steplist_lattice, fc.Vector(z=EH), copy=True, copy_quantity=layers)


# offset the whole procedure. z dictates the gap between the nozzle and the bed for the first layer, assuming the model was designed with a first layer z-position of 0
model_offset = fc.Vector(x=start_x, y=start_y, z=0.8*EH)

steps = fc.move(steplist_multilayer, model_offset) # all layers - comment out this or the previous line


# create annotations (these can also be produced during loops in the cell that creates the design)

annotation_pts = [fc.Point(x=start_x - seg_length * 5, y=start_y + seg_length * 5, z=0),
                  fc.Point(x=start_x, y=start_y, z=0),
                  fc.Point(x=start_x + seg_length * 5, y=start_y - seg_length * 5, z=0)]
annotation_labels = ["Lattices used in a research article", "Use TPU or similar ductile polymers", "More details: www.tinyurl.com/lattice-research"]

# update annotations from legacy to new format
for i in range(len(annotation_pts)):
    steps.append(fc.PlotAnnotation(point=annotation_pts[i], label=annotation_labels[i]))

# add initial settings for primer

initial_print_speed = 1000
initial_EW = EW
initial_EH = EH
primer = 'front_lines_then_y'

# the following parameters are over-written by user selections in the webapp:
# generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0
printer_name = 'ender_3'
nozzle_temp = 228
bed_temp = 40
fan_percent = 100
material_flow_percent = 100
print_speed_percent = 100

# fc printer_params

gcode_controls = fc.GcodeControls(
    printer_name=printer_name,
    initialization_data={
        'primer': primer,
        'print_speed': initial_print_speed,
        'nozzle_temp': nozzle_temp,
        'bed_temp': bed_temp,
        'fan_percent': fan_percent,
        'material_flow_percent': material_flow_percent,
        'print_speed_percent': print_speed_percent,
        'extrusion_width': initial_EW,
        'extrusion_height': initial_EH})

plot_controls = fc.PlotControls(
    style='tube',
    initialization_data={
        'extrusion_width': initial_EW,
        'extrusion_height': initial_EH})

design_name = 'star_polygon_lattice'

gcode_controls.save_as = design_name
fc.transform(steps, 'gcode', gcode_controls) if output == 'gcode' else fc.transform(steps, 'plot', plot_controls)
