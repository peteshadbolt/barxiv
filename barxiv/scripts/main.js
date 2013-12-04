// Globals
var rainbow = new Rainbow(); 
rainbow.setSpectrum('#eeeeff', '#ffdd77');
introductionExists = true;
var lastInputValue='';
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

// Update the bookmark link
function updateBookmarkLink(tags)
{
    var link='http://barxiv.appspot.com/?tags='+tags;
    $('#bookMarkLink').attr('href', link)
    localStorage.tags=tags.join('_')
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
    
    // Grab the page from the server
    console.log('Requesting page...');
    $.ajax({
      url:'instant?tags='+tags,
      dataType: 'html',
      success: function( data ) {
        console.log('Got page update');
        $('#container').html(data);
      },
      error: function( data ) {
        console.log( "Instant error");
      }
    });

}


// Set up the input box
function setInputBox(tags)  
{
    if (tags.length<=0) {return;}
    $('#inputbox').val(tags.replace(/_/g, ' '));
    removeIntroduction('fast');
    update();
}


// Gets called when the page loads
function main() 
{
    // Set up the input box from the query string and focus
    userTags=getQuery('tags')
    if (userTags=='' && localStorage.tags!=undefined){userTags=localStorage.tags;}
    setInputBox(userTags);
    $('#inputbox').focus(); 

    // Periodically check the inputbox and update
    intervalID = setInterval(update, 500);
}

