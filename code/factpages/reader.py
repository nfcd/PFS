import requests
from io import StringIO 
import pandas as pd 

class FP_reader:
    """
    Class to read NOD factpages
    """
    def __init__(self):
        """
        initialize strings to construct 
        the factpages URL as of May 2025
        """
        self.u_1 = "https://factpages.sodir.no/public?/Factpages/external/tableview/"
        self.u_2 = "&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f"
        self.u_3 = "&IpAddress=not_used&CultureCode=en&rs:Format=CSV&Top100=false"
    
    def read(self, descriptor):
        """
        Read data from NOD factpages
        Input:
            descriptor: NOD descriptor, 
            e.g. "field_production_monthly"
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # construct the URL
        url = self.u_1 + descriptor + self.u_2 + self.u_3

        # request the data
        response = requests.get(url)
        # if the request was successful
        if response.status_code == 200:
            # load csv data into a DataFrame
            self.df = pd.read_csv(StringIO(response.text))
        else:
            print(f"Error: {response.status_code}")
        
        return self.df