let map;
let selectedPoint = null;

async function initMap() {
    map = L.map("map").setView([34.8, 10.7], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

    const res = await fetch("/api/points");
    const data = await res.json();

    data.points.forEach(p => {
        const marker = L.marker([p.lat, p.lng]).addTo(map);

        marker.on("click", () => {
            selectedPoint = p;
            openModal();
        });

        marker.bindPopup(
            `<b>${p.type}</b><br>Capacité: ${p.capacite}<br>Niveau: ${p.niveau}`
        );
    });
}

function openModal() {
    document.getElementById("modalBg").style.display = "flex";
}

function closeModal() {
    document.getElementById("modalBg").style.display = "none";
}

async function sendProbleme() {
    const pb_type = document.getElementById("pb_type").value;
    const desc = document.getElementById("pb_desc").value;

    const res = await fetch("/api/client/signaler_probleme", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            lat: selectedPoint.lat,
            lng: selectedPoint.lng,
            pb_type: pb_type,
            description: desc
        })
    });

    const result = await res.json();

    if (result.status === "ok") {
        alert("✔ Problème signalé !");
        closeModal();
    } else {
        alert("Erreur: " + result.message);
    }
}

initMap();
