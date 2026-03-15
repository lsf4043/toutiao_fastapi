import pytest
import requests
import json

# API基础URL
BASE_URL = "http://localhost:8080"


class TestUserAPI:
    """用户API测试类"""
    
    def test_01_register_new_user(self):
        """测试用户注册 - 新用户"""
        print("\n测试1: 注册新用户")
        response = requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_new", "password": "123456"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "注册成功"
        assert "token" in data["data"]
        assert "userInfo" in data["data"]
        assert data["data"]["userInfo"]["username"] == "testuser_new"
        
    def test_02_register_duplicate_user(self):
        """测试用户注册 - 重复用户名"""
        print("\n测试2: 注册重复用户名")
        # 先注册一个用户
        requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_dup", "password": "123456"}
        )
        
        # 再次注册相同用户名
        response = requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_dup", "password": "123456"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "已存在" in data["message"]
        
    def test_03_login_success(self):
        """测试用户登录 - 成功"""
        print("\n测试3: 用户登录成功")
        # 先注册一个用户
        requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_login", "password": "123456"}
        )
        
        # 登录
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json={"username": "testuser_login", "password": "123456"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "登录成功"
        assert "token" in data["data"]
        assert "userInfo" in data["data"]
        
    def test_04_login_wrong_password(self):
        """测试用户登录 - 错误密码"""
        print("\n测试4: 用户登录错误密码")
        # 先注册一个用户
        requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_wrongpwd", "password": "123456"}
        )
        
        # 用错误密码登录
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json={"username": "testuser_wrongpwd", "password": "wrongpassword"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "错误" in data["message"]
        
    def test_05_login_nonexistent_user(self):
        """测试用户登录 - 不存在的用户"""
        print("\n测试5: 登录不存在的用户")
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json={"username": "nonexistent_user", "password": "123456"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "错误" in data["message"]
        
    def test_06_get_user_info_success(self):
        """测试获取用户信息 - 成功"""
        print("\n测试6: 获取用户信息成功")
        # 先注册并登录
        register_response = requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_info", "password": "123456"}
        )
        token = register_response.json()["data"]["token"]
        
        # 获取用户信息
        response = requests.get(
            f"{BASE_URL}/api/user/info",
            headers={"Authorization": token}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["username"] == "testuser_info"
        
    def test_07_get_user_info_no_token(self):
        """测试获取用户信息 - 无token"""
        print("\n测试7: 获取用户信息无token")
        response = requests.get(f"{BASE_URL}/api/user/info")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 401
        
    def test_08_get_user_info_invalid_token(self):
        """测试获取用户信息 - 无效token"""
        print("\n测试8: 获取用户信息无效token")
        response = requests.get(
            f"{BASE_URL}/api/user/info",
            headers={"Authorization": "invalid_token_12345"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 401
        
    def test_09_update_user_info(self):
        """测试更新用户信息"""
        print("\n测试9: 更新用户信息")
        # 先注册并登录
        register_response = requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_update", "password": "123456"}
        )
        token = register_response.json()["data"]["token"]
        
        # 更新用户信息
        response = requests.put(
            f"{BASE_URL}/api/user/update",
            json={
                "nickname": "测试昵称",
                "bio": "这是我的个人简介",
                "gender": "male"
            },
            headers={"Authorization": token}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "更新成功"
        assert data["data"]["nickname"] == "测试昵称"
        assert data["data"]["bio"] == "这是我的个人简介"
        assert data["data"]["gender"] == "male"
        
    def test_10_update_password_success(self):
        """测试修改密码 - 成功"""
        print("\n测试10: 修改密码成功")
        # 先注册
        register_response = requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_pwd", "password": "123456"}
        )
        token = register_response.json()["data"]["token"]
        
        # 修改密码
        response = requests.put(
            f"{BASE_URL}/api/user/password",
            json={
                "oldPassword": "123456",
                "newPassword": "newpassword123"
            },
            headers={"Authorization": token}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "密码修改成功"
        
        # 验证新密码可以登录
        login_response = requests.post(
            f"{BASE_URL}/api/user/login",
            json={"username": "testuser_pwd", "password": "newpassword123"}
        )
        assert login_response.json()["code"] == 200
        
    def test_11_update_password_wrong_old(self):
        """测试修改密码 - 错误的旧密码"""
        print("\n测试11: 修改密码错误旧密码")
        # 先注册
        register_response = requests.post(
            f"{BASE_URL}/api/user/register",
            json={"username": "testuser_pwd2", "password": "123456"}
        )
        token = register_response.json()["data"]["token"]
        
        # 用错误的旧密码修改
        response = requests.put(
            f"{BASE_URL}/api/user/password",
            json={
                "oldPassword": "wrongpassword",
                "newPassword": "newpassword123"
            },
            headers={"Authorization": token}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "错误" in data["message"]


class TestNewsAPI:
    """新闻API测试类"""
    
    def test_12_get_categories(self):
        """测试获取新闻分类"""
        print("\n测试12: 获取新闻分类")
        response = requests.get(f"{BASE_URL}/api/news/categories")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text[:200]}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0
        
    def test_13_get_news_list(self):
        """测试获取新闻列表"""
        print("\n测试13: 获取新闻列表")
        response = requests.get(
            f"{BASE_URL}/api/news/list",
            params={"categoryId": 1, "page": 1, "pageSize": 10}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text[:200]}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]
        assert "hasMore" in data["data"]
        
    def test_14_get_news_detail(self):
        """测试获取新闻详情"""
        print("\n测试14: 获取新闻详情")
        # 先获取新闻列表
        list_response = requests.get(
            f"{BASE_URL}/api/news/list",
            params={"categoryId": 1, "page": 1, "pageSize": 1}
        )
        news_list = list_response.json()["data"]["list"]
        
        if len(news_list) > 0:
            news_id = news_list[0]["id"]
            response = requests.get(
                f"{BASE_URL}/api/news/detail",
                params={"id": news_id}
            )
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["data"]["id"] == news_id
        else:
            print("没有新闻数据,跳过测试")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
