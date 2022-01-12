#!/usr/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
# 创建redis连接池（默认连接池最大连接数 2**31=2147483648）
pool = redis.ConnectionPool(host='localhost', port=6379, password='foobared', encoding='utf-8', max_connections=1000)
# 去连接池中获取一个连接
conn = redis.Redis(connection_pool=pool)
# 设置键值：15131255089="9999" 且超时时间为10秒（值写入到redis时会自动转字符串）
conn.set('name', "武沛齐", ex=10)
# 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
value = conn.get('name')
print(value.decode())