$(document).ready(function(){
    //Initialize Websocket
    var connection = new WebSocket("ws://" + window.location.host + "/websocket");
    var clientID = 0;
    var clients = [];

    var isPlaying = false;
    var time = 0;
    
    var playerID = 0;

    // Initialize music
    // TODO: fetch current music
    var music = new Howl({
        src: ['/static/test.mp3'],
        loop: false,
    });

    // Player start
    $('#player-play').click(function() {
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

    connection.onclose = function(e) {
    }

    connection.onmessage = function(e) {
        if (music.duration() == 0) // Not initialized yet
            return;

        var jukebox = JSON.parse(e.data);

        // Determine if we should go for the next song
        if (music.duration() <= jukebox["time"]) {
            $.getJSON("/nextsong", function(data) {
                music = new Howl({
                    src: [data["src"]]
                });

                // Immediate playing
                if (isPlaying)
                    playerID = music.play();

                $(".progress-bar").css({'width': '0%'});
            }); 
        }

        // Progress bar
        if (music.duration() > 0) {
            var progressMax = music.duration();
            var currentProgress = Math.round(jukebox["time"]/(progressMax/100));
            if (currentProgress <= 100)
                $(".progress-bar").css({'width': currentProgress + '%'});
        }

        time = jukebox["time"];
        $("#listener-amount").html(jukebox["listeners"]);
        $("#player-title").html(jukebox["title"]);
        $("#player-artist").html(jukebox["artist"]);
    }
});

