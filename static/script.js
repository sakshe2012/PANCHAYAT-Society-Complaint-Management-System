document.addEventListener('DOMContentLoaded', () => {
    const micBtn = document.getElementById('mic-btn');
    const descriptionField = document.getElementById('description');
    const statusText = document.getElementById('recording-status');

    if (micBtn && descriptionField) {
        // Check for browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            micBtn.style.display = 'none';
            statusText.innerText = "Speech Recognition API not supported in this browser. Please try Chrome or Edge.";
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = true; // Keep recording until user clicks stop
        recognition.interimResults = true; // Show text as they speak
        recognition.lang = 'en-US';

        let isRecording = false;
        let originalText = ""; // To remember what was already in the textbox

        micBtn.addEventListener('click', () => {
            if (isRecording) {
                recognition.stop();
            } else {
                originalText = descriptionField.value;
                if (originalText.length > 0 && !originalText.endsWith(' ')) {
                    originalText += ' ';
                }
                try {
                    recognition.start();
                } catch (e) {
                    console.error("Could not start recognition", e);
                }
            }
        });

        recognition.onstart = () => {
            isRecording = true;
            micBtn.classList.add('recording');
            micBtn.innerHTML = '<i class="fas fa-stop"></i>';
            statusText.innerText = "Listening... Speak your complaint (Click square to stop).";
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            
            if (finalTranscript) {
                originalText += finalTranscript + ' ';
            }
            
            // Show live updating text in the description box
            descriptionField.value = originalText + interimTranscript;
        };

        recognition.onend = () => {
            isRecording = false;
            micBtn.classList.remove('recording');
            micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            statusText.innerText = "";
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            isRecording = false;
            micBtn.classList.remove('recording');
            micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            
            if (event.error === 'not-allowed') {
                statusText.innerText = "Error: Microphone access denied. Please allow mic permissions in your browser address bar.";
            } else {
                statusText.innerText = `Error: ${event.error}`;
            }
        };
    }
});
