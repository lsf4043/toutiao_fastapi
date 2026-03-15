import pytest
import requests

BASE_URL = "http://localhost:8080"


class TestFavoriteAPI:
    """收藏API测试类"""
    
    def setup_method(self):
        """每个测试方法前的准备工作"""
        # 登录获取token
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = response.json()["data"]["token"]
        self.headers = {"Authorization": self.token}
    
    def test_01_check_favorite_not_favorited(self):
        """测试检查收藏状态 - 未收藏"""
        print("\n测试1: 检查未收藏的新闻")
        response = requests.get(
            f"{BASE_URL}/api/favorite/check",
            params={"newsId": 1},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "isFavorite" in data["data"]
        
    def test_02_add_favorite(self):
        """测试添加收藏"""
        print("\n测试2: 添加收藏")
        response = requests.post(
            f"{BASE_URL}/api/favorite/add",
            json={"newsId": 1},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "收藏成功"
        
    def test_03_check_favorite_favorited(self):
        """测试检查收藏状态 - 已收藏"""
        print("\n测试3: 检查已收藏的新闻")
        # 先添加收藏
        requests.post(
            f"{BASE_URL}/api/favorite/add",
            json={"newsId": 2},
            headers=self.headers
        )
        
        # 检查收藏状态
        response = requests.get(
            f"{BASE_URL}/api/favorite/check",
            params={"newsId": 2},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["isFavorite"] == True
        
    def test_04_add_duplicate_favorite(self):
        """测试重复添加收藏"""
        print("\n测试4: 重复添加收藏")
        # 先添加收藏
        requests.post(
            f"{BASE_URL}/api/favorite/add",
            json={"newsId": 3},
            headers=self.headers
        )
        
        # 再次添加
        response = requests.post(
            f"{BASE_URL}/api/favorite/add",
            json={"newsId": 3},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "已收藏" in data["message"]
        
    def test_05_get_favorite_list(self):
        """测试获取收藏列表"""
        print("\n测试5: 获取收藏列表")
        # 先添加几个收藏
        for i in range(4, 7):
            requests.post(
                f"{BASE_URL}/api/favorite/add",
                json={"newsId": i},
                headers=self.headers
            )
        
        # 获取收藏列表
        response = requests.get(
            f"{BASE_URL}/api/favorite/list",
            params={"page": 1, "pageSize": 10},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]
        assert "hasMore" in data["data"]
        
    def test_06_remove_favorite(self):
        """测试取消收藏"""
        print("\n测试6: 取消收藏")
        # 先添加收藏
        requests.post(
            f"{BASE_URL}/api/favorite/add",
            json={"newsId": 10},
            headers=self.headers
        )
        
        # 取消收藏
        response = requests.delete(
            f"{BASE_URL}/api/favorite/remove",
            params={"newsId": 10},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "取消收藏成功"
        
    def test_07_remove_not_favorited(self):
        """测试取消未收藏的新闻"""
        print("\n测试7: 取消未收藏的新闻")
        response = requests.delete(
            f"{BASE_URL}/api/favorite/remove",
            params={"newsId": 999},
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        
    def test_08_clear_favorites(self):
        """测试清空所有收藏"""
        print("\n测试8: 清空所有收藏")
        # 先添加一些收藏
        for i in range(20, 25):
            requests.post(
                f"{BASE_URL}/api/favorite/add",
                json={"newsId": i},
                headers=self.headers
            )
        
        # 清空收藏
        response = requests.delete(
            f"{BASE_URL}/api/favorite/clear",
            headers=self.headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "成功删除" in data["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
