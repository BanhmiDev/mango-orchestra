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

    // Fetch information from server 
    updateJukebox();
    window.setInterval(updateJukebox, 1000);

    function updateJukebox() {
        $.get("/jukebox", function(data) {
            var jukebox = JSON.parse(data);
            $("#listener-amount").html(jukebox['listeners']);
            
            //$.inArray(clientID, clients) ||
            if (jukebox["isMaster"]) { // Determine if client is master
                //clients.push(jukebox["clientID"]);
                // Send player timestamp to server
                $.post("/sync", { time: music.seek() });
            } else {
                // Update client-side timestamp
                time = jukebox["time"];
            }
        });
    }
    
    // Player start
    $('#player-play').click(function(){
        if (!isPlaying) {
            isPlaying = true;
            playerID = music.play();
            music.volume($("#player-volume").val()); // Directly fetch from slider
            music.seek(time + 10, playerID);
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
    }
});

