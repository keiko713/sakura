# Show or Hide map
viewmap = (id, lat, lng) ->
  mapDiv = document.getElementById(id)
  # hide mapDiv if it's already shown
  if (mapDiv.style.display == "block")
    mapDiv.style.display = "none"
    return false
  # show mapDiv
  mapDiv.style.display = "block"
  latlng = new google.maps.LatLng(lat, lng)
  myOptions = {
    zoom: 12,
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
    }},
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

