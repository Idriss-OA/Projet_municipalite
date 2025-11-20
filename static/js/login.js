function login() {
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: user, password: pass})
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === "ok") {

            if (data.role === "admin") window.location.href = "/admin";
            if (data.role === "employe") window.location.href = "/employe";
            if (data.role === "chauffeur") window.location.href = "/chauffeur";
            if (data.role === "client") window.location.href = "/client";

        } else {
            document.getElementById("error").textContent = "Identifiants incorrects";
        }
    });
}
