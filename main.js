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

// the main function
function main() 
{
    parseRSS('http://arxiv.org/rss/quant-ph', populate);
}

// this gets called when the rss is loaded
function populate(newtext)
{
    $('p').text('awd');
    console.log(newtext);
}


