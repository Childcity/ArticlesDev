"""Публікація виміряних результатів пунктів 4–6 без наперед заданого переможця."""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from reports import write,table,image
from comparators import PG_ORDER


def read(out,name):return json.loads((out/(name+'.json')).read_text())


def validate_pg_order(protocol,selection,tables):
    """Єдина гладкість протоколу в доборі, перевірці та ресурсних задачах."""
    if protocol.get('pg_order')!=PG_ORDER:raise ValueError('Expected PG order 4 protocol')
    for method,chosen in selection.items():
        if method.startswith('pg_') and chosen.get('config',{}).get('order')!=PG_ORDER:
            raise ValueError('PG selection must use order 4')
    for name,rows in tables.items():
        for row in rows:
            if name=='failure_map' or row.get('method','').startswith('pg_'):
                if row.get('config',row).get('order')!=PG_ORDER:
                    raise ValueError(f'PG order must be 4 in {name}')


def aggregate(rows,keys,group='method'):
    result=[]
    for name in sorted({r[group] for r in rows if group in r}):
        selected=[r for r in rows if r.get(group)==name and r.get('status')=='ok']
        row={group:name,'n':len(selected),'failures':sum(r.get('status')!='ok' for r in rows if r.get(group)==name)}
        for key in keys:
            values=[r[key] for r in selected if key in r]
            row[key]=float(np.median(values)) if values else None
            if key=='band_rmse':
                seeds=sorted({r['seed'] for r in selected if 'seed' in r})
                medians=[float(np.median([r[key] for r in selected if r.get('seed')==seed and key in r])) for seed in seeds]
                row[key+'_seed_min']=min(medians) if medians else None
                row[key+'_seed_max']=max(medians) if medians else None
        result.append(row)
    return result


def figures(out,holdout,resolution,failures,resources):
    def save(fig,name):
        for ext in ('png','pdf'):fig.savefig(out/(name+'.'+ext),dpi=160)
        plt.close(fig)
    methods=sorted({r['method'] for r in holdout})
    palette={m:plt.get_cmap('tab10')(i) for i,m in enumerate(methods)}
    fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for ax,dim in zip(axes,(2,3)):
        rows=aggregate([r for r in holdout if r['dim']==dim],['band_rmse'])
        ax.bar(range(len(rows)),[r['band_rmse'] or np.nan for r in rows])
        ax.set_xticks(range(len(rows)),[r['method'] for r in rows],rotation=65,ha='right',fontsize=8)
        ax.set(title=f'{dim}D held-out geometries (PG n=4)',ylabel='Median band RMSE',yscale='log')
    save(fig,'holdout')
    fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
    for ax,shape in zip(axes,('rounded_box','torus')):
        for method in methods:
            data=sorted([r for r in resolution if r.get('status')=='ok' and r['shape']==shape and r['method']==method and r['offset']==0],key=lambda r:r['resolution'])
            if data:ax.plot([r['resolution'] for r in data],[r.get('sampled_offset_hausdorff',np.nan) for r in data],'o-',label=method)
        ax.set(title=shape,xlabel='Extraction resolution per axis',ylabel='Sampled offset distance');ax.legend(fontsize=6)
    save(fig,'resolution')
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
    for method in methods:
        data=[r for r in resolution if r.get('status')=='ok' and r['shape']=='torus' and r['method']==method and r['offset']==-.19]
        if data:ax.plot([r['resolution'] for r in data],[r['model_b1'] for r in data],'o-',label=method)
    data=[r for r in resolution if r.get('status')=='ok' and r['shape']=='torus' and r['offset']==-.19 and r['method']==methods[0]]
    ax.plot([r['resolution'] for r in data],[r['reference_b1'] for r in data],'k--',linewidth=2,label='Reference discretization')
    ax.set(xlabel='Extraction resolution',ylabel='Digital beta1',title='Thin torus: t=-0.19');ax.legend(fontsize=7,ncol=2)
    save(fig,'torus_topology')
    colors={'within_threshold':0,'quality_threshold':1,'uncovered_support':2,'rank_deficient':3,'algebraic_failure':4}
    hs=sorted({r['h'] for r in failures})
    rhos=sorted({r['rho'] for r in failures})
    ratios=sorted({r['delta_ratio'] for r in failures})
    fig,axes=plt.subplots(len(hs),2,figsize=(11,2.8*len(hs)),layout='constrained',squeeze=False)
    for line,h in enumerate(hs):
        for ax,strategy in zip(axes[line],('grid','isolines')):
            data=[r for r in failures if r['h']==h and r['strategy']==strategy]
            values=np.array([[colors[next(r for r in data if r['rho']==rho and r['delta_ratio']==ratio)['flag']]
                              for rho in rhos] for ratio in ratios])
            im=ax.imshow(values,vmin=0,vmax=4,cmap='viridis',aspect='auto')
            ax.set_xticks(range(len(rhos)),[f'{r:g}' for r in rhos])
            ax.set_yticks(range(len(ratios)),[f'{r:g}' for r in ratios])
            ax.set(xlabel='rho',ylabel='Isoline spacing Δ/h',title=f'{strategy}, h={h:g}, n=4')
    fig.colorbar(im,ax=axes.ravel().tolist(),ticks=range(5),label='0 within; 1 quality; 2 coverage; 3 rank; 4 solve')
    save(fig,'failure_map')
    fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    for ax,dim in zip(axes,(2,3)):
        for row in resources:
            if row['status']!='ok' or row['dim']!=dim:continue
            ax.scatter(row['query_seconds'],row['mean_offset_error'],s=30+row['stored_bytes']/2000,
                       marker='*' if row['pareto'] else 'o',color=palette[row['method']],label=row['method'])
            ax.annotate(f"h={row['h']:g}",(row['query_seconds'],row['mean_offset_error']),fontsize=6)
        ax.set(title=f'{dim}D (* = nondominated)',xlabel='Query time, 8192 points (s)',ylabel='Mean sampled offset distance',xscale='log',yscale='log')
    handles,labels=axes[0].get_legend_handles_labels()
    unique=dict(zip(labels,handles))
    fig.legend(unique.values(),unique.keys(),loc='outside lower center',ncol=3,fontsize=8)
    save(fig,'pareto')


def publish(out):
    protocol=read(out,'protocol');selection=read(out,'selection');training=read(out,'training')
    holdout=read(out,'holdout');resolution=read(out,'resolution');failures=read(out,'failure_map');resources=read(out,'resources')
    validate_pg_order(protocol,selection,dict(training=training,holdout=holdout,resolution=resolution,
                                            failure_map=failures,resources=resources))
    date=protocol['date'];figures(out,holdout,resolution,failures,resources)
    chosen=[dict(method=m,**r.get('config',{}),**{k:v for k,v in r.items() if k!='config'}) for m,r in selection.items()]
    for row in chosen:
        if not row['method'].startswith('pg_'):row['order']=None
    dims={d:aggregate([r for r in holdout if r['dim']==d],['band_rmse','gradient_rmse','sampled_offset_hausdorff','sign_error']) for d in (2,3)}
    per_shape=[]
    for shape in sorted({r['shape'] for r in holdout}):
        per_shape.extend(dict(r,shape=shape) for r in aggregate([x for x in holdout if x['shape']==shape],['band_rmse','sampled_offset_hausdorff','gradient_rmse']))
    (out/'by_shape.json').write_text(json.dumps(per_shape,indent=2,allow_nan=False))
    summary=dict(protocol=protocol['version'],pg_order=PG_ORDER,selection=selection,holdout_2d=dims[2],holdout_3d=dims[3],
                 failure_counts={k:sum(r['flag']==k for r in failures) for k in sorted({r['flag'] for r in failures})},
                 resource_failures=[r for r in resources if r['status']!='ok'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False,allow_nan=False))
    write('Experiment4.tex','Експеримент 4: добір і незалежні форми',r'''
\section*{Протокол, зафіксований до оцінювання}
Навчальні форми: коло й квадрат; seeds $0,1,2$, Sobol по 512 точок,
$h=0.25$. Критерій --- RMSE у смузі $|d|<0.25$.
Псевдогаусове ядро має фіксовану гладкість $n=4$:
\[
 \phi_{4,r}(s)=(1-s^2/r^2)_+^5.
\]
Добираються лише радіус підтримки та, для isolines, крок рівнів.
Кожен параметризований метод має не більше шести наперед заданих
кандидатів; linear/cubic/EDT мають один варіант без параметрів.
Грубий набір не гарантує оптимальності жодного методу.
Кандидат із відмовою хоча б на одній навчальній задачі не обирається.
Вибір збережено у \texttt{selection.json} перед фінальною перевіркою.

Незалежні форми: capsule, rounded box, перешийок, два диски,
сфера й тор. Capsule та rounded box додано як нові аналітичні SDF.
Seeds $10,11,12$ задають нові кути й зсуви.
Для 2D $h=0.2,0.3$, для 3D $h=0.4,0.5$; рівні $t=-0.1,0,0.1$.
Параметри з 2D переносяться в 3D без нового добору; це перевірка
перенесення, а не окремо оптимізовані 3D-методи.

\section*{Справедливість і вартість}
Спільні центри, float64, область $[-1,1]^D$, запас $4h$.
Кількість коефіцієнтів/значень однакова для основних методів.
Для $q=\|x-c\|/r$ використано
\[
 \phi_{C^2}(q)=(1-q)_+^4(4q+1),\qquad
 \phi_{C^4}(q)=(1-q)_+^6(35q^2+18q+3)/3.
\]
Це сімейства Вендланда для розмірностей 2/3; параметр $n$
у таблиці добору стосується лише псевдогаусового ядра.
Для grid перебирається $\rho=1.25,1.5,2,2.5,3,4$;
для isolines --- добуток $\rho=1.5,2,3$ та $\Delta/h=0.5,1$.
Для Wendland наводяться окремо grid/isolines: додатна визначеність
при спільних вузлах не переноситься автоматично на зміщені вузли.
Cubic --- SciPy RegularGridInterpolator not-a-knot з прямим
розв'язувачем; linear --- білінійна/трилінійна інтерполяція.
Додатковий EDT-контроль: cubic витягується на сітку з кроком $h/2$,
потім знакова відстань EDT інтерполюється лінійно. Це окрема
дискретна baseline з додатковою пам'яттю та дрейфом поверхні.

Лічильники містять SDF API calls/points і projection calls/points;
аналітичні операції всередині проєктора не маскуються під однакову
вартість black-box запиту. Тому це однаковий максимум кандидатів,
а не гарантовано рівна кількість інформації про геометрію.
Час усіх кандидатів, включно з невдалими, включений у tuning time.
''' +table(chosen,[('method','Метод'),('rho',r'$\rho$'),('order','$n$'),('delta_ratio',r'$\Delta/h$'),('train_score','Train RMSE'),('tuning_seconds','Добір, с'),('tuning_sdf_points','SDF points'),('tuning_projection_points','Projection points')])+r'''
\section*{Результати на нових формах}
Таблиці --- медіани описових вимірювань, не незалежні статистичні
оцінки: кілька офсетів та h належать тій самій формі/seed.
Seed min/max --- діапазон медіан трьох окремих seeds, не довірчий
інтервал. За формами розкладено дані в by\_shape.json.
Відмови збережено, не замінено нульовою похибкою.
''' +table(dims[2],[('method','2D метод'),('band_rmse','RMSE смуги'),('band_rmse_seed_min','Seed min'),('band_rmse_seed_max','Seed max'),('gradient_rmse','RMSE градієнта'),('sampled_offset_hausdorff',r'$H_{sample}$'),('failures','Відмови')])+table(dims[3],[('method','3D метод'),('band_rmse','RMSE смуги'),('band_rmse_seed_min','Seed min'),('band_rmse_seed_max','Seed max'),('gradient_rmse','RMSE градієнта'),('sampled_offset_hausdorff',r'$H_{sample}$'),('failures','Відмови')])+image('extended/holdout'),date)
    write('Experiment5.tex','Експеримент 5: офсети, градієнти й топологія',r'''
\section*{Диференціальні метрики}
Псевдогаусове поле в цій серії використовує $n=4$ та
$\phi(q)=(1-q^2)_+^5$; гладкість не входить до добору.
Для компактної суми похідна обчислюється аналітично:
\[
 \nabla f(x)=\sum_j a_j\phi'(\|x-c_j\|/r)
 \frac{x-c_j}{r\|x-c_j\|}.
\]
У центрах внесок дорівнює нулю за границею.
Еталонні похідні SDF оцінено центральними різницями з кроками
$10^{-5}$ і $2\cdot10^{-5}$. Залишено точки, де різниця градієнтів
менша $10^{-4}$ і норма відрізняється від одиниці менш ніж на $10^{-4}$.
Це чисельна маска локальної регулярності, не аналітичний опис
усієї медіальної осі. Точки --- незалежні Sobol, маска й кількість
виключених записані. Для grid-методів похідні беруться різницями
$10^{-5}h$, тому їхня похибка включає цю апроксимацію.
\[
 E_g=\sqrt{\operatorname{mean}\|\nabla f-\nabla d\|^2},\quad
 E_{eik}=\sqrt{\operatorname{mean}(\|\nabla f\|-1)^2}.
\]
Також виміряно середній косинус напряму нормалі.

\section*{Дискретизація й топологія}
Поля фіксовані після добору; при зміні роздільності не перебудовуються.
Роздільності 2D: $51,101,201$, 3D: $25,41,65$ на вісь.
$H_{sample}$ --- відстань між хмарами вершин дискретних контурів,
а не доведена відстань Гаусдорфа неперервних поверхонь.
Окремо виміряно $|d(x)-t|$ на вершинах модельної поверхні.
Стабілізація трьох чисел є емпіричною перевіркою; збіжність не доведена.

Для foreground обрано 4/6-зв'язність, background 8/26.
З числа компонент $\beta_0$, порожнин $\beta_2$ та характеристики
Ейлера $\chi$ визначається $\beta_1=\beta_0+\beta_2-\chi$ у 3D;
у 2D $\beta_1=\beta_0-\chi$. Перетин межі області позначається
прапорцем; тоді це не топологія необмеженого тіла.
Тонка трубка тора при $t=-0.19$ має радіус лише $0.01$:
навіть 65 точок на вісь можуть не розрізняти її правильно.
''' +image('extended/resolution')+image('extended/torus_topology')+table([r for r in resolution if r.get('status')=='ok' and r['shape']=='torus' and r['offset']==0 and r['resolution']==65],[('method','Метод'),('reference_b1',r'$\beta_{1,d}$'),('model_b1',r'$\beta_{1,f}$'),('sampled_offset_hausdorff',r'$H_{sample}$'),('gradient_rmse',r'$E_g$')]),date)
    resource_rows=[dict(r,peak_MB=r.get('peak_rss_bytes',0)/2**20,payload_KiB=r.get('stored_bytes',0)/1024) for r in resources if r['status']=='ok']
    write('Experiment6.tex','Експеримент 6: відмови, ресурси та Парето',r'''
\section*{Повний добуток параметрів}
Для псевдогаусового методу фіксовано $n=4$.
Для повернутого квадрата перебрано $h=0.2,0.3$,
$\rho=0.5,1,1.5,2,3$, grid/isolines,
$\Delta/h=0.5,1$. Це 40 конфігурацій; повтори grid за
$\Delta$ залишено явно. Геометрична перевірка --- сітка $101^2$.
Ранг і SVD обчислюються до 600 центрів; поза цією межею не вигадуються.
Покриття --- незалежні 1024 Sobol-точки. Наперед заданий прапорець
якості: $H_{sample}>0.1$ або різні цифрові Betti-числа.
Це інженерний поріг, а не теорема придатності. Прапорець
геометрії на одній роздільності --- screening, не доказ самоперетину.
''' +table([dict(flag=k,count=v) for k,v in summary['failure_counts'].items()],[('flag','Прапорець'),('count','Кількість')])+image('extended/failure_map')+r'''
\section*{Час і пам'ять}
Кожен метод/розмір/розмірність запускається в окремому subprocess.
BLAS/OMP --- один потік, три побудови та три повтори кожної серії
256, 2048, 8192 запитів; показано медіани, raw samples збережено.
RSS вимірюється через Linux ru\_maxrss і включає нативні бібліотеки;
окремо записано імпортний baseline та приріст максимуму.
Нульовий приріст може означати, що імпортний максимум був більшим.
Витягування ізоповерхні виконується після обліку RSS запитів.
Число байтів поля --- лише числовий payload, а не вся пам'ять процесу.

\[
 T(B,Q)=T_{build}+B\,T_{query}(Q),\qquad B=1,10,100.
\]
Таблиці містять також projection time, solve time та повні витрати
для B; це вартість готового поля. Добір параметрів із пункту 4
оплачується додатково і не приховується в build time.
Окремо виміряно редагування: зсув SDF на $0.01,-0.01,0.02$.
Режим cached зберігає вузли й факторизацію; для isolines ці вузли
вже не обов'язково є найближчими до нової геометрії. Другий режим
повністю перебудовує поле й перевибирає вузли. Обидві якості та
три часові повтори записані. Для cubic також кешується not-a-knot
матриця, тож повторна факторизація не нав'язується лише конкуренту.
Вартість cached: $T_{prepare}+B(T_{update}+T_{query})$;
час повного rebuild наведено окремо. Записано числовий обсяг
L/U/перестановок, а фактична пам'ять редагування --- окремий peak RSS.
Реалізації Python/SciPy є дослідницькими; ці числа не визначають
граничну швидкодію всього класу алгоритмів.

Парето визначено окремо для 2D/3D за трьома цілями:
середня похибка офсетів, байти payload і час 8192 запитів.
Домінування потребує не гірших усіх цілей та строго кращої однієї.
Час підготовки й абсолютний RSS показано окремо, вони не підміняються
часом запиту й payload. Різні h входять до того самого простору вибору.
''' +table(resource_rows,[('dim','D'),('method','Метод'),('h','$h$'),('mean_offset_error','Похибка'),('build_seconds','Build, с'),('query_seconds','8192, с'),('cached_update_seconds','Update, с'),('full_rebuild_seconds','Rebuild, с'),('payload_KiB','Payload KiB'),('peak_MB','Peak MiB'),('pareto','Парето')])+image('extended/pareto'),date)
    nextstep(out,protocol,summary,resolution,resources)
    markdown(out,protocol,summary,resolution,resources)


def nextstep(out,protocol,summary,resolution,resources):
    best2=min([r for r in summary['holdout_2d'] if r['band_rmse'] is not None],key=lambda r:r['band_rmse'])
    best3=min([r for r in summary['holdout_3d'] if r['band_rmse'] is not None],key=lambda r:r['band_rmse'])
    pg={dim:{r['method']:r for r in summary[f'holdout_{dim}d']} for dim in (2,3)}
    pg_text=('Для псевдогаусового ядра RMSE grid/isolines становить '
             f"{pg[2]['pg_grid']['band_rmse']:.4g}/{pg[2]['pg_isolines']['band_rmse']:.4g} у 2D та "
             f"{pg[3]['pg_grid']['band_rmse']:.4g}/{pg[3]['pg_isolines']['band_rmse']:.4g} у 3D.\n")
    body=r'''Пункти 4--6 виконано як відтворювану скінченну серію.
Псевдогаусове ядро має стандартну гладкість $n=4$;
добираються радіус і крок ізоліній.
Параметри вибрано на колі/квадраті й заморожено перед перевіркою
на шести інших формах і нових seeds. Порівняно дев'ять методів:
псевдогаусова сума та Wendland C²/C⁴ з двома стратегіями вузлів,
linear, cubic і окрема дискретна cubic+EDT baseline.

'''+pg_text+f"Найменшу медіанну RMSE смуги в цій серії дав {best2['method'].replace('_',r'\_')} у 2D " +f"({best2['band_rmse']:.4g}) та {best3['method'].replace('_',r'\_')} у 3D ({best3['band_rmse']:.4g}). "+r'''
Це опис перевірених бюджетів і геометрій, а не універсальний переможець.
Повні відмови й похибки збережено.

Офсети витягнуто на трьох роздільностях. Додано похибки градієнта,
ейконалу, напряму нормалі та цифрові Betti-числа. Отвір тора тепер
відрізняється від зв'язної компоненти. Для тонких критичних офсетів
еталон також може бути недорозділеним; такі числа не є доказом
неправильної топології неперервного поля.

Побудовано карту взаємодій h, радіуса, кроку рівнів і стратегії
вузлів при $n=4$. Виміряно побудову, проєкцію, розв'язання, серії запитів
та нативний peak RSS у незалежних процесах. Окремо виміряно
редагування з кешем і повною перебудовою; фіксовані вузли isolines
при редагуванні не підміняються новим адаптивним вибором. Криві Парето враховують
похибку офсетів, payload і час запитів; вартість добору показана окремо.

Наступне дослідження: більші зовнішні дані, складні 3D-форми,
аналіз невизначеності та доведені умови збіжності/стійкості.
Поточний benchmark не доводить глобальної новизни, статистичної
переваги або граничної продуктивності алгоритму. Метрики відстані
є дискретними; градієнт еталона використовує перевірені різниці.

Деталі та формули --- Experiment4.tex, Experiment5.tex,
Experiment6.tex; raw data, протокол і версії --- results/extended/.
'''
    write('NextStep.tex','Що встановлено після пунктів 4–6',body,protocol['date'])


def markdown(out,protocol,summary,resolution,resources):
    lines=['# Дослідження пунктів 4–6',f"\nДата: {protocol['date']}. Протокол: `{protocol['version']}`.",
           '\nПсевдогаусове ядро має стандартну гладкість **n=4**: `φ(q)=(1−q²)_+⁵`. Добираються радіус підтримки та крок ізоліній; гладкість фіксована.',
           '\n## Незалежна перевірка','\nПараметри заморожено після кола/квадрата, до оцінювання шести інших геометрій. Медіани нижче — описові; офсети та h повторюються для тих самих форм.',
           '\n| Метод | 2D RMSE смуги | 3D RMSE смуги |','|---|---:|---:|']
    a={r['method']:r for r in summary['holdout_2d']};b={r['method']:r for r in summary['holdout_3d']}
    for method in a:lines.append(f"| {method} | {a[method]['band_rmse']:.6g} | {b[method]['band_rmse']:.6g} |")
    lines+=['\n## Карта відмов','\nПорогова перевірка H>0.1 або цифрової топології не є доказом геометричної непридатності у всіх умовах.']
    lines.extend(f"- `{k}`: {v}" for k,v in summary['failure_counts'].items())
    lines+=['\n## Ресурси','\nPeak RSS включає нативні бібліотеки та імпорти. Payload, build time і час запитів подано окремо. Raw timings містять три повтори; вони не є оцінкою промислової реалізації.',
            '\n## Обмеження','\nШість кандидатів — обмежений пошук, не оптимум. Перенесення параметрів 2D→3D явне. SDF/projection API counts не вимірюють усі аналітичні операції проєктора. Три роздільності не доводять збіжності. Тонкий тор залишається складним навіть для еталона. Повна літературна перевірка новизни не виконана.',
            '\n## Відтворення','\n`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../.venv/bin/python run_extended.py` з папки CompactKernelResearch.',
            '\n`protocol.json`, `selection.json`, CSV/JSON у results/extended містять усі конфігурації, відмови, лічильники, хеші коду й версії. `--resume` дозволений лише за незмінних хешів.']
    (out.parent.parent/'ExtendedResearch.md').write_text('\n'.join(lines)+'\n')
