import cadquery2 as cq

step=19.05 # mm
gap = 0.95

radius = 33 # mm
height = 10.8 # mm

r1=0.25 # base corners
r2=2.0    # top edge corners
r3=0.5  # top edge
r=5

#calculated values:
o=[8,8,4,0,4,-1] # -1 is special case of space row profile

o1=o[r]

size=step - gap
h_size=size/2
top= size-(2*r2)

# in between top most and bottom most edges that are non horizontal
selection='not(>Z or <Z or |X or |Y)'

if o1 == 0:
    select_top='not( <<Z[-2] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-3] )'
elif o1 == -1:
    select_top='not( <<Z[-3] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-7] )'
else:
    select_top='not( <<Z[-3] or <Z or >>X[-2] or <<X[-2] or >>Y[-3] or <<Y[-3] or >>Z[-9] )'

if o1 != -1:
    ball = cq.Workplane(origin=(o1,0,height+radius))
else:
    ball = cq.Workplane(origin=(0,0,height+radius))

ball = ball.sphere(radius)

cube = cq.Workplane(origin=(0,0,-size*.1))
cube = cube.box(size,size,size*.2)

base = cq.Workplane(origin=(0,0,-step/2))
base = base.box(step,step,step)

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
if r == 4:
    form = form.rotate((0,0,0),(0,0,1),90)
else:
    form = form.rotate((0,0,0),(0,0,1),-90)





result = form

#highlight = result.edges(select_top)

show_object(result, name="body", options={ "color": "azure"})

#ebug(highlight)