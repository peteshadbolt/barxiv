// Globals
var rainbow = new Rainbow(); 
rainbow.setSpectrum('#eeeeff', '#ffdd77');
introductionExists = true;
var lastInputValue='';
var intervalID='none';
var sortPosts=false;
var searchTerms=[];

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
function saveSettings()
{
    var link='http://barxiv.appspot.com/?tags='+searchTerms;
    link+='&sort=' + (sortPosts ? '1' : '0');
    $('#bookMarkLink').attr('href', link)
    localStorage.searchTerms=searchTerms.join('_');
    localStorage.sortPosts=sortPosts;
    console.log('Wrote sort value to localStorage:' + localStorage.sortPosts);
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
function update(force=false)
{
    // Skip if the input box has not changed
    var inputValue=$('#inputbox').val()
    if (lastInputValue == inputValue && !force){return;}
    lastInputValue=inputValue;

    // Clear the introduction if necessary
    if (inputValue.length>2) {removeIntroduction('slow');}
    
    // Parse the user's command 
    searchTerms = parseTags(inputValue);
    
    // Build the url
    var url='?tags='+searchTerms
    sortPosts = $('#sortCheckBox').is(':checked');
    url += '&sort='+(sortPosts ? '1' : '0');
    saveSettings();
    
    // Grab the page from the server
    console.log('Requesting page...');
    $.ajax({
      url: 'instant'+url,
      dataType: 'html',
      success: function( data ) { $('#container').html(data); },
      error: function( data ) { console.log( "Page error"); }
    });
}

// Set up the input box
function setInputBox()  
{
    if (searchTerms.length<=0) {return;}
    var s = searchTerms.replace(/_/g, ' ');
    $('#inputbox').val(s);
    lastInputValue=s;
    removeIntroduction('fast');
}

function postClicked(arxiv_id, short_id)
{
    console.log('/abstract?arxiv_id='+arxiv_id);
    $.ajax({
      url:'/abstract?arxiv_id='+arxiv_id,
      dataType: 'html',
      success: function( data ) { 
        $('#'+short_id+' .abstract').html(data);
        $('#'+short_id+' .abstract').toggle();
      },
      error: function( data ) { console.log( "Page error"); }
    });
}

// Gets called when the page loads
function main() 
{
    // Set up the input box from the query string and focus
    var userTags=getQuery('tags')
    if (userTags=='' && localStorage.searchTerms!=undefined){userTags=localStorage.searchTerms;}
    $('#inputbox').focus(); 
    setInputBox(userTags);

    // Set up the checkbox
    console.log('On startup, found sort value ' + localStorage.sortPosts);
    if (localStorage.sortPosts!=undefined){ $('#sortCheckBox').prop(':checked', localStorage.sortPosts); }
    $('#sortCheckBox').change(update);

    // Periodically check the inputbox and update
    intervalID = setInterval(update, 500);
}

