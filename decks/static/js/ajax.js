// Ensure ajax requests include csrf token, if necessary
$(function() {
    var DEBUG = true;

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

   // add this class to a delete link to submit it via ajax
    $(".delete-card").click(function() {
        var self = $(this);
        $.ajax({
            url: self.attr("href"),
            type: "POST",
            data: {},
            success: function(response) {
                tr = self.closest("tr");
                tr.fadeOut("slow", function() {
                    $(this).remove();
                });
            },
            error: function(data) {
                if (DEBUG)
                    alert("ajax error deleting deck");
            }
        });
        return false; // prevents default submit behavior, which would
        // cause a broken pipe in our ajax app

    });

});

