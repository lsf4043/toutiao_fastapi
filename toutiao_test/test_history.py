"""
浏览历史模块测试
"""
import pytest
import httpx
import asyncio

# 测试配置
BASE_URL = "http://localhost:8080"


class TestHistoryAPI:
    """浏览历史API测试"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前准备"""
        self.client = httpx.Client(base_url=BASE_URL, timeout=30.0)
        self.token = None

    def teardown_method(self):
        """测试后清理"""
        self.client.close()

    def test_01_login(self):
        """测试1: 登录获取Token"""
        print("\n测试1: 登录获取Token")

        response = self.client.post(
            "/api/user/login",
            json={
                "username": "admin",
                "password": "123456"
            }
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]

        self.token = data["data"]["token"]
        print(f"Token: {self.token}")

    def test_02_add_history(self):
        """测试2: 添加浏览记录"""
        print("\n测试2: 添加浏览记录")

        # 先登录
        login_response = self.client.post(
            "/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = login_response.json()["data"]["token"]

        # 添加浏览记录
        response = self.client.post(
            "/api/history/add",
            json={"newsId": 1},
            headers={"Authorization": self.token}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "添加成功"
        assert "id" in data["data"]
        assert "userId" in data["data"]
        assert "newsId" in data["data"]

    def test_03_get_history_list(self):
        """测试3: 获取浏览历史列表"""
        print("\n测试3: 获取浏览历史列表")

        # 先登录
        login_response = self.client.post(
            "/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = login_response.json()["data"]["token"]

        # 添加多条浏览记录
        for i in range(1, 7):
            self.client.post(
                "/api/history/add",
                json={"newsId": i},
                headers={"Authorization": self.token}
            )

        # 获取浏览历史列表
        response = self.client.get(
            "/api/history/list",
            headers={"Authorization": self.token}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]
        assert "hasMore" in data["data"]

    def test_04_get_history_list_with_pagination(self):
        """测试4: 分页获取浏览历史"""
        print("\n测试4: 分页获取浏览历史")

        # 先登录
        login_response = self.client.post(
            "/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = login_response.json()["data"]["token"]

        # 分页获取
        response = self.client.get(
            "/api/history/list",
            params={"page": 1, "pageSize": 3},
            headers={"Authorization": self.token}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) <= 3

    def test_05_delete_history(self):
        """测试5: 删除单条浏览记录"""
        print("\n测试5: 删除单条浏览记录")

        # 先登录
        login_response = self.client.post(
            "/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = login_response.json()["data"]["token"]

        # 添加浏览记录
        add_response = self.client.post(
            "/api/history/add",
            json={"newsId": 1},
            headers={"Authorization": self.token}
        )
        print(f"添加响应: {add_response.json()}")
        history_id = add_response.json()["data"]["id"]

        # 删除浏览记录
        response = self.client.delete(
            f"/api/history/delete/{history_id}",
            headers={"Authorization": self.token}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "删除成功"

    def test_06_delete_not_exist_history(self):
        """测试6: 删除不存在的浏览记录"""
        print("\n测试6: 删除不存在的浏览记录")

        # 先登录
        login_response = self.client.post(
            "/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = login_response.json()["data"]["token"]

        # 删除不存在的记录
        response = self.client.delete(
            "/api/history/delete/99999",
            headers={"Authorization": self.token}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        # 应该返回400错误(浏览记录不存在)
        assert response.status_code == 400

    def test_07_clear_history(self):
        """测试7: 清空浏览历史"""
        print("\n测试7: 清空浏览历史")

        # 先登录
        login_response = self.client.post(
            "/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = login_response.json()["data"]["token"]

        # 添加一些浏览记录
        for i in range(1, 4):
            self.client.post(
                "/api/history/add",
                json={"newsId": i},
                headers={"Authorization": self.token}
            )

        # 清空浏览历史
        response = self.client.delete(
            "/api/history/clear",
            headers={"Authorization": self.token}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "清空成功" in data["message"]

    def test_08_no_token(self):
        """测试8: 无Token访问"""
        print("\n测试8: 无Token访问")

        response = self.client.get("/api/history/list")

        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")

        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
