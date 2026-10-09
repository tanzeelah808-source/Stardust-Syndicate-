from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord
import astropy.units as u

# 1. THE TIMEOUT FIX: Force the connection to give up after 15 seconds
# This stops the infinite spinner and allows your error message to actually show up!
SkyView.TIMEOUT = 15  

# 2. THE SIZE FIX: Changed radius from 10 to 5. 
# A 5-arcminute box is 4x smaller in file size than a 10-arcminute box, making it much faster to download.
def fetch_infrared_cutout(ra, dec, survey='2MASS-K', radius=5):
    """Fetches an infrared image array from NASA SkyView."""
    target = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    fits_files = SkyView.get_images(position=target, survey=[survey], radius=radius*u.arcmin)
    return fits_files[0][0].data