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


// get the query string (http://www.mysite.com/index.php?x=x1&x=x2&x=x3)
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
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


// this function populates the page
function populate(jsonData)
{
    for (var i=0; i<jsonData.length; i++) { $('#container').append(getPost(jsonData[i])); }
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
    // fill the screen
    populate(arxivData);
    
    // randomize once 
    $('#container').randomize('div.post');

    // Bind to input box update
    $('#inputbox').keyup(update);

    // set the input box from the query string
    //$('#inputbox').val(getParameterByName('tags'));
}
