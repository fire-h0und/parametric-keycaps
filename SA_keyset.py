import cadquery2 as cq
from cadquery2 import exporters


step=19.05 # mm
gap = 0.95

radius = 33 #mm
height = 10.8 #mm
wall   =  2  # mm how thick wall we want

ride   =  5.5 # mm how deep the switch goes
sw_body= 14   # mm how much the switch requires

r1=0.25 # base corners
r2=2.0    # top edge corners
r3=0.5  # top edge
r4=0.5

row=3

#calculated values:
o=[8,8,4,0,4,-1] # -1 is special case of space row profile

o1=o[row]

size=step - gap
h_size=size/2
top= size-(2*r2)

cave = size-2*wall
if cave < sw_body:
    cave = sw_body

# in between top most and bottom most edges that are non horizontal
selection='not(>Z or <Z or |X or |Y)'

if o1 == 0:
    select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-3] )'
elif o1 == -1:
    select_top='not( <<Z[-3] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-6] )'
else:
    select_top='not( <<Z[-3] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-9] )'

ball = cq.Workplane()
ball = ball.sphere(radius)
ball = ball.rotate([0,0,0],[0,1,0],90)
if o1 != -1:
    ball = ball.translate([o1,0,height+radius])
else:
    ball = ball.translate([0,0,height+radius])

ribs = cq.Workplane(origin=(0,0,ride+1))
ribs = ribs.box(1,cave,2)
ribs = ribs.box(cave,1,2)

cutaway = cq.Workplane(origin=(0,-12,7))
cutaway = cutaway.box(40,20,40)
cutaway = cutaway.rotate([0,0,0],[0,0,1],45)

alps_stem=cq.Workplane(origin=(-1.0,2.15,0))
alps_stem=alps_stem.line(0.625, 0  )
alps_stem=alps_stem.line(0  , 0.1)
alps_stem=alps_stem.line(0.8, 0  )
alps_stem=alps_stem.line(0  ,-0.1)
alps_stem=alps_stem.line(0.625, 0  )
alps_stem=alps_stem.line(0  ,-0.1)

alps_stem=alps_stem.line(   0,-.375 )
alps_stem=alps_stem.line( 0.1, 0  )
alps_stem=alps_stem.line(   0,-.5 )
alps_stem=alps_stem.line(-0.1, 0  )
alps_stem=alps_stem.line(   0,-2.5)
alps_stem=alps_stem.line( 0.1, 0  )
alps_stem=alps_stem.line(   0,-.5 )
alps_stem=alps_stem.line(-0.1, 0  )
alps_stem=alps_stem.line(   0,-.375 )

alps_stem=alps_stem.line(-0.625, 0  )
alps_stem=alps_stem.line(0  ,-0.1)
alps_stem=alps_stem.line(-0.8, 0  )
alps_stem=alps_stem.line(0  , 0.1)
alps_stem=alps_stem.line(-0.625, 0  )
alps_stem=alps_stem.line(0  , 0.1)
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

cube = cq.Workplane(origin=(0,0,-size*.1))
cube = cube.box(size,size,size*.2)

base = cq.Workplane(origin=(0,0,-step/2))
base = base.box(step,step,step)

hole = cq.Workplane(origin=(0,0,-r4+1+ride/2))
hole = hole.box(cave,cave,ride+r4+2)
hole = hole.fillet(r4)
hole = hole.cut(alps_stem)


#single rounded side
side = cq.Workplane("bottom",origin=(h_size-radius,0))
side = side.cylinder(height=size,radius=radius,angle=90,combine=True)

#two opposing sides fused:
sides = side.rotate((0,0,0),(0,0,1),180)
sides = sides.intersect(side)

#fuse opposing sides to form a square
form = sides
form = form.rotate((0,0,0),(0,0,1),90)
form = form.intersect(sides)
form = form.union(cube) # add a base to enable fillet
form = form.edges(selection) # we are pencil (or rocket) shaped
form = form.fillet(r2)
if o1 != -1:
    form = form.cut(ball)
else:
    form = form.intersect(ball.translate([0,0,-(radius+height)-radius+height+gap]))
form = form.edges(select_top)
form = form.fillet(r3)
form = form.cut(base)
form = form.cut(hole)
if row == 4:
    form = form.rotate((0,0,0),(0,0,1),90)
else:
    form = form.rotate((0,0,0),(0,0,1),-90)
form = form.cut(cutaway)




result = form

#highlight = result.edges(select_top)

show_object(result, name="body")#, options={ "color": "azure"})

#ebug(highlight)

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
