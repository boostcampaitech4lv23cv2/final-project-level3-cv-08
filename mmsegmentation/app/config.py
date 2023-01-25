import sys
import yaml

sys.path.append('../')
from app.model import get_model

def get_setting():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        
    # model load
    model = config.pop('models')
    for key, val in model.items():
        model[key] = get_model(val['config_path'], val['checkpoint_path'])
    config['models'] = model
    return config