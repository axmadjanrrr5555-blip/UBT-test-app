<!DOCTYPE html>
<html lang="kk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Қасым Ахмад</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #121824;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Header / Заголовок */
        header {
            width: 100%;
            padding: 30px;
            text-align: center;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border-bottom: 2px solid #3b82f6;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        header h1 {
            font-size: 2.8rem;
            letter-spacing: 3px;
            color: #60a5fa;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
        }

        .container {
            width: 90%;
            max-width: 900px;
            margin: 40px auto;
            background: #1e293b;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        /* Формалар мен кіру бөлімі */
        .login-box, .dashboard {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        h2 {
            color: #93c5fd;
            border-bottom: 2px solid #334155;
            padding-bottom: 10px;
        }

        label {
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 5px;
            display: block;
        }

        input[type="text"], input[type="password"], input[type="number"], textarea, select {
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #475569;
            background-color: #0f172a;
            color: #fff;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }

        input:focus, textarea:focus {
            border-color: #3b82f6;
        }

        button {
            padding: 12px 24px;
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s, transform 0.1s;
        }

        button:hover {
            background-color: #1d4ed8;
        }

        button:active {
            transform: scale(0.98);
        }

        .logout-btn {
            background-color: #dc2626;
            margin-top: 20px;
        }

        .logout-btn:hover {
            background-color: #b91c1c;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            background-color: #3b82f6;
            color: white;
            margin-left: 10px;
        }

        .limit-info {
            background: #0f172a;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            margin-bottom: 20px;
        }

        .question-card {
            background: #0f172a;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            border: 1px solid #334155;
        }

        .options-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 10px;
        }

        .option-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .option-item input[type="text"] {
            flex: 1;
        }

        .hidden {
            display: none !important;
        }
    </style>
</head>
<body>

    <header>
        <h1>Қасым Ахмад</h1>
    </header>

    <div class="container">
        <!-- АВТОРИЗАЦИЯ (ЖҮЙЕГЕ КІРУ) -->
        <div id="loginSection" class="login-box">
            <h2>🔑 Жүйеге кіру[span_1](start_span)[span_1](end_span)</h2>
            <div>
                <label>Логин:</label>
                <input type="text" id="username" placeholder="Логинді енгізіңіз (director немесе zam)">
            </div>
            <div>
                <label>Пароль:</label>
                <input type="password" id="password" placeholder="Парольді енгізіңіз (123)">
            </div>
            <button onclick="login()">Кіру</button>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                * Демо кіру: <br>
                Директор: логин <b>director</b> / пароль <b>123</b> <br>
                Зам: логин <b>zam</b> / пароль <b>123</b>
            </p>
        </div>

        <!-- ДИРЕКТОР КАБИНЕТІ -->
        <div id="directorDashboard" class="dashboard hidden">
            <h2>👨‍💼 Директор кабинеті <span class="badge">Басқарушы</span></h2>
            
            <!-- Лимит орнату -->
            <div class="limit-info">
                <h3>Сұрақтар лимитін орнату</h3>
                <p>Қазiргi жалпы лимит: <b id="currentLimitText">10</b> сұрақ</p>
                <p>Қосылған сұрақтар саны: <b id="addedCountText">0</b></p>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <input type="number" id="newLimitInput" placeholder="Жаңа лимит енгізіңіз" style="width: 200px;">
                    <button onclick="updateLimit()">Лимитті сақтау</button>
                </div>
            </div>

            <!-- Сұрақ құрастыру (Бір дұрыс жауапты) -->
            <h3>➕ Жаңа сұрақ қосу (Тек бір дұрыс жауапты)</h3>
            <div>
                <label>Сұрақ мәтіні:</label>
                <textarea id="singleQText" rows="3" placeholder="Сұрақты жазыңыз..."></textarea>
            </div>
            <div class="options-group">
                <label>Варианттар (Дұрыс жауапты белгілеңіз):</label>
                <div class="option-item"><input type="radio" name="singleCorrect" value="0" checked> <input type="text" class="single-opt" placeholder="А варианты"></div>
                <div class="option-item"><input type="radio" name="singleCorrect" value="1"> <input type="text" class="single-opt" placeholder="B варианты"></div>
                <div class="option-item"><input type="radio" name="singleCorrect" value="2"> <input type="text" class="single-opt" placeholder="C варианты"></div>
                <div class="option-item"><input type="radio" name="singleCorrect" value="3"> <input type="text" class="single-opt" placeholder="D варианты"></div>
            </div>
            <button onclick="addSingleQuestion()" style="margin-top: 15px;">Сұрақты сақтау</button>

            <button class="logout-btn" onclick="logout()">Шығу</button>
        </div>

        <!-- ЗАМ (ОРЫНБАСАР) КАБИНЕТІ -->
        <div id="zamDashboard" class="dashboard hidden">
            <h2>🧑‍💼 Зам (Орынбасар) кабинеті <span class="badge" style="background:#10b981;">Редактор</span></h2>
            
            <div class="limit-info">
                <h3>Директор белгілеген лимит</h3>
                <p>Рұқсат етілген сұрақ саны: <b id="zamLimitText">10</b></p>
                <p>Қазіргі қосылған сұрақтар: <b id="zamAddedCountText">0</b></p>
            </div>

            <!-- Сұрақ құрастыру (Бірнеше дұрыс жауапты) -->
            <h3>➕ Жаңа сұрақ қосу (Бірнеше дұрыс жауабы бар)</h3>
            <div>
                <label>Сұрақ мәтіні:</label>
                <textarea id="multiQText" rows="3" placeholder="Сұрақты жазыңыз..."></textarea>
            </div>
            <div class="options-group">
                <label>Варианттар (Дұрыс жауаптарды чекбокспен белгілеңіз):</label>
                <div class="option-item"><input type="checkbox" class="multi-correct" value="0"> <input type="text" class="multi-opt" placeholder="А варианты"></div>
                <div class="option-item"><input type="checkbox" class="multi-correct" value="1"> <input type="text" class="multi-opt" placeholder="B варианты"></div>
                <div class="option-item"><input type="checkbox" class="multi-correct" value="2"> <input type="text" class="multi-opt" placeholder="C варианты"></div>
                <div class="option-item"><input type="checkbox" class="multi-correct" value="3"> <input type="text" class="multi-opt" placeholder="D варианты"></div>
            </div>
            <button onclick="addMultiQuestion()" style="margin-top: 15px; background-color: #059669;">Сұрақты сақтау</button>

            <button class="logout-btn" onclick="logout()">Шығу</button>
        </div>

        <!-- ҚОСЫЛҒАН СҰРАҚТАР ТІЗІМІ -->
        <div id="questionsListSection" class="dashboard hidden" style="margin-top: 20px;">
            <h2>📋 Қосылған сұрақтар тізімі</h2>
            <div id="questionsContainer"></div>
        </div>
    </div>

    <script>
        // Деректерді сақтау
        let questionLimit = 10;
        let questions = [];

        function updateUI() {
            document.getElementById('currentLimitText').innerText = questionLimit;
            document.getElementById('zamLimitText').innerText = questionLimit;
            document.getElementById('addedCountText').innerText = questions.length;
            document.getElementById('zamAddedCountText').innerText = questions.length;

            renderQuestions();
        }

        // Жүйеге кіру
        function login() {
            const user = document.getElementById('username').value.trim();
            const pass = document.getElementById('password').value.trim();

            if (user === 'director' && pass === '123') {
                document.getElementById('loginSection').classList.add('hidden');
                document.getElementById('directorDashboard').classList.remove('hidden');
                document.getElementById('questionsListSection').classList.remove('hidden');
            } else if (user === 'zam' && pass === '123') {
                document.getElementById('loginSection').classList.add('hidden');
                document.getElementById('zamDashboard').classList.remove('hidden');
                document.getElementById('questionsListSection').classList.remove('hidden');
            } else {
                alert('Логин немесе пароль қате!');
            }
            updateUI();
        }

        // Шығу
        function logout() {
            document.getElementById('loginSection').classList.remove('hidden');
            document.getElementById('directorDashboard').classList.add('hidden');
            document.getElementById('zamDashboard').classList.add('hidden');
            document.getElementById('questionsListSection').classList.add('hidden');
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }

        // Директор лимитті өзгерту
        function updateLimit() {
            const val = parseInt(document.getElementById('newLimitInput').value);
            if (val && val > 0) {
                questionLimit = val;
                alert('Сұрақтар лимиті сақталды: ' + questionLimit);
                updateUI();
            } else {
                alert('Оң сан енгізіңіз!');
            }
        }

        // Директор: Бір жауапты сұрақ қосу
        function addSingleQuestion() {
            if (questions.length >= questionLimit) {
                alert('Лимит толды! Басқа сұрақ қоса алмайсыз.');
                return;
            }

            const qText = document.getElementById('singleQText').value.trim();
            const opts = Array.from(document.querySelectorAll('.single-opt')).map(i => i.value.trim());
            const correctRadio = document.querySelector('input[name="singleCorrect"]:checked');

            if (!qText || opts.some(o => o === '')) {
                alert('Барлық өрістерді толтырыңыз!');
                return;
            }

            questions.push({
                type: 'single',
                author: 'Директор',
                question: qText,
                options: opts,
                correct: [parseInt(correctRadio.value)]
            });

            alert('Сұрақ сәтті қосылды!');
            document.getElementById('singleQText').value = '';
            document.querySelectorAll('.single-opt').forEach(i => i.value = '');
            updateUI();
        }

        // Зам: Бірнеше жауапты сұрақ қосу
        function addMultiQuestion() {
            if (questions.length >= questionLimit) {
                alert('Директор белгілеген лимит толды! Сұрақ қосылмайды.');
                return;
            }

            const qText = document.getElementById('multiQText').value.trim();
            const opts = Array.from(document.querySelectorAll('.multi-opt')).map(i => i.value.trim());
            const correctBoxes = Array.from(document.querySelectorAll('.multi-correct:checked')).map(c => parseInt(c.value));

            if (!qText || opts.some(o => o === '')) {
                alert('Барлық өрістерді толтырыңыз!');
                return;
            }

            if (correctBoxes.length === 0) {
                alert('Кем дегенде бір дұрыс жауапты белгілеңіз!');
                return;
            }

            questions.push({
                type: 'multi',
                author: 'Орынбасар (Зам)',
                question: qText,
                options: opts,
                correct: correctBoxes
            });

            alert('Сұрақ сәтті қосылды!');
            document.getElementById('multiQText').value = '';
            document.querySelectorAll('.multi-opt').forEach(i => i.value = '');
            document.querySelectorAll('.multi-correct').forEach(c => c.checked = false);
            updateUI();
        }

        // Сұрақтарды экранға шығару
        function renderQuestions() {
            const container = document.getElementById('questionsContainer');
            container.innerHTML = '';

            if (questions.length === 0) {
                container.innerHTML = '<p style="color: #94a3b8;">Әлі ешқандай сұрақ қосылмаған.</p>';
                return;
            }

            questions.forEach((q, idx) => {
                const card = document.createElement('div');
                card.className = 'question-card';
                
                let optionsHTML = '';
                q.options.forEach((opt, oIdx) => {
                    const isCorrect = q.correct.includes(oIdx) ? ' (Дұрыс)' : '';
                    const style = q.correct.includes(oIdx) ? 'color: #4ade80; font-weight: bold;' : '';
                    optionsHTML += `<li style="${style}">${opt}${isCorrect}</li>`;
                });

                card.innerHTML = `
                    <h4>${idx + 1}. ${q.question} <span style="font-size: 0.8rem; color: #94a3b8;">(${q.author} - ${q.type === 'single' ? 'Бір жауапты' : 'Көп жауапты'})</span></h4>
                    <ul style="margin-left: 20px; margin-top: 5px;">
                        ${optionsHTML}
                    </ul>
                `;
                container.appendChild(card);
            });
        }
    </script>
</body>
</html>
