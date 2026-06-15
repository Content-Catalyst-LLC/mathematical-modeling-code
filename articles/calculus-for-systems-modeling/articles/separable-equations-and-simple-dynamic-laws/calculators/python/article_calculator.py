#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'outputs'
@dataclass
class CalculatorResult: calculator:str; inputs:dict; result:dict; interpretation:str; warning:str=''
def exp_sol(t,x0,r): return x0*math.exp(r*t)
def exp_rate(x,r): return r*x
def log_sol(t,x0,r,k): return k/(1+((k-x0)/x0)*math.exp(-r*t))
def log_rate(x,r,k): return r*x*(1-x/k)
def write(name,payload):
    OUT.mkdir(parents=True, exist_ok=True); (OUT/f'{name}.json').write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding='utf-8')
    flat={'calculator':payload.calculator,'interpretation':payload.interpretation,'warning':payload.warning}; flat.update({f'input_{k}':v for k,v in payload.inputs.items() if not isinstance(v,list)}); flat.update({f'result_{k}':v for k,v in payload.result.items() if not isinstance(v,(list,dict))})
    with (OUT/f'{name}.csv').open('w', newline='', encoding='utf-8') as h: w=csv.DictWriter(h, fieldnames=list(flat.keys())); w.writeheader(); w.writerow(flat)
def emit(cmd,args,result,interp,warn=''):
    payload=CalculatorResult(cmd, vars(args), result, interp, warn); write(cmd.replace('-','_'), payload); print(json.dumps(asdict(payload), indent=2, sort_keys=True))
def series(model,x0,r,k,dt,steps):
    x=x0; rows=[]
    for n in range(steps+1):
        t=n*dt; analytical=exp_sol(t,x0,r) if model=='exponential' else log_sol(t,x0,r,k); rate=exp_rate(x,r) if model=='exponential' else log_rate(x,r,k)
        rows.append({'step':n,'time':t,'analytical_state':analytical,'euler_state':x,'absolute_error':abs(analytical-x),'rate':rate}); x += dt*rate
    OUT.mkdir(parents=True, exist_ok=True); (OUT/f'compare_euler_{model}_series.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    with (OUT/f'compare_euler_{model}_series.csv').open('w', newline='', encoding='utf-8') as h: w=csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return rows
p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command', required=True)
a=sub.add_parser('exponential-solution'); a.add_argument('--time',type=float,default=2); a.add_argument('--initial',type=float,default=10); a.add_argument('--growth-rate',type=float,default=0.25)
a=sub.add_parser('exponential-rate'); a.add_argument('--state',type=float,default=10); a.add_argument('--growth-rate',type=float,default=0.25)
a=sub.add_parser('logistic-solution'); a.add_argument('--time',type=float,default=2); a.add_argument('--initial',type=float,default=10); a.add_argument('--growth-rate',type=float,default=0.25); a.add_argument('--capacity',type=float,default=100)
a=sub.add_parser('logistic-rate'); a.add_argument('--state',type=float,default=10); a.add_argument('--growth-rate',type=float,default=0.25); a.add_argument('--capacity',type=float,default=100)
a=sub.add_parser('compare-euler'); a.add_argument('--model',choices=['exponential','logistic'],default='logistic'); a.add_argument('--initial',type=float,default=10); a.add_argument('--growth-rate',type=float,default=0.25); a.add_argument('--capacity',type=float,default=100); a.add_argument('--dt',type=float,default=0.1); a.add_argument('--steps',type=int,default=20)
args=p.parse_args(); cmd=args.command
if cmd=='exponential-solution': emit(cmd,args,{'state':exp_sol(args.time,args.initial,args.growth_rate)},'Computes P(t)=P0 exp(rt).','Exponential growth assumes no capacity constraint.')
elif cmd=='exponential-rate': emit(cmd,args,{'rate':exp_rate(args.state,args.growth_rate)},'Computes dP/dt = rP.','Proportional growth assumes current state drives rate.')
elif cmd=='logistic-solution': emit(cmd,args,{'state':log_sol(args.time,args.initial,args.growth_rate,args.capacity)},'Computes the analytical logistic solution.','Logistic growth assumes fixed carrying capacity.')
elif cmd=='logistic-rate': emit(cmd,args,{'rate':log_rate(args.state,args.growth_rate,args.capacity)},'Computes dP/dt = rP(1-P/K).','Capacity should be justified and sensitivity-tested.')
elif cmd=='compare-euler': rows=series(args.model,args.initial,args.growth_rate,args.capacity,args.dt,args.steps); emit(cmd,args,{'final_analytical_state':rows[-1]['analytical_state'],'final_euler_state':rows[-1]['euler_state'],'final_absolute_error':rows[-1]['absolute_error'],'records':len(rows)},'Compares analytical solution and explicit Euler approximation.','Euler error depends on step size.')
