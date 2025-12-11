async function loadReclamations() {

    let tbody = document.getElementById("reclamations-table");
    tbody.innerHTML = "";

    // --- 1. Charger problèmes carte interactive ---
    let pbReq = await fetch("/api/problemes_carte");
    let pbData = await pbReq.json();

    pbData.problemes
        .filter(pb => pb.status === "admin")
        .forEach(pb => {
            tbody.innerHTML += `
                <tr>
                    <td>${pb.id}</td>
                    <td>${pb.type}</td>
                    <td>${pb.description}</td>
                    <td>${pb.date}</td>
                    <td><span class="badge bg-warning text-dark">Carte interactive</span></td>
                </tr>
            `;
        });

    // --- 2. Charger réclamations chauffeur/client ---
    let recReq = await fetch("/api/reclamations_admin");
    let recData = await recReq.json();

    recData.reclamations.forEach((rec, index) => {
        tbody.innerHTML += `
            <tr>
                <td>R-${index + 1}</td>
                <td>${rec.type}</td>
                <td>${rec.motif}</td>
                <td>${rec.date}</td>
                <td><span class="badge bg-info">Réclamation</span></td>
            </tr>
        `;
    });
}
