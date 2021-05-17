import setuptools

setuptools.setup(

    name="SPAM",
    version="0.1",
    description="SPAM algoritm",
    author=['Gabriela Ossowska', 'Tomasz Sachanowski'],
    packages=setuptools.find_packages(),
    install_requires=['numpy','dataframe', 'click', 'tweepy']
)