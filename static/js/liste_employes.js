fetch("/api/employes")
    .then(r => r.json())
    .then(data => {
        let tbody = document.getElementById("tbody-employes");
        tbody.innerHTML = "";

        data.employes.forEach(emp => {

            let row = `
                <tr>
                    <td>${emp.cin}</td>
                    <td>${emp.nom}</td>
                    <td>${emp.prenom}</td>
                    <td>${emp.email}</td>
                    <td>${emp.adresse}</td>
                    <td>${emp.telephone}</td>
                    <td>${emp.poste}</td>
                    <td>${emp.salaire} DT</td>
                </tr>
            `;

            tbody.innerHTML += row;
        });
    });
