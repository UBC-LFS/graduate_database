$(document).ready(function() {

  // Make a navigation header active
  const role = window.location.pathname.split('/');

  if (role[1] === 'admin') {
    $('#nav-admin').addClass('active');
    $('#view-admin').addClass('active');

  } else if (role[1] === 'program-advisor-director') {
    $('#nav-program-advisor-director').addClass('active');
    $('#view-program-advisor-director').addClass('active');

  } else if (role[1] === 'supervisor') {
    $('#nav-supervisor').addClass('active');
    $('#view-supervisor').addClass('active');

  } else if (role[1] === 'guest') {
    $('#nav-gueset').addClass('active');
    $('#view-guest').addClass('active');
  }

});
