import redis
import re

idle_max = 300

r = redis.Redis( host='redis-15555.c10.us-east-1-2.ec2.cloud.redislabs.com',
                 port=15555,
                 password='passtest')
cl = r.execute_command("client", "list")

pattern = r"addr=(.*?) .*? idle=(\d*)"
regex = re.compile(pattern)
for match in regex.finditer(cl):
    if int(match.group(2)) > idle_max:
        r.execute_command("client", "kill", match.group(1))
