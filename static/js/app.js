
let chart;

const $ = id => document.getElementById(id);

const money = n => Number(n).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

const formatINR = n => '₹' + money(n);

function normalizeTicker(ticker) {
    ticker = ticker.toUpperCase().trim();
    if (ticker && !ticker.includes('.')) {
        ticker += '.NS';
    }
    return ticker;
}

async function loadTicker(ticker) {
    ticker = normalizeTicker(ticker);
    if (!ticker) return;

    $('ticker-input').value = ticker;
    $('order-ticker').value = ticker;
    $('chart-title').textContent = ticker + ' performance';
    $('quote-details').textContent = 'Loading quote…';

    try {
        const [qRes, hRes, aRes] = await Promise.all([
            fetch('/api/quote/' + encodeURIComponent(ticker)),
            fetch('/api/history/' + encodeURIComponent(ticker) +
                '?period=' + $('period').value),
            fetch('/api/analysis/' + encodeURIComponent(ticker))
        ]);

        const q = await qRes.json();
        const rows = await hRes.json();
        const a = await aRes.json();

        if (q.error) throw new Error(q.error);

        $('hero-price').textContent = formatINR(q.price);
        $('hero-change').textContent =
            (q.change_pct >= 0 ? '+' : '') + q.change_pct + '% today';

        $('metric-price').textContent = formatINR(q.price);
        $('metric-change').textContent =
            (q.change_pct >= 0 ? '+' : '') + q.change_pct + '%';

        $('metric-change').style.color =
            q.change_pct >= 0 ? '#15966b' : '#d34c5a';

        $('metric-sma5').textContent =
            a.sma_5 != null ? formatINR(a.sma_5) : '—';

        $('metric-sma20').textContent =
            a.sma_20 != null ? formatINR(a.sma_20) : '—';

        $('quote-details').innerHTML =
            '<b>' + q.ticker + '</b><br>' +
            'Price: <b>' + formatINR(q.price) + '</b><br>' +
            'Daily move: <b>' + q.change_pct + '%</b><br>' +
            'Currency: INR<br>' +
            'Data source: ' + q.source;

        $('source-note').textContent =
            'Source: ' + q.source + ' · ' + q.as_of;

        $('analysis-note').textContent =
            a.note || 'Historical descriptive indicators.';

        const ctx = $('priceChart').getContext('2d');

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: rows.map(x => x.date),
                datasets: [{
                    label: ticker + ' close (INR)',
                    data: rows.map(x => x.close),
                    borderColor: '#4267ef',
                    backgroundColor: 'rgba(66,103,239,.10)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        ticks: { maxTicksLimit: 7, color: '#8a94a7' },
                        grid: { display: false }
                    },
                    y: {
                        ticks: {
                            color: '#8a94a7',
                            callback: value => '₹' + value
                        },
                        grid: { color: '#edf0f5' }
                    }
                }
            }
        });

        $('order-message').textContent = '';

    } catch (e) {
        $('quote-details').textContent = e.message;
        $('source-note').textContent = 'Market data unavailable.';
    }
}

$('ticker-form').addEventListener('submit', e => {
    e.preventDefault();
    loadTicker($('ticker-input').value);
});

$('period').addEventListener('change', () => {
    loadTicker($('ticker-input').value);
});

$('order-form').addEventListener('submit', async e => {
    e.preventDefault();

    const ticker = normalizeTicker($('order-ticker').value);

    try {
        const quoteResponse = await fetch(
            '/api/quote/' + encodeURIComponent(ticker)
        );

        const q = await quoteResponse.json();

        if (q.error) throw new Error(q.error);

        const body = {
            ticker: q.ticker,
            side: $('order-side').value,
            quantity: Number($('order-qty').value),
            price: q.price
        };

        const res = await fetch('/api/portfolio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        const result = await res.json();

        $('order-message').textContent =
            result.error || result.message;

        refreshPortfolio();

    } catch (e) {
        $('order-message').textContent = e.message;
    }
});

async function refreshPortfolio() {
    try {
        const response = await fetch('/api/portfolio');
        const p = await response.json();

        $('portfolio').innerHTML =
            '<b>Paper cash:</b> ' + formatINR(p.cash) +
            ' &nbsp; <b>Positions:</b> ' +
            (Object.keys(p.positions).length
                ? Object.entries(p.positions)
                    .map(([k, v]) => k + ': ' + v).join(', ')
                : 'None');

    } catch (e) {
        $('portfolio').textContent = 'Portfolio unavailable.';
    }
}

loadTicker('RELIANCE.NS');
refreshPortfolio();
