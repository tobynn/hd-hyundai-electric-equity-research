"""End-2026 scenarios in KRW bn and KRW/share. Inputs are estimates, not guidance."""
import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shares=35_992_704
price=389_500
tax=.24; ke=.105; wd=.15; kd=.05; wacc=(1-wd)*ke+wd*kd*(1-tax)
g=.022; terminal_roic=.14; terminal_roe=.15
base_book=2305.516; q4_income=302.048; dividend=46.7905152
book2026=base_book+q4_income-dividend
netcash_q3=648.574
q4_ebit=4650*.246-829.797
q4_da=45.; q4_capex=350-(242.045+10.513); q4_nwc=30.
q4_fcff=q4_ebit*(1-tax)+q4_da-q4_capex-q4_nwc
netcash2026=netcash_q3+q4_fcff-dividend
inputs=[(2027,5185,.246,155,400,150),(2028,5630,.24,195,410,140),(2029,6011,.234,230,360,130),(2030,6342,.228,250,330,120),(2031,6627,.22,270,330,110)]
rows=[];book=book2026;pvri=0.;pvdiv=0.;pvfcff=0.
for i,(year,revenue,margin,da,capex,nwc) in enumerate(inputs,1):
    ebit=revenue*margin;nopat=ebit*(1-tax);fcff=nopat+da-capex-nwc
    # Explicit normalised non-operating, minority and finance adjustment; analyst assumption.
    net_income=nopat-69.4508
    dist=.50*net_income;ri=net_income-ke*book
    pvri+=ri/(1+ke)**i;pvdiv+=dist/(1+ke)**i;pvfcff+=fcff/(1+wacc)**i
    closing=book+net_income-dist
    rows.append(dict(year=year,revenue=revenue,margin=margin,ebit=ebit,nopat=nopat,da=da,capex=capex,nwc=nwc,fcff=fcff,opening_equity=book,net_income=net_income,dividend=dist,residual_income=ri,closing_equity=closing))
    book=closing
terminal_fcff=rows[-1]['nopat']*(1+g)*(1-g/terminal_roic)
pv_tv_dcf=terminal_fcff/(wacc-g)/(1+wacc)**5
dcf_equity=pvfcff+pv_tv_dcf+netcash2026-4.028
terminal_ni=book*terminal_roe
terminal_ri=book*(terminal_roe-ke)
pv_terminal_ri=terminal_ri/(ke-g)/(1+ke)**5
rim_equity=book2026+pvri+pv_terminal_ri
terminal_payout=1-g/terminal_roe
pv_terminal_div=terminal_ni*terminal_payout/(ke-g)/(1+ke)**5
ddm_equity=pvdiv+pv_terminal_div
assert abs(rim_equity-ddm_equity)<1e-8
eps27=rows[0]['net_income']*1e9/shares
comps=[{'name':'효성중공업','price_20261126':1613000,'eps_2027_broker':127970,'broker_date':'2026-11-02','source':'https://file.alphasquare.co.kr/media/pdfs/company-report/_%ED%9A%A8%EC%84%B1%EC%A4%91%EA%B3%B5%EC%97%85_3Q26%20Review_261102%E2%98%86_%EC%84%B1%EC%A2%85%ED%99%94_2135_Online%20report%20_%206_10p_%ED%9A%A8%EC%84%B1%EC%A4%91%EA%B3%B5%EC%97%85.pdf'},{'name':'LS ELECTRIC','price_20261126':113400,'eps_2027_broker':5117,'broker_date':'2026-10-19','source':'https://imfnsec.tistory.com/124?category=856551'}]
for c in comps:c['forward_per']=c['price_20261126']/c['eps_2027_broker']
# Emphasise directly comparable power transformers/GIS; this is a judgement, not a regression.
weighted=.7*comps[0]['forward_per']+.3*comps[1]['forward_per']
out={'status':'research scenarios; forecasts and peer weights are judgements; no mechanically confirmed target','date_price':'2026-11-26','valuation_date':'2026-12-31 estimated','units':'KRW bn except per-share figures','price':price,'shares':shares,'cost_of_equity':ke,'debt_weight':wd,'debt_cost_pretax':kd,'wacc':wacc,'tax':tax,'growth':g,'terminal_roic':terminal_roic,'terminal_roe':terminal_roe,'q4_bridge':{'book_q3':base_book,'q4_income_estimate':q4_income,'dividend_declared':dividend,'book_2026e':book2026,'cash_q3':netcash_q3,'q4_ebit':q4_ebit,'q4_da':q4_da,'q4_capex':q4_capex,'q4_nwc':q4_nwc,'q4_fcff':q4_fcff,'cash_2026e':netcash2026,'other_cash_flows_assumed_zero':True},'forecast':rows,'dcf':{'pv_fcff':pvfcff,'pv_terminal':pv_tv_dcf,'nci':4.028,'equity':dcf_equity,'price':dcf_equity*1e9/shares},'rim':{'equity':rim_equity,'price':rim_equity*1e9/shares,'ddm_equity':ddm_equity,'terminal_dividend_payout':terminal_payout,'terminal_ni':terminal_ni},'per':{'own_2027_eps':eps27,'peer_2027':comps,'weight_hyosung':.7,'weight_ls':.3,'forward_per':weighted,'price':eps27*weighted,'warning':'Peer analyst estimates use differing methods, dates and business mixes; weights are judgement, not objectively calibrated. DCF, DDM and RIM share forecast.'}}
outdir=root/'model';outdir.mkdir(exist_ok=True)
(outdir/'coherent_rebuild_20261127.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
summary={'status':'research scenarios, not a final target','reference_price':price,'reference_date':'2026-11-26','valuation_date':'2026-12-31 estimate','DCF':{'price':round(dcf_equity*1e9/shares),'wacc':wacc},'PER':{'price':round(eps27*weighted),'method':'FY2027 peer weighting is analyst judgement'},'RIM':{'price':round(rim_equity*1e9/shares),'method':'earnings and dividend path reconciled to DDM'},'target_price':None,'rating':'under review','detail':'model/coherent_rebuild_20261127.json'}
(outdir/'valuation_results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
with (outdir/'coherent_forecast_20261127.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
print(json.dumps({'wacc':wacc,'q4':out['q4_bridge'],'dcf':out['dcf'],'rim':out['rim'],'per':out['per']},ensure_ascii=False,indent=2))
