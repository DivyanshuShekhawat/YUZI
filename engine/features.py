import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat
import threading
import queue

con = sqlite3.connect("yuzi.db")
cursor = con.cursor()

# Create a simple response cache
response_cache = {}

# Fast responses for common questions
quick_responses = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi there! What can I do for you?",
    "how are you": "I'm doing well, thanks for asking!",
    "who are you": "I'm YUZI, your personal AI assistant.",
    "what time is it": "Please check the clock on your device.",
    "thank you": "You're welcome!",
    "thanks": "Happy to help!",
    "bye": "Goodbye! Have a great day!",
    "good morning": "Good morning! How can I assist you today?",
    "good afternoon": "Good afternoon! How can I help?",
    "good evening": "Good evening! Need any assistance?",
    "what can you do": "I can answer questions, open apps, play YouTube videos, and more.",
}

# Add more robust quick responses as fallbacks
fallback_responses = {
    # General knowledge
    "who": "I'm YUZI, your AI assistant developed to help you with various tasks and answer questions.",
    "what": "I'm an AI assistant that can help with information, control your computer, and assist with various tasks.",
    "when": "I don't have real-time data for dates and times. Please check a calendar or clock for that information.",
    "where": "I exist as software running on your computer right now. I was developed to assist with various tasks.",
    "why": "I was created to make your computer interactions easier and more natural through voice commands and AI assistance.",
    "how": "I work by processing your voice commands and responding with helpful information using AI technology.",
    "can you": "I can answer questions, open applications, play videos, send messages, and help with many other tasks. Just ask!",
    "tell me about": "I'd be happy to tell you about that topic. What specific aspects would you like to know?",
    "explain": "I'll explain that as simply as possible. Let me know if you need more details on any part.",
   
}

@eel.expose
def playAssistantSound():
    music_dir= "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)  


# Mobile functionality
def makeCall(name, mobile_no):
    mobile_number_str = str(mobile_no)
    if not mobile_number_str.startswith('+91'):
        mobile_number_str = '+91' + mobile_number_str
    
    jarvis_message = "Calling to "+name
    
    # Construct the URL for phone call
    call_url = f"tel:{mobile_number_str}"
    
    # Construct the full command
    full_command = f'start "" "{call_url}"'
    
    # Open phone app with the constructed URL
    subprocess.run(full_command, shell=True)
    speak(jarvis_message)


def sendMessage(message, mobile_no, name):
    mobile_number_str = str(mobile_no)
    if not mobile_number_str.startswith('+91'):
        mobile_number_str = '+91' + mobile_number_str
    
    jarvis_message = "Message sent successfully to "+name
    
    # Construct the URL for SMS
    sms_url = f"sms:{mobile_number_str}?body={quote(message)}"
    
    # Construct the full command
    full_command = f'start "" "{sms_url}"'
    
    # Open messaging app with the constructed URL
    subprocess.run(full_command, shell=True)
    speak(jarvis_message)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("y")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()




# Whatsapp Message Sending
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    


def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 19
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 13
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 12
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)


# Function to handle HugChat in a separate thread
def get_hugchat_response(query, result_queue):
    try:
        print(f"Creating ChatBot with query: {query}")
        chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        
        system_message = "You are a helpful assistant that provides concise answers in exactly 2-3 lines total. Summarize information into these 2-3 lines rather than cutting off mid-thought."
        print("Sending system message")
        chatbot.chat(system_message)
        
        print("Sending user query")
        message_obj = chatbot.chat(query)
        
        # Debug output to see what we're getting
        print(f"Response type: {type(message_obj)}")
        
        # Wait for the response to complete
        print("Waiting for message to complete...")
        message_obj.wait_until_done()
        
        # Get the final text using the proper method
        response = message_obj.get_final_text()
        print(f"Got response: {response[:100]}...")
        
        # Don't truncate, as we've asked for a brief summary already
        result_queue.put(("success", response))
    except Exception as e:
        print(f"ERROR IN HUGCHAT: {str(e)}")
        result_queue.put(("error", f"Error: {str(e)}"))

def simple_fallback_response(query):
    """Generate a more specific response based on keywords when API fails"""
    query = query.lower()
    
    # First look for exact matches in quick_responses
    if query in quick_responses:
        return quick_responses[query]
    
    # Look for exact phrase matches in fallback_responses
    if query in fallback_responses:
        return fallback_responses[query]
    
    # Try to find the most specific keyword match
    best_match = None
    longest_match = 0
    
    # First prioritize multi-word matches
    for keyword, response in fallback_responses.items():
        if keyword in query and len(keyword.split()) > 1:
            # If we find a multi-word match that's longer than previous matches
            if len(keyword) > longest_match:
                longest_match = len(keyword)
                best_match = response
    
    # If no multi-word match, try single word matches
    if best_match is None:
        for keyword, response in fallback_responses.items():
            if keyword in query and len(keyword.split()) == 1:
                if len(keyword) > longest_match:
                    longest_match = len(keyword)
                    best_match = response
    
    # If we found a match, return it
    if best_match is not None:
        return best_match
            
    # If we get here, no specific keyword matched
    # Check if query is asking about a person, place, or thing
    if "who is" in query or "what is" in query or "tell me about" in query:
        topic = query.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        return f"I don't have specific information about {topic} right now. Try asking in a different way or about a different topic."
    
    # Default fallback
    return "I don't have enough information about that. Please try asking something else."

def chatBot(query):
    try:
        # Clean the query
        user_input = query.lower().strip()
        print(f"Processing query: '{user_input}'")
        
        # Check if we have a quick response for common greetings only
        for key, response in quick_responses.items():
            if (key == user_input or key in user_input) and len(key.split()) <= 2:
                print(f"Using quick response for common greeting: {user_input}")
                speak(response)
                return response
        
        # Check cache for existing response
        if user_input in response_cache:
            print(f"Using cached response for: {user_input}")
            cached_response = response_cache[user_input]
            speak(cached_response)
            return cached_response
        
        # Get fallback response but don't use it immediately
        fallback = simple_fallback_response(user_input)
            
        # Modify the query to request a 2-3 line summary
        formatted_query = "Summarize in exactly 2-3 lines: " + user_input
        
        # Start speaking immediately with a waiting message
        speak("Let me think about that...")
        
        # Set up threading to make it non-blocking
        result_queue = queue.Queue()
        chat_thread = threading.Thread(
            target=get_hugchat_response, 
            args=(formatted_query, result_queue)
        )
        chat_thread.daemon = True
        print("Starting thread for HugChat request")
        chat_thread.start()
        
        # Wait for response with longer timeout
        print("Waiting for response (timeout: 120s)")
        chat_thread.join(timeout=120)  # Increased timeout to 2 minutes
        
        status = "error"  # Default status in case of timeout
        if result_queue.empty():
            print("TIMEOUT: No response received in time")
            speak("This is taking longer than expected. Using a simpler answer instead.")
            response = fallback
        else:
            status, response = result_queue.get()
            print(f"Queue returned status: {status}")
            if status == "error":
                print(f"Error from HugChat: {response}")
                speak("I had trouble getting that information. Here's what I know:")
                response = fallback
        
        # Only cache successful responses
        if status == "success" and "error" not in response.lower() and "sorry" not in response.lower():
            response_cache[user_input] = response
            
        # Speak the final response
        speak(response)
        return response
    except Exception as e:
        error_msg = f"Error in chatBot function: {str(e)}"
        print(error_msg)
        
        # Use fallback only as last resort
        speak("I encountered an error getting your answer. Let me try a simpler approach.")
        fallback = simple_fallback_response(query)
        speak(fallback)
        return fallback

