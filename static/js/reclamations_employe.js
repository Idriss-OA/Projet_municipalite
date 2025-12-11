async function loadRecs() {
    let r = await fetch("/api/reclamations");
    let data = await r.json();

    let tbody = document.querySelector("#recEmpTable tbody");
    tbody.innerHTML = "";

    data.reclamations.forEach((rec, index) => {
        tbody.innerHTML += `
            <tr>
                <td>${rec.type}</td>
                <td>${rec.cin}</td>
                <td>${rec.date}</td>
                <td>${rec.motif}</td>
                <td><span class="badge bg-info">${rec.status}</span></td>

                <td>
                    <button class="btn btn-success btn-action" onclick="approve(${index})">✔ Approuver</button>
                    <button class="btn btn-danger btn-action" onclick="reject(${index})">✖ Refuser</button>
                    <button class="btn btn-primary btn-action" onclick="sendAdmin(${index})">📤 Envoyer Admin</button>
                    <button class="btn btn-warning btn-action" onclick="callTech(${index})">🛠 Technicien</button>
                </td>
            </tr>
        `;
    });
}

loadRecs();


async function approve(id) {
    await updateRec(id, "approuve");
}

async function reject(id) {
    await updateRec(id, "refuse");
}

async function sendAdmin(id) {
    await updateRec(id, "admin");
}

async function callTech(id) {
    await updateRec(id, "technicien");
}

async function updateRec(id, status) {
    let r = await fetch("/api/reclamations/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, status })
    });

    let data = await r.json();

    if (data.status === "ok") {
        alert("Statut mis à jour !");
        loadRecs();
    }
}
