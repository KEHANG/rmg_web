## index page

- beautify (TODO)

## find_molecule

- beautify (TODO)

## run_rmg_job

- `recent jobs` automatically (rather than manually) updates top 10 finished jobs (TODO)

- `recent jobs` should rank by job completion (done)

- db should record the timestamps of job creation and job completion (done)

- every some time to refresh `recent jobs` (done)

- beautify `run_rmg_job` (Great thanks to Greg for making it)

- combine `run_rmg_job_upload` and `run_rmg_job` (done)

## user work flow for rmg job running

- create an job id (done)

- upload a file to `temp+id` (done)

- store job id, cmd, job name info into db (done)

- run job and store result into db (done)

- provide a link for user to download result file (done)