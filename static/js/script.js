$( document ).ready(function() {
	var currentView = "basic";
	var previousView = "";
	var currentAuthorId = -1;
	var currentAlbumId = -1;
    $( "#autocomplete" ).on( "listviewbeforefilter", function ( e, data ) {
        var ul = $( this ),
			input = $( data.input ),
			value = input.val();
        ul.html( "" );
		ul.listview( "refresh" );
		if (currentView === "basic") {
			basicSearch(ul, value);
		} else if (currentView === "albums") {
			albumsSearch(ul, currentAlbumId, value);
		} else if (currentView === "songs") {
			songsSearch(ul, currentAuthorId, value);
		}

 
    });
    $('#autocomplete').on('click', '.albums', function () {
        albumId = $(this).find('input').val();
        $('input').val("");       
        var ul = $('#autocomplete');
        var html = '';
        ul.html("");
		albumsSearch(ul, albumId);
		previousView = currentView;
		currentView = "albums";
    });
    $('#autocomplete').on('click', '.authors', function () {
        authorId = $(this).find('input').val();
        $('input').val("");
        var ul = $('#autocomplete');
        var html = '';
        ul.html("");
        songsSearch(ul, authorId);
		previousView = currentView;
		currentView = "songs";
    });
    
	function basicSearch(ul, query) {
		$.ajax({
			url: "http://localhost:8080/api/basicSearch",
			dataType: "json",
			crossDomain: true,
			data: {
				query: query
			}
		})
		.then( function ( response ) {
			var html = "<li data-theme='b' data-role='list-divider'>Authors</li>";
			$.each( response.authors, function ( i, val ) {
				html += "<li class='authors elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'>" + val.name + "<input type='hidden' value='" + val.id + "'/></li>";
			});
			html += "<li data-theme='b' data-role='list-divider'>Songs</li>";
			$.each( response.songs, function ( i, val ) {
				html += "<li class='songs elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Album: </strong>" + val.album.name + "<strong> Author: </strong>" + val.author.name + "</p></li>";
			});
			html += "<li data-theme='b' data-role='list-divider'>Albums</li>";
			$.each( response.albums, function ( i, val ) {
				html += "<li class='albums elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2>" + val.name + "</h2><p><strong> Author: </strong>" + val.author.name + " </p><input type='hidden' value='" + val.id + "'/></li>";
			});
			ul.html( html );
			ul.listview( "refresh" );
			ul.trigger( "updatelayout");
		});	
	}

	function albumsSearch(ul, albumId, query) {
		currentAlbumId = albumId;
		$.ajax({
			url: "http://localhost:8080/api/songs",
			dataType: "json",
			crossDomain: true,
			data: {
				album:  albumId,
				query: (typeof query === "undefined" ? "" : query)
			}
		})
		.then( function (response) {
			var html = "<li data-theme='b' data-role='list-divider'>Songs</li>";
			$.each( response, function ( i, val ) {
				html += "<li class='songs elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Album: </strong>" + val.album.name + "<strong> Author: </strong>" + val.author.name + "</p></li>";
			});
			ul.html( html );
			ul.listview( "refresh" );
			ul.trigger( "updatelayout");
//			previousView = currentView;
//				currentView = "songs";
		});
	}

	function songsSearch(ul, authorId, query) {
		currentAuthorId = authorId;
		var callParameters;
		if (authorId === -1) {
			callParameters = {
				query: (typeof query === "undefined" ? "" : query)
			}
		} else {
			callParameters = {
				author:  authorId,
				query: (typeof query === "undefined" ? "" : query)
			}
		}
		$.ajax({
			url: "http://localhost:8080/api/albums",
			dataType: "json",
			crossDomain: true,	
			data: callParameters
		})
		.then( function ( response ) {
			var html = "<li data-theme='b' data-role='list-divider'>Albums</li>";
			$.each( response, function ( i, val ) {
				html += "<li class='albums elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Author: </strong>" + val.author.name + "</p><input type='hidden' value='" + val.id + "'/></li>";
			});
			$.ajax({
				url: "http://localhost:8080/api/songs",
				dataType: "json",
				crossDomain: true,
				data: callParameters
			})
			.then( function ( response ) {
				html += "<li data-theme='b' data-role='list-divider'>Songs</li>";
				$.each( response, function ( i, val ) {
					html += "<li class='songs elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Album: </strong>" + val.album.name + "<strong> Author: </strong>" + val.author.name + "</p></li>";
				});
				ul.html( html );
				ul.listview( "refresh" );
				ul.trigger( "updatelayout");
			});
		});	
	}

});


