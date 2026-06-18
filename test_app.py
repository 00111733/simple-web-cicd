"""Flask App v2.0 单元测试"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    """首页应返回 200"""
    rv = client.get("/")
    assert rv.status_code == 200


def test_index_contains_title(client):
    """首页应包含 CI/CD 关键词"""
    rv = client.get("/")
    assert "CI/CD" in rv.data.decode("utf-8")


def test_index_contains_version(client):
    """首页应包含 v2.0 版本号"""
    rv = client.get("/")
    assert "v2.0" in rv.data.decode("utf-8")


def test_health_check(client):
    """健康检查接口应返回 healthy"""
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "healthy"


def test_api_info(client):
    """API 信息接口应返回版本信息"""
    rv = client.get("/api/info")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["version"] == "2.0"
    assert data["status"] == "running"


def test_api_reset(client):
    """API 重置接口应正常工作"""
    rv = client.get("/api/reset")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "success"
