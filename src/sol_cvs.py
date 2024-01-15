"""
Utility functions for reading cvs files into dataframes and writing dataframes to cvs files
"""

import calendar
import datetime as dt
import os.path

import numpy as np
import pandas as pd
import pvlib as pv

Yr = dt.datetime.now().year
if calendar.isleap(Yr): Yr += 1

def convert_pvgis_hourly_to_sol_avg(inCsv, outCsv ="", TZone = 0):

    if TZone < 0: TZstr = f'Etc/GMT+{-TZone}'
    elif TZone > 0: TZstr = f'Etc/GMT-{TZone}'
    else: TZstr = 'Etc/GMT'

    # put file in dataframe
    f, finp, fmeta = pv.iotools.read_pvgis_hourly(inCsv)

    # copy month, day, hour, and minute out of datetime index
    f['month'] = f.index.month
    f['day'] = f.index.day
    f['hour'] = f.index.hour
    f['minute'] = f.index.minute

    # average out the years, grouped by month day and hour, month/day/hour is a new multiindex.
    f = f.groupby(['month', 'day', 'hour']).mean()

    # drop all leap day rows
    f = f.drop(index = (2, 29))

    # Create an Epoch index  - coerce this year if not leap, else next.
    f = f.reset_index(drop = True)  # start with a simple consecutive index.
    Epoch0 = pd.Timestamp(year = Yr, month = 1, day = 1).timestamp()
    f['Epoch'] = ((f.index * 60 + f['minute']) * 60) + Epoch0
    f = f.set_index('Epoch')


    # Upsample and/or shift to only have 1/2 hourly rows on 0 and 30mins.
    if f.iloc[0]['minute'] != 0:
        X = np.linspace(start = Epoch0, stop = Epoch0 + 31534200, num = 17520)
        f = f.reindex(f.index.union(X))
        f = f.interpolate(method = 'linear', limit_direction = 'both')
        f = f[f.index % 1800 == 0]  # only keep indexes on 0mins and 30mins
    else:
        X = np.linspace(start=Epoch0 + 1800, stop=Epoch0 + 31534200, num=8760)
        f = f.reindex(f.index.union(X))
        f = f.interpolate(method = 'linear', limit_direction = 'both')

    # Reorder the dataframe so that first row is midnight on 1 Jan local time.  Simple shift (using concat)
    # is far more efficient than sorting.
    if TZone < 0:
        f_tzs = f.head(-TZone * 2)
        f = pd.concat([f.tail(len(f) + TZone * 2), f_tzs])
    elif TZone > 0:
        f_tzs = f.tail(TZone * 2)
        f = pd.concat([f_tzs, f.head(len(f) - TZone * 2)])

    # Create the new datetime index
    times = pd.date_range(start = f'{Yr}-01-01 00:00', end = f'{Yr}-12-31 23:30', freq='30T', tz=TZstr)
    f  = f.set_index(times, drop = True)

    # final touch up and clean up
    f['ghi'] = f['poa_direct'] + f['poa_sky_diffuse']
    f['dni'] = f['poa_direct'] / np.sin(f['solar_elevation'] * np.pi / 180)
    f['dni'] = f['dni'].fillna(0)
    f = f.rename(columns = {'poa_sky_diffuse': 'dhi'})

    loc = pv.location.Location(latitude = finp['latitude'], longitude = finp['longitude'], altitude = finp['elevation'], tz=TZstr)
    f = pd.concat([f, loc.get_solarposition(times = times, temperature = f['temp_air'])], axis = 'columns')

    f = f[['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed', 'apparent_elevation', 'azimuth']].round(5)

    if outCsv == "": outCsv = os.path.join(os.path.dirname(inCsv), f'sol_avg_{finp['latitude']}_{finp['longitude']}_{finp['elevation']}.cvs')
    f.to_csv(outCsv)


def convert_pvgis_tmy_to_sol_tmy(inCsv, outCsv = "", TZone = 0):

    if TZone < 0: TZstr = f'Etc/GMT+{-TZone}'
    elif TZone > 0: TZstr = f'Etc/GMT-{TZone}'
    else: TZstr = 'Etc/GMT'

    # put file in dataframe
    f, m, finp, fmeta = pv.iotools.read_pvgis_tmy(inCsv)

    # Create an Epoch index  - coerce this year if not leap, else next.
    f = f.reset_index(drop = True)  # start with a simple consecutive index.
    Epoch0 = pd.Timestamp(year = Yr, month = 1, day = 1).timestamp()
    f['Epoch'] = f.index * 3600 + Epoch0
    f = f.set_index('Epoch')


    # Upsample and add 1/2 hourly rows
    X = np.linspace(start=Epoch0 + 1800, stop=Epoch0 + 31534200, num=8760)
    f = f.reindex(f.index.union(X))
    f = f.interpolate(method = 'linear', limit_direction = 'both')

    # Reorder the dataframe so that first row is midnight on 1 Jan local time.  Simple shift (using concat)
    # is far more efficient than sorting.
    if TZone < 0:
        f_tzs = f.head(-TZone * 2)
        f = pd.concat([f.tail(len(f) + TZone * 2), f_tzs])
    elif TZone > 0:
        f_tzs = f.tail(TZone * 2)
        f = pd.concat([f_tzs, f.head(len(f) - TZone * 2)])

    # Create the new datetime index
    times = pd.date_range(start = f'{Yr}-01-01 00:00', end = f'{Yr}-12-31 23:30', freq='30T', tz=TZstr)
    f  = f.set_index(times, drop = True)

    loc = pv.location.Location(latitude = finp['latitude'], longitude = finp['longitude'], altitude = finp['elevation'], tz=TZstr)
    f = pd.concat([f, loc.get_solarposition(times = times, pressure = f['pressure'], temperature = f['temp_air'])], axis = 'columns')

    # final touch up and clean up
    f = f[['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed', 'apparent_elevation', 'azimuth']].round(5)

    if outCsv == "": outCsv = os.path.join(os.path.dirname(inCsv), f'sol_tmy_{finp['latitude']}_{finp['longitude']}_{finp['elevation']}.cvs')
    f.to_csv(outCsv)

def create_sol_clearsky(lat, long, alt, outCsv, TZone):

    if TZone < 0: TZstr = f'Etc/GMT+{-TZone}'
    elif TZone > 0: TZstr = f'Etc/GMT-{TZone}'
    else: TZstr = 'Etc/GMT'

    times = pd.date_range(start = f'{Yr}-01-01 00:00', end = f'{Yr}-12-31 23:30', freq='30T', tz=TZstr)
    loc = pv.location.Location(latitude=lat, longitude=long, altitude=alt, tz=times.tz)
    f = pd.concat([loc.get_clearsky(times), loc.get_solarposition(times)], axis = 'columns')

    f = f[['ghi', 'dni', 'dhi', 'apparent_elevation', 'azimuth']].round(5)

    f.to_csv(outCsv)
