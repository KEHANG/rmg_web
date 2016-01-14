$('document').ready( function() {

    console.log('something works');


});

function renderResult(d,tStatus, jqxhr){
    $("#result")[0].innerHTML = d;
}

function click_send() {
    var baseUrl = "/python/test.py";
    dat = $('#input')[0].value;
    $.ajax(baseUrl, {'success':renderResult} );
}
