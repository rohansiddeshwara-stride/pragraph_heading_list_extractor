from setuptools import setup, find_packages
from typing import List


def get_requirements(file_path:str)-> List[str]:
    requirements=[]

    with open(file_path) as f:
        f.readlines()
        
    requirements=[req.replace("\n","") for req in requirements]

    if "-e ." in requirements:
        requirements.remove('-e .')

    return requirements

setup(
    name='pragraph_bullet_headdings_extractor-app',
    version='0.0.1',
    description='A Flask web application for extracting heading, pragraph, bullet list and numbred list from PDF files.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements("requirements.txt")
)