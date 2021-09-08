import yaml

yaml_file = open("pages.yaml", 'r')
yaml_content = yaml.load(yaml_file)

print("Key: Value")
for key, value in yaml_content.items():
    print(f"{key}: {value}")