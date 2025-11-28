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
function modifierChauffeur(cin) {
    fetch("/api/chauffeurs")
        .then(r => r.json())
        .then(data => {

            let ch = data.chauffeurs.find(x => x.cin === cin);
            if (!ch) return alert("Chauffeur introuvable");

            let new_cin = prompt("Nouveau CIN :", ch.cin);
            let new_nom = prompt("Nom :", ch.nom);
            let new_prenom = prompt("Prénom :", ch.prenom);
            let new_email = prompt("Email :", ch.email);
            let new_adresse = prompt("Adresse :", ch.adresse);
            let new_tel = prompt("Téléphone :", ch.telephone);
            let new_poste = prompt("Poste :", ch.poste);
            let new_salaire = prompt("Salaire :", ch.salaire);

            fetch("/api/update_chauffeur", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    old_cin: cin,        // ancien CIN
                    cin: new_cin,        // nouveau CIN
                    nom: new_nom,
                    prenom: new_prenom,
                    email: new_email,
                    adresse: new_adresse,
                    telephone: new_tel,
                    poste: new_poste,
                    salaire: new_salaire
                })
            })
            .then(r => r.json())
            .then(res => {
                if (res.status === "ok") {
                    alert("Chauffeur modifié ✔");
                    chargerChauffeurs();
                }
            });
        });
}
