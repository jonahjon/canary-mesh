
#!/usr/bin/env python
import setuptools

requirements = [
    'boto',
    'boto3>=1.9.166',
    'botocore',
]

setuptools.setup(
    name="canary",
    version="0.0.0",

    author="Jonah Jones",
    author_email="jonahjo@amazon.com",

    description="Lambda Canary Deploymeny",

    packages=setuptools.find_packages(),

    install_requires=requirements,

    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
)