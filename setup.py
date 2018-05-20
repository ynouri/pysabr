from setuptools import setup
setup(
    name='pysabr',
    description='SABR volatility model for interest rates options',
    url='https://github.com/ynouri/pysabr',
    version='0.2.0',
    license='MIT',
    author='Yacine Nouri',
    packages=['pysabr', 'web'],
    python_requires='>=3',
    install_requires=['numpy', 'scipy', 'falcon']
)
