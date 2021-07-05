"""
Django settings for movie_rating project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import django_heroku
# import json
import os
from django.contrib.messages import constants as messages
import time
import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import sklearn
from sklearn.decomposition import TruncatedSVD
import pickle

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

"""
Reading Machine Learning Model 1 Data files
"""
movie_user_mat_csv= BASE_DIR / 'movie_rating/models/Data/movie_user_mat.csv'

MOVIE_USER_MAT = pd.read_csv(movie_user_mat_csv, index_col=0)

df_inner_movies_links_csv= BASE_DIR / 'movie_rating/models/Data/movies_links.csv'

DF_INNER_MOVIES_LINKS = pd.read_csv(df_inner_movies_links_csv)

SVD = TruncatedSVD(n_components=12, random_state=5)
resultant_matrix = SVD.fit_transform(MOVIE_USER_MAT)

CORR_MAT = np.corrcoef(resultant_matrix)

# Arabic Files
"""
Done reading Machine Learning Model 1 Data files
"""

"""
Reading Machine Learning Model 2 Data files
"""
infile1 = open(BASE_DIR / "movie_rating/models/Data/English_indices", 'rb')
IDX_WEIGHTS_UPDATED = pickle.load(infile1)
infile1.close()

infile2 = open(BASE_DIR / "movie_rating/models/Data/English_Cosine_Weights", 'rb')
COSINE_SIM = pickle.load(infile2)
infile2.close()

movies_csv = BASE_DIR / "movie_rating/models/Data/English_movies_df.csv"
MOVIES_DF = pd.read_csv(movies_csv)

# Arabic Files

infile1 = open(BASE_DIR / "movie_rating/models/Data/Arabic_indices", 'rb')
AINDICES = pickle.load(infile1)
infile1.close()

infile2 = open(BASE_DIR / "movie_rating/models/Data/Arabic_Cosine_Weights", 'rb')
ACOS_SIM = pickle.load(infile2)
infile2.close()

movies_csv = BASE_DIR / "movie_rating/models/Data/Arabic_movies_df.csv"
AMOVIES_DF = pd.read_csv(movies_csv)
"""
Done reading Machine Learning Model 2 Data files
"""

#Read secrets file
# with open('../secrets.json', 'r') as file:
#     data = file.read()

# secrets = json.loads(data)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('DEBUG_VALUE') == 'True')

ALLOWED_HOSTS = ['megamoviez.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'movies.apps.MoviesConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'storages',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'movies.middleware.MyMiddleware',
]

ROOT_URLCONF = 'movie_rating.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'movie_rating.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
LOGIN_URL = 'login'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

django_heroku.settings(locals())
