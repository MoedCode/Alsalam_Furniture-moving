#!/usr/bin/env python3
import subprocess
import json
import yaml
import sys

def generate_openapi_json():
    """Run manage.py spectacular to generate schema.json"""
    cmd = ["./manage.py", "spectacular", "--file", "schema.json", "--format", "openapi-json"]
    print("Generating OpenAPI JSON schema...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running spectacular:\n", result.stderr)
        sys.exit(1)
    print("OpenAPI JSON schema generated successfully.")

def convert_json_to_yaml():
    """Convert the schema.json file to schema.yml"""
    print("Converting JSON schema to YAML...")
    with open("schema.json", "r") as f_json:
        data = json.load(f_json)
    with open("schema.yml", "w") as f_yaml:
        yaml.dump(data, f_yaml, sort_keys=False)
    print("schema.yml generated successfully.")

if __name__ == "__main__":
    generate_openapi_json()
    convert_json_to_yaml()
