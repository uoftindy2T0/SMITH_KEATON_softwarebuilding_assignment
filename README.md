# README File for Building Robust Software Summative Assignment - Keaton Smith

The following is some key information for the evaluator of this file:
1) Some datasets in the Spotify API require additional field values.
    - For example, the dataset I included in my job_file.yml required a market field value to be set, so I set it to CA (which represents Canada)
2) For consistency, I am following the docstring documentation given in the assignment outline rather than making an entirely new docstring on my own. I also maintained the same function names even though they could likely be changed in some cases to something more relevant to the function (i.e. the 'compute_analysis' function could likely be renamed to 'top_tracks_duration'.)
3) I added the client_id and client_secret (both in user_config.yml) that I used in case you do not want to make your own Spotify API Web Application. In practice, this information should not be uploaded and shared to GitHub, but for the sake of this assignment's completeness, I have included it.
4) The test cases are not exhaustive. There was a lot more that I could have tested, but I decided that the tests I included would be sufficient for this assignment.