"""Одна конфігурація в окремому процесі: нативний peak RSS та час CPU."""
import gc,json,resource,sys,time
import numpy as np
from comparators import CountedGeometry,build
from quality import probes,measure


def run(config):
    dim=config['dim'];geometry=CountedGeometry(shape='capsule' if dim==2 else 'torus',angle=47.,shift=.01)
    baseline=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    builds=[];projection=[];solve=[];counts=[]
    for repeat in range(3):
        model,info=build(config['method'],geometry,h=config['h'],**config['config'])
        builds.append(info['build_seconds']);projection.append(info['projection_seconds']);solve.append(info['solve_seconds'])
        if repeat<2:del model;gc.collect()
    timings={}
    for count in (256,2048,8192):
        points=probes(dim,count,seed=51)
        model.evaluate(points[:32])  # Окремий прогрів; не включений у запит.
        samples=[]
        for repeat in range(3):
            start=time.perf_counter();model.evaluate(points);samples.append(time.perf_counter()-start)
        timings[str(count)]=samples
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    # Похибки вимірюються після обліку RSS запитів, щоб витягування сітки не домішувалося.
    quality=measure(model,geometry,81 if dim==2 else 31)
    errors=[q.get('sampled_offset_hausdorff') for q in quality]
    if any(e is None for e in errors):raise ValueError('unresolved_offset_in_resource_case')
    result=dict(config,status='ok',build_seconds=float(np.median(builds)),build_samples=builds,
                projection_seconds=float(np.median(projection)),solve_seconds=float(np.median(solve)),
                peak_rss_bytes=int(peak),import_peak_rss_bytes=int(baseline),
                incremental_peak_rss_bytes=int(max(0,peak-baseline)),stored_bytes=model.stored_bytes,
                query_samples=timings,query_seconds=float(np.median(timings['8192'])),
                mean_offset_error=float(np.mean(errors)),offset_metrics=quality)
    result['total_seconds']={str(n):result['build_seconds']+n*result['query_seconds'] for n in (1,10,100)}
    from editing import benchmark
    edit=benchmark(config['method'],geometry,config['h'],config['config'],probes(dim,256,seed=77))
    result.update(edit)
    result['editing_peak_rss_bytes']=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    result['total_edit_seconds']={str(n):result['cache_prepare_seconds']+n*(result['cached_update_seconds']+result['query_seconds']) for n in (1,10,100)}
    return result

if __name__=='__main__':
    try:result=run(json.loads(sys.argv[1]))
    except (ValueError,RuntimeError) as error:result=dict(status='failed',error=str(error))
    print(json.dumps(result,allow_nan=False))
