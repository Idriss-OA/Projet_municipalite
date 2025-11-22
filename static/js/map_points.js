// ---------------------
// 1) Initialisation map
// ---------------------
let map = L.map('map').setView([34.73932841894739, 10.759143636429094], 12);

// Layer OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);


// ---------------------
// 2) Charger points existants
// ---------------------
fetch("/api/points")
    .then(r => r.json())
    .then(data => {
        data.points.forEach(p => {
            afficherPoint(p);
        });
    });


// ---------------------
// 3) Ajouter un point
// ---------------------
map.on("click", function (e) {

    // ❌ si c'est pas un admin : empêcher l'ajout
    if (userRole !== "admin" && userRole !== "employe") {
    alert("Vous n'avez pas la permission d'ajouter un point.");
    return;
}


    // ✔ sinon admin peut ajouter
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    if (!confirm("Ajouter un point de collecte à cet endroit ?")) return;

    let type = prompt("Type de collecte ?");
    let capacite = prompt("Capacité (kg) ?");

    fetch("/api/add_point", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            lat: lat,
            lng: lng,
            type: type,
            capacite: capacite
        })
    })
    .then(r => r.json())
    .then(res => {
        if (res.status === "ok") {
            alert("Point ajouté !");
            afficherPoint({ lat, lng, type, capacite, niveau: 0 });
        }
    });
});



// ---------------------
// 4) Afficher un point sur la carte
// ---------------------
function afficherPoint(p) {

    let deleteButton = "";

    // ✔ bouton supprimé seulement pour admin
if (userRole === "admin" || userRole === "employe") {
    deleteButton = `
        <br>
        <button onclick="supprimerPoint(${p.lat}, ${p.lng})" style="
            background:#c62828;
            color:white;
            padding:6px 12px;
            border:none;
            border-radius:6px;
            cursor:pointer;
            margin-top:5px;
        ">
            Supprimer
        </button>
    `;
}


    let marker = L.marker([p.lat, p.lng]).addTo(map);

    marker.bindPopup(`
        <b>Point de collecte</b><br>
        Type : ${p.type}<br>
        Capacité : ${p.capacite} kg<br>
        Niveau : ${p.niveau}%<br>
        ${deleteButton}
    `);
}




// ---------------------
// 5) Supprimer un point
// ---------------------
function supprimerPoint(lat, lng) {
    if (!confirm("Supprimer ce point ?")) return;

    fetch("/api/delete_point", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lat: lat, lng: lng })
    })
        .then(r => r.json())
        .then(res => {
            if (res.status === "ok") {
                alert("Point supprimé !");
                location.reload();
            }
        });
}
// ---------------------
// 6) Afficher tableau des points
// ---------------------
document.getElementById("btn-table").onclick = function () {

    fetch("/api/points")
        .then(r => r.json())
        .then(data => {
            let html = `
                <table class="table table-bordered table-striped table-dark mt-3">
                    <thead>
                        <tr>
                            <th>Latitude</th>
                            <th>Longitude</th>
                            <th>Type</th>
                            <th>Capacité (kg)</th>
                            <th>Niveau (%)</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.points.forEach(p => {
                html += `
                    <tr>
                        <td>${p.lat}</td>
                        <td>${p.lng}</td>
                        <td>${p.type}</td>
                        <td>${p.capacite}</td>
                        <td>${p.niveau}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;

            document.getElementById("points-table").innerHTML = html;
            document.getElementById("points-table").style.display = "block";
        });
};
