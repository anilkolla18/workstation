import yaml

def create_yaml_from_keys(public_key_file, private_key_file, output_yaml_file):
    with open(public_key_file, 'r') as public_key_file:
        public_key = public_key_file.read()

    with open(private_key_file, 'r') as private_key_file:
        private_key = private_key_file.read()

    data = {
        'publicKey': public_key,
        'privateKey': private_key
    }

    with open(output_yaml_file, 'w') as output_file:
        yaml.dump(data, output_file, default_flow_style=False)

    print(f'YAML file "{output_yaml_file}" created successfully.')

# Example usage:
public_key_file = 'path/to/public_key.pem'
private_key_file = 'path/to/private_key.pem'
output_yaml_file = 'output_keys.yaml'

create_yaml_from_keys(public_key_file, private_key_file, output_yaml_file)
