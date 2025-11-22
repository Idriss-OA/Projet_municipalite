let cinTrouve = null;

function rechercherEmploye() {
    let cin = document.getElementById("rechCin").value.trim();

    fetch("/api/employes")
        .then(r => r.json())
        .then(data => {
            let emp = data.employes.find(e => e.cin === cin);

            if (!emp) {
                document.getElementById("msg").innerHTML =
                    "<span class='text-danger'>Employé introuvable ❌</span>";
                document.getElementById("resultSection").style.display = "none";
                return;
            }

            cinTrouve = emp.cin;

            document.getElementById("empInfo").innerHTML = `
                <li class="list-group-item"><b>CIN :</b> ${emp.cin}</li>
                <li class="list-group-item"><b>Nom :</b> ${emp.nom}</li>
                <li class="list-group-item"><b>Prénom :</b> ${emp.prenom}</li>
                <li class="list-group-item"><b>Email :</b> ${emp.email}</li>
                <li class="list-group-item"><b>Adresse :</b> ${emp.adresse}</li>
                <li class="list-group-item"><b>Téléphone :</b> ${emp.telephone}</li>
                <li class="list-group-item"><b>Poste :</b> ${emp.poste}</li>
            `;

            document.getElementById("resultSection").style.display = "block";
            document.getElementById("msg").innerHTML = "";
        });
}


function deleteEmp() {
    if (!confirm("Confirmer la suppression de cet employé ?")) return;

    fetch("/api/delete_employe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cin: cinTrouve })
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") {
            document.getElementById("msg").innerHTML =
                "<span class='text-success'>Employé supprimé ✔</span>";
            document.getElementById("resultSection").style.display = "none";
        } else {
            document.getElementById("msg").innerHTML =
                "<span class='text-danger'>Erreur : Employé introuvable ❌</span>";
        }
    });
}
