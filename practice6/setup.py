from setuptools import setup, find_packages

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()


setup(
    name='information retrieval',
    version='1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Mohammed Rouabah - William Maillard',
    author_email='mohamed.rouabah@univ-st-etienne.fr - william.maillard@etu.univ-st-etienne.fr',
    description='Project of the information course in order to implement a search engine',
    url='https://github.com/mohamedlrouabah1/RIM2DSC/',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
