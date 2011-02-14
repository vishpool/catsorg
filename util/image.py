import struct
import hashlib
import math
import time
import urllib

from StringIO import StringIO
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from util.cache import *

class ImageUtil:

    # See http://code.google.com/p/pyib/source/browse/trunk/img.py
    @staticmethod
    def getThumbDimensions(width, height, maxsize):
        wratio = (float(maxsize) / float(width))
        hratio = (float(maxsize) / float(height))
        
        if (width <= maxsize) and (height <= maxsize):
            return width, height
        else:
            if (wratio * height) < maxsize:
              thumb_height = math.ceil(wratio * height)
              thumb_width = maxsize
            else:
              thumb_width = math.ceil(hratio * width)
              thumb_height = maxsize
        
        return int(thumb_width), int(thumb_height)
    
    # See http://code.google.com/p/pyib/source/browse/trunk/img.py
    @staticmethod
    def getImageInfo(url):
        cache_ttl = 60*60*24*30

        logging.getLogger().setLevel(logging.DEBUG)   

        key = md5.new(url).hexdigest()
        res = memcache.get(key, namespace='image_info')
        if res is not None:
            logging.debug('Cached response (%s): %s', key, res)

            return res
        else:
            data = urlfetch.fetch(url, deadline=10).content
            #data = CacheUtil.getCachedResponse(url)
            data = str(data)
            size = len(data)
            height = -1
            width = -1
            content_type = ''
        
            # handle GIFs
            if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
                # Check to see if content_type is correct
                content_type = 'image/gif'
                w, h = struct.unpack("<HH", data[6:10])
                width = int(w)
                height = int(h)
        
            # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
            # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
            # and finally the 4-byte width, height
            elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
                  and (data[12:16] == 'IHDR')):
                content_type = 'image/png'
                w, h = struct.unpack(">LL", data[16:24])
                width = int(w)
                height = int(h)
        
            # Maybe this is for an older PNG version.
            elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
                # Check to see if we have the right content type
                content_type = 'image/png'
                w, h = struct.unpack(">LL", data[8:16])
                width = int(w)
                height = int(h)
        
            # handle JPEGs
            elif (size >= 2) and data.startswith('\377\330'):
                content_type = 'image/jpeg'
                jpeg = StringIO(data)
                jpeg.read(2)
                b = jpeg.read(1)
                try:
                    while (b and ord(b) != 0xDA):
                        while (ord(b) != 0xFF): b = jpeg.read
                        while (ord(b) == 0xFF): b = jpeg.read(1)
                        if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                            jpeg.read(3)
                            h, w = struct.unpack(">HH", jpeg.read(4))
                            break
                        else:
                            jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                        b = jpeg.read(1)
                    width = int(w)
                    height = int(h)
                except struct.error:
                    pass
                except ValueError:
                    pass
    
            res = [content_type, width, height]
            logging.debug('Caching response (%s): %s', key, res)
            memcache.add(key, res, time=cache_ttl, namespace='image_info')
            
            return res
