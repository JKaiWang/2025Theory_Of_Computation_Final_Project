async function send() {

    document.getElementById("loadingModal").style.display = "flex";

    const payload = {
        user_name: document.getElementById("user_name").value,
        partner_name: document.getElementById("partner_name").value,
        context: document.getElementById("context").value,
        chat_logs: document.getElementById("chat_logs").value,
    };

    // Show status and disable controls while analyzing
    const statusEl = document.getElementById("status");
    statusEl.textContent = "Analyzing... Please wait.";
    const buttons = document.querySelectorAll('button');
    buttons.forEach(b => b.disabled = true);

    const r = await fetch("/analyze", {
        method: "POST",
        cache: "no-store",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    try {
        const data = await r.json();

        // 修正: 使用 marked.parse() 將 Markdown 轉為 HTML，並用 innerHTML 寫入
        if (typeof marked !== 'undefined') {
            document.getElementById("output").innerHTML = marked.parse(data.report);
        } else {
            // 如果 marked 沒載入成功，則退回純文字顯示
            document.getElementById("output").textContent = data.report;
        }

        // show download link if available
        if (data.download_url) {
            const btn = document.getElementById("downloadBtn");
            btn.href = data.download_url;
            btn.style.display = "block";
        }

        statusEl.textContent = "Analysis complete.";
    } catch (err) {
        statusEl.textContent = "An error occurred while processing the analysis.";
        console.error(err);
    } finally {
        // 修正: 無論結果如何，隱藏載入畫面
        document.getElementById("loadingModal").style.display = "none"; 
        // 重新啟用按鈕
        buttons.forEach(b => b.disabled = false);
    }
}


async function saveChat() {
    const payload = {
        user_name: document.getElementById("user_name").value,
        partner_name: document.getElementById("partner_name").value,
        context: document.getElementById("context").value,
            // Split chat_logs by line for appending
            chat_logs: document.getElementById("chat_logs").value.split("\n").map(s => s.trim()).filter(s => s.length > 0),
    };

    // disable buttons while saving
    const statusEl = document.getElementById("status");
    statusEl.textContent = "Saving chat...";
    const buttons = document.querySelectorAll('button');
    buttons.forEach(b => b.disabled = true);

    try {
        const r = await fetch("/save_history", {
            method: "POST",
            cache: "no-store",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await r.json();

        if (data.download_url) {
            const btn = document.getElementById("downloadChatBtn");
            btn.href = data.download_url;
            btn.style.display = "block";
        }

        if (data.error) {
            alert("Save failed: " + data.error);
            statusEl.textContent = "Save failed.";
        } else {
            statusEl.textContent = "Chat saved.";
        }
    } catch (err) {
        alert("Save failed: " + err);
        statusEl.textContent = "Save failed.";
        console.error(err);
    } finally {
        buttons.forEach(b => b.disabled = false);
    }
    // Load chat history from a JSON file and populate the form
    document.getElementById('loadChatFile').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(evt) {
            try {
                const data = JSON.parse(evt.target.result);
                document.getElementById("user_name").value = data.user_name || "";
                document.getElementById("partner_name").value = data.partner_name || "";
                document.getElementById("context").value = data.context || "";
                // If chat_logs is array, join with newlines; if string, use as is
                if (Array.isArray(data.chat_logs)) {
                    document.getElementById("chat_logs").value = data.chat_logs.join("\n");
                } else {
                    document.getElementById("chat_logs").value = data.chat_logs || "";
                }
                document.getElementById("status").textContent = "Chat history loaded.";
            } catch (err) {
                document.getElementById("status").textContent = "Failed to load chat history.";
                console.error(err);
            }
        };
        reader.readAsText(file);
    });
}