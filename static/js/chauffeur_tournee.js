// =============================================
// Charger la tournée du chauffeur connecté
// =============================================
async function loadTournee() {
    let r = await fetch("/api/chauffeur/tournee");
    let data = await r.json();

    let tbody = document.getElementById("tournee-table");
    tbody.innerHTML = "";

    if (data.tournees.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-warning fw-bold">
                    ❌ Aucune tournée prévue.
                </td>
            </tr>`;
        return;
    }

    data.tournees.forEach(t => {
        let pointsList = t.points.map(p => `(${p.lat}, ${p.lng})`).join("<br>");

        tbody.innerHTML += `
            <tr id="row-${t.id}">
                <td>${t.id}</td>
                <td>${t.vehicule}</td>
                <td>${t.date}</td>
                <td>${pointsList}</td>
                <td>
                    <button id="btn-${t.id}" class="btn btn-success btn-sm fw-bold"
                        onclick="startTournee('${t.id}')">
                        Commencer
                    </button>
                </td>
            </tr>`;
    });
}

// =============================================
// DÉBUT D’UNE TOURNÉE
// =============================================
async function startTournee(id) {

    let start = Date.now();

    // stock local sur navigateur
    localStorage.setItem("tournee_start_" + id, start);

    // Enregistrement dans XML
    await fetch("/api/tournee/start", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id_tournee: id, start })
    });

    // Update bouton
    let btn = document.getElementById("btn-" + id);
    btn.innerText = "Terminer";
    btn.classList.remove("btn-success");
    btn.classList.add("btn-danger");
    btn.setAttribute("onclick", `endTournee('${id}')`);
}

// =============================================
// FIN D’UNE TOURNÉE
// =============================================
async function endTournee(id) {

    let start = parseInt(localStorage.getItem("tournee_start_" + id));
    let end = Date.now();

    let diffMinutes = Math.round((end - start) / 60000); // 60000 ms = 1 minute


    // Enregistrement dans XML
    await fetch("/api/tournee/end", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            id_tournee: id,
            end,
            temps_total: diffMinutes
        })
    });

    alert("⏱ Temps total : " + diffMinutes + " minutes");


    // Réinitialiser bouton
    let btn = document.getElementById("btn-" + id);
    btn.innerText = "Commencer";
    btn.classList.add("btn-success");
    btn.classList.remove("btn-danger");
    btn.setAttribute("onclick", `startTournee('${id}')`);
}

loadTournee();
