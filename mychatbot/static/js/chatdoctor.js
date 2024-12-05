// 選取聊天框、輸入框、表單及按鈕
const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');
const btnAuto = document.querySelector('.btn-auto');
const btnSend = document.querySelector('.btn-send');

// 監聽「送出」按鈕的表單送出事件
messageForm.addEventListener('submit', (event) => {
    event.preventDefault(); // 防止表單重新整理

    const message = messageInput.value.trim(); // 取得輸入框的內容並移除多餘空白
    if (message.length === 0) return; // 若輸入為空，則不處理

    // 新增使用者的訊息
    addMessage(message, 'sent');

    // 模擬機器人回應
    setTimeout(() => {
        addMessage(`這是機器人的回應：你剛剛說了 "${message}"`, 'received');
    }, 500);

    // 清空輸入框
    messageInput.value = '';
});

// 監聽「輔助輸入」按鈕的點擊事件
btnAuto.addEventListener('click', () => {
    const suggestions = [
        '請問今天的健康提醒是什麼？',
        '我該如何改善我的生活習慣？',
        '有哪些可以增強免疫力的小技巧？'
    ];
    const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
    messageInput.value = randomSuggestion; // 將建議文字填入輸入框
});

// 新增訊息到訊息列表的功能
function addMessage(text, type) {
    const message = document.createElement('li');
    message.classList.add('message', type);
    message.innerHTML = `
        <div class="message-text">${text}</div>
    `;
    messagesList.appendChild(message);

    // 滾動到最新訊息
    messagesList.scrollTop = messagesList.scrollHeight;
}
