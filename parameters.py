step=19.05 # mm
gap = 0.95

#stabilizers TODO:
##########
#
# Cherry
#
##########
#stabs on <> are Y centered:
#11.938mm ?
#23.8572mm (exactly 0.94" for 2.xxU and 1.5" for 3U according to Cherry spec sheet)
#Cherry            : 2U                  :<mount> = center     , <stab> 23.86mm apart
#Cherry            : 2.25U               :<mount> = center     , <stab> 23.86mm apart
#Cherry            : 2.75U               :<mount> = center     , <stab> 23.86mm apart
#Cherry            : 3U                  :<mount> = center     , <stab> 38.07mm apart
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <stab> 50mm apart
#Cherry G80-3000   : 6.25U space [118mm] :<mount> 11.9 to right, <stab> -"- (0.5U, 3.75U 5.75U)
#                  : 6.25U space [118mm]          -"-          , 40mm    (2.1U from center)
#                  : 6.25U space [118mm]          -"-          , 42.5mm  (3U from center)
#                  : 6.5U space  [123mm] :<mount> = center     , <stab> 52.25mm apart
#Corsair           : 6.5U space  [123mm] :<mount> = center     , <stab> 52.38mm apart (2.75U)
#                  : 7U space    [133mm] :<mount> = center     , <stab> 57.15mm apart (3U)
#Cherry            : 9U space    [171mm] :<mount> = center     , <stab> 66.675mm apart (3.5U)
#-"- Commodore PC-5: 10U space   [190mm] :<mount> = center     , <stab> 66.675mm apart (3.5U)
#TODO Enter keys

##########
#
# Alps
#
##########
#                  : 2U         [37.2mm] :<mount> = center     , <stab> 27 mm apart
#                  : 2.25U      [42.0mm] :<mount> = center     , <stab> 27 mm apart
#                  : 2.75U      [51.6mm] :<mount> = center     , <stab> 41 mm apart
#                  : 3U                  :<mount> = center     , <stab> ?? mm apart
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <MXstab> 50mm apart
#Big Foot          : 7U          [133mm] :<mount> = center     , <stabs> 98 mm apart,
#                                         another switch stem mount 35mm to the right and another
#                                                               special sleeve stabilizer
#                                                               4.0-3.8mm dia 35mm to the left
#                                                               protruding 6.0 mm thru the cap bottom plane
#TaiHAo            : 7U          [133mm] :<mount> = center     , <stab> 49mm each + 55m <MX> stab each
#                  : 7U space    [133mm] :<mount> = center     , <MXstab> 57.15mm apart (3U)
#TODO Enter keys


##########
#
# Choc
#
##########
#                  : 2U         [37.2mm] :<mount> = center     , <MXstab> 24 mm apart
#                  : 2.25U      [42.0mm] :<mount> = center     , <MXstab> 24 mm apart
#                  : 2.75U      [51.6mm] :<mount> = center     , <MXstab> 24 mm apart
#                  : 3U  ??? possibly 38 mm
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <MXstab> 50 mm apart

#general keycap measures
size=step - gap

#ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
ride   =  3.0 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
sw_body= 14   #mm how much space the switch requires

# our generic body values
r1=0.25  #mm base corners
r2=2     #mm top edge corners
r3=0.51  #mm top edge

ribsW= 1 #mm width of the stem ribs

#Alps stabilizer size and position (looking from top down)
# the measured value is (2.975) 3.325 x 2.055 mm on the brown (nylon?)
# Alps stabilizer insert, it most probably had some 0.15 mm
# high rib on the 3 mm sized faces for an assured interference fit.
stab_width = 3.20   #mm
stab_length= 2.10   #mm
stab_wall  = 1.0   #mm

# the stabilizer offset on the Matias set could likely benefit from
# increasing this value for some 0.2 to 0.3 mm (-2.3mm) but it
# remains to be tested and comfirmed
stab_offset = -2.0  #mm
stab_retract= -1.2  #mm

# stem is measured as 4.5 x 2.2 mm fron an OEM Alps cap
# the  intended dimension is however offset for tight fit:
# 4.55 mm x 2.25 mm
alps_stem_width = 4.50 #mm best intentionally left free of overlap
alps_stem_length= 2.25 #mm
stem_rib   = 0.1 #mm the half offset on the two opposing sides
stem_width = alps_stem_width - stem_rib*2
stem_length= alps_stem_length - stem_rib*2
stem_rib_w1= 0.5 #mm the double rib on the longer side
stem_rib_w2= 0.8 #mm the single rib on the narrow side
stem_rib_sp= 2.5 #mm how wide to putr the ribs apart

shape_compensation = 1.0 # how the convex height compares to the concave

row=1
