from setuptools import find_packages, setup

setup(
    name='real-estate-prediction',
    version='0.0.1',
    author='Shantanu',
    author_email='shantanu190ct@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas', 'numpy', 'seaborn', 'scikit-learn', 
        'xgboost', 'mysql-connector-python', 'streamlit',
        'folium', 'streamlit-folium', 'python-dotenv'
    ]
)