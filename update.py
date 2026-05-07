import re

def update_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CSS changes
    css_to_add = """
        .summary-cards {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }

        .summary-cards .top-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .summary-card.balance {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white;
            text-align: center;
        }
        .summary-card.balance .summary-title,
        .summary-card.balance .summary-amount {
            color: white;
        }

        .type-toggle {
            display: flex;
            background: var(--bg-color);
            border-radius: 12px;
            padding: 5px;
            margin-bottom: 20px;
        }

        .type-btn {
            flex: 1;
            padding: 10px;
            border: none;
            background: transparent;
            border-radius: 8px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.3s;
        }

        .type-btn.active.expense {
            background: var(--danger);
            color: white;
            box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
        }

        .type-btn.active.income {
            background: var(--success);
            color: white;
            box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
        }
        
        .tx-amount.income {
            color: var(--success);
        }
"""
    # Replace old summary-cards css
    content = re.sub(
        r'\.summary-cards \{[^}]+\}',
        css_to_add.strip(),
        content,
        count=1
    )

    # 2. Dashboard HTML
    old_dashboard = """<div class="summary-cards">
                <div class="summary-card">
                    <div class="summary-title">Aaj Ka Kharcha (Today)</div>
                    <div class="summary-amount today" id="todayTotal">₹0</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Mahine Ka (Month)</div>
                    <div class="summary-amount" id="monthTotal">₹0</div>
                </div>
            </div>"""
            
    new_dashboard = """<div class="summary-cards">
                <div class="summary-card balance">
                    <div class="summary-title">Total Balance</div>
                    <div class="summary-amount" id="totalBalance">₹0</div>
                </div>
                <div class="top-row">
                    <div class="summary-card">
                        <div class="summary-title">Income (Month)</div>
                        <div class="summary-amount" id="monthIncome" style="color: var(--success);">₹0</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-title">Expense (Month)</div>
                        <div class="summary-amount" id="monthExpense" style="color: var(--danger);">₹0</div>
                    </div>
                </div>
            </div>"""
    content = content.replace(old_dashboard, new_dashboard)

    # 3. Add View HTML
    old_add = """<h2 style="margin-bottom: 20px; font-size: 1.2rem;">Kharcha Add Karein</h2>

                <div class="action-buttons">"""
    new_add = """<h2 style="margin-bottom: 20px; font-size: 1.2rem;">Transaction Add Karein</h2>

                <div class="type-toggle">
                    <button type="button" class="type-btn expense active" onclick="setTxType('expense')">Kharcha</button>
                    <button type="button" class="type-btn income" onclick="setTxType('income')">Kamai</button>
                </div>

                <div class="action-buttons">"""
    content = content.replace(old_add, new_add)
    
    # 4. Remove hardcoded options in select
    old_select = """<select id="category" class="form-control" required>
                            <option value="Food">🍔 Food & Dining</option>
                            <option value="Travel">🚗 Travel & Transport</option>
                            <option value="Shopping">🛍️ Shopping</option>
                            <option value="Bills">📱 Bills & Recharges</option>
                            <option value="Groceries">🥦 Groceries</option>
                            <option value="Health">💊 Health</option>
                            <option value="Other">✨ Other</option>
                        </select>"""
    new_select = """<select id="category" class="form-control" required></select>"""
    content = content.replace(old_select, new_select)

    # 5. Replace JS from let expenses ... to document.addEventListener
    old_js_start = """let expenses = JSON.parse(localStorage.getItem('smart_expenses')) || [];
        let pieChartInstance = null;
        let barChartInstance = null;

        const categoryColors = {
            'Food': '#f59e0b',
            'Travel': '#3b82f6',
            'Shopping': '#ec4899',
            'Bills': '#8b5cf6',
            'Groceries': '#10b981',
            'Health': '#ef4444',
            'Other': '#6b7280'
        };

        const categoryIcons = {
            'Food': 'fa-hamburger',
            'Travel': 'fa-car',
            'Shopping': 'fa-shopping-bag',
            'Bills': 'fa-file-invoice-dollar',
            'Groceries': 'fa-carrot',
            'Health': 'fa-pills',
            'Other': 'fa-star'
        };"""
        
    new_js_start = """let expenses = JSON.parse(localStorage.getItem('smart_expenses')) || [];
        let pieChartInstance = null;
        let barChartInstance = null;
        let currentTxType = 'expense';

        const expenseCategories = {
            'Food': { color: '#f59e0b', icon: 'fa-hamburger', label: '🍔 Food & Dining' },
            'Travel': { color: '#3b82f6', icon: 'fa-car', label: '🚗 Travel & Transport' },
            'Shopping': { color: '#ec4899', icon: 'fa-shopping-bag', label: '🛍️ Shopping' },
            'Bills': { color: '#8b5cf6', icon: 'fa-file-invoice-dollar', label: '📱 Bills & Recharges' },
            'Groceries': { color: '#10b981', icon: 'fa-carrot', label: '🥦 Groceries' },
            'Health': { color: '#ef4444', icon: 'fa-pills', label: '💊 Health' },
            'Other': { color: '#6b7280', icon: 'fa-star', label: '✨ Other' }
        };

        const incomeCategories = {
            'Salary': { color: '#10b981', icon: 'fa-money-bill-wave', label: '💰 Salary' },
            'Business': { color: '#3b82f6', icon: 'fa-briefcase', label: '💼 Business' },
            'Gift': { color: '#f59e0b', icon: 'fa-gift', label: '🎁 Gift' },
            'Other': { color: '#6b7280', icon: 'fa-star', label: '✨ Other' }
        };

        function getCatDetails(type, cat) {
            const map = type === 'income' ? incomeCategories : expenseCategories;
            return map[cat] || map['Other'];
        }

        function setTxType(type) {
            currentTxType = type;
            document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
            document.querySelector(`.type-btn.${type}`).classList.add('active');
            
            const catSelect = document.getElementById('category');
            const map = type === 'income' ? incomeCategories : expenseCategories;
            catSelect.innerHTML = Object.entries(map).map(([val, obj]) => `<option value="${val}">${obj.label}</option>`).join('');
        }"""
    content = content.replace(old_js_start, new_js_start)

    # 6. document.addEventListener
    old_dom = """document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('date').valueAsDate = new Date();
            initTheme();
            updateDashboard();
        });"""
    new_dom = """document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('date').valueAsDate = new Date();
            initTheme();
            setTxType('expense');
            updateDashboard();
        });"""
    content = content.replace(old_dom, new_dom)

    # 7. switchView add
    old_switch = """if (viewName === 'add') {
                if (!document.getElementById('editId').value) {
                    document.getElementById('addForm').reset();
                    document.getElementById('date').valueAsDate = new Date();
                }
            }"""
    new_switch = """if (viewName === 'add') {
                if (!document.getElementById('editId').value) {
                    document.getElementById('addForm').reset();
                    document.getElementById('date').valueAsDate = new Date();
                    setTxType('expense');
                }
            }"""
    content = content.replace(old_switch, new_switch)

    # 8. form submit
    old_submit = """const expense = {
                id: id ? id : Date.now().toString(),
                amount: parseFloat(document.getElementById('amount').value),
                category: document.getElementById('category').value,
                note: document.getElementById('note').value,
                date: document.getElementById('date').value,
                source: 'manual'
            };"""
    new_submit = """const expense = {
                id: id ? id : Date.now().toString(),
                type: currentTxType,
                amount: parseFloat(document.getElementById('amount').value),
                category: document.getElementById('category').value,
                note: document.getElementById('note').value,
                date: document.getElementById('date').value,
                source: 'manual'
            };"""
    content = content.replace(old_submit, new_submit)

    # 9. Edit Expense
    old_edit = """function editExpense(id) {
            const exp = expenses.find(e => e.id === id);
            if (exp) {
                document.getElementById('editId').value = exp.id;
                document.getElementById('amount').value = exp.amount;"""
    new_edit = """function editExpense(id) {
            const exp = expenses.find(e => e.id === id);
            if (exp) {
                document.getElementById('editId').value = exp.id;
                setTxType(exp.type || 'expense');
                document.getElementById('amount').value = exp.amount;"""
    content = content.replace(old_edit, new_edit)

    # 10. keywords & parseSmartInput
    old_keywords = """const keywords = {
            'Food': ['sabzi', 'khana', 'food', 'restaurant', 'burger', 'pizza', 'tea', 'chai', 'coffee', 'hotel', 'lunch', 'dinner'],
            'Travel': ['bus', 'train', 'auto', 'cab', 'uber', 'ola', 'petrol', 'diesel', 'ticket', 'flight', 'metro'],
            'Shopping': ['clothes', 'kapde', 'shoes', 'amazon', 'flipkart', 'mall', 'shopping', 'shirt'],
            'Bills': ['recharge', 'bill', 'electricity', 'water', 'wifi', 'internet', 'gas', 'rent'],
            'Groceries': ['kirana', 'milk', 'doodh', 'grocery', 'ration', 'fruits', 'fal'],
            'Health': ['medicine', 'dawae', 'doctor', 'hospital', 'clinic', 'pharmacy']
        };

        function parseSmartInput(text) {
            text = text.toLowerCase();
            let amount = 0;
            const amountMatch = text.match(/(?:rs\.?|₹|rupees)?\s*(\d+)\s*(?:rs\.?|rupees)?/);
            if (amountMatch) amount = parseFloat(amountMatch[1]);

            let category = 'Other';
            for (const [cat, words] of Object.entries(keywords)) {
                if (words.some(word => text.includes(word))) {
                    category = cat;
                    break;
                }
            }
            return { amount, category, note: text };
        }"""
        
    new_keywords = """const expenseKeywords = {
            'Food': ['sabzi', 'khana', 'food', 'restaurant', 'burger', 'pizza', 'tea', 'chai', 'coffee', 'hotel', 'lunch', 'dinner'],
            'Travel': ['bus', 'train', 'auto', 'cab', 'uber', 'ola', 'petrol', 'diesel', 'ticket', 'flight', 'metro'],
            'Shopping': ['clothes', 'kapde', 'shoes', 'amazon', 'flipkart', 'mall', 'shopping', 'shirt'],
            'Bills': ['recharge', 'bill', 'electricity', 'water', 'wifi', 'internet', 'gas', 'rent'],
            'Groceries': ['kirana', 'milk', 'doodh', 'grocery', 'ration', 'fruits', 'fal'],
            'Health': ['medicine', 'dawae', 'doctor', 'hospital', 'clinic', 'pharmacy']
        };

        const incomeKeywords = {
            'Salary': ['salary', 'tankha', 'paisa mila', 'received', 'kamai', 'aaya'],
            'Business': ['business', 'dukan', 'sale', 'bikri'],
            'Gift': ['gift', 'tohfa', 'shagun']
        };

        function parseSmartInput(text, type = currentTxType) {
            text = text.toLowerCase();
            let amount = 0;
            const amountMatch = text.match(/(?:rs\.?|₹|rupees)?\s*(\d+)\s*(?:rs\.?|rupees)?/);
            if (amountMatch) amount = parseFloat(amountMatch[1]);

            let category = 'Other';
            const keywords = type === 'income' ? incomeKeywords : expenseKeywords;
            for (const [cat, words] of Object.entries(keywords)) {
                if (words.some(word => text.includes(word))) {
                    category = cat;
                    break;
                }
            }
            return { amount, category, note: text };
        }"""
    content = content.replace(old_keywords, new_keywords)

    # 11. createTxHTML
    old_tx = """function createTxHTML(exp) {
            return `
                <div class="transaction-item">
                    <div class="tx-left">
                        <div class="tx-icon" style="color: ${categoryColors[exp.category] || categoryColors['Other']}; background: ${(categoryColors[exp.category] || categoryColors['Other'])}20">
                            <i class="fas ${categoryIcons[exp.category] || categoryIcons['Other']}"></i>
                        </div>
                        <div class="tx-details">
                            <span class="tx-cat">${exp.category}</span>
                            <span class="tx-date">${formatDate(exp.date)} • ${exp.note || 'No note'}</span>
                        </div>
                    </div>
                    <div class="tx-right">
                        <span class="tx-amount">₹${exp.amount}</span>
                        <div class="tx-actions">
                            <button onclick="editExpense('${exp.id}')"><i class="fas fa-edit"></i></button>
                            <button onclick="deleteExpense('${exp.id}')"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                </div>
            `;
        }"""
        
    new_tx = """function createTxHTML(exp) {
            const type = exp.type || 'expense';
            const catInfo = getCatDetails(type, exp.category);
            const amountClass = type === 'income' ? 'tx-amount income' : 'tx-amount';
            const amountSign = type === 'income' ? '+' : '-';
            
            return `
                <div class="transaction-item">
                    <div class="tx-left">
                        <div class="tx-icon" style="color: ${catInfo.color}; background: ${catInfo.color}20">
                            <i class="fas ${catInfo.icon}"></i>
                        </div>
                        <div class="tx-details">
                            <span class="tx-cat">${exp.category}</span>
                            <span class="tx-date">${formatDate(exp.date)} • ${exp.note || 'No note'}</span>
                        </div>
                    </div>
                    <div class="tx-right">
                        <span class="${amountClass}">${amountSign}₹${exp.amount}</span>
                        <div class="tx-actions">
                            <button onclick="editExpense('${exp.id}')"><i class="fas fa-edit"></i></button>
                            <button onclick="deleteExpense('${exp.id}')"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                </div>
            `;
        }"""
    content = content.replace(old_tx, new_tx)

    # 12. updateDashboard
    old_dash_func = """function updateDashboard() {
            const today = new Date().toISOString().split('T')[0];
            const currentMonth = today.substring(0, 7);

            let todaySum = 0;
            let monthSum = 0;

            const sorted = [...expenses].sort((a, b) => new Date(b.date) - new Date(a.date) || b.id - a.id);

            sorted.forEach(exp => {
                if (exp.date === today) todaySum += exp.amount;
                if (exp.date.startsWith(currentMonth)) monthSum += exp.amount;
            });

            document.getElementById('todayTotal').innerText = `₹${todaySum}`;
            document.getElementById('monthTotal').innerText = `₹${monthSum}`;

            const recentList = document.getElementById('recentList');
            if (sorted.length === 0) {
                recentList.innerHTML = `<div class="empty-state"><i class="fas fa-wallet"></i><p>No expenses yet. Start adding!</p></div>`;
            } else {
                recentList.innerHTML = sorted.slice(0, 5).map(createTxHTML).join('');
            }
        }"""
        
    new_dash_func = """function updateDashboard() {
            const today = new Date().toISOString().split('T')[0];
            const currentMonth = today.substring(0, 7);

            let balance = 0;
            let monthIncome = 0;
            let monthExpense = 0;

            const sorted = [...expenses].sort((a, b) => new Date(b.date) - new Date(a.date) || b.id - a.id);

            sorted.forEach(exp => {
                const type = exp.type || 'expense';
                if (type === 'income') {
                    balance += exp.amount;
                    if (exp.date.startsWith(currentMonth)) monthIncome += exp.amount;
                } else {
                    balance -= exp.amount;
                    if (exp.date.startsWith(currentMonth)) monthExpense += exp.amount;
                }
            });

            document.getElementById('totalBalance').innerText = `₹${balance}`;
            document.getElementById('monthIncome').innerText = `₹${monthIncome}`;
            document.getElementById('monthExpense').innerText = `₹${monthExpense}`;

            const recentList = document.getElementById('recentList');
            if (sorted.length === 0) {
                recentList.innerHTML = `<div class="empty-state"><i class="fas fa-wallet"></i><p>No transactions yet. Start adding!</p></div>`;
            } else {
                recentList.innerHTML = sorted.slice(0, 5).map(createTxHTML).join('');
            }
        }"""
    content = content.replace(old_dash_func, new_dash_func)

    # 13. generateCharts
    old_charts = """function generateCharts() {
            const isDark = document.body.getAttribute('data-theme') === 'dark';
            const textColor = isDark ? '#f9fafb' : '#1f2937';
            const gridColor = isDark ? '#374151' : '#e5e7eb';

            const catTotals = {};
            const dailyTotals = {};

            expenses.forEach(exp => {
                catTotals[exp.category] = (catTotals[exp.category] || 0) + exp.amount;
                dailyTotals[exp.date] = (dailyTotals[exp.date] || 0) + exp.amount;
            });

            const pieCtx = document.getElementById('pieChart').getContext('2d');
            if (pieChartInstance) pieChartInstance.destroy();

            const catLabels = Object.keys(catTotals);
            const catData = Object.values(catTotals);
            const catBg = catLabels.map(l => categoryColors[l] || categoryColors['Other']);

            if (catLabels.length === 0) {
                pieCtx.font = "14px Outfit";
                pieCtx.fillStyle = textColor;
                pieCtx.textAlign = "center";
                pieCtx.fillText("No data for chart", 150, 100);
            } else {
                pieChartInstance = new Chart(pieCtx, {
                    type: 'doughnut',
                    data: {
                        labels: catLabels,
                        datasets: [{ data: catData, backgroundColor: catBg, borderWidth: 0 }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { position: 'right', labels: { color: textColor, font: { family: 'Outfit' } } } },
                        cutout: '70%'
                    }
                });
            }

            const barCtx = document.getElementById('barChart').getContext('2d');
            if (barChartInstance) barChartInstance.destroy();

            const last7Days = [];
            for (let i = 6; i >= 0; i--) {
                const d = new Date();
                d.setDate(d.getDate() - i);
                last7Days.push(d.toISOString().split('T')[0]);
            }

            const barData = last7Days.map(date => dailyTotals[date] || 0);
            const barLabels = last7Days.map(date => formatDate(date));

            barChartInstance = new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: barLabels,
                    datasets: [{
                        label: 'Expense',
                        data: barData,
                        backgroundColor: '#4f46e5',
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Outfit' } } },
                        x: { grid: { display: false }, ticks: { color: textColor, font: { family: 'Outfit' } } }
                    }
                }
            });
        }"""
        
    new_charts = """function generateCharts() {
            const isDark = document.body.getAttribute('data-theme') === 'dark';
            const textColor = isDark ? '#f9fafb' : '#1f2937';
            const gridColor = isDark ? '#374151' : '#e5e7eb';

            const catTotals = {};
            const dailyExpTotals = {};
            const dailyIncTotals = {};

            expenses.forEach(exp => {
                const type = exp.type || 'expense';
                if (type === 'expense') {
                    catTotals[exp.category] = (catTotals[exp.category] || 0) + exp.amount;
                    dailyExpTotals[exp.date] = (dailyExpTotals[exp.date] || 0) + exp.amount;
                } else {
                    dailyIncTotals[exp.date] = (dailyIncTotals[exp.date] || 0) + exp.amount;
                }
            });

            const pieCtx = document.getElementById('pieChart').getContext('2d');
            if (pieChartInstance) pieChartInstance.destroy();

            const catLabels = Object.keys(catTotals);
            const catData = Object.values(catTotals);
            const catBg = catLabels.map(l => (expenseCategories[l] || expenseCategories['Other']).color);

            if (catLabels.length === 0) {
                pieCtx.font = "14px Outfit";
                pieCtx.fillStyle = textColor;
                pieCtx.textAlign = "center";
                pieCtx.fillText("No expense data", 150, 100);
            } else {
                pieChartInstance = new Chart(pieCtx, {
                    type: 'doughnut',
                    data: {
                        labels: catLabels,
                        datasets: [{ data: catData, backgroundColor: catBg, borderWidth: 0 }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { position: 'right', labels: { color: textColor, font: { family: 'Outfit' } } } },
                        cutout: '70%'
                    }
                });
            }

            const barCtx = document.getElementById('barChart').getContext('2d');
            if (barChartInstance) barChartInstance.destroy();

            const last7Days = [];
            for (let i = 6; i >= 0; i--) {
                const d = new Date();
                d.setDate(d.getDate() - i);
                last7Days.push(d.toISOString().split('T')[0]);
            }

            const expData = last7Days.map(date => dailyExpTotals[date] || 0);
            const incData = last7Days.map(date => dailyIncTotals[date] || 0);
            const barLabels = last7Days.map(date => formatDate(date));

            barChartInstance = new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: barLabels,
                    datasets: [
                        {
                            label: 'Income',
                            data: incData,
                            backgroundColor: '#10b981',
                            borderRadius: 5
                        },
                        {
                            label: 'Expense',
                            data: expData,
                            backgroundColor: '#ef4444',
                            borderRadius: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: textColor, font: { family: 'Outfit' } } } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Outfit' } } },
                        x: { grid: { display: false }, ticks: { color: textColor, font: { family: 'Outfit' } } }
                    }
                }
            });
        }"""
    content = content.replace(old_charts, new_charts)

    # 14. PDF generation
    old_pdf = """const tableData = sorted.map(exp => {
                        totalAmount += exp.amount;
                        return [
                            formatDate(exp.date),
                            exp.category,
                            exp.note || '-',
                            `Rs. ${exp.amount}`
                        ];
                    });

                    doc.autoTable({
                        startY: 35,
                        head: [['Date', 'Category', 'Note', 'Amount']],
                        body: tableData,
                        foot: [['', '', 'Total:', `Rs. ${totalAmount}`]],"""
                        
    new_pdf = """const tableData = sorted.map(exp => {
                        const type = exp.type || 'expense';
                        if (type === 'income') totalAmount += exp.amount;
                        else totalAmount -= exp.amount;
                        
                        return [
                            formatDate(exp.date),
                            type === 'income' ? 'Income' : 'Expense',
                            exp.category,
                            exp.note || '-',
                            (type === 'income' ? '+Rs. ' : '-Rs. ') + exp.amount
                        ];
                    });

                    doc.autoTable({
                        startY: 35,
                        head: [['Date', 'Type', 'Category', 'Note', 'Amount']],
                        body: tableData,
                        foot: [['', '', '', 'Balance:', `Rs. ${totalAmount}`]],"""
    content = content.replace(old_pdf, new_pdf)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_file()
