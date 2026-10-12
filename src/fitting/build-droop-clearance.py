import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]
p=root/'Woozy-Headroom-Review/Lens-Project/Assets/Woozy-Motion-Runtime.fbx'
bpy.ops.import_scene.fbx(filepath=str(p))
o=bpy.data.objects['WoozyMotionBody'];keys=o.data.shape_keys.key_blocks
keys['GooHeadRoundness'].value=.65
def shape(name):
    return next(k for k in keys if k.name.endswith(name))
upper=shape('SlimeLeftFlowUpper');lower=shape('SlimeLeftFlowLower')
tables=[]
for ui in range(5):
    for li in range(5):
        upper.value=ui/4;lower.value=li/4
        bpy.context.view_layer.update()
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
        tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons])
        front=[];radial=[]
        for yi in range(31):
            y=-7+yi*.5
            row=[]
            for xi in range(65):
                x=-18+xi*.5
                hit=tree.ray_cast(Vector((x/10,-10,(y+12)/10)),Vector((0,1,0)))
                row.append(round(-hit[0].y*10,4) if hit[0] else None)
            valid=[i for i,v in enumerate(row) if v is not None]
            for i,v in enumerate(row):
                if v is None:row[i]=row[min(valid,key=lambda k:abs(k-i))] if valid else 0
            front.extend(row)
            for ai in range(128):
                angle=ai*math.tau/128;dx=math.cos(angle);dz=math.sin(angle)
                hit=tree.ray_cast(Vector(((-1+dx*100)/10,-dz*10,(y+12)/10)),Vector((-dx,dz,0)))
                radius=math.hypot(hit[0].x*10+1,-hit[0].y*10) if hit[0] else 0
                radial.append(round(radius,4))
        tables.append({'front':front,'radial':radial})
        ev.to_mesh_clear()
    print('Upper sample',ui/4,'complete',flush=True)
out={'x0':-18,'y0':-7,'step':.5,'width':65,'height':31,'angles':128,'levels':5,'tables':tables}
(root/'Fitting-source/woozy-droop-envelope.json').write_text(json.dumps(out,separators=(',',':')))
print('Built 25 morph surface samples; no animation timing changes.')
