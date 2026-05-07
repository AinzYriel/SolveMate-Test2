lucide.createIcons();
    let currentFormula = null;

    function toggleTheme() {
        const html = document.documentElement;
        const icon = document.getElementById('theme-icon');
        if (html.getAttribute('data-theme') === 'light') {
            html.setAttribute('data-theme', 'dark');
            icon.setAttribute('data-lucide', 'sun');
        } else {
            html.setAttribute('data-theme', 'light');
            icon.setAttribute('data-lucide', 'moon');
        }
        lucide.createIcons();
    }

    function formatNumber(num) {
        if (Math.abs(num) < 0.001 || Math.abs(num) > 10000) {
            return num.toExponential(3);
        }
        return num.toFixed(4);
    }

    function filterCategory(cat) {
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
        event.currentTarget.classList.add('active');

        document.querySelectorAll('.category-sec').forEach(sec => {
            sec.style.display = (cat === 'all' || sec.dataset.category === cat) ? 'block' : 'none';
        });
    }

    function handleSearch() {
        const q = document.getElementById('formulaSearch').value.toLowerCase();
        document.querySelectorAll('.card').forEach(card => {
            const match = card.dataset.title.toLowerCase().includes(q);
            card.style.display = match ? 'flex' : 'none';
        });
    }

    function openSolver(id) {
        fetch(`/api/formula/${id}`).then(r => r.json()).then(f => {
            currentFormula = f;
            document.getElementById('m-title').innerText = f.title;
            const container = document.getElementById('m-inputs');
            container.innerHTML = f.vars.map(v => `
                <div class="input-group">
                    <label style="font-size: 0.8rem; font-weight: 600;">${v.label} (${v.symbol})</label>
                    <div class="input-row">
                        <input type="number" id="v_${v.name}" placeholder="Value" step="any">
                        <select id="u_${v.name}">
                            ${v.units.map(unit => `<option value="${unit}">${unit}</option>`).join('')}
                        </select>
                    </div>
                </div>
            `).join('');

            document.getElementById('solution-area').style.display = 'none';
            document.getElementById('solverModal').style.display = 'flex';
            validateForm();
        });
    }

    function closeModal() {
        document.getElementById('solverModal').style.display = 'none';
    }

    function validateForm() {
        const inputs = Array.from(document.querySelectorAll('#m-inputs input'));
        const empty = inputs.filter(i => i.value === "");
        const btn = document.getElementById('m-calc-btn');
        btn.disabled = empty.length !== 1;
        if(empty.length === 1) {
            btn.innerText = `Solve for ${empty[0].parentElement.previousElementSibling.innerText}`;
        } else {
            btn.innerText = "Fill all but one";
        }
    }

    let lastCalculationData = null; // Store for explain button

function performCalculation() {
    const payload = { fid: currentFormula.id, vals: {}, units: {} };
    currentFormula.vars.forEach(v => {
        payload.vals[v.name] = document.getElementById(`v_${v.name}`).value;
        payload.units[v.name] = document.getElementById(`u_${v.name}`).value;
    });

    // Show loading
    document.getElementById('m-calc-btn').innerText = 'Calculating...';
    document.getElementById('m-calc-btn').disabled = true;

    fetch('/api/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        lastCalculationData = payload; // Store for explain
        const area = document.getElementById('solution-area');
        area.style.display = 'block';

        document.getElementById('steps-container').innerHTML = data.steps.map(s => `<div class="step">${s}</div>`).join('');
        document.getElementById('final-res').innerHTML = `Result: ${data.res_formatted || formatNumber(data.res)} ${data.unit}`;

        // NEW: Show Explain button
        document.getElementById('explain-btn').style.display = 'block';

        if (data.error) {
            document.getElementById('final-res').innerHTML = `<span style="color: #ef4444;">Error: ${data.error}</span>`;
            document.getElementById('explain-btn').style.display = 'none';
        }
    })
    .catch(err => {
        console.error('Calc error:', err);
    })
    .finally(() => {
        document.getElementById('m-calc-btn').innerText = 'Solve Formula';
        document.getElementById('m-calc-btn').disabled = false;
    });
}

// NEW: Explain button handler
// FIXED: Explain button handler
function showExplanation() {
    if (!lastCalculationData) return;

    document.getElementById('explain-btn').innerText = 'Loading explanation...';
    document.getElementById('explain-btn').disabled = true;

    fetch('/api/explain', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(lastCalculationData)
    })
    .then(r => r.json())
    .then(data => {
        // FIXED: Use data.steps (not data.explanation) + add tutor explanation
        const explanationContent = document.getElementById('explanation-content');
        
        // Show detailed steps first
        explanationContent.innerHTML = `
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <h5 style="margin: 0 0 10px 0; color: var(--primary);">📋 Detailed Steps:</h5>
                ${data.steps.map(s => `<div style="margin-bottom: 8px;">${s}</div>`).join('')}
            </div>
        `;
        
        // Add tutor explanation using utils function (via backend)
        if (data.tutor_explanation) {
            explanationContent.innerHTML += `
                <div style="background: rgba(16,185,129,0.1); padding: 1rem; border-radius: 8px;">
                    <h5 style="margin: 0 0 10px 0; color: var(--secondary);">🎓 Physics Insight:</h5>
                    ${data.tutor_explanation.map(e => `<div style="margin-bottom: 6px;">${e}</div>`).join('')}
                </div>
            `;
        }
        
        document.getElementById('explanation-panel').style.display = 'block';
        document.getElementById('explanation-content').scrollIntoView({ behavior: 'smooth' });
    })
    .catch(err => {
        console.error('Explain error:', err);
        document.getElementById('explanation-content').innerHTML = '<div style="color: #ef4444;">Error loading explanation</div>';
    })
    .finally(() => {
        document.getElementById('explain-btn').innerText = '📚 Explain in Detail';
        document.getElementById('explain-btn').disabled = false;
    });
}

// NEW: Toggle explanation panel
function toggleExplanation() {
    const panel = document.getElementById('explanation-panel');
    const btn = document.querySelector('#explanation-panel button');
    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        btn.textContent = '+';
    } else {
        panel.style.display = 'block';
        btn.textContent = '−';
    }
}
