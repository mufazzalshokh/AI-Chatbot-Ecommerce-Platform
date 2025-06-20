// document.addEventListener("DOMContentLoaded", function () {
//     const toggleBtn = document.getElementById("chat-toggle");
//     const chatWindow = document.getElementById("chat-window");
//     const chatMessages = document.getElementById("chat-messages");
//     const sendBtn = document.getElementById("chat-send");
//     const inputField = document.getElementById("chat-input-field");
  
//     toggleBtn.addEventListener("click", () => {
//       chatWindow.style.display = chatWindow.style.display === "none" ? "flex" : "none";
//     });
  
//     sendBtn.addEventListener("click", async () => {
//       const msg = inputField.value.trim();
//       if (!msg) return;
  
//       appendMessage("You", msg);
//       inputField.value = "";
//       appendMessage("Bot", "Thinking...");
  
//       const response = await fetch("/en/chatbot/api/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           "X-CSRFToken": getCSRFToken(),
//         },
//         body: JSON.stringify({ message: msg })
//       });
  
//       const data = await response.json();
//       const botMsg = data.response || "Oops, something went wrong!";
//       replaceLastBotMessage(botMsg);
//     });
  
//     function appendMessage(sender, text) {
//       chatMessages.innerHTML += `<p><strong>${sender}:</strong> ${text}</p>`;
//       chatMessages.scrollTop = chatMessages.scrollHeight;
//     }
  
//     function replaceLastBotMessage(text) {
//       const messages = chatMessages.querySelectorAll("p");
//       if (messages.length > 0) {
//         messages[messages.length - 1].innerHTML = `<strong>Bot:</strong> ${text}`;
//       }
//     }
  
//     function getCSRFToken() {
//       const name = "csrftoken";
//       const cookies = document.cookie.split(";");
//       for (let cookie of cookies) {
//         if (cookie.trim().startsWith(name + "=")) {
//           return decodeURIComponent(cookie.trim().split("=")[1]);
//         }
//       }
//       return "";
//     }
//   });

//   function toggleChatbot() {
//     const widget = document.getElementById('chatbot-widget');
//     widget.classList.toggle('hidden');
// }



// function sendMessage() {
//     const input = document.getElementById('chatbot-input');
//     const messages = document.getElementById('chatbot-messages');
//     const userText = input.value;
//     if (!userText.trim()) return;

//     messages.innerHTML += `<div><strong>You:</strong> ${userText}</div>`;
//     input.value = '';

//     fetch('/en/chatbot/api/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({ message: userText })
//     })
//     .then(res => res.json())
//     .then(data => {
//         messages.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
//         messages.scrollTop = messages.scrollHeight;
//     });
// }

// // CSRF helper
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         for (let cookie of document.cookie.split(';')) {
//             cookie = cookie.trim();
//             if (cookie.startsWith(name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
  

$(function() {
    // speech synthesis setup…
    let synth = window.speechSynthesis;
    let msg = new SpeechSynthesisUtterance();
    msg.voice = synth.getVoices()[0];
    msg.rate = 1;
    msg.pitch = 1;
  
    $('#chatbot-form-btn').click(e => {
      e.preventDefault();
      $('#chatbot-form').submit();
    });
  
    $('#chatbot-form-btn-clear').click(e => {
      e.preventDefault();
      $('#chatPanel .media-list').empty();
    });
  
    $('#chatbot-form-btn-voice').click(e => {
      // voice recognition logic…
    });
  
    $('#chatbot-form').submit(function(e) {
      e.preventDefault();
      let message = $('#messageText').val();
      $('.media-list').append(`
        <li class="media">
          <div class="media-body">
            <div class="media">
              <div style="text-align:right; color:#2EFE2E" class="media-body">
                ${message}<hr/>
              </div>
            </div>
          </div>
        </li>
      `);
  
      $.ajax({
        type: 'POST',
        url: '{% url "chatbot:chatbot_response" %}',
        data: $(this).serialize(),
        success: function(response) {
          $('#messageText').val('');
          let answer = response.response;
          $('.media-list').append(`
            <li class="media">
              <div class="media-body">
                <div class="media">
                  <div style="color:white" class="media-body">
                    ${answer}<hr/>
                  </div>
                </div>
              </div>
            </li>
          `);
          $('.fixed-panel').animate({
            scrollTop: $('.fixed-panel')[0].scrollHeight
          }, 500);
  
          msg.text = answer;
          synth.speak(msg);
        },
        error: console.error
      });
    });
  });
  