// 初始化假数据
const initialData = {
    allergies: "阿斯匹林, 消炎止痛藥",
    pastIllness: "氣喘",
    longTermMedication: "無",
    habits: "吸菸, 喝酒",
    pregnancyStatus: "無"
};

// 模拟数据库存储（使用 localStorage）
if (!localStorage.getItem("userData")) {
    localStorage.setItem("userData", JSON.stringify(initialData));
}

// 从 localStorage 加载数据
function loadUserData() {
    const userData = JSON.parse(localStorage.getItem("userData"));

    // 显示数据到页面
    document.getElementById("allergies").innerText = userData.allergies || "無";
    document.getElementById("past-illness").innerText = userData.pastIllness || "無";
    document.getElementById("long-term-medication").innerText = userData.longTermMedication || "無";
    document.getElementById("habits").innerText = userData.habits || "無";
    document.getElementById("pregnancy-status").innerText = userData.pregnancyStatus || "無";
}

// 显示修改表单
function showForm() {
    const userData = JSON.parse(localStorage.getItem("userData"));

    document.getElementById("formModal").classList.remove("hidden");

    // 恢复表单内容
    setCheckboxValues("allergy", userData.allergies.split(", "));
    setCheckboxValues("illness", userData.pastIllness.split(", "));
    setRadioValue("medication", userData.longTermMedication === "無" ? "否" : "是");
    document.getElementById("medication-other").value = userData.longTermMedication === "無" ? "" : userData.longTermMedication;
    setCheckboxValues("habit", userData.habits.split(", "));
    setRadioValue("pregnancy", userData.pregnancyStatus);
}

// 保存数据
function saveData() {
    // 获取表单数据
    const updatedData = {
        allergies: getCheckboxValues("allergy").join(", "),
        pastIllness: getCheckboxValues("illness").join(", "),
        longTermMedication: getRadioValue("medication") === "否" ? "無" : document.getElementById("medication-other").value,
        habits: getCheckboxValues("habit").join(", "),
        pregnancyStatus: getRadioValue("pregnancy")
    };

    // 替换“其他”选项为填写的内容
    ["allergies", "pastIllness"].forEach(field => {
        updatedData[field] = updatedData[field].replace(/,? ?其他/g, ""); // 移除“其他”
    });

    // 保存到 localStorage
    localStorage.setItem("userData", JSON.stringify(updatedData));

    // 更新页面数据
    loadUserData();

    // 关闭表单
    closeForm();

    alert("資料已儲存！");
}

// 关闭修改表单
function closeForm() {
    document.getElementById("formModal").classList.add("hidden");
}

// 获取选中的复选框值
function getCheckboxValues(groupName) {
    const checkboxes = document.querySelectorAll(`input[name="${groupName}"]:checked`);
    const values = Array.from(checkboxes).map(checkbox => checkbox.value);
    const otherInput = document.getElementById(`${groupName}-other`);
    if (values.includes("其他") && otherInput && otherInput.value.trim()) {
        values[values.indexOf("其他")] = otherInput.value.trim(); // 替换“其他”为填写内容
    }
    return values;
}

// 设置复选框的选中状态
function setCheckboxValues(groupName, values) {
    const checkboxes = document.querySelectorAll(`input[name="${groupName}"]`);
    checkboxes.forEach(checkbox => {
        checkbox.checked = values.includes(checkbox.value); // 恢复复选框状态
    });
    const otherInput = document.getElementById(`${groupName}-other`);
    if (values.some(value => value !== "無" && !Array.from(checkboxes).some(cb => cb.value === value)) && otherInput) {
        // 如果“其他”中有值，恢复内容到输入框
        otherInput.value = values.find(value => value !== "無" && !Array.from(checkboxes).some(cb => cb.value === value)) || "";
        otherInput.classList.remove("hidden");
        const otherCheckbox = Array.from(checkboxes).find(cb => cb.value === "其他");
        if (otherCheckbox) {
            otherCheckbox.checked = true; // 勾选“其他”
        }
    } else if (otherInput) {
        // 隐藏并清空“其他”输入框
        otherInput.classList.add("hidden");
        otherInput.value = "";
    }
}

// 动态取消其他选中项逻辑
document.querySelectorAll(".checkbox-group").forEach(group => {
    group.addEventListener("change", function (event) {
        const target = event.target; // 当前被点击的复选框
        const checkboxes = group.querySelectorAll('input[type="checkbox"]'); // 获取组内所有复选框
        const otherInput = group.querySelector('input[type="text"]'); // 找到“其他”输入框

        if (target.value === "無" && target.checked) {
            // 如果勾选了“無”，取消其他选项
            checkboxes.forEach(checkbox => {
                if (checkbox !== target) {
                    checkbox.checked = false;
                }
            });
            if (otherInput) {
                otherInput.value = ""; // 清空“其他”输入框
                otherInput.classList.add("hidden"); // 隐藏输入框
            }
        } else if (target.value !== "無" && target.checked) {
            // 如果勾选其他选项，取消“無”
            checkboxes.forEach(checkbox => {
                if (checkbox.value === "無") {
                    checkbox.checked = false;
                }
            });
        }
    });
});

// 获取单选按钮值
function getRadioValue(groupName) {
    const selected = document.querySelector(`input[name="${groupName}"]:checked`);
    return selected ? selected.value : "";
}

// 设置单选按钮的选中状态
function setRadioValue(groupName, value) {
    const radios = document.querySelectorAll(`input[name="${groupName}"]`);
    radios.forEach(radio => {
        radio.checked = radio.value === value;
    });
}

// 页面加载时初始化数据
loadUserData();
