$(document).ready(function(){
    //Initialize Websocket
    var connection = new WebSocket("ws://" + window.location.host + "/websocket");
    var clientID = 0;
    var clients = [];

    var isPlaying = false;
    var time = 0;
    
    // Initialize music
    var music = new Howl({
        src: ['/static/test.mp3']
    });
    var playerID = 0;

    // Player start
    $('#player-play').click(function(){
        if (!isPlaying) {
            isPlaying = true;
            playerID = music.play();
            music.volume($("#player-volume").val()); // Directly fetch from slider
            music.seek(time, playerID);
        }
    });

    // Player volume control 
    $("#player-volume").on("change mousemove", function() {
        music.volume($(this).val(), playerID);
    });

    // TODO
    connection.onclose = function(e) {
    }

    connection.onmessage = function(e) {
        //console.log(e.data);
        var jukebox = JSON.parse(e.data);
        time = jukebox["time"];
        $("#listener-amount").html(jukebox["listeners"]);
    }
});

