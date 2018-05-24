from setuptools import setup, find_packages

setup(
    name='pysabr',
    description='SABR volatility model for interest rates options',
    url='https://github.com/ynouri/pysabr',
    version='0.2.1',
    license='MIT',
    author='Yacine Nouri',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['numpy', 'scipy', 'falcon']
)
