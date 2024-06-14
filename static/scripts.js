function compareFiles() {
  var form = document.getElementById("uploadForm");
  var formData = new FormData(form);

  $.ajax({
    type: "POST",
    url: "/compare",
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      $("#comparisonResult").html(response);
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
}

// Update file input label text to show selected file name
$(".custom-file-input").on("change", function () {
  var fileName = $(this).val().split("\\").pop();
  $(this).next(".custom-file-label").addClass("selected").html(fileName);
});
