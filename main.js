// TODO: add science, npg, prl, keyboard shortcuts, 

// Globals
var rainbow = new Rainbow(); 
rainbow.setSpectrum('#eeeeff', '#ffdd77');
introductionExists = true;
var lastInputValue='';
var feedData='';
var intervalID='none';

// Run on startup
$(document).ready(main);

function strip(s) { return s.replace(/^\s\s*/, '').replace(/\s\s*$/, ''); }


// Get the query string (http://www.mysite.com/index.php?x=x1&x=x2&x=x3)
function getQuery(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


// Format a post
function getPost(entry, matches, color)
{
    // ALL of the below should be done by python! just bung in the matches and the background color!
    var post='';
    post+='<div class="post" style="background-color: ' + color + ';">';

    // Title and matches
    post+='<div>';
    post+='<a href="' + entry.link + '" target="_blank">' + entry.title + '</a>';
    if (matches.length>0) { post+='<div id="matches" class="match">'+matches+'</span></div>'; }
    post+='<br class="clear"/>';
    post+='</div>';

    // Authors and date
    post+='<div>';
    post+='<div class="authors">'+entry.authors+'</div>';
    if (entry.published=="New")
    {
        post+='<div class="newPost">'+entry.published+'</div>';
    } else 
    {
        post+='<div class="date">'+entry.published+'</div>';
    }

    post+='<br class="clear"/>';
    post+='</div>';

    // The abstract
    post+='<div class="abstract" style="display: none;">'+entry.abstract+'</div>';

    post+='</div>';
    return post;
}


// Parse the tags
function parseTags(raw) { 
    var rawtags=raw.replace(/,/g, ' ').split(' '); 
    var tags=new Array();
    for (var i=0; i<rawtags.length; i++)
    {
        if (rawtags[i].length>2){ tags.push(strip(rawtags[i])); }
    }
    return tags;
}


// Score a post
function getMatches(search, tags)
{
    var matches=new Array();
    for (var i=0; i<tags.length; i++)
    {
        if (search.indexOf(tags[i])!=-1){ matches.push(tags[i]); }
    }
    return matches;
}


// Update the bookmark link
function updateBookmarkLink(tags)
{
    var link='http://www.peteshadbolt.co.uk/barxiv/?tags='+tags.join('_');
    if (!$('#sortBox').is(':checked')){link+='\&nosort=1';}
    $('#bookMarkLink').attr('href', link)
}


// Remove the introduction panel
function removeIntroduction(speed)
{
    if (!introductionExists){return;}
    if (speed=='slow'){ $('#introduction').fadeOut(500, function() {$('#introduction').remove();}); }
    if (speed=='fast'){ $('#introduction').remove(); }
    introductionExists=false;
}


// Update the full page
function update(force)
{
    // Skip if the input box has not changed
    var inputValue=$('#inputbox').val()
    if (lastInputValue == inputValue && !force){return;}
    lastInputValue=inputValue;

    // Clear the introduction if necessary
    if (inputValue.length>2) {removeIntroduction('slow');}

    // Parse the user's command 
    var tags = parseTags(inputValue);
    updateBookmarkLink(tags);

    // Score each post
    var table = new Array();
    var max = 0;
    for (var i=0; i<feedData.length; i++) 
    { 
        var matches=getMatches(feedData[i].search, tags);
        if (matches.length>max){ max = matches.length; }
        table.push({'index':i, 'matches':matches, 'score':matches.length }); 
    }

    // Sort by number of matches
    if ($('#sortBox').is(':checked') && max>0) { table.sort(function(a,b){ return b['score']-a['score']; }); }

    // Rebuild the table
    $('#container').empty();  
    rainbow.setNumberRange(0, max==0 ? 1 : max);
    var s='<div>';
    for(var i=0; i < table.length; i++)
    {
        var row = table[i];
        var color = '#'+rainbow.colourAt(row['score']);        
        s += getPost(feedData[row['index']], row['matches'].join(' '), color);
    }    
    s+='</div>';

    // Put it in there
    $('#container').append(s);      
    
    // Hide all the abstracts
    //$('.abstract').hide();
    $('.post').click(function(){$(this).find('.abstract').slideToggle(100);});

}


// Set up the input box
function setInputBox(tags)  
{
    if (tags.length<=0) {return;}
    $('#inputbox').val(tags.replace(/_/g, ' '));
    removeIntroduction('fast');
    update();
}


// load a feed
function loadFeed(filename)
{
    if (intervalID!='none') {clearInterval(intervalID);}
    $.getJSON(filename, function( json ) {
        feedData = json;
        intervalID = setInterval(update, 250);
        update(true);
    });
}


// Gets called when the page loads
function main() 
{
    // Bind update to form changes
    $('#sortBox').change(function(){update(true);});
    $('.changesource').click(function()
    {
        $('.changesource').css('border', 'none');
        loadFeed($(this).text()+'.json');
        $(this).css('border', '1px solid red');
    });
    $('#firstChanger').css('border', '1px solid red');

    // Set up the input box from the query string and focus
    $('#sortBox').prop('checked', !(getQuery('nosort')=='1'));
    setInputBox(getQuery('tags'));
    $('#inputbox').focus(); 

    // Load the json and fill the screen
    loadFeed('quant-ph.json');
}
