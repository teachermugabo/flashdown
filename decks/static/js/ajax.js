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


    // and now set up the submit handler for adding a deck in overview.html
    $("#add_deck").submit(function() {
        var self = $(this);
        // TODO: validate
        $.ajax({
            url: self.attr("action"),
            type: "POST",
            data: {deck_name : self.find("#deck_name").val()},
            success: function(response) {
                $("#deck_list").append(response);
            },
            error: function(data) {
                if (DEBUG)
                    alert("ajax error");
            }
        });
        return false; // prevents default submit behavior, which would
        // cause a broken pipe in our ajax app
    });

    $('#new-card-form').submit(function() {
        var data = {'deck-id': $('#deck-id-input').val(),
                     front: $('#wmd-input-front').val(),
                     back: $('#wmd-input-back').val()
                    };
        var self = this;
        $.post($(this).attr("action"), data, function() {
            // clear card data
            $('#card-editor textarea').each(function(i, el) {
                $(el).val('');
            });

            // clear previews
            $('#card-editor .wmd-preview').each(function(i, el) {
                $(el).html('');
            });

            alert("success! now add that recently added section jackass.");
            // show recently added cards to right of addcard area

        }); // TODO; handle / log errors
        return false; // prevents default submit behavior, which would
        // cause a broken pipe in our ajax app
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

