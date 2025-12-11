let selectedLat = null;
let selectedLng = null;

let map = L.map('map').setView([34.78, 10.70], 12);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

let marker = null;

map.on("click", function(e) {
    selectedLat = e.latlng.lat;
    selectedLng = e.latlng.lng;

    if (marker) map.removeLayer(marker);

    marker = L.marker([selectedLat, selectedLng]).addTo(map)
        .bindPopup("Emplacement sélectionné").openPopup();
});

async function sendIncident() {

    if (!selectedLat || !selectedLng) {
        alert("Veuillez sélectionner un emplacement sur la carte !");
        return;
    }

    let payload = {
        type: document.getElementById("incident_type").value,
        description: document.getElementById("incident_desc").value,
        lat: selectedLat,
        lng: selectedLng
    };

    let r = await fetch("/api/reclamation/incident", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    let res = await r.json();

    if (res.status === "ok") {
        alert("Incident signalé avec succès !");
    } else {
        alert("Erreur : " + res.message);
    }
}

