import cadquery2 as cq
from cadquery2 import exporters

step=19.05 # mm
gap = 0.95

radius = 33 #mm
height = 10.8 #mm
wall   =  2  # mm how thick wall we want

ride   =  5.5 # mm how deep the switch goes
sw_body= 14   # mm how much the switch requires

row=1

#calculated values:
o=[8,8,4,0,4,-1] # -1 is special case of space row profile

o1=o[row]

#general keycap measures
size=step - gap

def ALPS_hole (ride,width):
    r4=0.5 # stem hole edges
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

def SA_cap (row,width):
    #
    # our generic body values
    r1=0.25 # base corners
    r2=1.5    # top edge corners
    r3=0.5  # top edge
    o1=o[row]
    #preparing the forming shapes:
    ball = cq.Workplane("front",origin=(0,0,0))
    if width != 1:
        #todo make a "pill" shape
        ball = ball.move((width-1)*step/2+radius,0)
        ball = ball.radiusArc(endPoint=((width-1)*step/2,-radius),radius=radius)
        ball = ball.line(-(width-1)*step,0)
        ball = ball.radiusArc(endPoint=(-(width-1)*step/2-radius,0),radius=radius)
        ball = ball.wire()
        ball = ball.revolve(0,[0,0,0],[1,0,0])
        ball = ball.rotate((0,0,0),(0,0,1),90)
    else:
        ball = ball.sphere(radius)
        ball = ball.rotate([0,0,0],[1,0,0],90)
    if o1 != -1:
        ball = ball.translate([o1,0,height+radius])
    else:
        ball = ball.translate([0,0,height+radius])
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
    if width != 1:
        sides_LW= sides_LW.box((width-1)*step,step*2,step) #we can't draw 0 width box
        #with (width-1) we are certainly clear the end of the side profiles
    sides_LW= sides_LW.intersect(b2.translate([0,0,step*2]).rotate((0,0,0),(0,0,1),90),clean=True)

    #fuse opposing sides to form a square
    form = sides
    form = form.rotate((0,0,0),(0,0,1),90)
    form = form.intersect(sides_LW)
    form = form.rotate((0,0,0),(0,0,1),90)
    if width == 1: #single unit size:
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
    if o1 == 0 or 5:
        select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-5] )'
    else:
        select_top='not( <<Z[-5] or <Z or >>X[-3] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-10] )'
    form = form.edges(select_top)
    form = form.fillet(r3)
    if width == 1:
        form = form.cut(base)
    form = form.cut(ALPS_hole(ride,width))
    if row == 4:
        form = form.rotate((0,0,0),(0,0,1),-90)
    else:
        form = form.rotate((0,0,0),(0,0,1),90)
    #TODO width
#    return sides.rotate((0,0,0),(0,0,1),90).intersect(sides_LW)
    return form
#selection='not( <Z or |X or |Y )'

'''
result = SA_cap (1,1)
#highlight = result.edges(selection)

show_object(result, name="body")#, options={ "color": "azure"})
#debug(highlight)
'''
#show a lot:
y=0
x=0
l=0
for s in [1,2,6.25,1]:
    
    y=y+(s+l)/2
    x=0
    for k in range(5):
        x=x+1
        r = k+1 #row
        result = SA_cap (r,s).translate ([y*19.05,x*19.05,0])
        show_object(result)
    l=s

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