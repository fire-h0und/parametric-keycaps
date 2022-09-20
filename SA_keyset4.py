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
#TODO Enter keys


#general keycap measures
size=step - gap

#shape parameters:
height = 13.5 #mm
wall   =  2  # mm how thick wall we want
radius = size + (height-8.5)*3   #mm sides radius
radius2 = 34  # top radius
radius3 = 34 - 8 # alternate top radius TODO


ride   =  5.5 # mm how deep the switch goes
sw_body= 14   # mm how much the switch requires

row=1

#calculated values:
o=[8,8,4,0,4,-1] # -1 is special case of space row profile

o1=o[row]

#general keycap measures
size=step - gap

def ALPS_hole (ride,width):
    r4=0.95 # stem hole edge chamfers
    ribsZ=2 # mm high
    ribsW=1 # mm wide
    cave = size-2*wall
    if cave < sw_body:
        cave = sw_body

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
    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(alps_stem)
    #hole = hole.rotate((0,0,0),(0,0,1),90)
    #TODO make 2U and other stabs
    return hole

def MX_hole (ride,width):
    r4=0.95 # stem hole edge chamfers
    ribsZ=2 # mm high
    ribsW=1 # mm wide
    cave = size-2*wall
    if cave < sw_body:
        cave = sw_body

    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave,ribsW,ribsZ)
    #shape the stem in positive form
    #TODO
    mx_stem=cq.Workplane(origin=(0,0,-1))
    #mx_stem=mx_stem.rect(4.15, 1.27)
    #mx_stem=mx_stem.rect(1.12, 4.15)
    mx_stem=mx_stem.circle(2.75)
    mx_stem=mx_stem.clean()
    mx_stem=mx_stem.extrude(ride+3.1)
    mx_stem=mx_stem.union(ribs)
    mx_stem_hole=cq.Workplane(origin=(0,0,-2))
    mx_stem_hole=mx_stem_hole.rect(4.15, 1.27)
    mx_stem_hole=mx_stem_hole.rect(1.12, 4.15)
    mx_stem_hole=mx_stem_hole.extrude(ride+2)
    mx_stem=mx_stem.cut(mx_stem_hole)
    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
    hole = hole.box(cave,cave+(step*(width-1)),ride+r4+2)
    hole = hole.fillet(r4)
    hole = hole.cut(mx_stem)
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
    #hole = hole.rotate((0,0,0),(0,0,1),90)
    #TODO make 2U and other stabs
    return hole

def SA_cap (row,width):
    if width > 0:
        #
        # our generic body values
        r1=0.25 # base corners
        r2=2    # top edge corners
        r3=0.5  # top edge
        o1=o[row]
        #preparing the forming shapes:
        ball = cq.Workplane("front",origin=(0,0,0))
        if width != 1.0:
            #todo make a "pill" shape
            ball = ball.move((width-1)*step/2+radius2,0)
            ball = ball.radiusArc(endPoint=((width-1)*step/2,-radius2),radius=radius2)
            ball = ball.line(-(width-1)*step,0)
            ball = ball.radiusArc(endPoint=(-(width-1)*step/2-radius2,0),radius=radius2)
            ball = ball.wire()
            ball = ball.revolve(0,[0,0,0],[1,0,0])
            ball = ball.rotate((0,0,0),(0,0,1),90)
        else:
            ball = ball.sphere(radius2)
            ball = ball.rotate([0,0,0],[1,0,0],90)
        if o1 != -1:
            ball = ball.translate([o1,0,height+radius2])
        else:
            ball = ball.translate([0,0,height+radius2])
        #the all containing shape
        cube = cq.Workplane(origin=(0,0,-size*.1))
        cube = cube.box(size*width,size,size*.2)
        #the bottom forming shape
        base = cq.Workplane(origin=(0,0,-step))
        base = base.box(step*width,step,step*2)
        #one more merely rotated 90 around Z axis
        b2 = base.box(step,step*width,step*2)
        #single rounded side
        side = cq.Workplane("bottom",origin=(size/2-radius,0))
        side = side.cylinder(height=size*(width+1),radius=radius,angle=90,combine=True)

        #two opposing sides fused:
        sides = side.rotate((0,0,0),(0,0,1),180)
        sides = sides.intersect(side)

        #two opposing sides at switch width distance
        sides_L = side
        sides_L = sides_L.intersect(base.translate([step/2,0,step*2])) # half side profile
        sides_L = sides_L.translate([((width-1)*step/2),0,0])
        sides_R = sides_L.rotate((0,0,0),(0,0,1),180)
        #sides_L = sides_L.intersect(side.translate([(step*width/2),0,0]))
        sides_LW= sides_L.union(sides_R)
        if width != 1.0:
            sides_LW= sides_LW.box((width-1)*step,step*2,step) #we can't draw 0 width box
            #with (width-1) we are certainly clear the end of the side profiles
        sides_LW= sides_LW.intersect(b2.translate([0,0,step*2]).rotate((0,0,0),(0,0,1),90),clean=True)

        #fuse opposing sides to form a square
        form = sides
        form = form.rotate((0,0,0),(0,0,1),90)
        form = form.intersect(sides_LW)
        form = form.rotate((0,0,0),(0,0,1),90)
        if width == 1: #single unit size:
            log ("cube")
            form = form.union(cube)

        # select between top most and bottom most edges that are non horizontal:
        if width == 1:
            selection='not( <Z or |X or |Y )'
        else:
            selection='not(>Z or <Z or |X or |Y)'
        form = form.edges(selection) # we are pencil (or rocket) shaped
        form = form.fillet(r2)
        if o1 != -1: # we are digging out a conqave shape:
            form = form.cut(ball)
        else: # we are building a convex shape:
            form = form.intersect(ball.translate([0,0,-(radius+height)-radius+height+gap]))
        if o1 == 0:
            select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-5] )'
        elif o1 == 5:
            select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-5] )'
        else:
            select_top='not( <<Z[-5] or <Z or >>X[-3] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-10] )'
        #form = form.edges(select_top)
        #form = form.fillet(r3)
        if width == 1:
            log ("cut_base")
            form = form.cut(base)
        form = form.cut(MX_hole(ride,width))
        if row == 4:
            form = form.rotate((0,0,0),(0,0,1),-90)
        else:
            form = form.rotate((0,0,0),(0,0,1),90)
        #TODO width
    #    return sides.rotate((0,0,0),(0,0,1),90).intersect(sides_LW)
    else:
        form = cq.Workplane()
    log (width)
    return form
selection='( <Z or |X or |Y )'

result = SA_cap (5,2.25)
#result = MX_hole (5,1.25)
#highlight = result.edges(selection)

#show_object(result, name="body", options={cq.Color("blue")})
#debug(highlight)

'''
#show a lot:
y=0
x=0
l=0
for s in [1,2,6.25,1]:
    
    y=y+(s+l)/2
    x=0
    for k in range(-1,5):
        x=x+1
        r = k+1 #row
        result = SA_cap (r,s).translate ([y*19.05,x*19.05,0])
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
    [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,2],[1,0]],
    [[2,1.5],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1.5],[2,0]],
    [[3,1.75],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,2.25],[3,0],[3,0]],
    [[4,2.25],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,2.75],[4,0],[4,0],[4,0]],
    [[4,1.25],[4,1.25],[4,1.25],[5,6.25],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,1.25],[4,1.25],[4,1.25],[4,1.25]],
    ]
'''
'''
a=0
b=0
for x in range(len(keybrd)):
    a=a+1
    log(b)
    b=0
    for y in range(len(keybrd[0])):
        s=keybrd[x][y][0]
        w=keybrd[x][y][1]
        b=b+w/2
        result = SA_cap(s,w).translate([-b*19.05,a*19.05,0])
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