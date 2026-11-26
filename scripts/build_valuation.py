from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
MODEL.mkdir(exist_ok=True)

# 금액은 KRW 십억원, 주당가치는 원. 2026년 이후는 분석 입력값이다.
forecast = [
    {"year": 2026, "revenue": 4650.0, "op_margin": 0.246, "ebit": 1143.9, "tax_rate": 0.240, "da": 125.0, "capex": 350.0, "nwc_change": 130.0, "fcff": None},
    {"year": 2027, "revenue": 5185.0, "op_margin": 0.246, "ebit": 1275.5, "tax_rate": 0.240, "da": 155.0, "capex": 400.0, "nwc_change": 150.0, "fcff": 574.38},
    {"year": 2028, "revenue": 5630.0, "op_margin": 0.240, "ebit": 1351.2, "tax_rate": 0.240, "da": 195.0, "capex": 410.0, "nwc_change": 140.0, "fcff": 671.912},
    {"year": 2029, "revenue": 6011.0, "op_margin": 0.234, "ebit": 1406.6, "tax_rate": 0.240, "da": 230.0, "capex": 360.0, "nwc_change": 130.0, "fcff": 809.0},
    {"year": 2030, "revenue": 6342.0, "op_margin": 0.228, "ebit": 1446.0, "tax_rate": 0.240, "da": 250.0, "capex": 330.0, "nwc_change": 120.0, "fcff": 898.9},
    {"year": 2031, "revenue": 6627.0, "op_margin": 0.220, "ebit": 1457.9, "tax_rate": 0.240, "da": 270.0, "capex": 330.0, "nwc_change": 110.0, "fcff": 938.0},
]

for row in forecast:
    row["ebit"] = row["revenue"] * row["op_margin"]
    if row["fcff"] is not None:
        row["fcff"] = row["ebit"] * (1 - row["tax_rate"]) + row["da"] - row["capex"] - row["nwc_change"]

wacc = 0.090
g = 0.022
shares_m = 35.99
net_cash = 648.574
nci = 4.028
fcff = [row["fcff"] for row in forecast[1:]]
pv_fcff = sum(value / (1 + wacc) ** index for index, value in enumerate(fcff, start=1))
# Terminal NOPAT reinvests g/ROIC; ROIC is an analyst assumption, not a company forecast.
terminal_roic = 0.14
terminal_nopat = forecast[-1]["ebit"] * (1 - forecast[-1]["tax_rate"])
terminal_fcff = terminal_nopat * (1 + g) * (1 - g / terminal_roic)
tv = terminal_fcff / (wacc - g)
pv_tv = tv / (1 + wacc) ** len(fcff)
ev = pv_fcff + pv_tv
dcf_equity = ev + net_cash - nci
dcf_price = dcf_equity * 1_000_000_000 / (shares_m * 1_000_000)

normal_eps = 25_000.0
applied_per = 14.2
per_price = normal_eps * applied_per

# RIM은 2026년 말 예상 지배주주자본에서 시작한다. 2027~2031년 순이익은
# 고점 마진이 완만하게 정상화된다는 가정을 반영한 입력값이다.
book_2026 = 2550.0
cost_of_equity = 0.105
payout = 0.50
rim_ni = [900.0, 930.0, 950.0, 965.0, 975.0]
book = book_2026
pv_ri = 0.0
rim_rows = []
for i, ni in enumerate(rim_ni, start=1):
    charge = book * cost_of_equity
    ri = ni - charge
    pv = ri / (1 + cost_of_equity) ** i
    end_book = book + ni * (1 - payout)
    rim_rows.append({
        "year": 2026 + i,
        "begin_book": round(book, 1),
        "net_income": ni,
        "equity_charge": round(charge, 1),
        "residual_income": round(ri, 1),
        "pv_residual_income": round(pv, 1),
        "end_book": round(end_book, 1),
    })
    pv_ri += pv
    book = end_book
terminal_roe = 0.150
terminal_ri = book * (terminal_roe - cost_of_equity)
terminal_value = terminal_ri / (cost_of_equity - g)
pv_terminal_ri = terminal_value / (1 + cost_of_equity) ** len(rim_ni)
rim_equity = book_2026 + pv_ri + pv_terminal_ri
rim_price = rim_equity * 1_000_000_000 / (shares_m * 1_000_000)

values = {
    "unit": "KRW billion except per-share values",
    "reference_price": 400000,
    "reference_date": "2026-11-24",
    "economic_shares_million": shares_m,
    "DCF": {
        "method": "FCFF DCF: power-equipment operating cash flow, separately bridged net cash",
        "wacc": wacc,
        "terminal_growth": g,
        "terminal_reinvestment_roic": terminal_roic,
        "terminal_nopat_2031": round(terminal_nopat, 4),
        "terminal_fcff_2032": round(terminal_fcff, 4),
        "pv_explicit_fcff": round(pv_fcff, 1),
        "pv_terminal_value": round(pv_tv, 1),
        "enterprise_value": round(ev, 1),
        "net_cash": net_cash,
        "non_controlling_interest": nci,
        "equity_value": round(dcf_equity, 1),
        "price": round(dcf_price),
    },
    "PER": {
        "method": "normalized-EPS cross-check; observed peer average not used",
        "normal_eps": normal_eps,
        "applied_per": applied_per,
        "price": round(per_price),
    },
    "RIM": {
        "method": "controlling equity with normalized residual-income path",
        "begin_book_2026": book_2026,
        "cost_of_equity": cost_of_equity,
        "terminal_roe": terminal_roe,
        "pv_explicit_ri": round(pv_ri, 1),
        "pv_terminal_ri": round(pv_terminal_ri, 1),
        "equity_value": round(rim_equity, 1),
        "price": round(rim_price),
    },
    "target_price": None,
    "rating": "under review",
    "downside": None,
}

with (MODEL / "forecast.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=forecast[0].keys())
    writer.writeheader()
    writer.writerows(forecast)
with (MODEL / "rim_schedule.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rim_rows[0].keys())
    writer.writeheader()
    writer.writerows(rim_rows)
with (MODEL / "valuation_results.json").open("w", encoding="utf-8") as f:
    json.dump(values, f, ensure_ascii=False, indent=2)
print(json.dumps(values, ensure_ascii=False, indent=2))
