##
# EPH_  Prefixes to loaded ephemiris tables

from skyfield import api as sf
# from skyfield import almanac
#from datetime import datetime
#from datetime import timedelta
#import dateutil.parser
#from calendar import monthrange

ts = sf.load.timescale()

# loader = api.Loader('./data')
# ds440s = loader('de440s.bsp')
# OR
Ephem = sf.Loader('./data')('de440s.bsp')

ephSunC = Ephem['Sun']      # Ephem for centre of sun.
ephEarthC = Ephem['Earth']  # Ephem for centre of ear
ephObs = ephEarthC + sf.Topos('48.324777 N', '11.405610 E', elevation_m = 519) # Ephem for Observer's position on earth's surface

# Barycentric position vector of Observer at time now (relative to Barycentre of the solar system)
vObs = ephObs.at(ts.now())
# Astrocentric position vector of Target (Sun) relative to the Observer accounting for speed of light
vSun = vObs.observe(ephSunC)
# Apparent position of Target accounts for gravitational deflection and atmosphere
vSunPos = vSun.apparent()
# OR
##vSunPos = ephObs.at(ts.now()).observe(ephSunC).apparent()

# Compute apparent altitude & azimuth for the sun's position

altitude, azimuth, distance = vSunPos.altaz()

# Print results (example)
print(f"Altitude: {altitude.degrees:.4f} °")
print(f"Azimuth: {azimuth.degrees:.4f} °")
print(f"Distance: {distance.au:.5f} au")
