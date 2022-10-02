from pathlib import Path
import datetime # 追加
import pymysql
import environ

env = environ.Env()
env.read_env('back.env')
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

#SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('Django_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
ALLOWED_HOSTS = ['133.49.24.149','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #追加
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        #全てのリクエストに対して認証が必要なクラス
        #'rest_framework.permissions.IsAuthenticated',
        #無制限のアクセスを許可
        'rest_framework.permissions.AllowAny',
        #getのみ認証なしでも可能
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
    ),
}
JWT_AUTH = {
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True, #Falseならトークンの期限永続化
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=86400), #JWTトークンの有効期限を設定
    'JWT_ALLOW_REFRESH': True,  #JWTトークを更新(Refresh)できるようにするかを決める
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7), #7日以内に更新されないとログアウト
    #token認証の際にtoken以外を取得するためのカスタム
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'project.jwt_utils.jwt_response_payload_handler',  # JWT_RESPONSE_PAYLOAD_HANDLERに自作のjwt_response_payload_handlerを指定する
}

# For e-mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
#メールにTLS暗号化を使うか指定
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

CROS_ORIGIN_ALLOW_ALL = env.bool('CROS_ORIGIN_ALLOW_ALL')
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080',
    'http://localhost:8040',
    'http://127.0.0.1:8040',
    'http://133.49.24.149:8080',
    'http://133.49.24.149:8040',
]

# レスポンスを公開する
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': env.db(),
}

AUTH_USER_MODEL = 'api.User'

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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'