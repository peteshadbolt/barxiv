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

// get the query string
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// clean up the title
function stripTitle(oldtitle) { return oldtitle.replace(/ *\([^)]*\) */g, ""); }

// clean up the authors
function stripAuthors(full) {
    console.log(full);
    //full=full.replaceAll("\&lt", "\<");
    //full=full.replaceAll("\&gt", "\>");
    return full.replaceAll("<[^>]*>", "");
}

// format a post
function getPost(entry)
{
    var post='';
    post+='<div class="post">';
    post+='<div>';
    post+='<span class="title">';
    post+=stripTitle(entry.title);
    post+='</span>';
    post+='</div>';

    post+='<div class="authors">';
    //post+=stripAuthors(entry.author);
    post+='awd'
    post+='</div>';
    post+='</div>';
    return post;
}

// this gets called when the rss is loaded
function populate(rssjson)
{
    
    $('p').text('Loading...');
    for (var i=0; i<rssjson.entries.length; i++)
    { 
        var entry=rssjson.entries[i];
        post=getPost(entry);
        $('#container').append(post);
    }
}

// the main function, gets called when the page loads
function main() 
{
    parseRSS('http://arxiv.org/rss/quant-ph', populate);
}
