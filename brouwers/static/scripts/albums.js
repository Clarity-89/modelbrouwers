$(document).ready(function() {    
    $('.no-javascript').remove(); //hide the warning
    
    $('.BBCode').focus(function(){
        $(this).select();
    });
    $('.BBCode').mouseup(function(e){
        e.preventDefault();
    });
    
    //fix afbeeldingen verticaal centreren
    fixVerticalCenter();
    
    // my albums - overzicht + editen etc.
    /*$('#personal-albums').on('mouseover', 'a.album', function() {
        $(this).find('.edit, .remove').show();
    });
    $('#personal-albums').on('mouseenter', 'a.album img', function() {
        $(this).parent().find('.edit, .remove').show();
    });*/
    $('a.album').hover(function() {
        $(this).find('.edit, .remove, .restore').show();
    });
    $('a.album img').hover(function() {
        $(this).parent().find('.edit, .remove, .restore').show();
    });
    /*$('#personal-albums').on('mouseout', 'li.album', function() {
        $(this).find('.edit, .remove').hide();
    });*/
    $('li.album').mouseout(function() {
        $(this).find('.edit, .remove, .restore').hide();
    });
    
    if ($('#new-album-dialog').length > 0){
        $('#new-album-dialog').dialog({
			    autoOpen: false,
			    height: 400,
			    width: 800,
			    modal: true,
			    title: "Nieuw album",
			    buttons: {
			        "Bewaren": function(){
			            data = $('form#new-album').serializeArray();
			            $.post(
			                url_new,
			                data,
			                function (response){
			                    $("#new-album-dialog").html(response);
			                }
			            );
			        },
			        "Annuleren": function() {
			            $(this).dialog("close");
			        }
			    }
	    });
	}
    if ($('#edit-dialog').length > 0){
        $('#edit-dialog').dialog({
			    autoOpen: false,
			    height: 400,
			    width: 800,
			    modal: true,
			    title: "Album bewerken",
			    buttons: {
			        "Opslaan": function(){
			            data = $('#form-edit-album').serializeArray();
			            var album_id = $(this).find('input[name="album"]').val();
			            $.post(
			                url_edit,
			                data,
			                function (response){
			                        $("#edit-dialog").html(response);
			                }
			            );
			        },
			        "Annuleren": function() {
			            $(this).dialog("close");
			            $(this).dialog("option", "height", 400);
			        }
			    }
	    });
	}
	if ($('#remove-dialog').length > 0){
        $('#remove-dialog').dialog({
			autoOpen: false,
			draggable: false,
			dialogClass: "remove-album",
			height: 200,
			width: 400,
			modal: true,
			title: "Naar prullenbak?",
			buttons: {
			    Bevestig: function(){
			        var album_id = $('#remove-album').val();
			        $.post(
			            url_remove,
			            {'album': album_id},
			            function (response){
			                if (response == 'ok'){
			                    $('li#album_'+album_id).remove();
			                    $('#remove-dialog').dialog("close");
			                } else {
			                    alert('Het verwijderen is niet geslaagd.');
			                }
			            }
			        );
			    },
			    Annuleren: function() {
			        $(this).dialog("close");
			    }
			}
	    });
	}
    
    $('img.edit').click(function(e){
    	openEditDialog(e, $(this));
    });
    
    $('img.remove').click(function(e){
    	openRemoveDialog(e, $(this));
    });
    
    $('img.restore').click(function(e){
    	restoreAlbum(e, $(this));
    });
    $('a#new-album-popup').click(function(e){
        e.preventDefault();
        $('#new-album-dialog').dialog('open');
        return false;
    });
    
    $('.photo-container2 img.photo, .in-photo-navigation').mouseenter(function() {
        $('div.in-photo-navigation').css('visibility', 'visible');
    });
    $('.photo-container2 img.photo').mouseleave(function() {
        $('div.in-photo-navigation').css('visibility', 'hidden');
    });
    
    var searchfield = $("#id_search");
    if (searchfield.val() == ''){
        searchfield.val('albums doorzoeken...');
        searchfield.css('color', '#555');
    }
    
    searchfield.focus(function () {
        searchfield.val('');
        searchfield.css('color', 'auto');
        $(this).autocomplete({
            source: "/albums/search/",
            autoFocus: true,
            minLength: 3,
            delay: 0,
            select:  function(e, ui) {
                window.location = ui.item.url;
            }
        });
    });
    searchfield.blur(function () {
        if (searchfield.val() == ''){
            searchfield.css('color', '555');
            searchfield.val('albums doorzoeken...');
        }
    });
    // setting the album cover
    $('.album-photos-list a.photo img').mouseenter(function(){
        if (!$(this).parent().parent().hasClass('cover')){
            $(this).parent().find('img.set_cover').show();
        }
    });
    $('.album-photos-list a.photo img').mouseleave(function(){
        $(this).parent().find('img.set_cover').hide();
    });
    $('.album-photos-list a.photo img.set_cover').click(function(e){
        e.stopPropagation();
        var a = $(this).parent();
        var p_id = a.attr('id').slice(6);
        $.post('/albums/set_cover/', {'photo': p_id}, function(data){
            if (data == 1){//success
                $('.cover').removeClass('cover');
                a.parent().addClass("cover");
            }
        });
        return false; // don't follow the url
    });
    try{
        initSortable($('#personal-albums'));
    }
    catch (err){
        //do nothing
    }
    $('#ShowAllAlbums').click(function(e){
        e.preventDefault();
        $.get(
            "/albums/all_own/",
            function (response){
                $('#personal-albums').replaceWith(response);
                initSortable($('#personal-albums'));
                fixVerticalCenter();
            }
        );
        return false;
    });
});

function hideNewAlbum(){
    $('div#new_album').html('');
    $('a#create_new_album').show();
}

function showHelp(e){
    //close all (the others)
    if ($(e).css('display') == 'none')
    {
        $('span.help_text').hide();
    }
    $('td.help_text div').hide();
    $(e).parent().parent().find('td.help_text div').toggle();
    $(e).siblings('.help_text').toggle();
}

function updateOrder(album, album_before, album_after){
    $.post(
        "/albums/reorder/",
        {
            'album': album, 
            'album_before': album_before,
            'album_after': album_after
        }
    );
}
function fixVerticalCenter(){
    var $a = $('a.album, a.photo');
    $.each($a, function(){
        var a_height = $(this).height();
        var img = $(this).children('img.thumb')[0];
        var img_height = $(img).attr('height');
        if (img_height > 0 && img_height != a_height){
            padding = (a_height - img_height) / 2;
            $(img).css('padding-top', padding);
            $(img).css('padding-bottom', padding);
        }
    });
}

function initSortable(element){
    element.sortable({
        placeholder: "sort-placeholder album",
        forcePlaceholderSize: true,
        helper: 'clone',
        forceHelperSize: true,
        opacity: 0.8,
        update: function(event, ui){
            var album = ui.item.find('input[name="album_id"]').val();
            var album_before = ui.item.prev().find('input[name="album_id"]').val();
            var album_after = ui.item.next().find('input[name="album_id"]').val();
            updateOrder(album, album_before, album_after);
        }
    });
}
function showCovers(){
    if ($('#photo-navigation').css('display') == 'none')
    {
        $('#photo-navigation').show();
        height = $('#photo-navigation').height();
        new_height = height + $("#edit-dialog").dialog( "option", "height" )+20;
        $('#edit-dialog').parent().css('top', '100px');
        $("#edit-dialog").dialog( "option", "height", new_height );
        
        $('#edit-dialog #photo-navigation img').click(function(){
            var p_id = $(this).next().val();
            $('#form-edit-album input[name="cover"]').val(p_id);
            $('#photo-navigation li').removeClass('cover');
            $(this).closest('li').addClass('cover');
        });
    }
    else
    {
        $('#photo-navigation').hide();
        height = $('#photo-navigation').height();
        new_height = $("#edit-dialog").dialog( "option", "height" ) - height - 20;
        $("#edit-dialog").dialog( "option", "height", new_height );
    }
    return false;
}
function openEditDialog(e, element, album_id){
    e.preventDefault();
    if (typeof album_id == 'undefined'){
	    var li = $(element).closest('li.album');
	    var album_id = li.children('input[name="album_id"]').val();
	}
	$.get(
	    url_edit,
	    {'album': album_id},
	    function (response){
	        $("#edit-dialog").html(response);
	        
	        $('#id_hidden_cover').val($('#id_cover').val());
	        var a = "<a href=\"#\" onclick=\"showCovers();\">";
	        a += "<u>Cover kiezen</u></a>";
            $('#id_cover').replaceWith(a);
	    }
	);
	
	$("#edit-dialog").dialog("open");
	$('button').button();
	$(".ui-icon-closethick").click(function(){
	    $("#edit-dialog").dialog("option", "height", 350);
	});
    return false;
}
function openRemoveDialog(e, element){
    e.preventDefault();
    var li = $(element).closest('li.album');
    remove_album_id = li.children('input[name="album_id"]').val();
    $('#remove-album').val(remove_album_id);
    $.get(
        url_get_title,
        {'album': remove_album_id},
        function (title){
            $("span#id-album-title").text(title);
        }
    );
    $("#remove-dialog").dialog("open");
    return false;
}
function restoreAlbum(e, element){
    e.preventDefault();
    var li = $(element).closest('li.album');
    album_id = li.children('input[name="album_id"]').val();
    
    $.post(
        url_restore,
		{'album': album_id},
		function (response){
		    if (response == 'ok'){
			    $('li#album_'+album_id).remove();
			} else {
			    alert('Het terugzetten is niet geslaagd.');
			}
		}
	);
    return false;
}
