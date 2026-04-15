# Oil Forecast Evaluation Summary

## Main dataset
- EIA Brent vintages: 11 publication years used in realized evaluation
- Forecast observations used in 3y/5y evaluation: 20

## Benchmark results
      model  horizon_years  n_forecasts        ME       MAE      RMSE     MAPE
        EIA              3           11 20.438661 26.006072 34.974008 0.388205
        EIA              5            9 26.641034 28.086861 34.321603 0.380629
Random Walk              3           11 17.250898 31.656702 42.989204 0.438045
Random Walk              5            9 13.794846 38.901808 47.341602 0.512064

## Rolling model results
               model  horizon_years  n_forecasts        ME       MAE      RMSE     MAPE
          Rolling AR              3           26 10.131831 35.328167 48.951906 0.447015
          Rolling AR              5           24 -5.407059 35.948212 51.237855 0.379464
Rolling AR + Futures              3            9 17.960273 40.109557 52.510599 0.549114
Rolling AR + Futures              5            7  7.571707 36.614364 53.230335 0.539137

## Notes
- Main analysis uses EIA Brent Spot forecasts from AEO Table 12, deflated to 2025 dollars with CPI.
- Realized annual Brent prices come from FRED DCOILBRENTEU aggregated to annual averages.
- The market-augmented model uses Brent front-month futures from Yahoo Finance (`BZ=F`) as a market-information proxy.
- World Bank archive data are downloaded as supplementary material because the forecast object is `Crude oil, avg`, not exact Brent.