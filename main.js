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
function getQuery(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


// format a post
function getPost(entry)
{
    var post='';
    post+='<div id="post' + String(entry.index)+ '" class="post">';

    post+='<div>';
    post+='<a href="' + entry.link + '">' + entry.title + '</a>';
    post+='<div id="matches' + String(entry.index)+ '" class="match">hello</span>'
    post+='</div>';

    post+='<div class="authors">';
    post+=entry.authors;
    post+=' <i>' + entry.published + '</i>'; 
    post+='</div>';

    post+='</div>';
    return post;
}


// this function populates the page
function populate(jsonData)
{
    for (var i=0; i<jsonData.length; i++) 
    { 
        $('#container').append(getPost(jsonData[i])); 
    }
}

// parse tags from the user
function parseTags(raw) { return raw.replace(/,/g, ' ').split(' '); }

// score a post
function getMatches(search, tags)
{
    var matches=[];
    for (var i=0; i<tags.length; i++)
    {
        var tag=tags[i].replace(/^\s\s*/, '').replace(/\s\s*$/, ''); 
        if (tag.length>2 && search.indexOf(tag)!=-1){ matches.push(tags[i]); }
    }
    return matches;
}

// update the ordering etc
function update()
{
    // clear the introduction if necessary
    if ($('#introduction').length && $('#inputbox').val().length) 
    { 
        $('#introduction').fadeOut(500, function() {$('#introduction').remove();}); 
    }

    // parse the user's command and score each post
    var tags = parseTags($('#inputbox').val());
    var table = [];
    for (var i=0; i<arxivData.length; i++) 
    { 
        var matches=getMatches(arxivData[i].search, tags);
        table.push([arxivData[i].index, matches.length]); 
        var color=matches.length>0 ? '#ffdd88' : '#eeeeff';
        $('#post'+String(arxivData[i].index)).css('background-color', color);
        $('#matches'+String(arxivData[i].index)).text(matches.join(', '));
    }

    // sort by number of matches
    table.sort(function(a,b){ return a[1] - b[1]; });
    console.log(table);

    // set the ordering
    var elems = $('#container').children('div.post');
    $('#container').empty();  
    for(var i=0; i < elems.length; i++)
    {
        $('#container').append(elems[table[i][0]]);      
    }    

    // update the link
    var link='http://www.peteshadbolt.co.uk/barxiv.html?'+tags.join('_');
    $('#bookMarkLink').text(link);
    $('#bookMarkLink').attr('href', 'link')}


// the main function, gets called when the page loads
function main() 
{
    // fill the screen
    populate(arxivData);
    
    // randomize once 
    $('#container').randomize('div.post');

    // Bind to input box update
    $('#inputbox').keyup(update);
    $('#inputbox').focus();

    // set the input box from the query string
    //$('#inputbox').val(getQuery('tags'));
}
