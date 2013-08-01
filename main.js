//run on startup
$(document).ready(main);


// jquery extension to do the randomization
(function($) {
$.fn.randomize = function(childElem) {
  return this.each(function() {
      var $this = $(this);
      var elems = $this.children(childElem);
      elems.sort(function() { return (Math.round(Math.random())-0.5); });  
      $this.empty();  
      for(var i=0; i < elems.length; i++)
        $this.append(elems[i]);      
  });    
}
})(jQuery);


// parse some rss
function parseRSS(url, callback) 
{
  $.ajax({
      url: 'http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=100&callback=?&q=' + encodeURIComponent(url),
    dataType: 'json',
    success: function(data) {
      callback(data.responseData.feed);
    }
  });
}

// get the query string (http://www.mysite.com/index.php?x=x1&x=x2&x=x3)
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
    full=String(full);
    full=full.replace(/\&lt/g, '<');
    full=full.replace(/\&gt/g, '>');
    full=full.replace(/<[^>]*>/g, '');
    full=full.replace(/;/g, '');
    return full
}


// format a post
function getPost(entry)
{
    var post='';
    post+='<div class="post">';
    post+='<div>';
    post+='<span class="title">';
    var link = entry.link.replace(/abs/, 'pdf');
    post+='<a href="'+link+'">';
    post+=stripTitle(entry.title);
    post+='</a>'
    post+='</span>';
    post+='</div>';

    post+='<div class="authors">';
    post+=stripAuthors(entry.author);
    post+='</div>';
    post+='</div>';
    return post;
}


// this gets called when the rss is loaded
function populate(rssjson)
{
    console.log(rssjson);
    $('p').text('Loading...');
    for (var i=0; i<rssjson.entries.length; i++)
    { 
        var entry=rssjson.entries[i];
        post=getPost(entry);
        $('#container').append(post);
    }
}


// update the ordering etc
function update()
{
    // clear the introduction if necessary
    if ($('#introduction').length) { $('#introduction').slideUp(1000, function() {$('#introduction').remove();}); }

    // set the ordering
    $('#container').randomize('div.post');
}


// the main function, gets called when the page loads
function main() 
{
    parseRSS('http://arxiv.org/rss/quant-ph', populate);
    //var arxiv_query='http://export.arxiv.org/api/query?search_query=cat:quant-ph&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending';
    //parseRSS(arxiv_query, populate);
    
    // randomize once 
    $('#container').randomize('div.post');

    // Bind to input box update
    $('#inputbox').keyup(update);

    // set the input box from the query string
    //$('#inputbox').val(getParameterByName('tags'));
}
