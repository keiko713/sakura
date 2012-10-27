from PIL import Image
import urllib2
import os
import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from tweets.models import Photo

photos = Photo.objects.filter(converted=False)

for idx, photo in enumerate(photos):
    if idx < 0:
        continue
    url = photo.origin_path
    error = False

    for i in range(3):
        try:
            res = urllib2.urlopen(url)
            break
        except urllib2.URLError:
            if i < 2:
                pass
            else:
                print 'cannot get a picture: ', url
                error = True
    if error:
        continue
    try:
        origin = open('static/photos/tmp.jpg', 'wb')
        origin.write(res.read())
        origin.close()
        original = Image.open('static/photos/tmp.jpg')
        original.thumbnail((360, original.size[1]), Image.ANTIALIAS)
        saved_name = 'photos/%s.jpg' % (photo.id)
        original.save('static/' + saved_name)
        photo.converted_path = settings.STATIC_URL + saved_name
        photo.converted = True
        photo.save()
    except IOError:
        print 'cannot create thumbnail for ', url
