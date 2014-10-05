$( document ).ready(function() {
			$( "#autocomplete" ).on( "listviewbeforefilter", function ( e, data ) {
				var ul = $( this ),
					input = $( data.input ),
					value = input.val(),
					html = "";
				ul.html( "" );
				if ( value && value.length > 1 ) {
					ul.html( "" );
					ul.listview( "refresh" );
					$.ajax({
						url: "http://localhost:8080/api/basicSearch",
						dataType: "json",
						crossDomain: true,
						data: {
							query: input.val()
						}
					})
					.then( function ( response ) {
                        $.each( response.authors, function ( i, val ) {
                            html += "<li class='elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'>Author: " + val.name + "</li>";
                        });
						$.each( response.songs, function ( i, val ) {
                           html += "<li class='elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'>Song: " + val.name + "</li>";
                        });
                        $.each( response.albums, function ( i, val ) {
                            html += "<li class='elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2>" + val.name + "</h2><p> Author: " + val.author.name + " </p></li>";
                         });
						ul.html( html );
						ul.listview( "refresh" );
						ul.trigger( "updatelayout");
					});

				}
			});

});
