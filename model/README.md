# [모델 파일]

`HD_Hyundai_Electric_Equity_Research_Model.xlsx`에는 Actuals, Forecast, DCF, RIM, PER, Sources 시트가 있다. 금액은 KRW 십억원이며, 주당가치는 원이다.

- 실제치는 `data/actuals_and_sources.json`과 출처를 맞춘다.
- 전망 입력값은 `data/valuation_assumptions.json`에 있다.
- `scripts/build_valuation.py`를 실행하면 CSV와 JSON 결과를 다시 만든다.
- 엑셀 파일은 같은 가정을 사람이 읽기 쉽게 옮긴 파일이다. 목표주가는 자동 공시 감지로 바뀌지 않는다.
