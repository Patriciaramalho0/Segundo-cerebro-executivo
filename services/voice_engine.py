import streamlit as st
import streamlit.components.v1 as components
import re

def render_tts_script(text_to_speak, enabled=True, assistant_name="Luna"):
    if not enabled or not text_to_speak:
        return

    clean_text = re.sub(r'[*#_`\-]', '', text_to_speak)
    clean_text = clean_text.replace('"', '\\"').replace('\n', ' ')

    tts_js = f"""
    <script>
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        var utterance = new SpeechSynthesisUtterance("{clean_text}");
        utterance.lang = 'pt-BR';
        let voices = window.speechSynthesis.getVoices();
        let ptVoice = voices.find(v => v.lang.includes('pt') && (v.name.includes('Luciana') || v.name.includes('Google') || v.name.includes('Maria')));
        if (ptVoice) {{ utterance.voice = ptVoice; }}
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """
    components.html(tts_js, height=0, width=0)

def render_wake_word_listener(wake_word="Luna"):
    html_code = f"""
    <div style="background: white; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; font-family: sans-serif; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div>
            <h4 style="margin: 0; color: #0f172a; font-size: 14px;">🎙️ Comando de Voz Ativo ({wake_word})</h4>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 12px;" id="statusVoice">Clique no botão para falar.</p>
        </div>
        <button id="micToggleBtn" onclick="toggleMic()" style="background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 13px;">Falar com a IA</button>
    </div>

    <script>
    let recognition = null;
    let isListening = false;

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
        let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'pt-BR';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function() {{
            isListening = true;
            document.getElementById('micToggleBtn').style.backgroundColor = '#ef4444';
            document.getElementById('micToggleBtn').innerText = 'Ouvindo...';
            document.getElementById('statusVoice').innerText = 'Pode falar o comando...';
        }};

        recognition.onresult = function(event) {{
            let transcript = event.results[0][0].transcript;
            document.getElementById('statusVoice').innerText = 'Enviando: "' + transcript + '"';
            
            try {{
                let chatInput = window.parent.document.querySelector('textarea[aria-label*="Digite sua mensagem"]') || window.parent.document.querySelector('input[type="text"]');
                if (chatInput) {{
                    let nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, "value")?.set || Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, "value")?.set;
                    if (nativeInputValueSetter) {{
                        nativeInputValueSetter.call(chatInput, transcript);
                    }} else {{
                        chatInput.value = transcript;
                    }}
                    chatInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    setTimeout(() => {{
                        let enterEvent = new KeyboardEvent('keydown', {{
                            key: 'Enter',
                            code: 'Enter',
                            keyCode: 13,
                            which: 13,
                            bubbles: true
                        }});
                        chatInput.dispatchEvent(enterEvent);
                    }}, 300);
                }}
            }} catch(e) {{ console.log(e); }}
        }};

        recognition.onerror = function() {{ resetMic(); }};
        recognition.onend = function() {{ resetMic(); }};
    }}

    function toggleMic() {{
        if (!recognition) {{
            alert("Seu navegador não suporta reconhecimento de voz.");
            return;
        }}
        if (isListening) {{
            recognition.stop();
            resetMic();
        }} else {{
            recognition.start();
        }}
    }}

    function resetMic() {{
        isListening = false;
        let btn = document.getElementById('micToggleBtn');
        if(btn) {{
            btn.style.backgroundColor = '#2563eb';
            btn.innerText = 'Falar com a IA';
        }}
        let status = document.getElementById('statusVoice');
        if(status) status.innerText = 'Clique no botão para falar.';
    }}
    </script>
    """
    components.html(html_code, height=75)