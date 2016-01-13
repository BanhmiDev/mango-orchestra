var isPlaying = false;
var time = 0;

$(document).ready(function(){
    //Initialize Websocket
    var connection = new WebSocket("ws://" + window.location.host + "/websocket");
 
    window.setInterval(updateJukebox, 1000);

    function updateJukebox() {
        $.get("/jukebox", function(data) {
            var jukebox = JSON.parse(data);
            $("#listener-amount").html(jukebox['listeners']);
        });
    }

    var music = new Howl({
        src: ['/static/test.mp3']
    });       

    $.get("/sync", function(data) {
        if (data == "master") {
            time = 0;
            
            window.setInterval(function(){
                    $.post("/sync", { time: music.seek() });
            }, 1000);

        } else {
            time = data;

            window.setInterval(function(){
                $.get("/sync", function(data){
                    time = data; 
                });
            }, 1000);
        }
    });

    $('#player-play').click(function(){
        if (!isPlaying) {
            var id = music.play();
            music.seek(time + 10, id);
        }
    }); 

    connection.onclose = function(e) {
    }

    connection.onmessage = function(e) {
    }
});

