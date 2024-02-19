from pytest import raises
from Analysis import Analysis

analysis_obj = Analysis('configs/job_file.yml')

def test_data_request_integration():
    import requests
    import yaml

    # We want this to raise an AssertionError, since it is clearly not the correct client_id and client_secret.
    response = requests.post('https://accounts.spotify.com/api/token', 
                            data = {
                                    'grant_type': 'client_credentials',
                                    'client_id': 'intended fail',
                                    'client_secret': 'intended fail',
                            })
    with raises(AssertionError):
        assert response.status_code == 200, 'Request did not go through; ensure client_id and client_secret are correct'

    # A correct client_id and client secret are supplied in tests.md, so this should not raise an error.
    with open('configs/user_config.yml', 'r') as f:
        config = yaml.safe_load(f)
            
    response = requests.post('https://accounts.spotify.com/api/token', 
                        data = {
                                'grant_type': 'client_credentials',
                                'client_id': config["client_id"],
                                'client_secret': config["client_secret"],
                        })
    
    assert response.status_code == 200, 'Request did not go through; ensure client_id and client_secret are correct'

def test_analysis_output_before_data():
    # Should fail since it is initialized before load_data
    with raises(AttributeError):
        analysis_obj.compute_analysis() 

def test_plot_data_before_data():
    # Should fail since it is initialized before load_data
    with raises(AttributeError):
        analysis_obj.plot_data() 

def test_load_data():
    analysis_obj.load_data()

def test_notify_done():
    with raises(AttributeError):
        analysis_obj.notify_done(26)
    
    with raises(AttributeError):
        analysis_obj.notify_done(True)
        
def test_usage_example():
    analysis_obj = Analysis('configs/job_file.yml')
    analysis_obj.load_data()

    analysis_output = analysis_obj.compute_analysis()
    print(analysis_output)

    analysis_figure = analysis_obj.plot_data()