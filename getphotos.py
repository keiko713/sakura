from PIL import Image
import urllib2
import os
import settings
import multiprocessing
from multiprocessing import Process, Lock


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from tweets.models import Photo


def resize_photo(photo, lock):
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
                return
    try:
        tmp_name = 'static/photos/tmp%s.jpg' % (photo.id)
        origin = open(tmp_name, 'wb')
        origin.write(res.read())
        origin.close()
        original = Image.open(tmp_name)
        original.thumbnail((360, original.size[1]), Image.ANTIALIAS)
        saved_name = 'photos/%s.jpg' % (photo.id)
        original.save('static/' + saved_name)
        photo.converted_path = settings.STATIC_URL + saved_name
        photo.converted = True
        lock.acquire()
        photo.save()
        lock.release()
        os.remove(tmp_name)
    except IOError:
        print 'cannot create thumbnail for ', url

if __name__ == '__main__':
    cpu_num = multiprocessing.cpu_count()
    photos = Photo.objects.filter(converted=False)
    process_list = []
    lock = Lock()

    for photo in photos:
        process = Process(target=resize_photo, args=(photo, lock))
        process_list.append(process)
        process.start()
