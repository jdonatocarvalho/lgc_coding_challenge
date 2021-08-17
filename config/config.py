import yaml

with open("config/hosts.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    api_url = cfg['lgc_api']['base_url']

with open("config/test_data.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    COUNTRY = cfg['lgc_coding_challenge']['country']

with open("config/test_data.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    sample_methods = cfg['lgc_coding_challenge']['sample_methods']