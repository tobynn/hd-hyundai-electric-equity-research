"""Illustrative two-stage justified PER, with all inputs stated; not peer evidence."""
import json
from pathlib import Path

eps0=25000.0
cost=.105
growth=.07
incremental_roe=.18
terminal_growth=.022
terminal_roe=.15
periods=5
retention=growth/incremental_roe
terminal_retention=terminal_growth/terminal_roe
assert 0 <= retention <= 1 and 0 <= terminal_retention <= 1
assert cost > terminal_growth
rows=[]
for year in range(1,periods+1):
    earnings=eps0*(1+growth)**year
    dividend=earnings*(1-retention)
    rows.append({'period':year,'eps':earnings,'dividend':dividend,'pv_dividend':dividend/(1+cost)**year})
terminal_eps=rows[-1]['eps']*(1+terminal_growth)
terminal_dividend=terminal_eps*(1-terminal_retention)
pv_terminal=terminal_dividend/(cost-terminal_growth)/(1+cost)**periods
value=sum(r['pv_dividend'] for r in rows)+pv_terminal
out={'status':'illustrative; EPS is at t0 and first forecast dividend is at t1, not a peer-derived multiple','eps_t0':eps0,'cost_of_equity':cost,'growth_first_five_years':growth,'incremental_roe':incremental_roe,'growth_retention':retention,'terminal_growth':terminal_growth,'terminal_roe':terminal_roe,'terminal_retention':terminal_retention,'forecast':rows,'pv_terminal':pv_terminal,'value_per_share':value,'justified_per':value/eps0,'note':'Growth, return on incremental equity and clean surplus are assumptions; DCF and RIM may use incompatible EPS timing. No fair target implied.'}
path=Path(__file__).resolve().parents[1]/'model/per_rebuild_20261126.json'
path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
