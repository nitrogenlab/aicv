from setuptools import find_packages
from distutils.core import setup

if __name__== '__main__':
    setup(include_package_data=True,
          description='Altair Interactive Cluster Visualization',
          long_description="""Python package doing cluster and interactive visualizations using altair""",
          author="Avanti Shrikumar, Deeya Viradia",
          author_email="avanti.shrikumar@gmail.com, viradiadeeya@gmail.com",
          url='https://github.com/nitrogenlab/aicv',
          version='0.1.0.0',
          packages=find_packages(),
          setup_requires=[],
          install_requires=['altair', 'numpy', 'pandas', 'scipy',
                            'sklearn', 'leidenalg'],
          extras_require={'altair': ['altair']},
          scripts=[],
          name='aicv')
