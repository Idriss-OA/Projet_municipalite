// Charger liste chauffeurs au démarrage
chargerChauffeurs();

// =======================
// 🔹 Charger Chauffeurs
// =======================
function chargerChauffeurs() {
    fetch("/api/chauffeurs")
        .then(r => r.json())
        .then(data => {
            let tbody = document.getElementById("tbody-chauffeurs");
            tbody.innerHTML = "";

            data.chauffeurs.forEach(ch => {
                tbody.innerHTML += ligneChauffeur(ch);
            });
        });
}

// =======================
// 🔹 Template d’une ligne chauffeur
// =======================
function ligneChauffeur(ch) {
    return `
        <tr id="row-${ch.cin}">
            <td>${ch.cin}</td>
            <td>${ch.nom}</td>
            <td>${ch.prenom}</td>
            <td>${ch.email}</td>
            <td>${ch.adresse}</td>
            <td>${ch.telephone}</td>
            <td>${ch.poste}</td>
            <td>${ch.salaire} DT</td>
            <td>
                <button class="btn-action btn-edit" onclick="modifierChauffeur('${ch.cin}')">Modifier</button>
                <button class="btn-action btn-delete" onclick="supprimerChauffeur('${ch.cin}')">Supprimer</button>
            </td>
        </tr>
    `;
}

// =======================
// 🔹 Ajouter chauffeur
// =======================
document.getElementById("btn-add").onclick = function () {
    let tbody = document.getElementById("tbody-chauffeurs");

    tbody.insertAdjacentHTML("afterbegin", `
        <tr id="new-row">
            <td><input class="form-control" id="cin"></td>
            <td><input class="form-control" id="nom"></td>
            <td><input class="form-control" id="prenom"></td>
            <td><input class="form-control" id="email"></td>
            <td><input class="form-control" id="adresse"></td>
            <td><input class="form-control" id="telephone"></td>
            <td><input class="form-control" id="poste"></td>
            <td><input class="form-control" id="salaire"></td>
            <td><button class="btn-action btn-edit" onclick="validerAjout()">✔ Ajouter</button></td>
        </tr>
    `);
};

function validerAjout() {
    let ch = {
        cin: cin.value,
        nom: nom.value,
        prenom: prenom.value,
        email: email.value,
        adresse: adresse.value,
        telephone: telephone.value,
        poste: poste.value,
        salaire: salaire.value
    };

    fetch("/api/add_chauffeur", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(ch)
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") chargerChauffeurs();
    });
}

// =======================
// 🔹 Supprimer chauffeur
// =======================
function supprimerChauffeur(cin) {
    if (!confirm("Supprimer ce chauffeur ?")) return;

    fetch("/api/delete_chauffeur", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ cin })
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") {
            document.getElementById("row-" + cin).remove();
        }
    });
}

// =======================
// 🔹 Modifier chauffeur
// =======================
function modifierVehicule(matricule) {
    fetch("/api/vehicules")
        .then(r => r.json())
        .then(data => {
            let v = data.vehicules.find(x => x.matricule === matricule);
            if (!v) return alert("Introuvable");

            let new_matricule = prompt("Matricule :", v.matricule);
            let new_marque = prompt("Marque :", v.marque);
            let new_capacite = prompt("Capacité :", v.capacite);
            let new_prix = prompt("Prix d'achat :", v.prix);
            let new_age = prompt("Âge :", v.age);

            fetch("/api/update_vehicule", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    matricule: matricule,
                    new_matricule: new_matricule,
                    marque: new_marque,
                    capacite: new_capacite,
                    prix: new_prix,
                    age: new_age
                })
            })
            .then(r => r.json())
            .then(res => {
                if (res.status === "ok") {
                    alert("Véhicule modifié ✔");
                    chargerVehicules();
                }
            });
        });
}
