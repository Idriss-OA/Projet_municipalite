let map = L.map('map').setView([34.74, 10.76], 13);
let selectedMarker = null;
let selectedLatLng = null;

// --- Affichage des points existants ---
let pointsExistants = [];

fetch("/api/points")
    .then(res => res.json())
    .then(data => {
        pointsExistants = data.points;

        data.points.forEach(p => {
            L.marker([p.lat, p.lng]).addTo(map);
        });
    });

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// --- Client clique sur la carte pour proposer un point ---
map.on("click", function(e) {
    let lat = e.latlng.lat;
    let lng = e.latlng.lng;

    // Vérifier distance min
    for (let p of pointsExistants) {
        let d = map.distance([lat, lng], [p.lat, p.lng]);
        if (d < 50) {
            alert("❌ Ce point est trop proche d'un autre point (minimum 50 mètres).");
            return;
        }
    }

    if (selectedMarker) map.removeLayer(selectedMarker);

    selectedMarker = L.marker([lat, lng], { draggable: true }).addTo(map);
    selectedLatLng = { lat, lng };

    document.getElementById("formBox").style.display = "block";
});

// --- Envoi de la demande ---
function envoyerDemande() {
    if (!selectedLatLng) {
        alert("Veuillez choisir un emplacement sur la carte.");
        return;
    }

    let type = document.getElementById("type").value;
    let capacite = document.getElementById("capacite").value;

    fetch("/api/reclamation/nouveau_point", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            lat: selectedLatLng.lat,
            lng: selectedLatLng.lng,
            type: type,
            capacite: capacite
        })
    })
    .then(res => res.json())
    .then(rep => {
        if (rep.status === "ok") {
            alert("Votre demande a été enregistrée !");
            window.location.href = "/client";
        } else {
            alert("Erreur : " + rep.message);
        }
    });
}
