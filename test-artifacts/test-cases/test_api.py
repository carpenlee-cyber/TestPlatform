import pytest
import requests
import json
import os

BASE_URL = "http://localhost:8080"
TOKEN = None
created_tc_id = None
created_bug_id = None

def get_token():
    global TOKEN
    if TOKEN:
        return TOKEN
    resp = requests.post(f"{BASE_URL}/api/auth/login",
                         json={"username": "admin", "password": "admin123"}, timeout=10)
    TOKEN = resp.json().get("data", {}).get("token", "")
    return TOKEN

def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}


class TestTC001_LoginSuccess:
    def test_login_success(self):
        """TC-001: 正确账号密码登录，应返回200和token"""
        resp = requests.post(f"{BASE_URL}/api/auth/login",
                             json={"username": "admin", "password": "admin123"}, timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}"
        body = resp.json()
        token = body.get("data", {}).get("token") if isinstance(body.get("data"), dict) else None
        assert token, f"响应中未找到token，body={body}"
        global TOKEN
        TOKEN = token
        print(f"\n  ✅ Token获取成功: {token[:20]}...")


class TestTC002_LoginWrongPassword:
    def test_login_wrong_password(self):
        """TC-002: 错误密码登录，应返回非200 code"""
        resp = requests.post(f"{BASE_URL}/api/auth/login",
                             json={"username": "admin", "password": "wrongpass"}, timeout=10)
        body = resp.json()
        code = body.get("code", resp.status_code)
        assert code != 200 or resp.status_code in [401, 403], \
            f"期望拒绝，实际 http={resp.status_code} code={code}"
        print(f"\n  ✅ 错误密码被正确拒绝，code={code}")


class TestTC003_NoTokenAccess:
    def test_no_token_access(self):
        """TC-003: 无token访问受保护接口，应返回401或403"""
        resp = requests.get(f"{BASE_URL}/api/testcases", timeout=10)
        assert resp.status_code in [401, 403], \
            f"期望401/403，实际{resp.status_code}"
        print(f"\n  ✅ 无token被拒绝: {resp.status_code}")


class TestTC004_GetTestCases:
    def test_get_testcases_with_token(self):
        """TC-004: 带有效token获取测试用例列表"""
        resp = requests.get(f"{BASE_URL}/api/testcases", headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}，body={resp.text[:200]}"
        print(f"\n  ✅ 用例列表获取成功")


class TestTC005_CreateTestCase:
    def test_create_testcase(self):
        """TC-005: 创建测试用例"""
        global created_tc_id
        payload = {
            "title": "自动化测试-登录功能验证",
            "description": "验证用户能够使用正确的用户名和密码成功登录系统",
            "status": "PENDING",
            "priority": "HIGH"
        }
        resp = requests.post(f"{BASE_URL}/api/testcases", json=payload,
                             headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}，body={resp.text[:200]}"
        body = resp.json()
        tc_id = body.get("data", {}).get("id") if isinstance(body.get("data"), dict) else None
        if tc_id:
            created_tc_id = tc_id
        print(f"\n  ✅ 测试用例创建成功，ID={created_tc_id}")


class TestTC006_GetBugs:
    def test_get_bugs_with_token(self):
        """TC-006: 带有效token获取Bug列表"""
        resp = requests.get(f"{BASE_URL}/api/bugs", headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}"
        print(f"\n  ✅ Bug列表获取成功")


class TestTC007_CreateBug:
    def test_create_bug(self):
        """TC-007: 创建Bug"""
        global created_bug_id
        payload = {
            "title": "自动化测试-登录页面样式异常",
            "description": "在1920x1080分辨率下，登录页面背景图片显示不完整",
            "status": "OPEN",
            "severity": "MEDIUM",
            "assignee": "admin"
        }
        resp = requests.post(f"{BASE_URL}/api/bugs", json=payload,
                             headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}，body={resp.text[:200]}"
        body = resp.json()
        bug_id = body.get("data", {}).get("id") if isinstance(body.get("data"), dict) else None
        if bug_id:
            created_bug_id = bug_id
        print(f"\n  ✅ Bug创建成功，ID={created_bug_id}")


class TestTC008_Dashboard:
    def test_dashboard_stats(self):
        """TC-008: 获取Dashboard统计数据"""
        resp = requests.get(f"{BASE_URL}/api/dashboard/stats",
                            headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}，body={resp.text[:200]}"
        body = resp.json()
        data = body.get("data")
        assert data is not None, "data字段为空"
        print(f"\n  ✅ Dashboard统计: {json.dumps(data, ensure_ascii=False)}")


class TestTC009_Pagination:
    def test_testcases_paginated(self):
        """TC-009: 测试用例分页查询"""
        resp = requests.get(f"{BASE_URL}/api/testcases?page=0&size=10",
                            headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}"
        print(f"\n  ✅ 分页查询成功")


class TestTC010_DeleteTestCase:
    def test_delete_testcase(self):
        """TC-010: 删除测试用例（清理TC-005创建的数据）"""
        global created_tc_id
        if not created_tc_id:
            pytest.skip("TC-005未创建用例，跳过删除")
        resp = requests.delete(f"{BASE_URL}/api/testcases/{created_tc_id}",
                               headers=auth_headers(), timeout=10)
        assert resp.status_code == 200, f"期望200，实际{resp.status_code}"
        print(f"\n  ✅ 用例 ID={created_tc_id} 删除成功")
