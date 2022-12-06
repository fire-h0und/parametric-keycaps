from .parameters import *
import cadquery as cq

def tri_h (k,h):
    '''Right Triangle's height: k= kathete, h=hypotenuse
    '''
    a = sqrt( h**2 - (k/2)**2 ) # answer (other kathete)
    return a

#the radius and the origin points can form a shape:
#        ^
#       /|\ r
#      / |h\
#     -------
# -pos   0   pos
#

#radius intersection point:
#h = tri_h (pos*2,r)

def init(style:str):
    #"low","semilow","medium","semihigh","high"
    global o,height,wall,roundness,radius,radius2,radius3,ride,r2,r3,r4,sw_body,ribsZ,ride,cave,radius_offset,shape_compensation

    if style in ["low","semilow","semihigh","high","max"]:
        print(style)
        if style == "low": # this is most suited for Choc V2 switch
            height   = 3.5 #mm
            wall     =  1.5   #mm how thick wall we want
            roundness= 3.0 # measureless factor: from 0 to height gives sane values, a good default is 8.5
            radius   = size + (height-roundness)*4   #mm sides radius tuned to height 8.5-0
            radius2  = 67     #mm top radius (37 or 64 mm)
            radius3  = radius2 - 14 #mm alternate top radius TODO (default is 8 or 11 mm)
            radius_offset = 1.1 #mm special case when space radius needs tweaking
            shape_compensation = 1.0

            ride   =  2.5 #mm how deep the switch goes (5.5 for Alps, 3.0 mm for Choc V2)
            r4     = 0.95 #mm stem hole edge chamfers
            sw_body= 15.5   #mm how much the switch requires
            ribsZ= 0.25 #mm high (stem ribs)
            o=[6,6,2,0,2,-1]

        elif style == "semilow": # this is a low ride cap suited for fast or low switches
            height   = 7.6
            wall     =  2
            roundness= 4.5
            radius   = size + (height-roundness)*4
            radius2  = 57
            radius3  = radius2 - 11
            radius_offset = 1.15
            shape_compensation = .5

            ride   = 4.0
            r4     = 0.5
            sw_body= 15.5
            ribsZ  = 0.5
            o=[7,7,3,0,3,-1]

        elif style == "semihigh": # this is classical middle ride full size switch preset
            height   = 10.5
            wall     =  2
            roundness= 4.5
            radius   = size + (height-roundness)*4
            radius2  = 57
            radius3  = radius2 - 8
            radius_offset = 1.15
            shape_compensation = 0.25

            ride   =  5.5
            r3     = 0.69
            r4     = 0.95
            sw_body= 14
            ribsZ  = 1.0
            o=[7,7,4,0,4,-1]

        elif style == "high": # this is similar to the vintage SA DSA profile
            height   = 11.9
            wall     =  2
            roundness= 5.5
            radius   = size + (height-roundness)*4
            radius2  = 37
            radius3  = radius2 - 11
            radius_offset = 1.2
            shape_compensation = 0.55

            ride   =  5.5
            r4     = 0.95
            sw_body= 14
            ribsZ  = 1.5
            o=[8,8,5,0,5,-1]

        elif style == "max": # this is for living on high heels
            height   = 13.7
            wall     =  2
            roundness= 4.5
            radius   = size + (height-roundness)*4
            radius2  = 32
            radius3  = radius2 - 11
            radius_offset = 1.2
            shape_compensation = 0.35

            ride   =  5.5
            r4     = 1.5
            r2     = 2.0
            sw_body= 14
            ribsZ= 2.5
            o=[8,8,5,0,5,-1]
            o=[step/2,step/2,step/4,0,step/4,-1]

    else:
        #generic shape parameters:
        height   = 8.6 # this is classical middle ride full size switch preset
        wall     =  2
        roundness= 4.5
        radius   = size + (height-roundness)*4
        radius2  = 57
        radius3  = radius2 - 8
        radius_offset = 1.15
        shape_compensation = 0.5

        ride   =  5.5
        r4     = 0.95
        sw_body= 14
        ribsZ  = 1.5
        o=[7,7,4,0,4,-1]

    cave = size-2*wall # "cave" is the stem hole depth
    if cave < sw_body: # fitting the upper switch body
        cave = sw_body
    return

def hole_gen(dims,ride):
    width,length=dims

    #shape the hole in negative
    hole = cq.Workplane(origin=(0,0,(ride+ribsZ)/2-r4/2))
    # shift it down for half the radius
    # so the bottom part of it can be cut off
    hole = hole.box(cave+(step*(length-1)),cave+(step*(width-1)),r4+ride+ribsZ)
    hole = hole.fillet(r4)
    return hole

def rib_gen (dims):
    width,length=dims
    global ride
    #shape the ribs in the hole ceiling
    ribs = cq.Workplane(origin=(0,0,ride+ribsZ/2))
    ribs = ribs.box(ribsW,cave+(step*(width-1)),ribsZ)
    ribs = ribs.box(cave+(step*(length-1)),ribsW,ribsZ)
    return ribs

def alpsstem(dims):
    width,length=dims

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
    #alps_stem=alps_stem.union(ribs)

    return alps_stem

def alpsstab(dims):
    width,length=dims

    alps_stab=cq.Workplane(origin=(stab_offset,0,-1))#-stab_retract+ribsZ/2+r4))
    alps_stab=alps_stab.rect(stab_width+2*stab_wall,stab_length+2*stab_wall)
    #alps_stab=alps_stab.clean()
    alps_stab=alps_stab.extrude(ride+ribsZ+r4)
    #alps_stab=alps_stab.union(ribs)

    alps_stab_hole=cq.Workplane(origin=(stab_offset,0,-1))
    alps_stab_hole=alps_stab_hole.rect(stab_width,stab_length)
    alps_stab_hole=alps_stab_hole.extrude(ride+ribsZ/2+r4+2)
    alps_stab=alps_stab.cut(alps_stab_hole)
    return alps_stab

def chocv1stem(dims):
    width,length=dims
    correction= 0.025          #mm
    stemX     = 1.2-correction #mm
    stemfree  = 0.8            #mm
    stemY     = 3.0-correction #mm
    apartX    = 5.7/2          #mm
    apartY    = stemY/2-stemfree/2

    #shape the ribs in the hole ceiling
    ribs = rib_gen(dims)

    stem=cq.Workplane(origin=(0,0,-1))
    stem=stem.pushPoints([(apartY,apartX),(-apartY,apartX),(-apartY,-apartX),(apartY,-apartX)])
    stem=stem.rect(stemfree,stemX)
    stem=stem.pushPoints([(0,apartX),(0,-apartX)])
    stem=stem.rect(stemY,stemfree)
    stem=stem.extrude(ride+1+2.50) # this is fixed length
    stem=stem.union(ribs)

    return stem

def mxstem(dims):
    width,length=dims
    #this very MX stem is tested so far to fit:
    # Kailh ChocV2,
    # Kailh BOX (square)
    # Kailh Silent BOX (round stem)
    # Cherry MX "+" like stem
    mx_x_x, mx_x_y =4.15-0.05, 1.27+0.05
    mx_y_x, mx_y_y =1.12+0.05, 4.15-0.05

    mx_stem=cq.Workplane(origin=(0,0,-1))
    mx_stem=mx_stem.circle(2.75) # this is fixed value
    mx_stem=mx_stem.clean()
    mx_stem=mx_stem.extrude(ride+ribsZ+3.1) # this is fixed length
    #my stem size fixes for FDM (a smidge too tight)
    mx_stem_hole=cq.Workplane(origin=(0,0,-2))
    mx_stem_hole=mx_stem_hole.rect(mx_x_x, mx_x_y)
    mx_stem_hole=mx_stem_hole.rect(mx_y_x, mx_y_y)
    mx_stem_hole=mx_stem_hole.extrude(ride+2.95) # +2 mm to just be on the safe side here
    mx_stem=mx_stem.cut(mx_stem_hole)
    return mx_stem

def alps_hole(ride,dims):
    width,length=dims

    rotation=-90
    if width == 1 and length >1.75:
        rotation=0
        width = length
        length = 1

    #shape the ribs in the hole ceiling
    ribs = rib_gen(dims)

    #shape the stem in positive form
    alps_stem=alpsstem(dims)

    #add Alps stab stems:
    alps_stab=alpsstab(dims)
    #TODO

    hole = hole_gen(dims,ride)
    hole = hole.cut(ribs)
    hole = hole.cut(alps_stem)

    #add stabilizers
    spacing = 0
    if width == 7 or width == 6.25: # space keys:
        spacing = 98 #mm
    elif width == 2.75 or width == 3: # where will you find 3U stabilizer wire anyway?
        spacing = 41 #mm
    elif width == 2.25 or width == 2:
        spacing = 27 #mm
    if spacing != 0:
        hole=hole.cut(alps_stab.translate([0,spacing/2,0]))
        hole=hole.cut(alps_stab.translate([0,-spacing/2,0]))

    #TODO add the 35mm offset 4mm dia stabilizer axle too
    # add the 35mm to the right 2nd alps stem to every 7U space bar
    if width == 7: # space keys:
        hole = hole.cut(alps_stem.translate([0,35,0]))

    return hole.rotate((0,0,0),(0,0,1),rotation)

def alpsmx_hole(ride,dims):
    width,length=dims

    #shape the ribs in the hole ceiling
    ribs = rib_gen(dims)

    #shape the stem in positive form
    alps_stem=alpsstem(dims)

    #MX stab stems:
    mx_stem=mxstem(dims)

    hole = hole_gen(dims,ride)
    hole = hole.cut(ribs)
    hole = hole.cut(alps_stem)

    #add stabilizers:
    spacing = 0

    if width > 7: # huuge space keys (we''l use 7U stab onward)
        spacing = ( 7 - 1 ) * 3/4 * 25.38 #mm
    elif width > 2.75: # space keys:
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

def chocv1_hole (ride,dims):
    width,length=dims

    rotation=-90
    if width == 1 and length >1.75:
        rotation=0
        width = length
        length = 1

    ribs = rib_gen(dims)

    #shape the stem in positive form
    stem=chocv1stem(dims)
    mx_stem=mxstem(dims)
    offset = 0.65 #mm Choc stem stabilizer offset

    hole = hole_gen(dims,ride)
    hole = hole.cut(ribs)
    hole = hole.cut(stem)


    #add stabilizers:
    spacing = 0
    if width >= 6.25: # space keys:
        spacing = 50*2 #mm
    elif width > 2.75: # space keys:
        spacing = 38 #mm
    #elif width > 2.75: # it's 3U:
    #    spacing=1.5 * 25.38 #mm   (it's 3/4" (== 1U) x  3U - (2 x 1/2U) exactly )
    elif width > 1.75:
        spacing= 24 #mm
    if spacing != 0:
        mx_stab=mx_stem.translate([offset,spacing/2,0])
        hole=hole.cut(mx_stab)
        mx_stab=mx_stem.translate([offset,-spacing/2,0])
        hole=hole.cut(mx_stab)
    return hole.rotate((0,0,0),(0,0,1),rotation)

def mx_hole (ride,dims):
    width,length=dims

    #shape the ribs in the hole ceiling
    ribs = rib_gen(dims)

    #shape the stem in positive form
    mx_stem=mxstem(dims)

    hole = hole_gen(dims,ride)
    hole = hole.cut(ribs)
    hole = hole.cut(mx_stem)

    #add stabilizers:
    spacing = 0
    if width > 7: # huuge space keys (we''l use 7U stab onward)
        spacing = ( 7 - 1 ) * 3/4 * 25.38 #mm
    elif width > 2.75: # space keys:
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

def topstamp (width,length,stamp_radius):
    #width=1.25
    #length=2

    #TODO:
    #  account for sub 1U sized keycaps one day maybe

    if width == 1 and length == 1:
        #we have a plain 1U key:
        stamp = cq.Workplane("front",origin=(0,0,0))
        stamp = stamp.sphere(stamp_radius)
        # rotate the spere so the seam is more favorably placed upun the body
        stamp = stamp.rotate([0,0,0],[1,0,0],90)
    elif length == 1:
        #we have an 1U long but wider key
        stamp = cq.Workplane("front",origin=(0,0,0))
        stamp = stamp.move((width-1)*step/2+stamp_radius,0)
        stamp = stamp.radiusArc(endPoint=((width-1)*step/2,-stamp_radius),radius=stamp_radius)
        stamp = stamp.line(-(width-1)*step,0)
        stamp = stamp.radiusArc(endPoint=(-(width-1)*step/2-stamp_radius,0),radius=stamp_radius)
        stamp = stamp.wire()
        stamp = stamp.revolve(0,[0,0,0],[1,0,0])
        #stamp = stamp.rotate((0,0,0),(0,0,1),90)
    elif width == 1:
        #we have a 1U narrow but longer key
        stamp = cq.Workplane("front",origin=(0,0,0))
        stamp = stamp.move((length-1)*step/2+stamp_radius,0)
        stamp = stamp.radiusArc(endPoint=((length-1)*step/2,-stamp_radius),radius=stamp_radius)
        stamp = stamp.line(-(length-1)*step,0)
        stamp = stamp.radiusArc(endPoint=(-(length-1)*step/2-stamp_radius,0),radius=stamp_radius)
        stamp = stamp.wire()
        stamp = stamp.revolve(0,[0,0,0],[1,0,0])
        #and just rotate for lenghtwise application
        stamp = stamp.rotate((0,0,0),(0,0,1),90)
    else:
        # we have a sizeable keycap here
        stamp = cq.Workplane("XY",origin=(0,0,-stamp_radius))
        stamp = stamp.rect((length-1)/2*step,(width-1)/2*step)
        stamp = stamp.offset2D(stamp_radius)
        stamp = stamp.extrude(stamp_radius*2+.01)
        stamp = stamp.edges('not( |Z )')
        stamp = stamp.fillet(stamp_radius)
    return stamp

def spherical_cap (stem,row,dims):
    width,length=dims

    cap_radius = radius2
    if row < -1: #negative means accented (except -1)
        cap_radius = radius3
        row = abs(row)

    if width > .75:
        o1=o[row]
        #preparing the forming shapes:
        stamp = topstamp (width,length,cap_radius)

        if o1 != -1: # are we convex? -1 is convex dead center
            stamp = stamp.translate([0,o1,height+cap_radius]) # slide as per row offset
        else:
            stamp = stamp.translate([0,0,height*radius_offset-cap_radius])  # we are, put it dead on center

        #the base containing shape
        cube = cq.Workplane(origin=(0,0,-size*.1))
        cube = cube.box(size*width,size*length,size*.2)

        #the bottom forming shape
        base = cq.Workplane(origin=(0,0,-step))
        # we want go high because sculpt is measured
        # from the dish lowest point -
        # we need enough material at the rim
        base = base.box(step*width,step*length,step*2.25)

        #single rounded side
        side = cq.Workplane("bottom",origin=(size/2-radius,0))
        side = side.cylinder(height=step*(width+0),radius=radius,angle=90,combine=True)
        side1 = cq.Workplane("bottom",origin=(size/2-radius,0))
        side1= side1.cylinder(height=step*(length+0),radius=radius,angle=90,combine=True)

        #two opposing sides fused:
        if length !=1:
            side2 =  side.intersect(base.rotate((0,0,0),(0,0,1),90).translate([0,0,height*1.35]))
            side2 = side2.intersect(base.rotate((0,0,0),(0,0,1),90).translate([0,0,height*1.35])) # half side profile
            side2 = side2.translate([ ((length-1)*step/2) , 0 , 0 ])
            sides = side2.rotate((0,0,0),(0,0,1),180)
            sides = sides.union(side2)
        else:
            sides = side.rotate((0,0,0),(0,0,1),180)
            sides = sides.intersect(side)
        sides = sides.rotate((0,0,0),(0,0,1),90)

        #two opposing sides at switch width distance
        sides_L = side1
        sides_L = sides_L.intersect(base.translate([step/2,0,step-2])) # half side profile
        sides_L = sides_L.translate([ ((width-1)*step/2) , 0 , 0 ])
        sides_R = sides_L.rotate((0,0,0),(0,0,1),180)
        #sides length wise:
        sides_LW= sides_L.union(sides_R)
        #are we wider than 1U?
        if width != 1.0: # for non unit size switchs
            sides_LW= sides_LW.box((width-1)*step,(length)*step*1.1,step*2) #we can't draw 0 width box
            #with (width-1) we are certainly clear the end of the side profiles
        sides_LW= sides_LW.intersect(base.translate([0,0,step-2]),clean=True)

        #fuse opposing sides to form a square
        form  = sides_LW
        sides = sides.rotate((0,0,0),(0,0,1),0.05)
        form  = form.intersect(sides)

        #
        # fillet sides
        #
        e_selection='not( #Z )'
        d = form#.edges(e_selection)
        form = form.edges(e_selection) # we are pencil (or rocket) shaped
        form = form.fillet(r2)

        #o1 = -1 is space row
        if o1 != -1: # we are digging out a conqave shape:
            stamp_offset=[0,0,0]
            stamp = stamp.rotate((0,0,0),(0,0,1),-0.05)
            shape = stamp.translate(stamp_offset)
            form = form.cut(stamp)
        else: # we are building a convex shape:
            stamp_offset=[0,0,height*5]
            stamp = stamp.rotate((0,0,0),(0,0,1),-0.05)
            shape = base.translate(stamp_offset).cut(stamp.translate([0,0,shape_compensation]))
            form = form.cut(shape,clean=True)

        # special case for row 4 (before we cut the switch hole)
        if row == 4:
            form = form.rotate((0,0,0),(0,0,1),180)
            #log("rotated :180")
        #
        # fillet top
        #
        f_select_top = '%SPHERE or ( %CYLINDER exc (<X or >X or <Y or >Y) )'
        e_select_top = 'not( %CIRCLE )'
        #d    = form.faces(f_select_top).edges(e_select_top)
        #d = form.edges(e_select_top)
        form = form.faces(f_select_top).edges(e_select_top)
        form = form.fillet(r3) # iff this fails try rise stamp_offset Z multiplier to 5 or more

        form = form.cut(base.translate([0,0,-2.5]))
        rotation=0
        if width == 1 and length!=1:
            tw,tl=length,width
            width,length=tw,tl
            rotation=90
        else:
            pass
        if stem in ["","MX","mx"]:
            form = form.cut(mx_hole(ride,(width,length)).rotate((0,0,0),(0,0,1),rotation))
        elif stem in ["Alps","ALPS","alps"]:
            form = form.cut(alps_hole(ride,(width,length)).rotate((0,0,0),(0,0,1),rotation))
        elif stem in ["AlpsMX","ALPSMX","alpsmx"]:
            form = form.cut(alpsmx_hole(ride,(width,length)).rotate((0,0,0),(0,0,1),rotation))
        elif stem in ["ChocV1","V1","chocv1","Choc","choc"]:
            form = form.cut(chocv1_hole(ride,(width,length)).rotate((0,0,0),(0,0,1),rotation))
            #form = form.rotate((0,0,0),(0,0,1),90)

        #    return sides.rotate((0,0,0),(0,0,1),90).intersect(sides_LW)
    else:
        form = cq.Workplane()
    return form
