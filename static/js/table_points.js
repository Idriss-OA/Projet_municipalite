fetch("/api/points")
    .then(r => r.json())
    .then(data => {

        let html = `
            <table class="table table-dark table-striped table-bordered align-middle">
                <thead>
                    <tr class="text-center">
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
                <tr class="text-center">
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

        document.getElementById("table-container").innerHTML = html;
    });
