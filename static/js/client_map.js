let map;
let userMarker = null; // ← le marker du client
let routingControl = null;

function initMap() {
    map = L.map("map").setView([34.8, 10.7], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19
    }).addTo(map);

    // ---- Quand le client clique sur la carte ----
    map.on("click", function (e) {
        addOrMoveUserMarker(e.latlng);
    });

    loadPoints();
}

function addOrMoveUserMarker(latlng) {
    // --- si un marker existe déjà → on le supprime
    if (userMarker !== null) {
        map.removeLayer(userMarker);
    }

    // --- créer le nouveau marker ---
    userMarker = L.marker(latlng, {
        draggable: true
    }).addTo(map);

    userMarker.bindPopup("📍 Votre position").openPopup();
}

// Charger les points depuis API
async function loadPoints() {
    const res = await fetch("/api/points");
    const data = await res.json();

    data.points.forEach(p => {
        L.marker([p.lat, p.lng]).addTo(map)
         .bindPopup(`<b>${p.type}</b><br>Capacité: ${p.capacite}<br>Niveau: ${p.niveau}`);
    });
}

// Bouton "aller au point le plus proche"
function enableRoute() {
    if (!userMarker) {
        alert("Veuillez d'abord cliquer sur la carte pour définir votre position.");
        return;
    }

    findNearestPoint();
}

async function findNearestPoint() {
    const res = await fetch("/api/points");
    const data = await res.json();

    let userPos = userMarker.getLatLng();
    let nearest = null;
    let minDist = Infinity;

    data.points.forEach(p => {
        let dist = map.distance(userPos, L.latLng(p.lat, p.lng));
        if (dist < minDist) {
            minDist = dist;
            nearest = p;
        }
    });

    // Supprimer ancien routing si existe
    if (routingControl != null) {
        map.removeControl(routingControl);
    }

    // Tracer la route
    routingControl = L.Routing.control({
        waypoints: [
            userPos,
            L.latLng(nearest.lat, nearest.lng)
        ],
        lineOptions: { styles: [{ color: "blue", weight: 5 }] }
    }).addTo(map);
}

// Lancer la carte
initMap();
