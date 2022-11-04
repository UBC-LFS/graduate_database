$(document).ready(function() {

  // Search students
  $("#enter-student").on("input", function() {
    const name = $(this).val();

    if (name.length === 0) {
      $("#display-students").children().remove();
    } else {
      $.ajax({
        method: 'GET',
        url: $(this).data('url'),
        data: { 'name': name },
        dataType: 'json',
        success: function(res) {
          console.log(res);
          if (res.status === 'success') {
            if (res.data.length > 0) {
              let students = '<ul class="search-result students list-no-bullets">';
              for (let stud of res.data) {
                students += '<li data-id="' + stud.id + '" data-first-name="' + stud.first_name + '" data-last-name="' + stud.last_name + '" data-student-number="' + stud.student_number + '">' + stud.first_name + ' ' + stud.last_name + ' (' + stud.student_number + ')</li>';
              }
              students += '</ul>';
              $("#display-students").html(students);
            } else {
              $("#display-students").html('<div class="search-result"><p>No students found.</p></div>');
            }
          }
        }
      });
    }
  });

  // Display a list of students
  $("#display-students").on("click", ".search-result > li", function() {
    const id = $(this).data('id');
    const first_name = $(this).data('first-name');
    const last_name = $(this).data('last-name');
    const student_number = $(this).data('student-number');

    $('#input-student').val(id);
    $('#enter-student').hide();
    $("#display-students").children().remove();

    let html = first_name + ' ' + last_name + ' (' + student_number + ')';
    html += '<button class="delete-student btn btn-danger btn-xs ml-2" type="button"><i class="fa fa-times" aria-hidden="true"></i></button>';
    $('#selected-student').html(html);
    $('#selected-student').show();
  });

  // Delete the selected student
  $("#selected-student").on("click", ".delete-student", function() {
    $('#selected-student').html('');
    $('#selected-student').hide();
    $('#input-student').val('');
    $('#enter-student').val('');
    $('#enter-student').show();
  });

});
