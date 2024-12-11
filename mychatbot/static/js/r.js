// 打開同意書彈跳視窗
function saveData() {
    const consentModal = document.getElementById('consentModal');
    consentModal.classList.remove('hidden');
}

function closeConsentModal(showAlert = true) {
    const consentModal = document.getElementById('consentModal');
    consentModal.classList.add('hidden');

    if (showAlert) {
        // 顯示提醒訊息
        alert('為了提供更準確的健康建議，您需填寫病歷資料才能完成註冊。');
    }
}



// 監聽同意書勾選
document.getElementById('consentCheckbox').addEventListener('change', function () {
    const agreeButton = document.getElementById('agreeButton');
    agreeButton.disabled = !this.checked; // 勾選時啟用按鈕，未勾選時禁用
});

// 確認同意書後執行儲存
document.getElementById('agreeButton').addEventListener('click', function () {
    var url = document.getElementById("Url").getAttribute('data-url');
    alert('註冊完成！將引導至登入畫面進行登入。');
    closeConsentModal(false); // 不顯示提醒
    // 導向登入畫面
    window.location.href = url; // 將 'login.html' 替換為你的登入頁面 URL
});
document.addEventListener('DOMContentLoaded', function () {
    // 選取所有 "其他" 選項的 checkbox
    const otherCheckboxes = document.querySelectorAll('input[type="checkbox"][value="其他"]');

    otherCheckboxes.forEach(checkbox => {
        // 獲取對應的輸入框
        const relatedInput = document.getElementById(checkbox.id.replace('-checkbox', '-input'));

        // 綁定變更事件
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                relatedInput.classList.remove('hidden'); // 顯示輸入框
            } else {
                relatedInput.classList.add('hidden'); // 隱藏輸入框
                relatedInput.value = ''; // 清空輸入框內容
            }
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registration-form");

    form.addEventListener("submit", function (event) {
        const inputs = form.querySelectorAll("input");
        let isValid = true;

        inputs.forEach((input) => {
            if (!input.value.trim()) {
                input.classList.add("error"); // 添加紅色邊框
                isValid = false;
            } else {
                input.classList.remove("error"); // 移除紅色邊框
            }
        });

        if (!isValid) {
            event.preventDefault(); // 阻止表單提交
            alert("請完整填寫所有欄位！");
        }
    });
});
function closeForm() {
    // 跳轉到 register.html
    window.location.href = "{% url 'register'%}";
}




