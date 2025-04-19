$(document).ready(function () {

    // Display Speak Message (no longer uses eel)
    function DisplayMessage(message) {
        console.log("DisplayMessage:", message);
        if ($(".siri-message").length) {
            $(".siri-message").text(message);
        } else if ($("#siri-message").length) {
            $("#siri-message").text(message);
        }
    }

    // Exposing for compatibility
    window.DisplayMessage = DisplayMessage;

    // Display hood
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    // Exposing for compatibility
    window.ShowHood = ShowHood;

    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message && message.trim && message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Exposing for compatibility
    window.senderText = senderText;

    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message && message.trim && message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Exposing for compatibility
    window.receiverText = receiverText;
    
    // Compatibility functions for eel
    if (typeof eel !== 'undefined') {
        // These were originally exposed to eel but now we're exposing them globally
        eel.expose(DisplayMessage);
        eel.expose(ShowHood);
        eel.expose(senderText);
        eel.expose(receiverText);
    }
});