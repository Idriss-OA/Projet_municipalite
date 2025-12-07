// =======================
// CHARGER CHAUFFEURS
// =======================
async function loadChauffeurs() {
    let r = await fetch("/api/chauffeurs");
    let data = await r.json();

    let select = document.getElementById("chauffeur");
    if (!select) return;

    select.innerHTML = "<option value=''>-- Sélectionner un chauffeur --</option>";

    data.chauffeurs.forEach(c => {
        select.innerHTML += `
            <option value="${c.cin}">
                ${c.nom} ${c.prenom} — ${c.cin}
            </option>
        `;
    });
}

// =======================
// CHARGER VEHICULES
// =======================
async function loadVehicules() {
    let r = await fetch("/api/vehicules");
    let data = await r.json();

    let select = document.getElementById("vehicule");
    if (!select) return;

    select.innerHTML = "<option value=''>-- Sélectionner un véhicule --</option>";

    data.vehicules.forEach(v => {
        select.innerHTML += `
            <option value="${v.matricule}">
                ${v.matricule} — ${v.marque}
            </option>
        `;
    });
}

// =======================
// CHARGER POINTS
// =======================
async function loadPoints() {
    let r = await fetch("/api/points");
    let data = await r.json();

    let select = document.getElementById("points");
    if (!select) return;

    select.innerHTML = "";

    data.points.forEach(p => {
        select.innerHTML += `
            <option value="${p.lat},${p.lng}">
                ${p.type} — ${p.lat}, ${p.lng}
            </option>
        `;
    });
}


// =======================
// CRÉER UNE TOURNÉE
// =======================
async function creerTournee() {
    let chauffeur = document.getElementById("chauffeur").value;
    let vehicule = document.getElementById("vehicule").value;
    let date = document.getElementById("date").value;

    let ptsSelect = document.getElementById("points");
    let selectedPoints = [...ptsSelect.selectedOptions].map(o => {
        let c = o.value.split(",");
        return { lat: c[0], lng: c[1] };
    });

    let msg = document.getElementById("msg");

    if (!chauffeur || !vehicule || !date || selectedPoints.length === 0) {
        msg.innerHTML = `<span class="text-danger fw-bold">⚠ Veuillez remplir tous les champs !</span>`;
        return;
    }

    let response = await fetch("/api/create_tournee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            chauffeur,
            vehicule,
            date,
            points: selectedPoints
        })
    });

    let data = await response.json();

    if (data.status === "busy") {
        msg.innerHTML = `<span class="text-danger fw-bold">${data.msg}</span>`;
    }
    else if (data.status === "ok") {
        msg.innerHTML = `<span class="text-success fw-bold">${data.msg}</span>`;
        setTimeout(() => window.location.reload(), 1000);
    }
    else {
        msg.innerHTML = `<span class="text-danger fw-bold">❌ Erreur inconnue</span>`;
    }
}


// ===================================================================
//         🔥 🔥 🔥  GESTION DE LA LISTE DES TOURNEES  🔥 🔥 🔥
// ===================================================================


// =======================
// CHARGER TOUTES LES TOURNEES
// =======================
async function loadTournees() {
    let r = await fetch("/api/tournees");
    let data = await r.json();

    let tbody = document.getElementById("tournees-table");
    if (!tbody) return;

    tbody.innerHTML = "";

    data.tournees.forEach(t => {
        let points = t.points.map(p => `(${p.lat}, ${p.lng})`).join("<br>");

        tbody.innerHTML += `
            <tr id="row-${t.id}">
                <td>${t.id}</td>
                <td contenteditable="true">${t.chauffeur}</td>
                <td contenteditable="true">${t.vehicule}</td>
                <td contenteditable="true">${t.date}</td>
                <td>${points}</td>

                <td>
                    <button class="btn btn-primary btn-sm w-100 mb-1"
                        onclick="saveEdit('${t.id}')">💾 Enregistrer</button>

                    <button class="btn btn-danger btn-sm w-100"
                        onclick="deleteTournee('${t.id}')">🗑 Supprimer</button>
                </td>
            </tr>
        `;
    });
}


// =======================
// SUPPRESSION (SweetAlert)
// =======================
async function deleteTournee(id) {

    Swal.fire({
        title: "Supprimer cette tournée ?",
        text: "Cette action est irréversible.",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: "Annuler",
        confirmButtonText: "Oui, supprimer",
        confirmButtonColor: "#d33"
    }).then(async (result) => {

        if (result.isConfirmed) {

            let r = await fetch("/api/delete_tournee", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ id })
            });

            let data = await r.json();

            if (data.status === "ok") {

                Swal.fire({
                    icon: "success",
                    title: "Supprimée !",
                    timer: 1500,
                    showConfirmButton: false
                });

                loadTournees();
            }
        }
    });
}


// =======================
// SAUVEGARDE MODIFICATION INLINE
// =======================
async function saveEdit(id) {
    let row = document.getElementById("row-" + id);

    let chauffeur = row.children[1].innerText.trim();
    let vehicule = row.children[2].innerText.trim();
    let date = row.children[3].innerText.trim();

    let r = await fetch("/api/update_tournee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, chauffeur, vehicule, date })
    });

    let data = await r.json();

    Swal.fire({
        icon: "success",
        title: "Modifications enregistrées !",
        timer: 1500,
        showConfirmButton: false
    });
}


// =======================
// AUTO-LAUNCH AU CHARGEMENT
// =======================
document.addEventListener("DOMContentLoaded", () => {
    loadChauffeurs();
    loadVehicules();
    loadPoints();
    loadTournees();
});

// =======================
// SELECT MULTIPLE SANS CTRL
// =======================
document.addEventListener("mousedown", function(e) {
    if (e.target.tagName === 'OPTION' && e.target.parentElement.multiple) {
        e.preventDefault();
        e.target.selected = !e.target.selected;
        return false;
    }
});
