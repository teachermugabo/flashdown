$(function () {
    // ==================================  MODALS ============================================================ //
    // If one of the modals has errors, it's because we just sent the user back here to fix them.  Show the modal.
    if (($("#register-modal").find(".help-inline").length > 0) || ($("#register-modal").find(".alert").length > 0)) {
        $("#register-modal").modal("show");
    }
    else if (($("#login-modal").find(".help-inline").length > 0) || ($("#login-modal").find(".alert").length > 0)) {
        $("#login-modal").modal("show");
    }
    else if (($("#new-deck-modal").find(".help-inline").length > 0) || ($("#login-modal").find(".alert").length > 0)) {
        $("#new-deck-modal").modal("show");
    }

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



