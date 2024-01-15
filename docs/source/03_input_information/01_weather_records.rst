.. title:: PVPlant | Input Information | Weather Records

.. include:: ..\globals.inc

.. _weather_records:

Weather Records
===============

.. TODO:: Fix this.

A project under OSFPGA foundation :cite:`osfpga_web`

See :cite:`1987:nelson` for an introduction to non-standard analysis.
Non-standard analysis is fun :cite:`1987:nelson`.

Weather records typically measure or calculate parameters at that time instant. PVGIS ERA Data
are an exception to this, but the Resolution of ERA data is 27x27Km2 whereas SARAH2 data is ~5x5km2

It is 
Weather records are typically TMY or hourly over multiple years.  It is important to know the
uncertainties of these irradiance values.  Typically, TMY is said to have a 3% uncertainty, and 
the uncertainty of hourly data is calculated using techniques found here: https://solargis.com/docs/accuracy-and-comparisons/combining-model-uncertainty-and-interannual-variability

.. TODO:: Find a ref for 3% uncertainty of of TMS DATA.

Accuracy of Weather records: https://solargis.com/docs/methodology/tmy-generation

Time Series vs. TMY vs. Synthetic Hourly Time Series

Some popular simulation software are able to generate synthetic hourly time series from long-term monthly averages. Mathematical models for generating synthetic time series have been tuned for few specific sites in temperate climate. The performance of these models is not validated in other climatic zones such as rain tropics or arid deserts. This is a widely used approach. However, it generates a distorted representation of actual time series.

Typical Meteorological Year data are closest to real time series as they include 12 fragments of real data that describe a climate more realistically based on the given selection criteria. Energy Yield simulations using TMY data represent better accuracy compared to energy yield simulations done using synthetic time series data.

It is important to note that the data reduction in TMY is not possible without loss of information contained in the original multiyear time series. As a result of generating TMY and mathematical rounding, long-term monthly and annual averages calculated from TMY data files may not fit accurately to the statistical information calculated from the multiyear time series.

Therefore time series data are considered as the most accurate reference suitable for the statistical analysis of solar resource and meteorological parameters of the site. Only time series data can be used for the statistical analysis of solar climate.
