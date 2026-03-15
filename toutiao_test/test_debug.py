import httpx
import traceback

BASE_URL = "http://localhost:8080"

try:
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # 登录
    r = client.post('/api/user/login', json={'username':'admin','password':'123456'})
    print('Login response:', r.json())
    token = r.json()['data']['token']
    print('Token:', token)

    # 添加浏览记录
    print('\nAdding history...')
    r2 = client.post('/api/history/add', json={'newsId':1}, headers={'Authorization':token})
    print('Status:', r2.status_code)
    print('Headers:', dict(r2.headers))
    print('Response:', r2.text)

except Exception as e:
    print('Error:', e)
    traceback.print_exc()
finally:
    client.close()
