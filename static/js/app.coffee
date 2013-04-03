# Show or Hide map
window.viewmap = (id, lat, lng) ->
  mapDiv = document.getElementById(id)
  # hide mapDiv if it's already shown
  if (mapDiv.style.display == "block")
    mapDiv.style.display = "none"
    return false
  # show mapDiv
  mapDiv.style.display = "block"
  latlng = new google.maps.LatLng(lat, lng)
  myOptions = {
    zoom: 14,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(mapDiv, myOptions)
  marker = new google.maps.Marker({
    position: latlng,
    map: map,
  })
  return false

# adjust time based on timezone
adjusttime = () ->
  $('.datetime').each((idx, obj) ->
    mydate = new Date($(obj).attr('alt'))
    $(obj).html(myformat(mydate)) if mydate?
  )

# format time yyyy/MM/dd HH:mm:ss
myformat = (datetime) ->
  y = datetime.getFullYear()
  m = addzero(datetime.getMonth() + 1)
  d = addzero(datetime.getDate())
  time = datetime.toLocaleTimeString()
  return "#{y}/#{m}/#{d} #{time}"

# add zero if the arg is less than 10
addzero = (arg) ->
  arg = '0' + arg if arg < 10
  return arg

# get min value
# (digit length is too long so cannot use Math.min.apply)
getmin = (array) ->
  min = array[0]
  for val in array
    if val < min
      min = val

  return min


# Initialization
$ ->
  adjusttime()

  $thumbnails = $('#id_thumbnails')

  $thumbnails.imagesLoaded(() ->
    $thumbnails.masonry({
      itemSelector: '.box'
    })
  )

  $thumbnails.infinitescroll({
    navSelector: '#page-nav',
    nextSelector: '#page-nav a',
    itemSelector: '.box',
    bufferPx: 1500,
    loading: {
      img: "#{STATIC_URL}img/loading.gif",
      msgText: '読込中... Loading...',
    },
    path: (pageNumber) ->
      maxId = getmin($('.max-id').map(() ->
        $(this).data('maxid')
      ).get())
      return "/page/#{maxId}/"
    }
    (newElements) ->
      $newElems = $(newElements).css({ opacity: 0 })
      $newElems.imagesLoaded(() ->
        $newElems.css({ opacity: 1 })
        $thumbnails.masonry('appended', $newElems, false, () ->
          $('infscr-loading').hide()
          adjusttime()
        )
      )
  )

