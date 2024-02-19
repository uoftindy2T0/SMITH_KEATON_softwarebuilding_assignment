from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import logging
import numpy as np


class Analysis():
    def __init__(self, analysis_config: str) -> None:
        ''' Load config into an Analysis object and initialize logging.

        Load system-wide configuration from 'configs/system_config.yml', user configuration from
        'configs/user_config.yml', and the specified analysis configuration file (configs/job_file.yml)

        Parameters
        ----------
        analysis_config : str
            Path to the analysis/job-specific configuration file

        Returns
        -------
        analysis_obj : Analysis
            Analysis object containing consolidated parameters from the configuration files

        Notes
        -----
        The configuration files should include parameters for:
            * Spotify API token
            * ntfy.sh topic
            * Plot color
            * Plot title
            * Plot x and y axis titles
            * Figure size
            * Default save path
        '''
        
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config

        logging.basicConfig(
            handlers=(logging.StreamHandler(), logging.FileHandler('Analysis.log')),
                      level = logging.INFO)

    def load_data(self) -> None:
        ''' Retrieve data from the GitHub API

        This function makes an HTTPS request to the Spotify API and retrieves the selected data from the dataset url 
        found in the job_file.yml. 
        Also retrieves the token authorization headers needed for subsequent calls in other functions, if needed.
        The data is stored in the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''

        # Get the access token for the Spotify API
        response = requests.post('https://accounts.spotify.com/api/token', 
                                 data = {
                                         'grant_type': 'client_credentials',
                                         'client_id': self.config['client_id'],
                                         'client_secret': self.config['client_secret'],
                                 })
        access_token = response.json()['access_token']
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
        }

        # Accessing the Spotify API for the data.
        try: 
            data = requests.get(self.config['dataset_url'], headers=headers)
            logging.info(f'Successfully loaded {self.config["dataset_url"]}')
        except Exception as e: 
            logging.error('Data has not been loaded properly.', exc_info=e)
            raise e
        
        self.dataset = data
        self.headers = headers # Needed if you want to make subsequent access calls in other functions.

    def compute_analysis(self) -> Any:
        '''Analyzes total length of top tracks, given in minutes and seconds. 
        
        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : Any

        '''

        # Ensure that data has been loaded.
        try: 
            tracks = self.dataset.json()['tracks']
        except Exception as e: 
            logging.error('Data has not been loaded.', exc_info=e)
            raise e
        
        duration_list = [] # List of song durations in milliseconds
        for track in tracks: duration_list.append(track['duration_ms'])
        total_length = np.sum(duration_list)

        # Convert from milliseconds into hours, minutes, and seconds
        seconds = total_length // 1000
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        formatted_total_length = (f"Total length of top 10 tracks: {minutes} minutes and {remaining_seconds} seconds")

        return formatted_total_length

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        ''' Analyze and plot data

        Generates a plot, display it to screen, and save it to the path in the parameter 'save_path', or 
        the path from the configuration file if not specified.

        Parameters
        ----------
        save_path : str, optional
            Save path for the generated figure

        Returns
        -------
        fig : matplotlib.Figure

        '''

        # Ensure that data has been loaded.
        try: 
            tracks = self.dataset.json()['tracks']
        except Exception as e: 
            logging.error('Data has not been loaded.', exc_info=e)
            raise e
        
        song_names = []
        song_popularities = []
        for track in tracks: 
            song_names.append(track['name'])
            song_popularities.append(track['popularity'])
        
        plt.figure(figsize = (self.config['plot.config']['figure_size_width'], self.config['plot.config']['figure_size_height']))
        # creating the bar plot
        plt.bar(song_names, song_popularities, color = self.config['plot.config']['plot_color'], width = 0.1)
        plt.title(self.config['plot.config']['title'])
        plt.xlabel(self.config['plot.config']['xlabel'])
        plt.ylabel(self.config['plot.config']['ylabel'])
        plt.xticks(rotation = 75, fontsize = 8)
        if save_path is None: plt.savefig(self.config['plot.config']['default_save_path'] + 'song_popularity_bargraph.pdf')
        else: plt.savefig(save_path + 'song_popularity_bargraph.pdf')
        plt.show()

    def notify_done(self, message: str) -> None:
        ''' Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Parameters
        ----------
        message : str
        Text of the notification to send

        Returns
        -------
        None

        '''

        # Check that message is of correct type
        try: 
            requests.post(f"https://ntfy.sh/{self.config['notify_done_topicname']}", 
                data=message.encode(encoding='utf-8'))
            logging.info(f'"{message}" has been sent successfully!')
        except Exception as e: 
            logging.error('message must be of type "str".', exc_info=e)
            raise e