import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]
p=root/'Woozy-Headroom-Review/Lens-Project/Assets/Woozy-Motion-Runtime.fbx'
bpy.ops.import_scene.fbx(filepath=str(p))
o=bpy.data.objects['WoozyMotionBody']
if o.data.shape_keys and 'GooHeadRoundness' in o.data.shape_keys.key_blocks:
    o.data.shape_keys.key_blocks['GooHeadRoundness'].value=.65
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons])
def ray(x,y,z,dx,dz):
    hit=tree.ray_cast(Vector((x/10,-z/10,(y+12)/10)),Vector((dx, -dz,0)))
    return Vector((hit[0].x*10,hit[0].z*10-12,-hit[0].y*10)) if hit[0] else None
def face(x,y):
    return ray(x,y,100,0,-1)
def edge(y):
    hit=ray(100,y,0,-1,0)
    return hit.x if hit else 10
def goggle(v):
    x,y,z=v[0],v[1]+1.6,v[2]+9.9
    if x>3.8:
        limit=min(10.62,edge(y)-.45)
        x=3.8+(x-3.8)*max(.35,(limit-3.8)/(10.62-3.8))
    hit=face(x,y)
    if hit:z=v[2]+hit.z+2.5
    return Vector((x,y,z))
def outside(pos,clearance=.55):
    direction=Vector((pos.x+1,0,pos.z))
    if direction.length<.01:return pos
    direction.normalize()
    start=Vector((-1, pos.y,0))+direction*100
    hit=ray(start.x,pos.y,start.z,-direction.x,-direction.z)
    if hit:
        radius=(pos-Vector((-1,pos.y,0))).length
        need=(hit-Vector((-1,pos.y,0))).length+clearance
        if radius<need:return Vector((-1,pos.y,0))+direction*need
    return pos
meshes=json.loads((root/'Fitting-source/goggle-original-meshes.json').read_text())
fitted={};min_clear=100
for d in meshes:
    original=d['vertices'];vertices=original[:]
    for i in range(0,len(vertices),8):
        v=original[i:i+8]
        if d['group']=='goggles':
            pos=goggle(v)
        else:
            old=Vector((v[0],v[1]+1.6,v[2]+9.9))
            direction=Vector((old.x+1,0,old.z));direction.normalize()
            start=Vector((-1,old.y,0))+direction*100
            hit=ray(start.x,old.y,start.z,-direction.x,-direction.z)
            thickness=.10*(v[3]*direction.x+v[5]*direction.z)
            pos=hit+direction*(.65+thickness) if hit else old
            t=max(0,min(1,(old.z-3)/5));t=t*t*(3-2*t)
            pos=pos.lerp(goggle(v),t)
            pos=outside(pos,.50+thickness)
        vertices[i:i+3]=[round(pos.x,6),round(pos.y-1.6,6),round(pos.z-9.9,6)]
    # Preserve authored seams: recalculate surface normals by coincident position.
    normals={}
    def key(i):return tuple(vertices[i*8:i*8+3])
    for j in range(0,len(d['indices']),3):
        ids=d['indices'][j:j+3]
        a,b,c=[Vector(vertices[k*8:k*8+3]) for k in ids]
        n=(b-a).cross(c-a)
        for k in ids:
            ky=key(k);normals[ky]=normals.get(ky,Vector())+n
    for i in range(len(vertices)//8):
        n=normals[key(i)]
        if n.length>1e-9:n.normalize();vertices[i*8+3:i*8+6]=[round(v,6) for v in n]
    fitted[d['group']+'/'+d['material']]=vertices
(root/'Fitting-source/goggle-fitted-vertices.json').write_text(json.dumps(fitted,separators=(',',':')))
print('Fitted',len(fitted),'mesh batches against the authored body, with strap clearance.')
