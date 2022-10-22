$(document).ready(function() {

  $('#btn-student-form').on('click', function() {
    const current_tab = $(this).data('current-tab');

    const form_data = $('#create-student-form').serializeArray();
    const json = convert_object_to_json(form_data);

    console.log(json);

  });

});


function convert_object_to_json(data, path) {
  let obj = {};

  for (let d of data) {
    let key = d['name'];
    if (obj[key]) {
      if ( !Array.isArray(obj[key]) ) {
        let temp = obj[key];
        obj[key] = [temp];
      }
      obj[key].push(d['value']);
    } else {
      obj[key] = d['value'];
    }
  }

  return obj;
}
