//run on startup
$(document).ready(main);

// parse some rss
function parseRSS(url, callback) 
{
  $.ajax({
      url: 'http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=10&callback=?&q=' + encodeURIComponent(url),
    dataType: 'json',
    success: function(data) {
      callback(data.responseData.feed);
    }
  });
}

function stripTitle(oldtitle)
{
    return oldtitle.replace(/ *\([^)]*\) */g, "");
}


// this gets called when the rss is loaded
function populate(rssjson)
{
    
    $('p').text('awd');
    for (var i=0; i<rssjson.entries.length; i++)
    { 
        var entry=rssjson.entries[i]
        console.log(entry.title);
        $('#container').append(entry.title);
        //document.write(cars[i] + "<br>");
    }
}


// the main function
function main() 
{
    parseRSS('http://arxiv.org/rss/quant-ph', populate);
}
