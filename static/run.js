$('document').ready( function() {

    console.log('something works');
    var baseUrl = "/python/test.py/";
    dat = $('#input')[0].value;
    $.ajax(baseUrl + dat, {'success':renderResult} );


});

function renderResult(d,tStatus, jqxhr){
    console.log(d);
}
