<!DOCTYPE html>
<html lang="kk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Онлайн Тест - Рейтинг</title>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --border-color: #475569;
            --highlight-bg: rgba(59, 130, 246, 0.15);
            --highlight-border: #3b82f6;
        }

        .light-theme {
            --bg-primary: #f1f5f9;
            --bg-secondary: #ffffff;
            --bg-card: #f8fafc;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --accent-color: #2563eb;
            --accent-hover: #1d4ed8;
            --border-color: #e2e8f0;
            --highlight-bg: rgba(37, 99, 235, 0.08);
            --highlight-border: #2563eb;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Styles */
        .sidebar {
            width: 280px;
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            padding: 24px 16px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            flex-shrink: 0;
        }

        .user-stats-card {
            background-color: var(--bg-primary);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid var(--border-color);
        }

        .level-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 12px;
        }

        .xp-bar-container {
            width: 100%;
            height: 8px;
            background-color: var(--border-color);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 6px;
        }

        .xp-bar-fill {
            height: 100%;
            background-color: #eab308;
            width: 0%;
            border-radius: 4px;
            transition: width 0.5s ease-out;
        }

        .xp-text {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 16px;
        }

        .stat-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95rem;
            margin-top: 8px;
        }

        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex-grow: 1;
        }

        .menu-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            color: var(--text-secondary);
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            cursor: pointer;
            font-weight: 500;
        }

        .nav-item:hover {
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        .nav-item.active {
            background-color: var(--accent-color);
            color: white;
        }

        .theme-btn {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-weight: 600;
        }

        /* Main Content Styles */
        .main-content {
            flex-grow: 1;
            padding: 32px;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-y: auto;
        }

        .header {
            width: 100%;
            max-width: 900px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }

        .header h1 {
            font-size: 1.8rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .leaderboard-container {
            width: 100%;
            max-width: 900px;
            background-color: var(--bg-secondary);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }

        .table-responsive {
            width: 100%;
            overflow-x: auto;
        }

        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        .leaderboard-table th {
            background-color: var(--bg-card);
            padding: 16px 20px;
            font-size: 0.85rem;
            text-transform: uppercase;
            color: var(--text-secondary);
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--border-color);
        }

        .leaderboard-table td {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.95rem;
        }

        .leaderboard-table tr:last-child td {
            border-bottom: none;
        }

        .rank-cell {
            font-weight: bold;
            font-size: 1.1rem;
            width: 80px;
        }

        .user-cell {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: var(--accent-color);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9rem;
        }

        .badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        .badge-level {
            background-color: rgba(34, 197, 94, 0.15);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }

        /* Top Ranks Styling */
        .rank-1 { color: #eab308; }
        .rank-2 { color: #94a3b8; }
        .rank-3 { color: #d97706; }

        .row-current-user {
            background-color: var(--highlight-bg) !important;
            border-left: 4px solid var(--highlight-border);
        }

        .current-tag {
            font-size: 0.75rem;
            background-color: var(--accent-color);
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 6px;
        }

        @media (max-width: 768px) {
            body {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
            }
            .main-content {
                padding: 16px;
            }
        }
    </style>
</head>
<body>

    <!-- Сол жақ айналмалы мәзір -->
    <aside class="sidebar">
        <div class="user-stats-card">
            <div class="level-badge">
                ⭐ <span id="sidebar-level">Level 1</span>
            </div>
            <div class="xp-bar-container">
                <div class="xp-bar-fill" id="sidebar-xp-bar"></div>
            </div>
            <div class="xp-text">
                <span id="sidebar-xp">0</span> / 500 XP
            </div>

            <div class="stat-item">
                🔥 Streak: <strong id="sidebar-streak" style="margin-left: auto;">0 күн</strong>
            </div>
            <div class="stat-item">
                🎯 Күндік мақсат: <strong id="sidebar-target" style="margin-left: auto;">0/50</strong>
            </div>
        </div>

        <nav class="nav-menu">
            <div class="menu-title">Мәзір:</div>
            <a href="#" class="nav-item">🏠 Басты бет</a>
            <a href="#" class="nav-item">📝 Тест тапсыру</a>
            <a href="#" class="nav-item">🎈 Қателерім</a>
            <a href="#" class="nav-item">📊 Статистика</a>
            <a href="#" class="nav-item active">🏆 Рейтинг</a>
        </nav>

        <button class="theme-btn" id="theme-toggle-btn">
            🌙 Dark Mode
        </button>
    </aside>

    <!-- Негізгі бөлім (Рейтинг) -->
    <main class="main-content">
        <div class="header">
            <h1>🏆 ONLINE TEST рейтингі</h1>
        </div>

        <div class="leaderboard-container">
            <div class="table-responsive">
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th>Орын</th>
                            <th>Қолданушы</th>
                            <th>Деңгей</th>
                            <th>Ұпай (XP)</th>
                            <th>Streak</th>
                        </tr>
                    </thead>
                    <tbody id="leaderboard-body">
                        <!-- Деректер JS арқылы динамикалық түрде салынады -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        // Қолданушылар базасы (Мысал ретінде)
        const usersData = [
            { id: 1, name: "Арман Қайратов", xp: 1450, level: 3, streak: 15, isCurrent: false },
            { id: 2, name: "Айша Серікқызы", xp: 1200, level: 3, streak: 9, isCurrent: false },
            { id: 3, name: "Нұрсұлтан Ә.", xp: 850, level: 2, streak: 5, isCurrent: false },
            { id: 4, name: "Сіз (Ағымдағы қолданушы)", xp: 320, level: 1, streak: 3, isCurrent: true },
            { id: 5, name: "Динара М.", xp: 210, level: 1, streak: 2, isCurrent: false },
            { id: 6, name: "Бекзат Тұрсын", xp: 90, level: 1, streak: 1, isCurrent: false }
        ];

        // Экранды және деректерді жүктеу
        function renderLeaderboard() {
            // Қолданушыларды XP бойынша сұрыптау (Үлкеннен кішіге)
            usersData.sort((a, b) => b.xp - a.xp);

            const tbody = document.getElementById('leaderboard-body');
            tbody.innerHTML = '';

            usersData.forEach((user, index) => {
                const rank = index + 1;
                const tr = document.createElement('tr');
                
                if (user.isCurrent) {
                    tr.classList.add('row-current-user');
                    // Sidebar көрсеткіштерін жаңарту
                    document.getElementById('sidebar-level').textContent = `Level ${user.level}`;
                    document.getElementById('sidebar-xp').textContent = user.xp;
                    document.getElementById('sidebar-streak').textContent = `${user.streak} күн`;
                    document.getElementById('sidebar-target').textContent = `${Math.min(user.xp, 50)}/50`;
                    
                    const xpPercent = Math.min((user.xp / 500) * 100, 100);
                    document.getElementById('sidebar-xp-bar').style.width = `${xpPercent}%`;
                }

                // Орын медальдарын белгілеу
                let rankDisplay = rank;
                let rankClass = '';
                if (rank === 1) { rankDisplay = '🥇 1'; rankClass = 'rank-1'; }
                else if (rank === 2) { rankDisplay = '🥈 2'; rankClass = 'rank-2'; }
                else if (rank === 3) { rankDisplay = '🥉 3'; rankClass = 'rank-3'; }

                // Инициалдар дайындау (Аватар үшін)
                const initials = user.name.split(' ').map(n => n[0]).join('').substring(0, 2);

                tr.innerHTML = `
                    <td class="rank-cell ${rankClass}">${rankDisplay}</td>
                    <td>
                        <div class="user-cell">
                            <div class="avatar">${initials}</div>
                            <div>
                                ${user.name}
                                ${user.isCurrent ? '<span class="current-tag">Сіз</span>' : ''}
                            </div>
                        </div>
                    </td>
                    <td><span class="badge badge-level">Level ${user.level}</span></td>
                    <td><strong>${user.xp}</strong> XP</td>
                    <td>🔥 ${user.streak} күн</td>
                `;

                tbody.appendChild(tr);
            });
        }

        // Түнгі/Күндізгі режимді ауыстыру
        const themeBtn = document.getElementById('theme-toggle-btn');
        themeBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            if (document.body.classList.contains('light-theme')) {
                themeBtn.innerHTML = '☀️ Light Mode';
            } else {
                themeBtn.innerHTML = '🌙 Dark Mode';
            }
        });

        // Іске қосу
        renderLeaderboard();
    </script>
</body>
</html>
