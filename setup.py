from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mosyr/__init__.py
from saas import __version__ as version

setup(
	name="saas",
	version=version,
	description="Manage creating ERP instances as a service, integrates with CRM and Sales module",
	author="AnvilERP",
	author_email="support@anvilerp.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
