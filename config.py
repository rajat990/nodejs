import configparser
import os

def read_ini(file_path=None):
    if not file_path:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, 'chatbot_data.ini')
        if not os.path.exists(file_path):
            raise Exception("Pre define Chatbot Data file is Absent")
    conf = configparser.ConfigParser()
    conf.read(file_path)
    return conf