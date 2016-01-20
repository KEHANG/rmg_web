$('document').ready( function() {

    console.log('something works');


});

function renderResult(d,tStatus, jqxhr){
    $("#progress")[0].innerHTML = "Done! Please check your results below.";
    id = d;
    var resultUrl = "/job_result/" + id;

    $("#resultLink")[0].href = resultUrl;
    $("#resultLink")[0].innerHTML = "chem_"+id+".inp";

}

function search_mol() {
	$("#progress")[0].innerHTML = "Waiting for result...";
    var baseUrl = "/python/search_mol.py";
    $.ajax(baseUrl, {'success':renderResult} );
    
}

function run_job(id) {
	$("#progress")[0].innerHTML = "Waiting for result...";
    var baseUrl = "/python/rmg/input.py/"+id;
    $.ajax(baseUrl, {'success':renderResult} );
}

$("#input_form").submit(function(e){
    
    var formData = new FormData($(this)[0]);
    // create job
    $.ajax({
        type: "POST",
        url: "/run_rmg_job",
        data: formData,
        async: true,
        success: function(data){
            alert("Your job is to run shortly with id " + data);
            // run job
            id = data;
            run_job(id);
        },
        cache: false,
        contentType: false,
        processData: false
    })
    e.preventDefault();
})