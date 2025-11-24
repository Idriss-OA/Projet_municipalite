// Charger la liste dès le début
chargerEmployes();

// =======================
// 🔹 CHARGER EMPLOYÉS
// =======================
function chargerEmployes() {
    fetch("/api/employes")
        .then(r => r.json())
        .then(data => {
            let tbody = document.getElementById("tbody-employes");
            tbody.innerHTML = "";

            data.employes.forEach(emp => {
                tbody.innerHTML += ligneEmploye(emp);
            });
        });
}

// =======================
// 🔹 TEMPLATE LIGNE EMPLOYÉ
// =======================
function ligneEmploye(emp) {
    return `
        <tr id="row-${emp.cin}">
            <td>${emp.cin}</td>
            <td>${emp.nom}</td>
            <td>${emp.prenom}</td>
            <td>${emp.email}</td>
            <td>${emp.adresse}</td>
            <td>${emp.telephone}</td>
            <td>${emp.poste}</td>
            <td>${emp.salaire} DT</td>
            <td>
                <button class="btn-action btn-edit" onclick="editEmploye('${emp.cin}')">Modifier</button>
                <button class="btn-action btn-delete" onclick="supprimerEmploye('${emp.cin}')">Supprimer</button>
            </td>
        </tr>
    `;
}

// =======================
// 🔹 AJOUTER UNE LIGNE D'AJOUT
// =======================
document.getElementById("btn-add").onclick = function () {

    let tbody = document.getElementById("tbody-employes");

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
            <td>
                <button class="btn-action btn-edit" onclick="validerAjout()">✔ Ajouter</button>
            </td>
        </tr>
    `);
};

function validerAjout() {
    let emp = {
        cin: cin.value,
        nom: nom.value,
        prenom: prenom.value,
        email: email.value,
        adresse: adresse.value,
        telephone: telephone.value,
        poste: poste.value,
        salaire: salaire.value
    };

    fetch("/api/add_employe", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(emp)
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") {
            chargerEmployes();
        }
    });
}

// =======================
// 🔹 SUPPRIMER EMPLOYÉ
// =======================
function supprimerEmploye(cin) {
    if (!confirm("Supprimer cet employé ?")) return;

    fetch("/api/delete_employe", {
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
function editEmploye(cin) {

    fetch("/api/employes")
        .then(r => r.json())
        .then(data => {

            let emp = data.employes.find(e => e.cin === cin);
            if (!emp) return alert("Employé introuvable");

            // NOUVEAU : demander un NOUVEAU CIN
            let new_cin = prompt("Nouveau CIN :", emp.cin);
            if (!new_cin) return;

            let new_nom = prompt("Nom :", emp.nom);
            let new_prenom = prompt("Prénom :", emp.prenom);
            let new_email = prompt("Email :", emp.email);
            let new_adresse = prompt("Adresse :", emp.adresse);
            let new_tel = prompt("Téléphone :", emp.telephone);
            let new_poste = prompt("Poste :", emp.poste);
            let new_salaire = prompt("Salaire :", emp.salaire);

            fetch("/api/update_employe", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    old_cin: cin,         // CIN actuel (pour identifier)
                    cin: new_cin,         // CIN modifié
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
                    alert("Employé modifié ✔");
                    chargerEmployes();
                }
            });
        });
}
