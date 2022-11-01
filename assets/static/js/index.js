$(document).ready(function() {

  // Make a navigation header active
  const role = window.location.pathname.split('/');

  if (role[1] === 'admin') {
    $('#nav-admin').addClass('active');
    $('#view-admin').addClass('active');

  } else if (role[1] === 'graduate-advisor') {
    $('#nav-graduate-advisor').addClass('active');
    $('#view-graduate-advisor').addClass('active');

  } else if (role[1] === 'supervisor') {
    $('#nav-supervisor').addClass('active');
    $('#view-supervisor').addClass('active');

  } else if (role[1] === 'guest') {
    $('#nav-gueset').addClass('active');
    $('#view-guest').addClass('active');
  }

});
