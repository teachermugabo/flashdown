// Ensure ajax requests include csrf token, if necessary
$(function() {
  var DEBUG = true;

  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
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


  // and now set up the submit handler 
  $("#add_deck").submit(function() {
    var self = $(this);
    // TODO: validate
    $.ajax({
      // trailing slash is very important. otherwise, since we have
      // APPEND_SLASH=true, Django re-routes our request and breaks
      // the expected functionality of this ajax call
      url: "/decks/new-deck/" + self.find("#deck_name").val() + "/",
      type: "POST",
      success: function(response) {
        $("#deck_list").append(response);
      },
      error: function(data) {
        if (DEBUG)
          alert("ajax problem: " + data);
      }
    });
    return false; // prevents default submit behavior, which would
    // cause a broken pipe in our ajax app
  });
});

