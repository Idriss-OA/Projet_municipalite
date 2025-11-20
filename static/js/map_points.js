// ---------------------
// 1) Initialisation map
// ---------------------
let map = L.map('map').setView([36.8065, 10.1815], 12);

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
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    if (!confirm("Ajouter un point de collecte à cet endroit ?")) return;

let type = prompt("Type de collecte (ex: Plastique, Verre, Mélange)");
let capacite = prompt("Capacité maximale du conteneur (kg)"); 


    fetch("/api/add_point", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
                afficherPoint({
                    lat: lat,
                    lng: lng,
                    type: type,
                    niveau: niveau
                });
            }
        });
});


// ---------------------
// 4) Afficher un point sur la carte
// ---------------------
function afficherPoint(p) {
    let marker = L.marker([p.lat, p.lng]).addTo(map);

    marker.bindPopup(`
        <b>Point de collecte</b><br>
        Type : ${p.type}<br>
        Capacité : ${p.capacite} kg<br>
        Remplissage : ${p.niveau}%<br><br>
        <button onclick="supprimerPoint(${p.lat}, ${p.lng})">
            Supprimer
        </button>
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
