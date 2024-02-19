1) test_data_request_integration(): 
- Tests to ensure an error is raised if incorrect credentials are inputted.
- Also tests that the correct response occurs if correct credentials are inputted.
2) test_analysis_output_before_data():
- Tests to ensure an error is raised for 'compute_analysis' function since data had not yet been loaded.
3) test_plot_data_before_data():
- Tests to ensure an error is raised for 'plot_data' function since data had not yet been loaded.
4) test_load_data():
- Tests to ensure that data is loading properly.
5) test_notify_done():
- Tests to assert that AttributeError occurs when input that is not of 'str' type is given.
6) test_usage_example():
- Tests to ensure that usage example given in assignment outline works without issue.