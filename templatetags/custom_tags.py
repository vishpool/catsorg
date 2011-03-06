from google.appengine.ext.webapp import template
import logging

register = template.create_template_register()

def cropimg(width, height, maxwidth, maxheight):
    logging.getLogger().setLevel(logging.DEBUG)   
    ratio = width / height
    maxratio = maxwidth / maxheight
    
    if ((maxheight * width) / height) > maxwidth:
        cropwidth = (maxheight * width) / height
        cropheight = maxheight
        trimx = ((cropwidth - maxwidth) / 2)
        trimy = 0
        croptop = 0
        cropright = maxwidth + trimx
        cropbottom = maxheight
        cropleft = trimx
        left = 0 - trimx
        top = 0
        logging.debug('cropimg (%dx%d => %dx%d): trimx=%d, trimy=%d', int(cropwidth), int(cropheight), int(maxwidth), int(maxheight), int(trimx), int(trimy))
    else:
        cropwidth = maxwidth
        cropheight = (maxwidth * height) / width
        trimx = 0
        trimy = ((cropheight - maxheight) / 2)
        croptop = trimy
        cropright = maxwidth
        cropbottom = maxheight + trimy
        cropleft = 0
        left = 0
        top = 0 - trimy
        logging.debug('cropimg (%dx%d => %dx%d): trimx=%d, trimy=%d', int(cropwidth), int(cropheight), int(maxwidth), int(maxheight), int(trimx), int(trimy))
    return 'style="width: %dpx; height: %dpx; clip: rect(%dpx %dpx %dpx %dpx); left: %dpx; top: %dpx"' % (int(cropwidth), int(cropheight), int(croptop), int(cropright), int(cropbottom), int(cropleft), int(left), int(top))

def boximg(width, height, maxwidth, maxheight):
    logging.getLogger().setLevel(logging.DEBUG)   
    ratio = width / height
    maxratio = maxwidth / maxheight
    
    if height > maxheight:
        logging.debug('boximg (%dx%d => %dx%d): max-height=%d', int(width), int(height), int(maxwidth), int(maxheight), int(maxheight))
        return 'style="max-height: %dpx;"' % (int(maxheight))
    else:
        logging.debug('boximg (%dx%d => %dx%d): max-width=%d', int(width), int(height), int(maxwidth), int(maxheight), int(maxwidth))
        return 'style="max-width: %dpx;"' % (int(maxwidth))

register.simple_tag(cropimg)
register.simple_tag(boximg)
