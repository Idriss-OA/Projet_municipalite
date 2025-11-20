function register() {
    let user = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let pass = document.getElementById("password").value;
    let lieu = document.getElementById("lieu").value;
    let postal = document.getElementById("postal").value;
    let cin = document.getElementById("cin").value;

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: user,
            email: email,
            password: pass,
            lieu: lieu,
            postal: postal,
            cin: cin
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === "ok") {
            document.getElementById("msg").innerHTML =
                "<span class='text-success fw-bold'>Compte créé ✔️</span>";

            setTimeout(() => window.location.href = "/", 1500);
        } else {
            document.getElementById("msg").innerHTML =
                "<span class='text-danger fw-bold'>Nom déjà utilisé ❌</span>";
        }
    });
}
