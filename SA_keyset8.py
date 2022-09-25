
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
#Cherry            : 2U                  :<mount> = center     , <stab> 23.86mm apart from center
#Cherry            : 2.25U               :<mount> = center     , <stab> 23.86mm apart from center
#Cherry            : 2.75U               :<mount> = center     , <stab> 23.86mm apart from center
#Cherry            : 3U                  :<mount> = center     , <stab> 38.07mm apart from center
#Signature Plastics: 6.25U space [118mm] :<mount> = center     , <stab> 50mm apart from center
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
# ALPS
#
##########
#                  : 2U                  :<mount> = center     , <stab> mm apart from center
#                  : 2.25U               :<mount> = center     , <stab> mm apart from center
#                  : 2.75U               :<mount> = center     , <stab> mm apart from center
#                  : 3U                  :<mount> = center     , <stab> mm apart from center
#Kudos to PigeonsLB o/
#Big Foot          : 7U          [133mm] :<mount> = center     , <stabs> (93,75+(A+B)/4 mm apart)
#TaiHAo            : 7U          [133mm] :<mount> = center     , <stab> 49mm + 55m MX stab
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
stab_width = 3.0   #mm
stab_length= 2.0   #mm
stab_wall  = 0.8   #mm
stab_offset= -2.0  #mm

def alpsstem(width):

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave,ribsW,ribsZ)

    #shape the stem in positive form
    alps_stem=cq.Workplane(origin=(-1.0,2.15,0))
    alps_stem=alps_stem.line(0.625, 0  )
    alps_stem=alps_stem.line(0  , 0.1)
    alps_stem=alps_stem.line(0.8, 0  )
    alps_stem=alps_stem.line(0  ,-0.1)
    alps_stem=alps_stem.line(0.625, 0  )
    alps_stem=alps_stem.line(0  ,-0.1)
    #shorter side:
    alps_stem=alps_stem.line(   0,-.375 )
    alps_stem=alps_stem.line( 0.1, 0  )
    alps_stem=alps_stem.line(   0,-.5 )
    alps_stem=alps_stem.line(-0.1, 0  )
    alps_stem=alps_stem.line(   0,-2.5)
    alps_stem=alps_stem.line( 0.1, 0  )
    alps_stem=alps_stem.line(   0,-.5 )
    alps_stem=alps_stem.line(-0.1, 0  )
    alps_stem=alps_stem.line(   0,-.375 )
    #and a corner
    alps_stem=alps_stem.line(-0.625, 0  )
    alps_stem=alps_stem.line(0  ,-0.1)
    alps_stem=alps_stem.line(-0.8, 0  )
    alps_stem=alps_stem.line(0  , 0.1)
    alps_stem=alps_stem.line(-0.625, 0  )
    alps_stem=alps_stem.line(0  , 0.1)
    #and another :D
    alps_stem=alps_stem.line(   0, .375 )
    alps_stem=alps_stem.line(-0.1, 0  )
    alps_stem=alps_stem.line(   0, .5 )
    alps_stem=alps_stem.line( 0.1, 0  )
    alps_stem=alps_stem.line(   0, 2.5)
    alps_stem=alps_stem.line(-0.1, 0  )
    alps_stem=alps_stem.line(   0, .5 )
    alps_stem=alps_stem.line( 0.1, 0  )
    alps_stem=alps_stem.line(   0, .375 )
    alps_stem=alps_stem.close()
    alps_stem=alps_stem.extrude(ride+2.1)
    alps_stem=alps_stem.union(ribs)

    return alps_stem

def alpsstab(width):
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

def mxstem(width):

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave,ribsW,ribsZ)

    mx_stem=cq.Workplane(origin=(0,0,-1))
    mx_stem=mx_stem.circle(2.75)
    mx_stem=mx_stem.clean()
    mx_stem=mx_stem.extrude(ride+3.1)
    mx_stem=mx_stem.union(ribs)

    mx_stem_hole=cq.Workplane(origin=(0,0,-2))
    mx_stem_hole=mx_stem_hole.rect(4.15, 1.27)
    mx_stem_hole=mx_stem_hole.rect(1.12, 4.15)
    mx_stem_hole=mx_stem_hole.extrude(ride+2)
    mx_stem=mx_stem.cut(mx_stem_hole)
    return mx_stem

def alps_hole (ride,width):

    #shape the stem in positive form
    alps_stem=alpsstem(width)

    #add Alps stab stems:
    alps_stab=alpsstab(width)
    #TODO

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(alps_stem)

    #add stabilizers
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        hole=hole.cut(alps_stab.translate([0,spacing/2,0]))
        hole=hole.cut(alps_stab.translate([0,-spacing/2,0]))

    return hole.rotate((0,0,0),(0,0,1),90)

def alpsmx_hole (ride,width):

    #shape the stem in positive form
    alps_stem=alpsstem(width)

    #MX stab stems:
    mx_stem=mxstem(width)

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(alps_stem)

    #add stabilizers:
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        mx_stab=mx_stem.translate([0,spacing/2,0])
        hole=hole.cut(mx_stab)
        mx_stab=mx_stem.translate([0,-spacing/2,0])
        hole=hole.cut(mx_stab)
    return hole.rotate((0,0,0),(0,0,1),90)

def mx_hole (ride,width):

    #shape the stem in positive form
    mx_stem=mxstem(width)

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(mx_stem)

    #add stabilizers:
    spacing = 0
    if width > 2.75: # space keys:
        spacing = ( width - 1 ) * 3/4 * 25.38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing=15/16 * 25.38 #mm ( it's 3/4" x 5/4 ( 2.25U - (2 x 1/2U)) exactly )
    if spacing != 0:
        mx_stab=mx_stem.translate([0,spacing/2,0])
        hole=hole.cut(mx_stab)
        mx_stab=mx_stem.translate([0,-spacing/2,0])
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
        t="AlpsMX"
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
