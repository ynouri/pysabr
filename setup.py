from setuptools import setup
setup(
    name='pysabr',
    description='SABR volatility model for interest rates options',
    url='https://github.com/ynouri/pySABR',
    version='0.1.3',
    license='MIT',
    author='Yacine Nouri',
    packages=['sabr', 'black'],
    python_requires='>=3',
    install_requires=['numpy', 'scipy']
)
