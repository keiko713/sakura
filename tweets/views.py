# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from datetime import datetime
from tweets.models import *
import settings
import urllib2
import json
import time


API_JSON_ENCODING = 'utf-8'
parse_json = lambda s: json.loads(s.decode(API_JSON_ENCODING))


def index(request):
    photos = search_photos('1')
    return render_to_response('index.html', {
        'photos': photos,
    }, context_instance=RequestContext(request))


def get_page(request, page_id):
    """
    Get the given page_id's page, and return the fragment of HTML.
    """
    photos = search_photos(str(page_id))
    return render_to_response('photolist.html', {
        'photos': photos,
        'pageid': page_id,
    }, context_instance=RequestContext(request))


def search_photos(page_id):
    """
    Search photos that have hashtag #桜2012
    """
    photos = []
    END_POINT = 'http://search.twitter.com/search.json'
    search_key_uni = u'#桜2012'
    search_key = urllib2.quote(search_key_uni.encode('utf-8'))
    address = '%s?q=%s&include_entities=1&rpp=100&page=%s' % (
        END_POINT, search_key, page_id)
    results = httpget(address)['results']
    url_histories = {}

    for result in results:
        entities = result['entities']
        text = get_urlize_text(result)
        entities_urls = entities['urls']
        media = entities.get('media', '')
        date_epoch = result['created_at']

        from_user = result['from_user']
        if is_blacklist_name(from_user):
            continue
        username = '@%s' % (from_user)

        geo = result['geo']
        if geo:
            addr = get_location(geo['coordinates'])
            geo['addr'] = addr

        if media:
            for med in media:
                url = med['media_url']
                tco_url = med['url']
                if is_blacklist_url(tco_url):
                    continue
                if url and not url_histories.get(url, False):
                    imgsrc = get_or_save_imgsrc(url, date_epoch)
                    photos.append({
                        'text': text,
                        'url': med['expanded_url'],
                        'imgsrc': imgsrc,
                        'date': date_epoch,
                        'geo': geo,
                        'username': username,
                    })
                    url_histories[url] = 'true'
        elif entities_urls:
            for entities_url in entities_urls:
                url = entities_url['expanded_url']
                tco_url = entities_url['url']
                if is_blacklist_url(tco_url):
                    continue
                if url and not url_histories.get(url, False):
                    imgsrc = get_or_save_imgsrc(get_imgsrc(url), date_epoch)
                    if imgsrc is not None:
                        photos.append({
                            'text': text,
                            'url': url,
                            'imgsrc': imgsrc,
                            'date': date_epoch,
                            'geo': geo,
                            'username': username,
                        })
                        url_histories[url] = 'true'
    return photos


def get_or_save_imgsrc(imgsrc, date_e):
    """
    Get image src from Photo model,
    if there is no imgsrc, then create Photo model.
    """
    ps = Photo.objects.filter(origin_path=imgsrc)
    if ps:
        p = ps[0]
        if p.converted:
            imgsrc = p.converted_path
    elif imgsrc is not None:
        time_struct = time.strptime(date_e, "%a, %d %b %Y %H:%M:%S +0000")
        tweeted_at = datetime.fromtimestamp(time.mktime(time_struct))
        p = Photo(origin_path=imgsrc,
            converted_path=None, converted=False, tweeted_at=tweeted_at)
        p.save()
    return imgsrc


# Check if the URL is in BlackList
is_blacklist_url = lambda u: BlackList.objects.filter(tco_url=u)
# Check if the screen_name is in BlackList
is_blacklist_name = lambda u: BlackList.objects.filter(screen_name=u)


def json_response(data, code=200, mimetype='application/json'):
    """
    For ajax(json) response, wrapper json data to convert HttpResponse.
    """
    resp = HttpResponse(data, mimetype)
    resp.code = code
    return resp


def httpget(address, user_agent='myagent'):
    """
    Send GET request to the endpoint and get the information in JSON
    TODO need handlings of errors, such as urllib2.HTTPError(404, etc)
    """
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', user_agent)]
    result = opener.open(address).read()
    return parse_json(result)


def add_blacklist(request):
    """
    This method is for API that sets tco_url or screen_name to BlackList.
    Here is usage:
    When you want to report the photo that has url "http://t.co/hogehoge"
    You need to set the URL starts with http://t.co.

      http://sakura.playshiritori.com/api/
        add_blacklist?tco_url=http://t.co/hogehoge

    When you want to report the user that has name keiko713
      http://sakura.playshiritori.com/api/
        add_blacklist?screen_name=keiko713

    if you receive following, your report was succeed:
      "[Success] Your request is confirmed. Thank you for your help!"
    """
    message = None
    if request.method == 'GET':
        url = request.GET.get('tco_url', '')
        name = request.GET.get('screen_name', '')
        if not url and not name:
            message = '[Error: Invalid Request Parameters]' \
              + ' Please put the param either url or screen_name'
        else:
            if url and not url.startswith('http://t.co/'):
                message = '[Error: Invalid Request Parameters]' \
                  + ' Please put http://t.co/ URL for the url parameter'
            else:
                if not is_blacklist_url(url) or not is_blacklist_name(name):
                    black_list = BlackList(tco_url=url, screen_name=name)
                    black_list.save()
                    message = '[Success] Your request is confirmed.' \
                     + ' Thank you for your help!'
    resp = HttpResponse(message, 'text/plain')
    resp.code = 200
    return resp


def get_location(coordinates):
    """
    Get the location info (City, Prefecture) from lat and lng.
    TODO: supports only in Japan, need to support more!
    """
    END_POINT = 'http://geoapi.heartrails.com/api/' \
                + 'json?method=searchByGeoLocation'
    lat = coordinates[0]
    lng = coordinates[1]
    address = END_POINT + '&y=' + str(lat) + '&x=' + str(lng)
    results = httpget(address)['response']
    locations = results.get('location', None)
    if not locations:
        return 'Unknown place'
    # pick 1st location
    loc = locations[0]
    return loc['city'] + ', ' + loc['prefecture']


def get_urlize_text(result):
    """
    Converts URLs, hashtags in text into clickable links.
    """
    text = result['text']
    entities = result['entities']
    urls = result.get('urls', '')
    entities_urls = entities.get('urls', '')
    if urls:
        for url in urls:
            urlize = '<a href="%s">%s</a>' % (
                    url['url'], url['display_url'])
            text = text.replace(url['url'], urlize)
    if entities_urls:
        for e_url in entities_urls:
            urlize = '<a href="%s">%s</a>' % (
                    e_url['url'], e_url['display_url'])
            text = text.replace(e_url['url'], urlize)

    hash_tags = entities.get('hashtags', '')
    if hash_tags:
        for h_tag in hash_tags:
            href = 'https://twitter.com/#!/search/%23' + h_tag['text']
            tag = '#' + h_tag['text']
            urlize = u'<a href="%s">%s</a>' % (href, tag)
            text = text.replace(tag, urlize)
            # for zenkaku hash tag
            tag = u'＃' + h_tag['text']
            urlize = u'<a href="%s">%s</a>' % (href, tag)
            text = text.replace(tag, urlize)

    media = entities.get('media', '')
    if media:
        for med in media:
            urlize = '<a href="%s">%s</a>' % (
                    med['url'], med['display_url'])
            text = text.replace(med['url'], urlize)

    return text


#
def get_imgsrc(url):
    """
    Get image src from url.
    This app supports following third party photo upload:
      - yfrog
      - twipple
      - instagram
      - photozou
      - twitpic
      - flickr
      - movapic
      - f.hatena
      - lockerz
      - ow.ly
    """
    if url.startswith('http://yfrog.com/'):
        return url + ':iphone'
    if url.startswith('http://p.twipple.jp/'):
        tmp = url.split('/')
        return 'http://p.twipple.jp/show/large/' + tmp[-1]
    if url.startswith('http://instagr.am/p/'):
        return url + 'media/?size=m'
    if url.startswith('http://photozou.jp/'):
        tmp = url.split('/')
        return 'http://photozou.jp/p/img/' + tmp[-1]
    if url.startswith('http://twitpic.com/'):
        tmp = url.split('/')
        return 'http://twitpic.com/show/full/' + tmp[-1]
    if url.startswith('http://flic.kr/') \
        or url.startswith('http://www.flickr.com/'):
        return get_flickr_src(url)
    if url.startswith('http://movapic.com/'):
        tmp = url.split('/')
        return 'http://image.movapic.com/pic/s_%s.jpeg' % (tmp[-1])
    if url.startswith('http://f.hatena.ne.jp/'):
        tmp = url.split('/')
        u_id = tmp[3]
        ymd = tmp[4][:8]
        p_id = tmp[4][8:]
        return 'http://img.f.hatena.ne.jp/images/fotolife' \
                + '/%s/%s/%s/%s%s.jpg' % (u_id[0], u_id, ymd, ymd, p_id)
    if url.startswith('http://lockerz.com/'):
        return 'http://api.plixi.com/api/tpapi.svc/' \
                + 'imagefromurl?url=%s&size=mobile' % (url)
    if url.startswith('http://ow.ly/i/'):
        tmp = url.split('/')
        return 'http://static.ow.ly/photos/normal/%s.jpg' % (tmp[-1])
    return None


def get_flickr_src(url):
    """
    Get image src from flickr API.
    """
    API_KEY = settings.FLICKR_API_KEY
    END_POINT = 'http://api.flickr.com/services/rest/'
    if url.startswith('http://flic.kr/'):
        tmp = url.split('/')
        id = decode(tmp[-1])
    else:
        tmp = url.split('/')
        id = tmp[-2]

    address = '%s?method=flickr.photos.getSizes&api_key=%s&' \
            + 'photo_id=%s&format=json&nojsoncallback=1' % (
        END_POINT, API_KEY, str(id))
    results = httpget(address)
    sizes = results['sizes']
    size = sizes['size']
    for s in size:
        if s['label'] == 'Medium':
            return s['source']
    return url


def decode(s):
    """
    Decode base 58 encoded string into an integer.
    From https://gist.github.com/865912
    """
    alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    base_count = len(alphabet)

    """ Decodes the base58-encoded string s into an integer """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base_count

    return decoded
