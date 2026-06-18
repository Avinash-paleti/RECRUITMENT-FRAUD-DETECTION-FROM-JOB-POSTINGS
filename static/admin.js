fetch("/admin/stats")
  .then(res => res.json())
  .then(data => {
    const total   = data.total   || 0;
    const frauds  = data.frauds  || 0;
    const genuine = data.genuine || 0;

    // ── Stat counters (animated count-up) ──
    countUp("total",   total);
    countUp("frauds",  frauds);
    countUp("genuine", genuine);

    // ── Accuracy bars ──
    if (total > 0) {
      const fp = Math.round((frauds  / total) * 100);
      const gp = Math.round((genuine / total) * 100);
      setTimeout(() => {
        document.getElementById("fraud-bar").style.width    = fp + "%";
        document.getElementById("genuine-bar").style.width  = gp + "%";
        document.getElementById("fraud-pct").textContent   = fp + "%";
        document.getElementById("genuine-pct").textContent = gp + "%";
      }, 300);
    }

    // ── Donut chart ──
    const ctx = document.getElementById("donutChart").getContext("2d");
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Fraudulent", "Genuine"],
        datasets: [{
          data: [frauds, genuine],
          backgroundColor: ["#dc2626", "#16a34a"],
          borderColor: ["#fff", "#fff"],
          borderWidth: 3,
          hoverOffset: 6
        }]
      },
      options: {
        cutout: "72%",
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.label}: ${ctx.raw} (${total > 0 ? Math.round(ctx.raw/total*100) : 0}%)`
            }
          }
        }
      }
    });

    // ── Custom legend ──
    const legend = document.getElementById("chart-legend");
    const items = [
      { label: "Fraudulent", color: "#dc2626", value: frauds },
      { label: "Genuine",    color: "#16a34a", value: genuine }
    ];
    items.forEach(item => {
      legend.innerHTML += `
        <div style="display:flex;align-items:center;gap:6px;">
          <div style="width:10px;height:10px;border-radius:3px;background:${item.color};"></div>
          <span style="color:#64748b;font-weight:500;">${item.label}</span>
          <span style="color:${item.color};">${item.value}</span>
        </div>`;
    });
  })
  .catch(err => console.error("Stats fetch failed:", err));


// ── Utility: animated count-up ──
function countUp(id, target) {
  const el = document.getElementById(id);
  if (!el || target === 0) { if (el) el.textContent = "0"; return; }
  let current = 0;
  const step  = Math.max(1, Math.ceil(target / 40));
  const timer = setInterval(() => {
    current += step;
    if (current >= target) { el.textContent = target; clearInterval(timer); }
    else                    { el.textContent = current; }
  }, 30);
}