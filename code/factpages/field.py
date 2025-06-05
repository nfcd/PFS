from .reader import FP_reader # import class FP_reader

class Field(FP_reader):
    """ 
    Class to read field data from NOD factpages 
    """
    def __init__(self):
        """
        Initialize field class
        """
        # call parent class
        super().__init__()

    def monthly_production(self, fields=[]):
        """
        Read field monthly production data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_production_monthly")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["prfInformationCarrier"].isin(fields)]

        return df
    
    def yearly_production(self, fields=[]):
        """
        Read field yearly production data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_production_yearly")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["prfInformationCarrier"].isin(fields)]

        return df
    
    def monthly_total_production(self):
        """
        Read monthly total production data
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_production_totalt_NCS_month__DisplayAllRows")

        return df
    
    def yearly_total_production(self):
        """
        Read yearly total production data
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_production_totalt_NCS_year__DisplayAllRows")

        return df
    
    def operators(self, fields=[]):
        """
        Read field operators data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_operator_hst")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["fldName"].isin(fields)]

        return df
    
    def reserves(self, fields=[]):
        """
        Read field reserves data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_reserves")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["fldName"].isin(fields)]

        return df
    
    def inplace_volumes(self, fields=[]):
        """
        Read field in place volumes data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_inplace_volumes")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["fldName"].isin(fields)]

        return df

    def investments(self, fields=[]):
        """
        Read field investments data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_investment_yearly")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["prfInformationCarrier"].isin(fields)]

        return df
    
    def expected_investments(self, fields=[]):
        """
        Read field expected investments data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_investment_expected")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["prfInformationCarrier"].isin(fields)]

        return df
    
    def description(self, fields=[]):
        """
        Read field description data
        Input:
            fields: list of field names. Pass
            empty list to read all fields
        Output:
            df: DataFrame with the data or
            empty if data could not be read
        """
        # call parent class method
        df = self.read("field_description")
        # if df and fields are not empty
        if not df.empty and len(fields) > 0:
            # filter by field names
            df = df[df["fldName"].isin(fields)]

        return df