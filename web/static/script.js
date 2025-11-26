async function send() {
    const payload = {
        user_name: document.getElementById("user_name").value,
        partner_name: document.getElementById("partner_name").value,
        context: document.getElementById("context").value,
        chat_logs: document.getElementById("chat_logs").value,
    };

    const r = await fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await r.json();

    // 顯示報告
    document.getElementById("output").textContent = data.report;

    // 設定下載按鈕
    if (data.download_url) {
        const btn = document.getElementById("downloadBtn");
        btn.href = data.download_url;
        btn.style.display = "block";
    }
}
