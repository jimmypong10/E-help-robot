const questions = [
    { question: "成人每天應該至少運動多少分鐘以保持健康？", options: { A: "A: 20分鐘", B: "B: 30分鐘", C: "C: 60分鐘" }, answer: "B" },
    { question: "糖尿病患者應該特別注意哪一種營養成分的攝取？", options: { A: "A: 蛋白質", B: "B: 脂肪", C: "C: 碳水化合物" }, answer: "C" },
    { question: "哪種技巧被用來幫助管理壓力和焦慮？", options: { A: "A: 冥想和正念練習", B: "B: 多喝咖啡", C: "C: 過度使用社交媒體" }, answer: "A" },
    { question: "為什麼規律的睡眠對心理健康很重要？", options: { A: "有助於恢復大腦功能", B: "增加壓力水平", C: "導致更多的焦慮" }, answer: "A" },
    { question: "低脂飲食對於哪種健康狀況的管理特別有益？", options: { A: "A: 高血壓", B: "B: 糖尿病", C: "C: 高膽固醇" }, answer: "C" },
    { question: "減少飽和脂肪攝入量可以幫助預防什麼疾病？", options: { A: "A: 骨質疏鬆症", B: "B: 心臟病", C: "C: 癌症" }, answer: "B" },
    { question: "定期看牙醫的建議頻率是？", options: { A: "A: 每年一次", B: "B: 每半年一次", C: "C: 每兩年一次" }, answer: "B" },
    { question: "哪種成分在牙膏中能有效預防蛀牙？", options: { A: "A: 氟化物", B: "B: 鉀", C: "C: 鎂" }, answer: "A" },
    { question: "哪一種飲食方法有助於長期減重成功？", options: { A: "A: 極端低熱量飲食", B: "B: 均衡且持久的飲食改變", C: "C: 單一食品飲食" }, answer: "B" },
    { question: "哪種營養素在減重飲食中應保持適量攝入以維持肌肉質量？", options: { A: "A: 碳水化合物", B: "B: 脂肪", C: "C: 蛋白質" }, answer: "C" }
];

let currentQuestionIndex = 0;
let score = 0;
let selectedQuestions = [];
let selectedAnswer = '';
const totalQuestions = 5;

function startQuiz() {
    selectedQuestions = questions.sort(() => 0.5 - Math.random()).slice(0, totalQuestions);
    currentQuestionIndex = 0;
    score = 0;
    selectedAnswer = '';
    document.getElementById('question-container').style.display = 'block';
    document.getElementById('restart-btn').style.display = 'none';
    document.getElementById('score').innerText = '';
    showQuestion();
}

function showQuestion() {
    if (currentQuestionIndex < totalQuestions) {
        const currentQuestion = selectedQuestions[currentQuestionIndex];
        document.getElementById('question').innerText = currentQuestion.question;
        document.querySelectorAll('.option').forEach((button, index) => {
            button.innerText = currentQuestion.options[Object.keys(currentQuestion.options)[index]];
            button.classList.remove('selected');
        });
        document.getElementById('result').innerText = '';
        document.getElementById('confirm-btn').disabled = true;
    } else {
        document.getElementById('question-container').style.display = 'none';
        document.getElementById('result').innerHTML = `你完成了測驗！<br>你的總分是 ${score} 分。`;
        document.getElementById('restart-btn').style.display = 'block';
    }
}

function selectAnswer(answer) {
    selectedAnswer = answer;
    document.getElementById('confirm-btn').disabled = false;
    document.querySelectorAll('.option').forEach(button => {
        button.classList.remove('selected');
        if (button.innerText.includes(answer)) {
            button.classList.add('selected');
        }
    });
}

function confirmAnswer() {
    const currentQuestion = selectedQuestions[currentQuestionIndex];
    if (selectedAnswer === currentQuestion.answer) {
        score += 2;
    }
    currentQuestionIndex++;
    showQuestion();
}

function restartQuiz() {
    startQuiz();
}



document.addEventListener('DOMContentLoaded', startQuiz);