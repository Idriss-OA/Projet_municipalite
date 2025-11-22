function ajouterEmploye() {
let data = {
    cin: document.getElementById("cin").value,
    nom: document.getElementById("nom").value,
    prenom: document.getElementById("prenom").value,
    email: document.getElementById("email").value,
    adresse: document.getElementById("adresse").value,
    telephone: document.getElementById("telephone").value,
    poste: document.getElementById("poste").value,
    salaire: document.getElementById("salaire").value
};


    fetch("/api/add_employe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") {
            document.getElementById("msg").innerHTML =
                "<span class='text-success'>Employé ajouté ✔</span>";

            setTimeout(() => {
                window.location.href = "/employes"; // page du menu employé
            }, 1500);
        }
    });
}
