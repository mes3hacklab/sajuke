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
                html += "<li data-role='list-divider'>Authors</li>";
                $.each( response.authors, function ( i, val ) {
                    html += "<li class='authors elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'>" + val.name + "<input type='hidden' value='" + val.id + "'/></li>";
                });
                html += "<li data-role='list-divider'>Songs</li>";
                $.each( response.songs, function ( i, val ) {
                    html += "<li class='songs elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Album: </strong>" + val.album.name + "<strong> Author: </strong>" + val.author.name + "</p></li>";
                });
                html += "<li data-role='list-divider'>Albums</li>";
                $.each( response.albums, function ( i, val ) {
                    html += "<li class='albums elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2>" + val.name + "</h2><p><strong> Author: </strong>" + val.author.name + " </p><input type='hidden' value='" + val.id + "'/></li>";
                });
                ul.html( html );
                ul.listview( "refresh" );
                ul.trigger( "updatelayout");
            });
        }
    });
    $('#autocomplete').on('click', '.albums', function () {
        albumid = $(this).find('input').val();
        var ul = $('#autocomplete');
        var html = '';
        ul.html("");

        $.ajax({
            url: "http://localhost:8080/api/songs",
            dataType: "json",
            crossDomain: true,
            data: {
                album:  albumid
            }
        })
        .then( function (response) {
            html += "<li data-role='list-divider'>Songs</li>";
            $.each( response, function ( i, val ) {
                html += "<li class='songs elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Album: </strong>" + val.album.name + "<strong> Author: </strong>" + val.author.name + "</p></li>";
            });
            ul.html( html );
            ul.listview( "refresh" );
            ul.trigger( "updatelayout");
        });
    });
    $('#autocomplete').on('click', '.authors', function () {
        authorid = $(this).find('input').val();
        var ul = $('#autocomplete');
        var html = '';
        ul.html("");

        $.ajax({
            url: "http://localhost:8080/api/songs",
            dataType: "json",
            crossDomain: true,
            data: {
                author:  authorid
            }
        })
        .then( function (response) {
            html += "<li data-role='list-divider'>Albums</li>";
            $.each( response, function ( i, val ) {
                html += "<li class='albums elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.album.name + "</h2><p><strong> Author: </strong>" + val.author.name + "</p><input type='text' value='" + val.id + "'/></li>";
            });
            html += "<li data-role='list-divider'>Songs</li>";
            $.each( response, function ( i, val ) {
                html += "<li class='songs elem ui-btn ui-btn-icon-right ui-icon-carat-r ui-li ui-li-has-thumb' data-icon='arrow-r' data-iconpos='right'><img src='img/box.png'><h2> " + val.name + "</h2><p><strong> Album: </strong>" + val.album.name + "<strong> Author: </strong>" + val.author.name + "</p></li>";
            });
            ul.html( html );
            ul.listview( "refresh" );
            ul.trigger( "updatelayout");
        });
    });

});

