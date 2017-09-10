import os
import json

def get(key, default_value):
	FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
		'settings.json')
	data = {}
	if os.path.exists(FILENAME):
		with open(FILENAME, 'r') as f:
			try:
				data = json.load(f)
			except:
				pass
	if key not in data:
		data[key] = default_value
	with open(FILENAME, 'w') as f:
		f.write(json.dumps(data, sort_keys=True, indent=4))
	return data[key]
