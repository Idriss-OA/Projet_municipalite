async function loadRapport() {
    let r = await fetch("/api/chauffeur/rapport");
    let data = await r.json();

    let tbody = document.getElementById("rapport-table");
    tbody.innerHTML = "";

    if (data.rapport.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="3" class="text-center text-warning fw-bold">
                    ❌ Aucun rapport enregistré.
                </td>
            </tr>`;
        return;
    }

    data.rapport.forEach(rec => {
        tbody.innerHTML += `
            <tr>
                <td>${rec.id_tournee}</td>
                <td>${rec.chauffeur}</td>
                <td>${rec.temps_total} minutes</td>

            </tr>`;
    });
}

loadRapport();
