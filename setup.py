from setuptools import setup, find_packages

setup(
	name='TracSoftDueDate', version='1.0',
	packages=find_packages(exclude=['*.tests*']),
	entry_points = {
		'trac.plugins': [
			'softduedate = softduedate',
		],
	},
)
