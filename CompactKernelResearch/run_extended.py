"""Відтворюваний запуск пунктів 4–6. Публікує CSV/JSON, PNG/PDF та TeX."""
import argparse,csv,json,hashlib,platform,sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import importlib.metadata as metadata
import matplotlib
matplotlib.use('Agg')
import experiment4 as e4
import experiment5 as e5
import experiment6 as e6
from comparators import METHODS,candidates

ROOT=Path(__file__).parent;OUT=ROOT/'results'/'extended'


def save(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/(name+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    if isinstance(data,list) and data:
        fields=sorted(set().union(*(r.keys() for r in data)))
        with (OUT/(name+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fields,lineterminator='\n');writer.writeheader()
            for row in data:
                writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
    protocol=dict(version='extended-4-6-v1',date=datetime.now(ZoneInfo('Europe/Kyiv')).date().isoformat(),
        train=e4.TRAIN,holdout=e4.HOLDOUT,train_seeds=[0,1,2],holdout_seeds=[10,11,12],
        max_candidates=6,candidates={m:candidates(m) for m in METHODS},
        holdout_offsets=[-.1,0.,.1],failure_threshold_H=.1,
        topology='foreground 4/6 and background 8/26; boundary clipping flagged',
        source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')},
        environment=dict(python=sys.version,platform=platform.platform(),
                         packages={p:metadata.version(p) for p in ['numpy','scipy','matplotlib','scikit-image']}))
    protocol_path=OUT/'protocol.json'
    if args.resume and protocol_path.exists():
        old=json.loads(protocol_path.read_text())
        if old['source_hashes']!=protocol['source_hashes']:
            raise ValueError('Sources changed; rerun without --resume to avoid mixing protocols')
    save('protocol',protocol)
    if args.resume and (OUT/'selection.json').exists():selection=json.loads((OUT/'selection.json').read_text())
    else:
        selection,training=e4.tune();save('training',training);save('selection',selection)
    print('Selection frozen before held-out evaluation',flush=True)
    stages=[('holdout',lambda:e4.evaluate_holdout(selection)),('resolution',lambda:e5.run(selection)),
            ('failure_map',e6.failure_map),('resources',lambda:e6.resources(selection))]
    for name,run in stages:
        if args.resume and (OUT/(name+'.json')).exists():continue
        save(name,run());print(name,'written',flush=True)
    from extended_reports import publish
    publish(OUT)
    print('Extended reports complete',flush=True)

if __name__=='__main__':main()
