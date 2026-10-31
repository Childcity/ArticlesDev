"""Точні SDF та найближчі точки їхніх рівнів для еталонних геометрій.

Проєкція на багатокутниковий офсет перебирає сегменти, дуги та їхні
перетини. Це важливо біля кутів: крок за градієнтом там недостатній.
"""
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from matplotlib.path import Path

POLYGON = np.array([[-.85,-.4],[-.3,-.4],[-.3,-.10],[.3,-.10],
                    [.3,-.4],[.85,-.4],[.85,.4],[.3,.4],[.3,.10],
                    [-.3,.10],[-.3,.4],[-.85,.4]])


def polygon_sdf(p, vertices=POLYGON):
    a=vertices;v=np.roll(vertices,-1,axis=0)-a
    w=np.asarray(p)[:,None,:]-a
    t=np.clip(np.sum(w*v,axis=-1)/np.sum(v*v,axis=-1),0,1)
    distance=np.min(np.linalg.norm(w-t[:,:,None]*v,axis=-1),axis=1)
    inside=Path(np.vstack([vertices,vertices[0]])).contains_points(p)
    return np.where(inside,-distance,distance)


def unit(p):
    """Детермінований вибір напрямку для неєдиної проєкції з центра."""
    length=np.linalg.norm(p,axis=1)
    result=p/np.maximum(length[:,None],1e-30)
    result[length<1e-14]=np.eye(p.shape[1])[0]
    return result


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


@lru_cache(maxsize=512)
def polygon_primitives(vertices_tuple,level):
    """Кандидатні відрізки та кола офсету; їхні кінці після обрізання.

    Кожна точка рівня відстані до багатокутника належить зсунутому
    ребру або колу навколо вершини. Допустимі частини фільтруються SDF.
    Найближча точка обрізаної частини — ортопроєкція або її кінець.
    """
    vertices=np.asarray(vertices_tuple);a=vertices;b=np.roll(a,-1,axis=0)
    v=b-a;normal=np.column_stack([-v[:,1],v[:,0]])/np.linalg.norm(v,axis=1)[:,None]
    r=abs(level)
    starts=np.concatenate([a+r*normal,a-r*normal])
    ends=np.concatenate([b+r*normal,b-r*normal])
    endpoints=[*starts,*ends]
    # Перетини сегментів утворюють кінці видимих частин офсетних ребер.
    for i,(p,q) in enumerate(zip(starts,ends)):
        d=q-p
        for j in range(i):
            s=starts[j];e=ends[j]-s;det=cross(d,e)
            if abs(det)>1e-14:
                u=cross(s-p,e)/det;w=cross(s-p,d)/det
                if -1e-10<=u<=1+1e-10 and -1e-10<=w<=1+1e-10:
                    endpoints.append(p+u*d)
        if r>1e-14:
            for center in vertices:
                z=p-center
                roots=np.roots([d@d,2*z@d,z@z-r*r])
                for root in roots:
                    if abs(root.imag)<1e-8 and -1e-10<=root.real<=1+1e-10:
                        endpoints.append(p+root.real*d)
    if r>1e-14:
        for i,c in enumerate(vertices):
            for other in vertices[:i]:
                delta=other-c;distance=np.linalg.norm(delta)
                if 1e-14<distance<=2*r+1e-12:
                    mid=(c+other)/2
                    perp=np.array([-delta[1],delta[0]])/distance
                    height=np.sqrt(max(0,r*r-distance*distance/4))
                    endpoints.extend([mid+height*perp,mid-height*perp])
    endpoints=np.asarray(endpoints)
    valid=np.abs(polygon_sdf(endpoints,vertices)-level)<2e-8
    return starts,ends,vertices,endpoints[valid]


def polygon_project(p,vertices,level):
    starts,ends,circles,endpoints=polygon_primitives(tuple(map(tuple,vertices)),float(level))
    candidates=[]
    for a,b in zip(starts,ends):
        v=b-a;t=np.clip((p-a)@v/(v@v),0,1)
        candidates.append(a+t[:,None]*v)
    if abs(level)>1e-14:
        for c in circles:candidates.append(c+abs(level)*unit(p-c))
    for endpoint in endpoints:candidates.append(np.broadcast_to(endpoint,p.shape))
    best=np.full_like(p,np.nan);distance=np.full(len(p),np.inf)
    for candidate in candidates:
        valid=np.abs(polygon_sdf(candidate,vertices)-level)<3e-8
        d=np.linalg.norm(candidate-p,axis=1)
        take=valid & (d<distance)
        best[take]=candidate[take];distance[take]=d[take]
    return best


@dataclass(frozen=True)
class Geometry:
    shape: str='circle'
    angle: float=0.
    shift: float=0.
    square_half: float=.48

    def local(self,p):
        p=np.asarray(p,dtype=float).copy();p[:,0]-=self.shift
        a=np.deg2rad(self.angle)
        rotation=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        p[:,:2]=p[:,:2]@rotation
        return p

    def world(self,p):
        p=p.copy();a=np.deg2rad(self.angle)
        rotation=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        p[:,:2]=p[:,:2]@rotation.T;p[:,0]+=self.shift
        return p

    def __call__(self,points):
        p=self.local(points)
        if self.shape in ('circle','sphere'):return np.linalg.norm(p,axis=1)-.55
        if self.shape=='square':
            q=np.abs(p)-self.square_half
            return np.linalg.norm(np.maximum(q,0),axis=1)+np.minimum(np.max(q,axis=1),0)
        if self.shape=='two_circles':
            return np.minimum(np.linalg.norm(p-[-.4,0],axis=1),np.linalg.norm(p-[.4,0],axis=1))-.32
        if self.shape=='neck':return polygon_sdf(p)
        if self.shape=='torus':return np.hypot(np.linalg.norm(p[:,:2],axis=1)-.52,p[:,2])-.20
        raise ValueError(self.shape)

    def project_level(self,points,level):
        """Найближчі точки непорожнього рівня; NaN означає порожній рівень."""
        p=self.local(points);out=np.full_like(p,np.nan)
        if self.shape in ('circle','sphere'):
            radius=.55+level
            if radius>=-1e-12:out=max(0,radius)*unit(p)
        elif self.shape=='square':
            # Окремий аналітичний шлях для внутрішніх квадратів та зовнішніх дуг.
            a=self.square_half
            if level<=0:
                half=a+level
                if half>=-1e-12:
                    half=max(half,0);out=np.clip(p,-half,half)
                    inside=np.max(np.abs(p),axis=1)<half
                    rows=np.where(inside)[0];axis=np.argmax(np.abs(p[inside]),axis=1)
                    out[rows,axis]=np.where(p[rows,axis]>=0,half,-half)
            else:
                closest=np.clip(p,-a,a);delta=p-closest
                inside=np.linalg.norm(delta,axis=1)<1e-14
                rows=np.where(inside)[0];axis=np.argmax(np.abs(p[inside]),axis=1)
                closest[rows,axis]=np.where(p[rows,axis]>=0,a,-a)
                delta=p-closest;delta[inside]=closest[inside]-p[inside]
                out=closest+level*unit(delta)
        elif self.shape=='two_circles':
            radius=.32+level
            if radius>=-1e-12:
                radius=max(radius,0);candidates=[]
                for c in [np.array([-.4,0]),np.array([.4,0])]:
                    candidates.append(c+radius*unit(p-c))
                if radius>=.4:
                    z=np.sqrt(max(0,radius*radius-.16))
                    candidates.extend([np.broadcast_to([0,z],p.shape),np.broadcast_to([0,-z],p.shape)])
                best=np.full(len(p),np.inf)
                for candidate in candidates:
                    dfield=np.minimum(np.linalg.norm(candidate-[-.4,0],axis=1),np.linalg.norm(candidate-[.4,0],axis=1))-.32
                    d=np.linalg.norm(candidate-p,axis=1)
                    take=(np.abs(dfield-level)<1e-8)&(d<best)
                    out[take]=candidate[take];best[take]=d[take]
        elif self.shape=='neck':out=polygon_project(p,POLYGON,level)
        elif self.shape=='torus':
            radius=.20+level
            if radius>=-1e-12:
                radius=max(radius,0);u=np.linalg.norm(p[:,:2],axis=1)
                section=np.column_stack([u-.52,p[:,2]])
                v=np.array([.52,0])+radius*unit(section)
                # При закритті отвору відкидаємо частину перерізу u<0.
                invalid=v[:,0]<0
                if np.any(invalid):
                    z=np.sqrt(max(0,radius*radius-.52**2))
                    v[invalid,0]=0;v[invalid,1]=np.where(p[invalid,2]>=0,z,-z)
                out=np.column_stack([v[:,0,None]*unit(p[:,:2]),v[:,1]])
        else:raise ValueError(self.shape)
        return self.world(out)


def sdf(points,shape='circle',angle=0.,shift=0.):
    """Сумісність із початковими геометричними тестами."""
    return Geometry(shape,angle,shift)(points)
