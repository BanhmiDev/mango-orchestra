// TODO: better error checking
$(document).ready(function(){
    //Initialize Websocket
    var connection = new WebSocket("ws://" + window.location.host + "/websocket");
    
    var isPlaying = false;
    var time = 0;
    var end_time = 0;

    var music = null;
    var musicVolume = $("#player-volume").val();
    var playerID = 0;

    // Initialize music
    $.getJSON("/jukebox?song=current", function(data) {
        music = new Howl({
            src: [data["src"]],
            loop: false,
        });
    });

    // Player start
    $('#player-play').click(function() {
        if (!isPlaying && music != null) {
            isPlaying = true;
            playerID = music.play();
            music.volume(musicVolume);
            music.seek(time, playerID);
        }
    });

    // Player volume control 
    $("#player-volume").on("change mousemove", function() {
        if (music != null) {
            musicVolume = $(this).val();
            music.volume(musicVolume, playerID);
        }
    });

    connection.onclose = function(e) {
    }

    connection.onmessage = function(e) {
        if (music == null) // Not initialized yet
            return;

        var jukebox = JSON.parse(e.data);

        // Determine if we should go for the next song
        if (end_time != 0 && jukebox["time"] != 0 && end_time <= jukebox["time"]) {
            $.getJSON("/jukebox?song=next", function(data) {
                music = new Howl({
                    src: [data["src"]]
                });

                // Immediate playing
                if (isPlaying) {
                    playerID = music.play();
                    music.volume(musicVolume);
                }

                $(".progress-bar").css({'width': '0%'});
                time = 0;
            }); 
        }

        // Progress bar
        if (end_time != 0) {
            var progressMax = end_time;
            var currentProgress = Math.round(jukebox["time"]/(progressMax/100));
            if (currentProgress <= 100)
                $(".progress-bar").css({'width': currentProgress + '%'});
        }

        time = jukebox["time"];
        end_time = jukebox["end_time"];
        $("#listener-amount").html(jukebox["listeners"]);
        $("#player-title").html(jukebox["title"]);
        $("#player-artist").html(jukebox["artist"]);
    }
});

