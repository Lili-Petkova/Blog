$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#contactModal .modal-content").html("");
        $("#contactModal").modal("show");
      },
      success: function (data) {
        $("#contactModal .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {

          $("#contactModal").modal("hide");
          $(".container-fluid").prepend(data.answer)
        }
        else {
          $("#contactModal .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create contact
  $(".js-contact").click(loadForm);
  $("#contactModal").on("submit", ".js-contact-form", saveForm);


});