from setuptools import setup, find_packages

setup(
        author='Ana Nelson',
        author_email='ana@ananelson.com',
        include_package_data = True,
        install_requires = [
            'web.py'
            ],
        name='dexy_viewer',
        packages=find_packages(),
        url='http://dexy.it',
        version="0.0.5"
        )


