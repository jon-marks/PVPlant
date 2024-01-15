import sol_cvs as sc

sc.convert_pvgis_hourly_to_sol_avg('../data/Thomas_Tyres_-26.556_28.014_1471.0/Timeseries_-26.566_28.014_SA2_0deg_0deg_2005_2020.csv', "", 2)
sc.convert_pvgis_tmy_to_sol_tmy('../data/Thomas_Tyres_-26.556_28.014_1471.0/tmy_-26.566_28.014_2005_2020.csv', "", 2)
sc.create_sol_clearsky(-26.556, 28.014, 1471.0, "../data/Thomas_Tyres_-26.556_28.014_1471.0/sol_clr_-26.556_28.014_1471.0.csv", 2)
