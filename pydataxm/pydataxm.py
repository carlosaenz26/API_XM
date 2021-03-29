import requests
import json
import pandas as pd
import datetime as dt
# noinspection SpellCheckingInspection


class ReadDB(object):

    def __init__(self):
        """This object was created to extract data from API XM"""

        self.url = "http://servapibi.xm.com.co/hourly"
        self.connection = None
        self.request = ''
        lectura = requests.get(r'https://raw.githubusercontent.com/EquipoAnaliticaXM/API_XM/master/metricas.json').json()
        self.inventario_metricas = json.loads(lectura)
        
    def get_collections(self, coleccion):

        return self.inventario_metricas[coleccion]

    def request_data(self, coleccion, metrica, start_date, end_date):
        """ request public server data from XM by the API
        Args:
            coleccion: one of the set of variables availables at self.get_collections()
            metrica:one of this variables "DemaCome", "Gene", "GeneIdea", "PrecBolsNaci", "RestAliv"
            start_date: start date consult data
            end_date: end date consult data
        Returns: DataFrame with the raw Data
        """
        if coleccion not in self.inventario_metricas.keys():
            print('No existe la colección {}'.format(coleccion))
            return pd.DataFrame()
        if metrica > len(self.inventario_metricas[coleccion]):
            print('No existe la metrica')
            return pd.DataFrame()

        if self.inventario_metricas[coleccion][metrica][3] == 'Horaria':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}

                self.connection = requests.post(self.url, json=self.request)

                data_json = json.loads(self.connection.content)

                temporal_data = pd.json_normalize(data_json['Items'], 'HourlyEntities', 'Date', sep='_')

                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                start_date = start_date + dt.timedelta(30)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 30 | (end - end_date).days != 0) | aux
        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria' and coleccion == 'CapEfecNeta':
            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 1:
                    end = start_date + dt.timedelta(0)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'daily')
                self.connection = requests.post(self.url, json=self.request)

                data_json = json.loads(self.connection.content)

                temporal_data = pd.json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')

                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                start_date = start_date + dt.timedelta(1)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 1 | (end - end_date).days != 0) | aux
        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria':
            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'daily')
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(30)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 29 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Mensual':
            
            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 732:
                    end = start_date + dt.timedelta(731)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'monthly')
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'MonthlyEntities', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(732)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 731 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Anual':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 366:
                    end = start_date + dt.timedelta(365)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'annual')
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'AnnualEntities', 'Code', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(366)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 365 | (end - end_date).days != 0) | aux


        elif self.inventario_metricas[coleccion][metrica][3] == 'Lista':
            self.request = {"MetricId": coleccion,
                                # "StartDate": "{}".format(str(start_date)),
                                # "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
            self.url = self.url.replace('hourly', 'lists')
            self.connection = requests.post(self.url, json=self.request)
            data_json = json.loads(self.connection.content)
            data = pd.json_normalize(data_json['Items'], 'ListEntities','Date', sep='_')
            
        return data


if __name__ == "__main__":
    consult = ReadDB()
    df1 = consult.request_data("PRONE", 0, dt.date(2020, 7, 1), dt.date(2020, 7, 10))