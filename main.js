//run on startup
$(document).ready(main);

// here's how to do the fast re-ordering
//http://jsbin.com/oyaxa/1/edit
//$('button').click(function() {
//$("div.band").randomize("div.member");
//});
//(function($) {
//$.fn.randomize = function(childElem) {
  //return this.each(function() {
      //var $this = $(this);
      //var elems = $this.children(childElem);
      //elems.sort(function() { return (Math.round(Math.random())-0.5); });  
      //$this.empty();  
      //for(var i=0; i < elems.length; i++)
        //$this.append(elems[i]);      
  //});    
//}
//})(jQuery);


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
    if (entry.title.indexOf('UPDATED')==-1) { post+='<div class="post">';} else { post+='<div class="postupdated">';}
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
    $('#inputbox').val(getParameterByName('tags'));
    parseRSS('http://arxiv.org/rss/quant-ph', populate);
}
