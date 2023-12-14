import yaml
import base64

def create_secret_yaml(secret_name, cert_file, key_file, namespace="default"):
    # Read the contents of the certificate and key files
    with open(cert_file, "r") as cert_file:
        cert_data = cert_file.read().strip()

    with open(key_file, "r") as key_file:
        key_data = key_file.read().strip()

    # Encode certificate and key data in base64
    cert_b64 = base64.b64encode(cert_data.encode("utf-8")).decode("utf-8")
    key_b64 = base64.b64encode(key_data.encode("utf-8")).decode("utf-8")

    # Create a dictionary representing the Kubernetes secret
    secret_data = {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {
            "name": secret_name,
            "namespace": namespace,
        },
        "type": "tls",
        "data": {
            "tls.crt": cert_b64,
            "tls.key": key_b64,
        },
    }

    # Convert the dictionary to YAML format
    secret_yaml = yaml.dump(secret_data, default_flow_style=False)

    # Write the YAML to a file
    with open(f"{secret_name}_secret.yaml", "w") as yaml_file:
        yaml_file.write(secret_yaml)

    print(f"Secret YAML file '{secret_name}_secret.yaml' created successfully.")

# Example usage
create_secret_yaml("my-tls-secret", "path/to/certificate.crt", "path/to/private-key.key", "my-namespace")
