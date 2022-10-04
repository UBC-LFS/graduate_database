$(document).ready(function() {
  console.log("here");

  // const user_form = sessionStorage.getItem('user-form');
  // const prof_form = localStorage.getItem('prof-form');
  //
  // if (prof_form) {
  //   let json = JSON.parse(prof_form);
  //   console.log(json);
  //   console.log($('#id_office'));
  //   // $('#id_office').val(json.office);
  // }

  $('#btn-user-form').on('click', function() {
    const url = $(this).data('url');
    const href = $(this).data('href');

    const form_data = $('#form-user-add-edit').serializeArray();
    const json = convert_object_to_json(form_data, 'User');
    send_data(url, json, href);
    // localStorage.setItem('prof-form', json);


    // const temp = JSON.stringify(form_data);
    // console.log("btn user form", href, url);

    // console.log(form_data);
    // console.log(temp);
    // localStorage.setItem('prof-form', temp);

    //send_data(url, form_data, href);
  });

  $('#btn-prof-form').on('click', function() {
    const url = $(this).data('url');
    const href = $(this).data('href');

    const form_data = $('#form-user-add-edit').serializeArray();
    const json = convert_object_to_json(form_data, 'Professor');
    send_data(url, json, href);

    // const temp = JSON.stringify(form_data);
    // console.log("btn prof form", href, url);
    //
    // console.log(form_data);
    // console.log(temp);

    // localStorage.setItem('user-form', temp);

    // send_data(url, form_data, href);
  });

});

function convert_object_to_json(data, path) {
  let obj = { 'path': path };

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

function send_data(url, data, href) {
  console.log(url, href);
  console.log(data);
  $.ajax({
    method: 'GET',
    url: url,
    data: data,
    dataType: 'json',
    success: function(res) {
      window.location.href = href;
      // let message = '<div class="alert alert-STATUS alert-dismissible fade show" role="alert">' + res.message + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
      //
      // if (res.status === 'success') message = message.replace('STATUS', 'success');
      // else message = message.replace('STATUS', 'danger');
      //
      // $("#response-messages").append(message);
    },
    error: function(err) {
      console.log("error", err, href);
      let message = '<div class="alert alert-danger alert-dismissible fade show" role="alert">' + err + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
      $("#response-messages").append(message);
    }
  });
}
