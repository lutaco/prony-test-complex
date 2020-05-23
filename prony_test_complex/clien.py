from urllib.parse import quote_plus as quote

import ssl
import pymongo

url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
    user=quote('user1'),
    pw=quote('1879781482999919952'),
    hosts=','.join([
        'rc1b-h1swq8ccd8dq6490.mdb.yandexcloud.net:27018'
    ]),
    rs='rs01',
    auth_src='db1')

client = pymongo.MongoClient(
    url,
    ssl_ca_certs='/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt',
    ssl_cert_reqs=ssl.CERT_REQUIRED)
