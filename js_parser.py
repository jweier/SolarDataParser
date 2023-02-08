class JS_Parser():


    def __init__(self, data_file):
        self.solar_energy_exported = 0
        print(data_file)
        

        month_data_series_2 = re.findall("var monthDataSeries2.*\n.*\n.*", response_text)

        # test = 'var monthDataSeries2 = {  "prices":[8423.7,8423.5,8514.3,8481.85,8487.7,8506.9,8626.2,8668.95,8602.3,8607.55,8512.9,8496.25,8600.65,8881.1,9040.85,8340.7,8165.5,8122.9,8107.85,8128.0]}'

        print(month_data_series_2)