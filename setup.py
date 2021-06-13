import setuptools

setuptools.setup(

    name="CMSPAM",
    version="0.1",
    description="CMSPAM algoritm",
    author=['Gabriela Ossowska', 'Tomasz Sachanowski'],
    packages=setuptools.find_packages(),
    install_requires=['numpy','dataframe', 'click', 'tweepy', 'autocorrect']
)