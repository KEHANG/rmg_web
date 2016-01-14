$('document').ready( function() {

    console.log('something works');


});

function renderResult(d,tStatus, jqxhr){
    console.log(d);
}

function click_send() {
    var baseUrl = "/python/test.py";
    dat = $('#input')[0].value;
    console.log(dat);
    $.ajax(baseUrl, {'success':renderResult} );
}
