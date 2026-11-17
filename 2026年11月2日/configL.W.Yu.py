def read_device_config(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    except (FileNotFoundError, ValueError):
    
        return {}
    return config


file_path = "device_config.txt"
device_config = read_device_config(file_path)
print(device_config)
