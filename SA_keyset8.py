
import cadquery as cq
from cadquery import exporters

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
#TaiHAo            : 7U          [133mm] :<mount> = center     , <stab> 49mm + 55m MX stab
#                  : 7U space    [133mm] :<mount> = center     , <MXstab> 57.15mm apart (3U)
#TODO Enter keys


#general keycap measures
size=step - gap

#shape parameters:
height = 11.9 #mm values that work: 8.6, 10.5, 11.9, 13.7
wall   =  2   #mm how thick wall we want
roundness = 8.5 # measureless factor: from 0 to height gives sane values, a good default is 8.5
radius = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
log('radious')
log(radius)
radius2 = 34     #mm top radius
radius3 = 34 - 8 #mm alternate top radius TODO

#ride: for MX the ride can go as low as 2.5mm before the cap hits the plate
ride   =  5.5 #mm how deep the switch goes
sw_body= 14   #mm how much the switch requires

row=1

# calculated values for row stamping offsets:
# -1 is special case of space row profile
o=[8,8,4,0,4,-1]

# our generic body values
r1=0.25 #mm base corners
r2=2    #mm top edge corners
r3=0.5  #mm top edge

#general keycap measures
size=step - gap

r4=0.95 #mm stem hole edge chamfers
ribsZ=2 #mm high (stem ribs)
ribsW=1 #mm wide
cave = size-2*wall # "cave" is the stem hole depth

if cave < sw_body: # fitting the upper switch body
    cave = sw_body
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
stab_offset= -2.0  #mm

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

def alps_stem(width):

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave,ribsW,ribsZ)

    #shape the stem in positive form 
    
    #move away along the longer side for a start
    alps_stem=cq.Workplane(origin=(-1.0,stem_width/2,0))
    #we start drawing the narrow side from the corner:
    alps_stem=alps_stem.line((stem_length-stem_rib_w2)/2, 0  )
    #the ribs are ADDED to the stem size:
    alps_stem=alps_stem.line(0  , stem_rib)
    alps_stem=alps_stem.line(stem_rib_w2, 0  )
    alps_stem=alps_stem.line(0  ,-stem_rib)
    alps_stem=alps_stem.line((stem_length-stem_rib_w2)/2, 0  )
    alps_stem=alps_stem.line(0  ,-stem_rib)
    #wider side next:
    alps_stem=alps_stem.line(   0,-(stem_width-stem_rib_sp-stem_rib_w1*2)/2 ) 
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0,-stem_rib_w1 )
    alps_stem=alps_stem.line(-stem_rib, 0  )
    # we use defined rib spacing and are hardcoed for 2 ribs only
    alps_stem=alps_stem.line(   0,-stem_rib_sp)
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0,-stem_rib_w1 )
    alps_stem=alps_stem.line(-stem_rib, 0  )
    alps_stem=alps_stem.line(   0,-(stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    #and a corner and back to the other narrow side:
    alps_stem=alps_stem.line(-(stem_length-stem_rib_w2)/2, 0  )
    alps_stem=alps_stem.line(0  ,-stem_rib)
    alps_stem=alps_stem.line(-stem_rib_w2, 0  )
    alps_stem=alps_stem.line(0  , stem_rib)
    alps_stem=alps_stem.line(-(stem_length-stem_rib_w2)/2, 0  )
    alps_stem=alps_stem.line(0  , stem_rib)
    #and another wider side:
    alps_stem=alps_stem.line(   0, (stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    alps_stem=alps_stem.line(-stem_rib, 0  )
    alps_stem=alps_stem.line(   0, stem_rib_w1 )
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0, stem_rib_sp)
    alps_stem=alps_stem.line(-stem_rib, 0  )
    alps_stem=alps_stem.line(   0, stem_rib_w1 )
    alps_stem=alps_stem.line( stem_rib, 0  )
    alps_stem=alps_stem.line(   0, (stem_width-stem_rib_sp-stem_rib_w1*2)/2 )
    alps_stem=alps_stem.close()
    # Alps stem is ideally flush with the keycap bottom
    alps_stem=alps_stem.extrude(ride+2.1)
    alps_stem=alps_stem.union(ribs)

    return alps_stem

def alps_stab(width):
    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave,ribsW,ribsZ)

    alps_stab=cq.Workplane(origin=(stab_offset,0,-1))
    alps_stab=alps_stab.rect(stab_width+2*stab_wall,stab_length+2*stab_wall)
    alps_stab=alps_stab.clean()
    alps_stab=alps_stab.extrude(ride+3.1)
    alps_stab=alps_stab.union(ribs)

    alps_stab_hole=cq.Workplane(origin=(stab_offset,0,-2))
    alps_stab_hole=alps_stab_hole.rect(stab_width,stab_length)
    alps_stab_hole=alps_stab_hole.extrude(ride+2)
    alps_stab=alps_stab.cut(alps_stab_hole)
    return alps_stab

def mx_stem(width):
    #this very MX stem is tested so far to fit:
    # Kailh ChocV2,
    # Kailh BOX (square)
    # Kailh Silent BOX (round stem)
    # Cherry MX "+" like stem

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave,ribsW,ribsZ)

    mx_stem=cq.Workplane(origin=(0,0,-1))
    mx_stem=mx_stem.circle(2.75)
    mx_stem=mx_stem.clean()
    mx_stem=mx_stem.extrude(ride+3.1)
    mx_stem=mx_stem.union(ribs)
    #my stem size fixes for FDM (a smidge too tight)
    mx_stem_hole=cq.Workplane(origin=(0,0,-2))
    mx_stem_hole=mx_stem_hole.rect(4.15-0.05, 1.27+0.05)
    mx_stem_hole=mx_stem_hole.rect(1.12+0.05, 4.15-0.05)
    mx_stem_hole=mx_stem_hole.extrude(ride+2) # +2 mm to just be on the safe side here
    mx_stem=mx_stem.cut(mx_stem_hole)
    return mx_stem

def alps_hole (ride,width):

    #shape the stem in positive form
    alpsstem=alps_stem(width)

    #add Alps stab stems:
    alpsstab=alps_stab(width)
    #TODO

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(alpsstem)

    #add stabilizers
    spacing = 0
    if width == 7 or width == 6.25: # space keys:
        spacing = 98 #mm
    elif width == 2.75 or width == 3: # where will you find 3U stabilizer wire anyway?
        spacing = 41 #mm
    elif width == 2.25 or width == 2:
        spacing = 27 #mm
    if spacing != 0:
        hole=hole.cut(alpsstab.translate([0,spacing/2,0]))
        hole=hole.cut(alpsstab.translate([0,-spacing/2,0]))

    #TODO add the 35mm offset 4mm dia stabilizer axle too
    #TODO add the 35mm 2nd alps stem to 7U space bar

    return hole.rotate((0,0,0),(0,0,1),90)

def alpsmx_hole (ride,width):

    #shape the stem in positive form
    alpsstem=alps_stem(width)

    #MX stab stems:
    mxstem=mx_stem(width)

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(alpsstem)

    #add stabilizers:
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        mxstab=mxstem.translate([0,spacing/2,0])
        hole=hole.cut(mxstab)
        mxstab=mxstem.translate([0,-spacing/2,0])
        hole=hole.cut(mxstab)
    return hole.rotate((0,0,0),(0,0,1),90)

def mx_hole (ride,width):

    #shape the stem in positive form
    mxstem=mx_stem(width)

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(mxstem)

    #add stabilizers:
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        mxstab=mxstem.translate([0,spacing/2,0])
        hole=hole.cut(mx_stab)
        mxstab=mxstem.translate([0,-spacing/2,0])
        hole=hole.cut(mx_stab)
    return hole.rotate((0,0,0),(0,0,1),90)

def spherical_cap (stem,row,width):
    if width > .75:
        o1=o[row]
        #preparing the forming shapes:
        if width > 1:
            stamp = cq.Workplane("front",origin=(0,0,0))
            stamp = stamp.move((width-1)*step/2+radius2,0)
            stamp = stamp.radiusArc(endPoint=((width-1)*step/2,-radius2),radius=radius2)
            stamp = stamp.line(-(width-1)*step,0)
            stamp = stamp.radiusArc(endPoint=(-(width-1)*step/2-radius2,0),radius=radius2)
            stamp = stamp.wire()
            stamp = stamp.revolve(0,[0,0,0],[1,0,0])
            stamp = stamp.rotate([0,0,0],[1,0,0],90)
        else:
            stamp = cq.Workplane("front",origin=(0,0,0))
            stamp = stamp.sphere(radius2)
            # rotate the spere so the seam is more favorably placed upun the body
            stamp = stamp.rotate([0,0,0],[1,0,0],90)

        if o1 != -1: # are we convex? -1 is convex dead center
            stamp = stamp.translate([0,o1,height+radius2]) # slide as per row offset
        else:
            stamp = stamp.translate([0,0,height*1.1-radius2])  # we are, put it dead on center

        #the base containing shape
        cube = cq.Workplane(origin=(0,0,-size*.1))
        cube = cube.box(size*width,size,size*.2)

        #the bottom forming shape
        base = cq.Workplane(origin=(0,0,-step))
        # we want go high because sculpt is measured
        # from the dish lowest point -
        # we need enough material at the rim
        base = base.box(step*width,step,step*1.95)

        #single rounded side
        side = cq.Workplane("bottom",origin=(size/2-radius,0))
        side = side.cylinder(height=size*(width+1),radius=radius,angle=90,combine=True)

        #two opposing sides fused:
        sides = side.rotate((0,0,0),(0,0,1),180)
        sides = sides.intersect(side)

        #two opposing sides at switch width distance
        sides_L = side
        sides_L = sides_L.intersect(base.translate([step/2,0,step*1])) # half side profile
        sides_L = sides_L.translate([((width-1)*step/2),0,0])
        sides_R = sides_L.rotate((0,0,0),(0,0,1),180)
        #sides length wise:
        sides_LW= sides_L.union(sides_R)
        #are we wider than 1U?
        if width != 1.0: # for non unit size switchs
            sides_LW= sides_LW.box((width-1)*step,step*1.1,step*2) #we can't draw 0 width box
            #with (width-1) we are certainly clear the end of the side profiles
        sides_LW= sides_LW.intersect(base.translate([0,0,step*1]),clean=True)

        #fuse opposing sides to form a square
        form = sides
        form = form.rotate((0,0,0),(0,0,1),90)
        form = form.intersect(sides_LW)
        if width <= 0: #single unit size: a hack for selection:
            form = form.union(cube)
            # select between top most and bottom most edges that are non horizontal:
            selection='not( <Z or |X or |Y )'
        else:
            selection='not(>Z or <Z or |X or |Y)'

        form = form.edges(selection) # we are pencil (or rocket) shaped
        form = form.fillet(r2)

        #o1 = -1 is space row
        if o1 != -1: # we are digging out a conqave shape:
            stamp_offset=[0,0,0]
            shape = stamp.translate(stamp_offset)
            form = form.cut(stamp).clean()
        else: # we are building a convex shape:
            stamp_offset=[0,0,height*4]
            shape = base.translate(stamp_offset).cut(stamp).clean()
            form = form.cut(shape,clean=True)
        log(o1)

        if o1 == 0:
            select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-4] )'
        elif o1 == -1:
            select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-4] )'
        else:
            select_top='not( <<Z[-5] or <Z or >>X[-3] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-10] )'
        form = form.edges(select_top)
        form = form.fillet(r3)

        # special case for row 4 (before we cut the switch hole)
        if row == 4:
            form = form.rotate((0,0,0),(0,0,1),-180)
        #width
        if width > 0:
            form = form.cut(base)
        if stem in ["","MX","mx"]:
            form = form.cut(mx_hole(ride,width))
        elif stem in ["Alps","ALPS","alps"]:
            form = form.cut(alps_hole(ride,width))
        elif stem in ["AlpsMX","ALPSMX","alpsmx"]:
            form = form.cut(alpsmx_hole(ride,width))

        #form = form.rotate((0,0,0),(0,0,1),90)

    #    return sides.rotate((0,0,0),(0,0,1),90).intersect(sides_LW)
    else:
        form = cq.Workplane()
    return form
selection='( <Z or |X or |Y )'

result = spherical_cap ("AlpsMX",5,2.25)
#result = mx_hole (5,1.25)
#highlight = result.edges(selection)

#show_object(result, name="body", options={cq.Color("blue")})
#debug(highlight)


#show a lot:
y=0
x=0
l=0
'''
for s in [1,6.25,2.0]:

    y=y+(s+l)/2
    x=0
    for k in range(0,5):
        x=x+1
        r = k+1 #row
        result = spherical_cap ("Alps",r,s).translate ([y*step,x*step,0])
        show_object(result)
    l=s
'''

'''
# sculpt, width
#a MIT planck:
keybrd = [
#    [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]],
    [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]],
    [[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1]],
    [[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1]],
#    [[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1]],
    [[4,1],[4,1],[4,1],[4,1],[5,1],[5,2],[5,0],[5,1],[4,1],[4,1],[4,1],[4,1]],
    ]
'''


#ANSI 60%
keybrd = [
  [[1,1],[1,1],[0,.75],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,2],[1,0],[0,.75],[1,1],[1,1.5],[1,1.5]],
  [[2,1],[2,1],[0,.75],[2,1.5],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1.5],[2,0],[0,.75],[2,1],[2,1],[2,1],[2,1]],
  [[3,1],[3,1],[0,.75],[3,1.75],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,2.25],[3,0],[3,0],[0,.75],[3,1],[3,1],[3,1],[3,1]],
  [[4,1],[4,1],[0,.75],[4,2.25],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,2.75],[4,0],[4,0],[4,0],[0,.75],[4,1],[4,1],[4,1],[4,1]],
  [[4,1],[4,1],[0,.75],[4,1.25],[4,1.25],[4,1.25],[5,6.25],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,1.25],[4,1.25],[4,1.25],[4,1.25],[5,.75],[4,2],[4,1],[4,1]],
  ]


a=0
b=0
for x in range(len(keybrd)):
    a=a+1
    log(b)
    b=0
    for y in range(len(keybrd[x])):
        t="Alps"
        s=keybrd[x][y][0]
        w=keybrd[x][y][1]
        b=b+w/2
        result = spherical_cap(t,s,w).translate([-b*19.05,a*19.05,0])
        b=b+w/2
        show_object(result,options={cq.Color("blue")})


'''
exporters.export(
    result,
    'SA_keyset.stl',
    tolerance=0.15,
    angularTolerance=0.125
    )

exporters.export(
    result,
    'SA_keyset.svg',
    opt={
        "width": 300,
        "height": 300,
        "marginLeft": 40,
        "marginTop": 40,
        "showAxes": True,
        "projectionDir": (0.5, -0.5, 1),
        "strokeWidth": 0.25,
        "strokeColor": (255, 0, 0),
        "hiddenColor": (0, 0, 255),
        "showHidden": True,
        },
    )
'''
