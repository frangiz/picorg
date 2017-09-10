import os
import json

def get_setting(key, default_value):
	with open('settings.json', 'r+') as f:
		try:
			data = json.load(f)
		except json.decoder.JSONDecodeError:
			data = {}
	if key not in data:
		data[key] = default_value
	with open('settings.json', 'w') as f:
		f.write(json.dumps(data, sort_keys=True, indent=4))
	return data[key]
