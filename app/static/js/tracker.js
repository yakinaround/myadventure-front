(function () {
	'use strict';

	/**
	* Implementing String.format
	*/
	if (!String.prototype.format) {
		String.prototype.format = function() {
			var args = arguments;
			return this.replace(/{(\d+)}/g, function(match, number) {
				return typeof args[number] != 'undefined'
					? args[number]
					: match
				;
			});
		};
	}

	var defaultIcon = new L.Icon.Default(),
        photoLayer = new L.layerGroup([]),
        videoLayer = new L.layerGroup([]),
        blogLayer = new L.layerGroup([]),
        routeLayer = new L.layerGroup([]),
        androidTrackerLayer = new L.layerGroup([]),
				arduinoTrackerLayer = new L.layerGroup([]),
				delormeTrackerLayer = new L.layerGroup([]),
				unknownTrackerLayer = new L.layerGroup([]),
        charityLayer = new L.layerGroup([]),
        messageLayer = new L.layerGroup([]),
        pointUrl = apiUrl + '/adventure/' + slug + '/point';

	var photoIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'camera',
		extraClasses: 'tracker-icon',
    markerColor: 'blue'
  });

	var videoIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'video-camera',
    markerColor: 'blue'
  });

	var carIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'car',
		extraClasses: 'tracker-icon',
    markerColor: 'blue'
  });

	var flagIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'flag-checkered',
		extraClasses: 'tracker-icon',
    markerColor: 'red'
  });

	var blogIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'rss',
		extraClasses: 'tracker-icon',
    markerColor: 'blue'
  });

	var routeIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'road',
		extraClasses: 'tracker-icon',
    markerColor: 'red'
  });

	var trackerIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'road',
		extraClasses: 'tracker-icon',
    markerColor: 'blue'
  });

	var charityIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'globe',
		extraClasses: 'tracker-icon',
    markerColor: 'green'
  });

	var messageIcon = L.AwesomeMarkers.icon({
		prefix: 'fa',
    icon: 'comment',
		extraClasses: 'tracker-icon',
    markerColor: 'blue'
  });

	/**
	* The addMarker function adds a marker to a list.
	*/
	function addMarker(lat, lng, timestamp, title, message, elevation, direction, speed, resource, type) {
		var icon = defaultIcon;

		var content = ""

		if (title) {
			content = content.concat("<p><strong>{0}</strong></p>".format(title));
		} else {
			content = content.concat("<p>No Details for Point.<p>");
		}

		if (type === 'car' || type === 'tracker') {
			let d = new Date(Date.parse(timestamp))
			content = content.concat("<p>{0}</p>".format(d.toString()));
			content = content.concat("<p>{0}, {1}</p>".format(str(lat), str(lon)));
		}

		if (message) {
			content = content.concat("<p>{0}</p>".format(message));
		}

		if (elevation || direction || speed) {
			content = content.concat("<p>")
			if (elevation) {
				content = content.concat("Elevation: {0}<br>".format(elevation));
			}

			if (direction) {
				content = content.concat("Direction: {0}<br>".format(direction));
			}

			if (speed) {
				content = content.concat("Speed: {0}<br>".format(speed));
			}
			content = content.concat("</p>")
		}
		

		if (type === 'photo') {
			if (resource) {
				content = content.concat('<a href="{0}" target="_blank"><img src="{0}" class="photo-pin" alt="{1}" width="400px"/></a>'.format(resource, title));
			}
			icon = photoIcon;
		} else if (type === 'video') {
			if (resource) {
				content = content.concat('<iframe class="video-pin" width="560" height="315" src="{0}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'.format(resource));
			}
			icon = videoIcon;
		} else if (type === 'blog') {
			if (resource) {
				content = content.concat('<a href="{0}" class="btn btn-default btn-yakin" target="_blank">View Post</a>'.format(resource));
			}
			icon = blogIcon;
		} else if (type === 'route') {
			icon = routeIcon;
		} else if (type === 'tracker') {
			icon = trackerIcon;
		} else if (type === 'flag') {
			icon = flagIcon;
		} else if (type === 'car') {
			icon = carIcon;
		} else if (type === 'charity') {
			if (resource) {
				content = content.concat('<a href="{0}" class="btn btn-default btn-yakin" target="_blank">See More</a>'.format(resource));
			}
			icon = charityIcon;
		} else if (type === 'message') {
			icon = messageIcon;
		}

		var popup = new L.popup({ maxWidth: 600, maxHeight: 420 })
				.setContent(content);

		var marker = new L.Marker(new L.LatLng(lat, lng), { icon: icon, title: title });

		marker.bindPopup(popup);

		return marker;
	}

	/**
	* The loadPoints function loads all points from the API and adds them to the map.
	*/
	function loadPoints(map) {

		$.getJSON(pointUrl + '/video/', function(points) {
			if(points.length > 0) {
				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						videoLayer.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'video'));
					}
				});
			}
		});

		$.getJSON(pointUrl + '/photo/', function(json) {
			let points = json.points;

			if(points.length > 0) {

				var photoCluster = L.photo.cluster().on('click', function (event) {
					var photo = event.layer.photo,
							template = '<a href="{link}" target="_blank"><img src="{photo}"/></a><p>{caption}</p>';
					if (photo.video && (!!document.createElement('video').canPlayType('video/mp4; codecs=avc1.42E01E,mp4a.40.2'))) {
						template = '<video autoplay controls poster="{link}" width="400" height="400"><source src="{video}" type="video/mp4"/></video>';
					};
					event.layer.bindPopup(L.Util.template(template, photo), {
						className: 'leaflet-popup-photo',
						minWidth: 400
					}).openPopup();
				});

				var photos = [];

				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						// photoLayer.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'photo'));
						photos.push({
							lat: point['latitude'],
							lng: point['longitude'],
							photo: point['photo'],
							video: point['video'],
							caption: point['title'],
							link: point['resource'],
							thumbnail: point['thumb']
						});
					}
				});

				photoCluster.add(photos);

				photoLayer.addLayer(photoCluster);
			}
		});

		$.getJSON(pointUrl + '/blog/', function(json) {
			let points = json.points;

			if(points.length > 0) {
				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						blogLayer.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'blog'));
					}
				});
			}
		});

		$.getJSON(pointUrl + '/charity/', function(json) {
			let points = json.points;

			if(points.length > 0) {
				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						charityLayer.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'charity'));
					}
				});
			}
		});

		$.getJSON(pointUrl + '/message/', function(json) {
			let points = json.points;

			if(points.length > 0) {
				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						messageLayer.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'message'));
					}
				});
			}
		});

		$.getJSON(pointUrl + '/route/', function(json) {
			let points = json.points;

			if(points.length > 0) {

				var route = new L.MarkerClusterGroup({
    			iconCreateFunction: function(cluster) {
        		return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-red', iconSize: new L.Point(40, 40) });
    			}
				});

				// Create array of lat,lon points.
				var line_points = [],
						route_points = [];

				// Define polyline options
				var polyline_options = {
				    color: '#FF0000'
				};

				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						route_points.push(point);
						line_points.push([point['latitude'], point['longitude']]);
					}
				});

				var start = route_points.shift();
				var finish = route_points.pop();

				$.each(route_points, function(index, point) {
					route.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'route'));
				});

				routeLayer.addLayer(L.polyline(line_points, polyline_options));
				routeLayer.addLayer(route);
				routeLayer.addLayer(addMarker(parseFloat(start['latitude']), parseFloat(start['longitude']), start['timestamp'], start['title'], start['desc'], start['elevation'], start['direction'], start['speed'], start['resource'], 'flag'));
				routeLayer.addLayer(addMarker(parseFloat(finish['latitude']), parseFloat(finish['longitude']), finish['timestamp'], finish['title'], finish['desc'], finish['elevation'], finish['direction'], finish['speed'], finish['resource'], 'flag'));
			}
		});

		$.getJSON(pointUrl + '/tracker/', function(json) {
			let points = json.points;

			if(points.length > 0) {

				var android = new L.MarkerClusterGroup({
					iconCreateFunction: function(cluster) {
						return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-blue', iconSize: new L.Point(40, 40) });
					}
				});

				var arduino = new L.MarkerClusterGroup({
					iconCreateFunction: function(cluster) {
						return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-blue', iconSize: new L.Point(40, 40) });
					}
				});

				var delorme = new L.MarkerClusterGroup({
					iconCreateFunction: function(cluster) {
						return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-blue', iconSize: new L.Point(40, 40) });
					}
				});

				var unknown = new L.MarkerClusterGroup({
					iconCreateFunction: function(cluster) {
						return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'marker-cluster marker-cluster-blue', iconSize: new L.Point(40, 40) });
					}
				});

				// Create array of lat,lon points.
				var androidLinePoints = [],
						arduinoLinePoints = [],
						delormeLinePoints = [],
						unknownLinePoints = [],
						androidTrackerPoints = [],
						arduinoTrackerPoints = [],
						delormeTrackerPoints = [],
						unknownTrackerPoints = [],
						current;

				// Define polyline options
				var polyline_options = {
						color: '#0000FF'
				};

				$.each(points, function (index, point) {
					if(!point['hide'] && point['latitude'] && point['longitude']) {
						const source = point.source;

						switch(source) {
							case 'android':
								androidLinePoints.push([point['latitude'], point['longitude']]);
								androidTrackerPoints.push(point);
								break;
							case 'arduino':
								arduinoLinePoints.push([point['latitude'], point['longitude']]);
								arduinoTrackerPoints.push(point);
								break;
							case 'adafruit':
								arduinoLinePoints.push([point['latitude'], point['longitude']]);
								arduinoTrackerPoints.push(point);
							case 'delorme':
								delormeLinePoints.push([point['latitude'], point['longitude']]);
								delormeTrackerPoints.push(point);
							default:
								unknownLinePoints.push([point['latitude'], point['longitude']]);
								unknownTrackerPoints.push(point);
						}
					}
				});

				if (unknownTrackerPoints.length > 0) {
					var unknownCurrent = unknownTrackerPoints.pop();

					$.each(unknownTrackerPoints, function (index, point) {
						unknown.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'tracker'));
					});

					unknownTrackerLayer.addLayer(L.polyline(unknownLinePoints, polyline_options));
					unknownTrackerLayer.addLayer(unknown);
					unknownTrackerLayer.addLayer(addMarker(parseFloat(unknownCurrent['latitude']), parseFloat(unknownCurrent['longitude']), unknownCurrent['timestamp'], unknownCurrent['title'], unknownCurrent['desc'], unknownCurrent['elevation'], unknownCurrent['direction'], unknownCurrent['speed'], unknownCurrent['resource'], 'car'));

					map.addLayer(unknownTrackerLayer);

					current = unknownCurrent;
				}

				if (arduinoTrackerPoints.length > 0) {
					var arduinoCurrent = arduinoTrackerPoints.pop();

					$.each(arduinoTrackerPoints, function (index, point) {
						arduino.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'tracker'));
					});

					arduinoTrackerLayer.addLayer(L.polyline(arduinoLinePoints, polyline_options));
					arduinoTrackerLayer.addLayer(arduino);
					arduinoTrackerLayer.addLayer(addMarker(parseFloat(arduinoCurrent['latitude']), parseFloat(arduinoCurrent['longitude']), arduinoCurrent['timestamp'], arduinoCurrent['title'], arduinoCurrent['desc'], arduinoCurrent['elevation'], arduinoCurrent['direction'], arduinoCurrent['speed'], arduinoCurrent['resource'], 'car'));

					map.addLayer(arduinoTrackerLayer);

					current = arduinoCurrent;
				}

				if (delormeTrackerPoints.length > 0) {
					var delormeCurrent = delormeTrackerPoints.pop();

					$.each(delormeTrackerPoints, function (index, point) {
						delorme.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'tracker'));
					});

					delormeTrackerLayer.addLayer(L.polyline(delormeLinePoints, polyline_options));
					delormeTrackerLayer.addLayer(delorme);
					delormeTrackerLayer.addLayer(addMarker(parseFloat(delormeCurrent['latitude']), parseFloat(delormeCurrent['longitude']), delormeCurrent['timestamp'], delormeCurrent['title'], delormeCurrent['desc'], delormeCurrent['elevation'], delormeCurrent['direction'], delormeCurrent['speed'], delormeCurrent['resource'], 'car'));

					map.addLayer(delormeTrackerLayer);

					current = delormeCurrent;
				}

				if (androidTrackerPoints.length > 0) {
					var androidCurrent = androidTrackerPoints.pop();

					$.each(androidTrackerPoints, function (index, point) {
						android.addLayer(addMarker(parseFloat(point['latitude']), parseFloat(point['longitude']), point['timestamp'], point['title'], point['desc'], point['elevation'], point['direction'], point['speed'], point['resource'], 'tracker'));
					});

					androidTrackerLayer.addLayer(L.polyline(androidLinePoints, polyline_options));
					androidTrackerLayer.addLayer(android);
					androidTrackerLayer.addLayer(addMarker(parseFloat(androidCurrent['latitude']), parseFloat(androidCurrent['longitude']), androidCurrent['timestamp'], androidCurrent['title'], androidCurrent['desc'], androidCurrent['elevation'], androidCurrent['direction'], androidCurrent['speed'], androidCurrent['resource'], 'car'));

					map.addLayer(androidTrackerLayer);

					current = androidCurrent;
				}

				if (current) {
					map.panTo(new L.LatLng(parseFloat(current['latitude']), parseFloat(current['longitude'])));
					map.setZoom(8);
				}
			}
		});
	}

	/**
	* The initialize function initializes the map.
	*/
	function initialize() {
		L.mapbox.accessToken = 'pk.eyJ1IjoibXNwaWVyIiwiYSI6ImUwMmQ4OTBiNWNiMWIyZDE2MTU3MGZlYWI1MjdkMzkxIn0.3eCyZuMzgZfgDy-UznjdFA';

		var streets = new L.mapbox.tileLayer('mapbox.streets');
		var satellite = new L.mapbox.tileLayer('mapbox.satellite', { maxZoom: 14 });

		var base = {
    	"Streets": streets,
			"Satellite": satellite
		};

		var tracker = {
    	"Android": androidTrackerLayer,
			"DeLorme": delormeTrackerLayer,
			"Arduino": arduinoTrackerLayer,
			"Unknown": unknownTrackerLayer,
		};

		var overlays = {
    	"Photos": photoLayer,
    	"Videos": videoLayer,
			"Blogs": blogLayer,
			"Message": messageLayer,
			"Charity": charityLayer,
			"Route": routeLayer
		};

		var map = new L.map('map', {
    	center: [0.0,0.0],
    	zoom: 1,
    	layers: streets,
			minZoom: 3,
			maxZoom: 18,
			zoomControl: false
		});

		map.addLayer(photoLayer);
		map.addLayer(videoLayer);
		// map.addLayer(blogLayer);
		// map.addLayer(charityLayer);
		// map.addLayer(routeLayer);
		map.addLayer(messageLayer);

		L.control.layers(base, overlays, { collapsed: false, position: 'topright' }).addTo(map);
		L.control.layers(null, tracker, { collapsed: false, position: 'topright' }).addTo(map);

		new L.Control.Zoom({ position: 'bottomright' }).addTo(map);

		loadPoints(map);
	}

	/**
	* Initializing when the document is ready.
	*/
	$( document ).ready(function() {
		initialize();
		$(".button-collapse").sideNav();
	});

})();
