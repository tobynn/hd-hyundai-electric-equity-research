# [HD현대일렉트릭 | 기업분석]

> **모델 수정 안내:** 엑셀과 Python DCF에 성숙기 ROIC를 반영해 DCF 가정상 주당가치는 353,731원으로 재계산했습니다. 아래 기존 354,849원/355,000원과 SELL은 과거 버전이며 목표주가와 의견은 검토 중입니다. PER과 RIM도 근거 검증이 남아 있습니다.


> **2026.11.26 검토 알림:** 기존 목표주가와 투자의견은 밸류에이션 입력값 및 모델 일치 여부를 재검증 중입니다. 확정 투자판단으로 사용하지 마세요. [사업·밸류에이션 재검토](research/DEEP_DIVE_REVIEW.md) 및 [재계산과 민감도](research/VALUATION_RECALCULATION_20261126.md)에서 확인된 문제와 후속 검증 항목을 확인할 수 있습니다.

> 267260 · 발간일 2026.11.25 · 실적 기준일 2026년 3분기 · 금액 KRW 십억원, 주가 원/주

## [한눈에 보기]

| 항목 | 내용 |
| --- | --- |
| 투자의견 | **SELL** |
| 기준주가 | 400,000원 (2026.11.24 종가) |
| 목표주가 | **355,000원** |
| 하락여력 | 11.3% |
| 목표주가 기준 | 수주잔고의 매출 전환과 CAPEX를 반영한 FCFF DCF |

3분기 말 수주잔고는 88.43억달러다. 이 수주가 같은 이익률로 매출화된다고 가정하지 않았다. 수주 시점, 지역, 제품, 납기가 다르면 원가와 판가도 달라진다. 이 저장소는 전력변압기·GIS 중심의 전력기기와 배전기기·신사업을 분리해 수주잔고, 마진, CAPEX, 운전자본을 연결한다.

회사 발표 기준 2026년 3분기 매출은 1조1,799억원, 영업이익은 2,845억원이며 영업이익률은 24.1%다. 배전기기·신사업 매출은 전년 동기 대비 85.8% 늘었다. 3분기 말 수주잔고는 88.43억달러다. [회사 3분기 실적 보도자료](https://www.hd-hyundaielectric.com/elect/ko/PR/newsView.jsp?commBoardSeq=6206)

## [모델 읽는 순서]

1. `data/actuals_and_sources.json` — 분기 실적, 수주잔고, 재무상태표 실제치와 출처
2. `research/forecast_driver_notes.md` — 북미·중동·국내 수요, 증설, 가격, 운전자본 입력값
3. `research/peer_selection.md` — 비교기업을 고른 기준과 관측 PER 평균을 배제한 이유
4. `research/valuation_method.md` — DCF·정상화 PER·RIM의 목적과 한계
5. `research/capital_structure_and_sotp_bridge.md` — 순현금, 리스, 비지배지분, 주식 수의 처리
6. `data/valuation_assumptions.json` — 실제치와 분석 입력값의 분리
7. `model/HD_Hyundai_Electric_Equity_Research_Model.xlsx` — 연결된 계산 모델
8. `model/forecast.csv`, `model/rim_schedule.csv`, `model/valuation_results.json` — 재현 가능한 출력값
9. `report/FINAL_REPORT.md` — 산업, 기업, 실적, 전망, 밸류에이션 전문

## [평가 결과]

| 방법 | 주당가치 | 사용 목적 |
| --- | ---: | --- |
| DCF | 354,800원 | 목표주가의 기준 |
| 정상화 PER | 355,000원 | 정상화 EPS와 내재 배수 점검 |
| RIM | 176,600원 | 지배주주 자본과 장기 ROE 점검 |

RIM은 현재의 높은 ROE가 성숙기까지 유지되는지에 민감하다. 세 결과를 평균 내지 않았다. 목표주가는 DCF와 정상화 PER의 교차점에서 정했고, RIM은 현재 주가가 요구하는 장기 자본수익률을 점검하는 도구로 뒀다.

## [공시 자동 갱신]

GitHub Actions는 평일 한국시간 오전 8시 20분에 DART를 조회한다. 사업보고서, 반기보고서, 분기보고서, 영업잠정실적에서 새 공시를 찾으면 접수번호와 원문 링크를 기록한다.

실제치, 전망, DCF·RIM·PER, 목표주가는 자동으로 고치지 않는다. 공시 원문과 회사 IR 자료를 확인한 뒤 입력값을 바꾼다. 설정은 [AUTOMATION.md](research/AUTOMATION.md)에 정리했다.

## [면책]

이 저장소는 학습과 분석 기록을 위한 자료다. 투자 판단과 거래 책임은 이용자에게 있다.
