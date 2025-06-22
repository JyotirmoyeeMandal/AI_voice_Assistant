from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import json
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="GEMINI_API_KEY")  
model = genai.GenerativeModel('gemini-2.5-pro')

# HTML template with voice recognition
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Voice Assistant</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        .voice-button {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(45deg, #ff6b6b, #ff8e53);
            color: white;
            font-size: 24px;
            cursor: pointer;
            margin: 20px auto;
            display: block;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        }
        .voice-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
        }
        .voice-button.listening {
            background: linear-gradient(45deg, #4ecdc4, #44a08d);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            margin: 20px 0;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
        }
        .message {
            margin: 10px 0;
            padding: 12px 16px;
            border-radius: 20px;
            max-width: 80%;
        }
        .user-message {
            background: rgba(255, 107, 107, 0.3);
            margin-left: auto;
            text-align: right;
        }
        .ai-message {
            background: rgba(78, 205, 196, 0.3);
            margin-right: auto;
        }
        .status {
            text-align: center;
            margin: 15px 0;
            font-style: italic;
            opacity: 0.8;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .instructions {
            text-align: center;
            margin: 20px 0;
            opacity: 0.9;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Voice Assistant</h1>
        <div class="instructions">
            <p>Click the button and speak to your AI assistant!</p>
            <p>The AI can help answer questions, provide information, and have conversations.</p>
        </div>
        
        <button class="voice-button" id="voiceBtn"></button>
        <div class="status" id="status">Click to start talking</div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                Hello! I'm your AI assistant. Click the button and tell me how I can help you today!
            </div>
        </div>
    </div>

    <script>
        const voiceBtn = document.getElementById('voiceBtn');
        const status = document.getElementById('status');
        const chatContainer = document.getElementById('chatContainer');
        
        let recognition;
        let isListening = false;

        // Check if browser supports speech recognition
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            recognition = new SpeechRecognition();
        } else {
            status.textContent = 'Speech recognition not supported in this browser';
            voiceBtn.disabled = true;
        }

        if (recognition) {
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = function() {
                isListening = true;
                voiceBtn.classList.add('listening');
                voiceBtn.textContent = '🔴';
                status.textContent = 'Listening... Speak now!';
            };

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                addMessage(transcript, 'user');
                sendToAI(transcript);
            };

            recognition.onerror = function(event) {
                status.textContent = 'Error: ' + event.error;
                resetButton();
            };

            recognition.onend = function() {
                resetButton();
            };
        }

        voiceBtn.addEventListener('click', function() {
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });

        function resetButton() {
            isListening = false;
            voiceBtn.classList.remove('listening');
            voiceBtn.textContent = '';
            status.textContent = 'Click to start talking';
        }

        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.textContent = text;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function sendToAI(text) {
            status.textContent = 'AI is thinking...';
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: text})
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'ai');
                speak(data.response);
                status.textContent = 'Click to start talking';
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error. Please try again.', 'ai');
                status.textContent = 'Error occurred';
            });
        }

        function speak(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9;
                utterance.pitch = 1;
                utterance.volume = 0.8;
                speechSynthesis.speak(utterance);
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'I didn\'t hear anything. Please try again.'})
        
        # Generate AI response using Gemini
        prompt = f"""
        You are a helpful AI assistant. A user just said: "{user_message}"
        
        Respond naturally and helpfully. Keep responses conversational and under 150 words 
        since this will be spoken aloud. Be friendly, informative, and engaging.
        
        If they ask about connecting to a human or need complex help, let them know this 
        is a demo AI assistant and suggest they contact the appropriate service.
        """
        
        response = model.generate_content(prompt)
        ai_reply = response.text.strip()
        
        return jsonify({'response': ai_reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'I apologize, but I\'m having trouble processing your request right now. Please try again.'})

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'AI Voice Assistant'}

if __name__ == '__main__':
    print("Starting Web-Based AI Voice Assistant...")
    print("Access at: http://localhost:5000")
    print("Click microphone and start talking!")
    app.run(debug=True, host='0.0.0.0', port=5000)