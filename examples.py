
#TODO:
# pick sets of values across variables and make keyset presets

preset='high'
init(preset) # default (none) style
#
#"low"
#
#  a most low profile specially suited for Kailh Choc V1 and V2 switches
#  (depending on tems used)
#
#"semilow"
#
#  an down to the floor profile somewhat reminiscent to the Cherry profile
#  but with spherical tops
#
#"medium"
#
#  an mid way profile for quick typing well suited for most switches
#
#"semihigh"
#
#  an traditional and serious profile
#
#"high"
#
#  an SA lookalike profile for tightly moving switches like Kailh BOX
#
#
#"max"
#
# max height advised




'''

#selection='( <Z or |X or |Y )'
f_select_top = '%SPHERE or ( %CYLINDER exc (<X or >X or <Y or >Y) )'
e_select_top = 'not( %CIRCLE ) '

result = spherical_cap ("mx",4,(1.25,1))
#highlight = result.edges(selection)
#highlight = result.faces(f_select_top).edges(e_select_top)


show_object(result, name="body", options={cq.Color("blue")})
#debug(highlight)
'''
'''
#show a lot:
y=0
x=0
l=0


for s in [(1,2),(1.25,1),(1.5,1.5),(1.75,1),(2.0,1),(1,1)]:
    sx,sy=s
    y=y+(sx+l)/2
    x=0
    for k in range(0,5):
        x=x+sy
        r = k+1 #row
        result = spherical_cap ("choc",r,s).translate ([y*step,(x-(sy/2))*step,0])
        show_object(result)
        highlight = result.faces(f_select_top).edges(e_select_top)
        debug(highlight)

    l=sx
'''
'''
# sculpt, width
#a MIT planck:
keybrd = [
#    [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]],
    [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]],
    [[2,1],[2,1],[2,1],[2,1],[-2,1],[2,1],[2,1],[-2,1],[2,1],[2,1],[2,1],[2,1]],
    [[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1]],
#    [[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1]],
    [[4,1],[4,1],[4,1],[4,1],[5,1],[5,2],[5,0],[5,1],[4,1],[4,1],[4,1],[4,1]],
    ]
'''

#ANSI PC AT%
keybrd = [
  [[1,1],[1,1],[0,.75],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,2],[1,0],[0,.75],[1,1],[1,1.5],[1,1.5]],
  [[2,1],[2,1],[0,.75],[2,1.5],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1.5],[2,0],[0,.75],[2,1],[2,1],[2,1],[2,1]],
  [[3,1],[3,1],[0,.75],[3,1.75],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,2.25],[3,0],[3,0],[0,.75],[3,1],[3,1],[3,1],[3,1]],
  [[4,1],[4,1],[0,.75],[4,2.25],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,2.75],[4,0],[4,0],[4,0],[0,.75],[4,1],[4,1],[4,1],[4,1]],
  [[4,1],[4,1],[0,.75],[4,1.25],[4,1.25],[4,1.25],[5,6.25],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,0],[4,1.25],[4,1.25],[4,1.25],[4,1.25],[5,.75],[4,2],[4,1],[4,1]],
  ]

'''
#ANSI 60%
keybrd = [
  [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,2],[1,0]],
  [[2,1.5],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1],[2,1.5],[2,0]],
  [[3,1.75],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,1],[3,2.25],[3,0],[3,0]],
  [[4,2.25],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,2.75],[4,0],[4,0],[4,0]],
  [[4,1.25],[4,1.25],[4,1.25],[5,6.25],[4,1.25],[4,1.25],[4,1.25],[4,1.25]],
  ]

'''
'''
#ANSI unique keys
keybrd = [
  [[1,1],[1,2]], #esc row with 2U backspace key
  [[2,1.5],[2,1]], # ANSI tab row 2x 1.5U
  [[3,1.75],[3,1],[3,2.25]], # ANSI enter row non stepped CAPS
  [[4,2.25],[4,1],[4,2.75]], # ANSI shift row
  [[4,1.25],[5,6.25]], #6.25U space row (7x 1.25U)
  [[4,1.75]], # ISO with short shift
  [[5,7]], #7U space row
  ]

#Ortho unique keys
keybrd = [
  [[1,1]],
  [[2,1]], # TODO accented [2,1]
  [[3,1]],
  [[4,1],[5,1],[5,2]], # mods and 2U space
  ]
'''

a=-1
b=0
for x in range(len(keybrd)):
    a=a+1
    log(b)
    b=0
    for y in range(len(keybrd[x])):
        t="MX"
        s=keybrd[x][y][0]
        w=keybrd[x][y][1]
        b=b+w/2
        result = spherical_cap(t,s,(w,1)).translate([-b*19.05,a*19.05,0])
        b=b+w/2
        show_object(result)
        keyname=preset+'_'+t+'_R'+str(s)+'_W'+str(w)+'_parkey.stl'
        log (keyname)
        #exporters.export(
        #    result,
        #    keyname,
        #    tolerance=0.025,
        #    angularTolerance=0.1
        #    )

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
