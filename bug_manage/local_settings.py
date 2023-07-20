LANGUAGE_CODE = 'zh-hans'

SMS = 666

TENCENT_SMS_APP_ID = 1400621269
TENCENT_SMS_APP_KEY = "xx"
TENCENT_SMS_SIGN = "xx"

TENCENT_COS_ID = "xx"
TENCENT_COS_KEY = "xx"

GAODE_COS_KEY = "xx"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobared" # redis密码
        }
    }
}