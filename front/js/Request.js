/**
* Init Dashboard Component
* Component Event Handler
*/
class Request {
  constructor () {
  }

  get(url) { //load data via ajax
    $.ajax({
      method: 'GET',
      url: url,
      dataType: 'json',
      success: function(get) {
        console.log(get);
      }
    });
  }

  post(toPOST, url) { //load data via ajax
    $.ajax({
      method: 'POST',
      url: url,
      data: JSON.stringify(toPOST),
      dataType: 'json',
      contentType: "application/json; charset=utf-8"
    })
    .done(function(data) {
          // do stuff here
          console.log('success');
      })
      .fail(function(err) {
          // do stuff here
          console.log('failed');
      })
      .always(function(info) {
          // do stuff here
          console.log('hi');
      });
  }

  // LonLat to LatLon, to JSON
  wrap (coor, radius) {
    let ret = { points: {}, parameter: {}};
    let coorContainer = new Array();

    for(var i in coor) { // From xy to LonLat
      coorContainer.push(ol.proj.toLonLat(coor[i]));
    };

    // console.log(coorContainer);
    // console.log(radius);

    for(var i=0; i<coorContainer.length; i++){ // Points
      ret['points']['point'+ (i+1)] = {
        lontitude: coorContainer[i][0],
        latitude: coorContainer[i][1],
        radius: radius[i]
      };
    };

    ret['parameter']['w'] = '';
    ret['parameter']['month'] = 0;
    ret['parameter']['n'] = 10;


    // console.log(ret);
    return JSON.stringify(ret);
  }

}
