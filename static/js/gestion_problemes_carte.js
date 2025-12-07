async function loadProblemes() {
    let r = await fetch("/api/problemes_carte");
    let data = await r.json();

    let tbody = document.getElementById("problemes-table");
    tbody.innerHTML = "";

    data.problemes.forEach(p => {

        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.type}</td>
                <td>${p.description}</td>
                <td>${p.date}</td>
                <td>${p.status}</td>

                <td>
                    <button class="btn btn-primary btn-sm w-100 mb-1"
                        onclick="appelTechnicien('${p.id}')">
                        📞 Appeler technicien
                    </button>

                    <button class="btn btn-danger btn-sm w-100"
                        onclick="envoyerAdmin('${p.id}')">
                        📨 Envoyer à l'admin
                    </button>
                </td>
            </tr>
        `;
    });
}

async function appelTechnicien(id) {
    await fetch("/api/probleme_carte/technicien", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    });
    loadProblemes();
}

async function envoyerAdmin(id) {
    await fetch("/api/probleme_carte/admin", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id })
    });
    loadProblemes();
}

document.addEventListener("DOMContentLoaded", loadProblemes);
