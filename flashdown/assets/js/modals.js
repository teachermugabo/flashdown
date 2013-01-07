$(function () {
    // these are for password reset. If a url comes in with a hash matching a modal id, display that modal
    if (window.location.hash == "#register-modal") {
        $("#register-modal").modal("show");
        window.location.hash = "";
    }
    if (window.location.hash == "#login-modal") {
        $("#login-modal").modal("show");
        window.location.hash = "";
    }
});



