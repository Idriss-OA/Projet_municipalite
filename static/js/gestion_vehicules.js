// Charger liste au démarrage
chargerVehicules();

function chargerVehicules() {
    fetch("/api/vehicules")
        .then(r => r.json())
        .then(data => {
            let tbody = document.getElementById("tbody-vehicules");
            tbody.innerHTML = "";

            data.vehicules.forEach(v => {
                tbody.innerHTML += ligneVehicule(v);
            });
        });
}

function ligneVehicule(v) {
    return `
        <tr id="row-${v.matricule}">
            <td>${v.matricule}</td>
            <td>${v.marque}</td>
            <td>${v.capacite} Kg</td>
            <td>${v.prix} DT</td>
            <td>${v.age} ans</td>
            <td>
                <button class="btn btn-edit" onclick="modifierVehicule('${v.matricule}')">Modifier</button>
                <button class="btn btn-delete" onclick="supprimerVehicule('${v.matricule}')">Supprimer</button>
            </td>
        </tr>
    `;
}


document.getElementById("btn-add").onclick = function () {
    let tbody = document.getElementById("tbody-vehicules");

    tbody.insertAdjacentHTML("afterbegin", `
        <tr id="new-row">
            <td><input class="form-control" id="matricule"></td>
            <td><input class="form-control" id="marque"></td>
            <td><input class="form-control" id="capacite"></td>
            <td><input class="form-control" id="prix"></td>
            <td><input class="form-control" id="age"></td>
            <td><button class="btn btn-success" onclick="validerAjout()">Ajouter ✔</button></td>
        </tr>
    `);
};


function validerAjout() {

    let v = {
        matricule: matricule.value,
        marque: marque.value,
        capacite: capacite.value,
        prix: prix.value,
        age: age.value
    };

    fetch("/api/add_vehicule", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(v)
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") chargerVehicules();
    });
}



function supprimerVehicule(matricule) {
    if (!confirm("Supprimer ce véhicule ?")) return;

    fetch("/api/delete_vehicule", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ matricule })
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok")
            document.getElementById("row-" + matricule).remove();
    });
}


function modifierVehicule(matricule) {
    fetch("/api/vehicules")
        .then(r => r.json())
        .then(data => {

            let v = data.vehicules.find(x => x.matricule === matricule);
            if (!v) return alert("Véhicule introuvable");

            let new_matricule = prompt("Matricule :", v.matricule);
            let new_marque = prompt("Marque :", v.marque);
            let new_capacite = prompt("Capacité max :", v.capacite);
            let new_prix = prompt("Prix d'achat :", v.prix);
            let new_age = prompt("Âge :", v.age);

            fetch("/api/update_vehicule", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    old_matricule: matricule,    // ✔ envoyé correctement
                    matricule: new_matricule,
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

