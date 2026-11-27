"""Use the reconciled analyst DCF as a conditional year-end valuation."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'model/coherent_rebuild_20261127.json').read_text())
reference=data['price'];dcf=data['dcf']['price'];target=round(dcf/1000)*1000
change=target/reference-1
rating='BUY' if change>=.15 else 'SELL' if change<=-.15 else 'HOLD'
out={'status':'conditional analyst valuation; earnings, cash flows and comparables are estimates','reference_price':reference,'reference_date':'2026-11-26','valuation_date':'2026-12-31 estimate','horizon':'2026-12-31; approximately one month from 2026-11-26','DCF':{'price':round(dcf),'wacc':data['wacc'],'terminal_growth':data['growth']},'PER':{'price':round(data['per']['price']),'method':'FY2027 70% Hyosung + 30% LS, weights are analyst judgement'},'RIM':{'price':round(data['rim']['price']),'method':'residual income and dividend discount share same earnings and payout path'},'target_price':target,'rating':rating,'upside_price_only':change,'rating_rule':'price-only upside >=15% BUY, <=-15% SELL, otherwise HOLD; horizon 2026-12-31, not 12 months','detail':'model/coherent_rebuild_20261127.json','warnings':['Year-end book and net cash are estimates; Q4 nonoperating and debt movements set to zero.', 'DCF and RIM imply different steady-state returns and transitions and do not reconcile as identical economics.', 'Peer estimates from different brokers and dates, LS estimate predates Q3 results; 70:30 weight is judgement.', '3Q cash and NCI adjusted on an assumed bridge; actual year-end amounts can differ.']}
(root/'model/valuation_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(root/'model/final_scenario_20261127.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
