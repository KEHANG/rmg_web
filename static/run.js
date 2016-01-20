$('document').ready( function() {

    console.log('something works');
    var intervalID = setInterval(function(){refresh();}, 60000);


});

function renderResult(d,tStatus, jqxhr){
    $("#progress")[0].innerHTML = "Done! Please check your results below.";
    id = d;
    var resultUrl = "/job_result/" + id;

    $("#resultLink")[0].href = resultUrl;
    $("#resultLink")[0].innerHTML = "chem_"+id+".inp";

}

function renderRecentJob(d, tStatus, jqxhr){
    $("#firstId")[0].innerHTML = d.jobs[0][0];
    $("#firstName")[0].innerHTML = d.jobs[0][1];

    var resultUrl = "/job_result/" + d.jobs[0][0];
    $("#firstDownload")[0].href = resultUrl;


    $("#secondId")[0].innerHTML = d.jobs[1][0];
    $("#secondName")[0].innerHTML = d.jobs[1][1];

    resultUrl = "/job_result/" + d.jobs[1][0];
    $("#secondDownload")[0].href = resultUrl;


    $("#thirdId")[0].innerHTML = d.jobs[2][0];
    $("#thirdName")[0].innerHTML = d.jobs[2][1];

    resultUrl = "/job_result/" + d.jobs[2][0];
    $("#thirdDownload")[0].href = resultUrl;
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

function refresh(){
    // send ajax to query data from db
    // once success renderresult in html
    alert("going to ajax for job result query!");
    var refreshUrl = "/recent_jobs";
    $.ajax(refreshUrl, {'success':renderRecentJob});
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