function createWoozyDroopFitCore(envelope) {
    var currentU=-1,currentL=-1,current={front:[],radial:[]};
    function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
    function mix(a,b,t){return a+(b-a)*t;}
    function grid(table,kind,x,y) {
        var gy=clamp((y-envelope.y0)/envelope.step,0,envelope.height-1),iy=Math.min(envelope.height-2,Math.floor(gy)),fy=gy-iy;
        var width=kind==='front'?envelope.width:envelope.angles;
        var gx=kind==='front'?clamp((x-envelope.x0)/envelope.step,0,width-1):((x/(Math.PI*2)*width)%width+width)%width;
        var ix=kind==='front'?Math.min(width-2,Math.floor(gx)):Math.floor(gx),fx=gx-ix,jx=(ix+1)%width;
        var values=table[kind];
        return mix(mix(values[iy*width+ix],values[iy*width+jx],fx),mix(values[(iy+1)*width+ix],values[(iy+1)*width+jx],fx),fy);
    }
    function surface(kind,x,y,upper,lower) {
        if(!upper&&!lower)return grid(envelope.tables[0],kind,x,y);
        prepare(upper,lower);return grid(current,kind,x,y);
    }
    function prepare(upper,lower) {
        if(currentU===upper&&currentL===lower)return;
        currentU=upper;currentL=lower;
        var u=clamp(upper||0,0,1)*4,l=clamp(lower||0,0,1)*4;
        var ui=Math.min(3,Math.floor(u)),li=Math.min(3,Math.floor(l)),fu=u-ui,fl=l-li,t=envelope.tables;
        ['front','radial'].forEach(function(kind){
            var a=t[ui*5+li][kind],b=t[ui*5+li+1][kind],c=t[(ui+1)*5+li][kind],d=t[(ui+1)*5+li+1][kind],out=current[kind];
            for(var i=0;i<a.length;i++)out[i]=mix(mix(a[i],b[i],fl),mix(c[i],d[i],fl),fu);
        });
    }
    function frontSample(x,y,neutral) {
        var values=(neutral?envelope.tables[0]:current).front,width=envelope.width;
        var gx=clamp((x-envelope.x0)/envelope.step,0,width-1),gy=clamp((y-envelope.y0)/envelope.step,0,envelope.height-1);
        var ix=Math.min(width-2,Math.floor(gx)),iy=Math.min(envelope.height-2,Math.floor(gy)),fx=gx-ix,fy=gy-iy;
        var a=values[iy*width+ix],b=values[iy*width+ix+1],c=values[(iy+1)*width+ix],d=values[(iy+1)*width+ix+1];
        return {value:mix(mix(a,b,fx),mix(c,d,fx),fy),x:mix(b-a,d-c,fy)/envelope.step,y:mix(c-a,d-b,fx)/envelope.step};
    }
    function vertex(v,weight,pose,drop,isStrap) {
        var upper=drop.upper||0,lower=drop.lower||0;
        if(upper===0&&lower===0&&pose.goggleRoll===0&&pose.goggleX===0&&pose.goggleY===0&&pose.goggleZ===0)return v.slice();
        var w=isStrap?(weight>=.98?1:weight):1,a=pose.goggleRoll*w,co=Math.cos(a),si=Math.sin(a);
        var x=co*v[0]-si*v[1]+pose.goggleX*w,y=si*v[0]+co*v[1]+pose.goggleY*w;
        var z=v[2]+pose.goggleZ*w,nx=co*v[3]-si*v[4],ny=si*v[3]+co*v[4],nz=v[5];
        prepare(upper,lower);
        var base=frontSample(v[0],v[1]+1.6,true),now=frontSample(x,y+1.6,false);
        var delta=Math.max(0,now.value-base.value),front=isStrap?(weight>=.98?1:clamp((weight-.80)/.18,0,1)):1;
        z+=delta*front;
        if(!isStrap&&delta>0) {
            var gx=now.x-(co*base.x-si*base.y),gy=now.y-(si*base.x+co*base.y);
            nx-=gx*nz;ny-=gy*nz;
        }
        if(isStrap&&front<1) {
            var dx=x+1,dz=z+9.9,radius=Math.sqrt(dx*dx+dz*dz),angle=Math.atan2(dz,dx);
            var need=surface('radial',angle,y+1.6,upper,lower)+.55;
            if(radius>0&&radius<need){var scale=need/radius;x=-1+dx*scale;z=dz*scale-9.9;}
        }
        var length=Math.sqrt(nx*nx+ny*ny+nz*nz);
        if(length>0){nx/=length;ny/=length;nz/=length;}
        return [x,y,z,nx,ny,nz,v[6],v[7]];
    }
    return {vertex:vertex,surface:surface};
}
