$(document).ready(function () {
    
    // Initialize with animations
    initializeUI();
    
    // Detect environment and set up API URL
    let apiBaseUrl;

    // If NETLIFY_BACKEND_URL is set via environment variable (embedded in the page during build)
    if (typeof NETLIFY_BACKEND_URL !== 'undefined') {
        apiBaseUrl = NETLIFY_BACKEND_URL;
    }
    // Check if we're running locally
    else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        apiBaseUrl = '';  // Use relative URLs on localhost
    }
    // Default to production backend URL if deployed elsewhere
    else {
        apiBaseUrl = 'https://yuzi-backend.onrender.com';  // Replace with your actual backend URL
    }
    
    console.log("API Base URL:", apiBaseUrl);
    
    // Initialize SiriWave
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: false
    });

    // Show/hide animation and interface elements
    function toggleSiriWave(show) {
        if (show) {
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            siriWave.start();
        } else {
            siriWave.stop();
            $("#Oval").attr("hidden", false);
            $("#SiriWave").attr("hidden", true);
        }
    }

    // Function to handle sending a command to the backend
    function sendCommand(message) {
        if (message.trim() === "") return;
        
        // Display user message in chat
        addMessage(message, 'sender');
        
        // Clear input field
        $("#chatbox").val("");
        
        // Show Siri wave animation
        toggleSiriWave(true);
        $("#siri-message").text("Processing your request...");
        
        // Send command to backend API
        $.ajax({
            url: `${apiBaseUrl}/api/command`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ command: message }),
            success: function(response) {
                // Display response from the backend
                if (response && response.response) {
                    $("#siri-message").text(response.response);
                    setTimeout(function() {
                        addMessage(response.response, 'receiver');
                        toggleSiriWave(false);
                    }, 1500);
                } else {
                    $("#siri-message").text("Sorry, I couldn't process that request.");
                    setTimeout(function() {
                        addMessage("Sorry, I couldn't process that request.", 'receiver');
                        toggleSiriWave(false);
                    }, 1500);
                }
            },
            error: function(xhr, status, error) {
                console.error("API Error:", error);
                $("#siri-message").text("Sorry, I'm having trouble connecting to my brain.");
                setTimeout(function() {
                    addMessage(`Sorry, I'm having trouble connecting to my backend at ${apiBaseUrl}. Please make sure it's running.`, 'receiver');
                    toggleSiriWave(false);
                }, 1500);
            }
        });
    }

    // Function to add message to the chat history
    function addMessage(message, type) {
        var chatBox = document.getElementById("chat-canvas-body");
        
        if (type === 'sender') {
            chatBox.innerHTML += `
                <div class="row justify-content-end mb-4">
                    <div class="width-size">
                        <div class="sender_message">${message}</div>
                    </div>
                </div>`;
        } else {
            chatBox.innerHTML += `
                <div class="row justify-content-start mb-4">
                    <div class="width-size">
                        <div class="receiver_message">${message}</div>
                    </div>
                </div>`;
        }
        
        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // UI initialization 
    function initializeUI() {
        // Animation for the text
        if ($.fn.textillate) {
            $('.text').textillate({
                loop: true,
                sync: true,
                in: {
                    effect: "bounceIn",
                },
                out: {
                    effect: "bounceOut",
                }
            });
        }
    }

    // Toggle button visibility based on input field content
    function toggleSendButton(message) {
        if (message.length == 0) {
            $("#SendBtn").hide();
        } else {
            $("#SendBtn").show();
        }
    }

    // Event Handlers
    
    // Input field keyup event
    $("#chatbox").keyup(function() {
        let message = $(this).val();
        toggleSendButton(message);
    });
    
    // Send button click event
    $("#SendBtn").click(function() {
        let message = $("#chatbox").val();
        sendCommand(message);
    });

    // Enter key press in chat input
    $("#chatbox").keypress(function(e) {
        if (e.which == 13) { // Enter key
            let message = $(this).val();
            sendCommand(message);
        }
    });

    // Initial welcome message
    setTimeout(function() {
        addMessage("Hello! I'm Y.U.Z.I. How can I help you today?", 'receiver');
        
        // Show connection info
        if (apiBaseUrl) {
            addMessage(`I'm connected to backend at: ${apiBaseUrl}`, 'receiver');
        } else {
            addMessage("I'm using a relative API path for local development", 'receiver');
        }
    }, 1000);
});