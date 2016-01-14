$('document').ready( function() {

    console.log('something works');


});

function renderResult(d,tStatus, jqxhr){
    $("#result")[0].innerHTML = d;
}

function search_mol() {
	$("#result")[0].innerHTML = "Waiting for result...";
    var baseUrl = "/python/search_mol.py";
    dat = $('#input')[0].value;
    $.ajax(baseUrl, {'success':renderResult} );
}

function run_job() {
	$("#result")[0].innerHTML = "Waiting for result...";
    var baseUrl = "/python/rmg/input.py";
    dat = $('#input')[0].value;
    $.ajax(baseUrl, {'success':renderResult} );
}