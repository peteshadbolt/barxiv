//run on startup
$(document).ready(main);


// get the query string (http://www.mysite.com/index.php?x=x1&x=x2&x=x3)
function getQuery(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


// format a post
function getPost(entry, matches)
{
    if (matches==undefined){matches='';}
    var post='';
    post+='<div id="post' + String(entry.index)+ '" class="post">';

    post+='<div>';
    post+='<a href="' + entry.link + '">' + entry.title + '</a>';
    post+='<div id="matches" class="match">'+matches+'</span>'
    post+='</div>';

    post+='<div>';
    post+='<div class="authors">'+entry.authors+'</div>';
    post+='<div class="date">'+entry.published+'</div>';
    post+='<br class="clear"/>';
    post+='</div>';

    post+='</div>';
    return post;
}


// this function populates the page
function populate(jsonData)
{
    for (var i=0; i<jsonData.length; i++) 
    { 
        $('#container').append(getPost(jsonData[i]), '', ''); 
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
    if ($('#introduction').length && $('#inputbox').val().length>2) 
    { 
        $('#introduction').fadeOut(500, function() {$('#introduction').remove();}); 
    }

    // parse the user's command and score each post
    var tags = parseTags($('#inputbox').val());
    var table = [];
    var max = 1;
    for (var i=0; i<arxivData.length; i++) 
    { 
        var matches=getMatches(arxivData[i].search, tags);
        if (matches.length>max){max=matches.length;}
        table.push([i, matches, matches.length]); 
    }

    // sort by number of matches
    //if ($('#sortBox').is(':checked'))
    //{
        //table.sort(function(a,b){ return b[2]-a[2]; });
    //}

    // set the ordering
    $('#container').empty();  

    var rainbow = new Rainbow(); 
    rainbow.setNumberRange(0, max);
    rainbow.setSpectrum('#eeeeff', '#ffdd77');

    for(var i=0; i < arxivData.length; i++)
    {
        var color = '#'+rainbow.colourAt(table[i][2]);        
        var post=getPost(arxivData[table[i][0]], table[i][1].join(' '));
        $('#container').append(post);      
        //if (arxivData[table[i][0]].published=='Today'){color='red';}
        $('#post'+ String(arxivData[table[i][0]].index)).css('background-color', color);
    }    

    // update the link
    var link='http://www.peteshadbolt.co.uk/barxiv/?tags='+tags.join('_');
    if (!$('#sortBox').is(':checked')){link+='\&nosort=1';}
    $('#bookMarkLink').text(link);
    $('#bookMarkLink').attr('href', link)}


// the main function, gets called when the page loads
function main() 
{
    // fill the screen
    populate(arxivData);

    // Bind to input box update
    $('#inputbox').keyup(update);
    $('#inputbox').focus();
    
    // Bind the checkbox change
    $('#sortBox').change(update);

    // Bind to clicking divs
    //$('.post').click(function(){ $(this).slideUp(); });
    $('div.post').click(function(){console.log('click');});

    // set the input box from the query string
    var tags = getQuery('tags');
    if (tags.length>0)
    {
        $('#inputbox').val(tags.replace(/_/g, ' '));
        $('#introduction').remove();
        update();
    }

    // see if we should sort
    var nosort = getQuery('nosort');
    $('#sortBox').prop('checked', nosort!='1');
}
