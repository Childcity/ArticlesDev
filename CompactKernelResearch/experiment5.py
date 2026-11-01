"""Пункт 5: ті самі поля, три роздільності, офсети й Betti-числа."""
from comparators import CountedGeometry,build
from experiment4 import case
from quality import measure,gradient_quality


def run(selection):
    rows=[]
    # Різна гладкість і критичні зміни, включно з отвором тора.
    scenarios=[('rounded_box',(-.1,0.,.1)),('two_circles',(.06,.08,.10)),
               ('neck',(-.12,-.10,-.08)),('sphere',(-.1,0.,.1)),
               ('torus',(-.19,0.,.30,.34))]
    for shape,offsets in scenarios:
        dim=3 if shape in ('sphere','torus') else 2
        h=.4 if dim==3 else .2
        for method,chosen in selection.items():
            if chosen['status']!='ok':continue
            geometry=CountedGeometry(**case(shape,42))
            try:
                model,info=build(method,geometry,h=h,**chosen['config'])
                gradients=gradient_quality(model,geometry,dim,42)
                # Поле не переналаштовується при зміні сітки витягування.
                for resolution in ((25,41,65) if dim==3 else (51,101,201)):
                    for q in measure(model,geometry,resolution,offsets):
                        rows.append(dict(shape=shape,method=method,h=h,seed=42,status='ok',**q,**gradients))
            except (ValueError,RuntimeError) as error:
                rows.append(dict(shape=shape,method=method,h=h,status='failed',error=str(error)))
        print('Resolution study',shape,'complete',flush=True)
    return rows
