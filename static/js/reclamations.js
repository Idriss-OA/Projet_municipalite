async function loadReclamations() {
    let r = await fetch("/api/problemes_carte");
    let data = await r.json();

    let tbody = document.getElementById("reclamations-table");
    tbody.innerHTML = "";

    data.problemes
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
}
