"""
Flask Web 应用 v2.0 — CI/CD 实验演示
新增功能：API 接口、访问计数、系统信息
"""
from flask import Flask, render_template_string
from collections import Counter

app = Flask(__name__)
visit_counter = Counter()

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD 实验 — Flask App v2.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .card {
            background: #fff; border-radius: 20px; padding: 48px 40px;
            max-width: 550px; width: 90%; box-shadow: 0 25px 70px rgba(0,0,0,0.35);
            text-align: center;
        }
        h1 { color: #333; font-size: 32px; margin-bottom: 8px; }
        .version { color: #11998e; font-size: 16px; font-weight: 700; margin-bottom: 24px; }
        .status { display: inline-block; background: #d4edda; color: #155724;
                  padding: 8px 20px; border-radius: 25px; font-size: 14px; margin-bottom: 24px; }
        .info { background: #f8f9fa; border-radius: 12px; padding: 20px;
                text-align: left; font-size: 13px; color: #555; line-height: 1.9; }
        .info span { color: #222; font-weight: 600; }
        .feature { display: inline-block; background: #e7f3ff; color: #0c63e4;
                   padding: 4px 12px; border-radius: 12px; font-size: 12px; margin: 4px; }
        .features { margin-top: 16px; text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌟 CI/CD 部署成功！</h1>
        <p class="version">Flask App v2.0 | 学生：林怡臻 学号：2440666113 | Python {{ python_version }}</p>
        <div class="status">✅ 服务运行正常</div>
        <div class="info">
            <p><span>容器 ID：</span>{{ hostname }}</p>
            <p><span>部署时间：</span>{{ deploy_time }}</p>
            <p><span>环境：</span>{{ environment }}</p>
            <p><span>学生：</span>林怡臻</p>
            <p><span>学号：</span>2440666113</p>
            <p><span>访问次数：</span>{{ visit_count }} 次</p>
            <p><span>CPU 核心：</span>{{ cpu_count }} 核</p>
        </div>
        <div class="features">
            <span class="feature">✨ API 接口</span>
            <span class="feature">📊 访问计数</span>
            <span class="feature">💻 系统监控</span>
        </div>
    </div>
</body>
</html>"""


@app.route("/")
def index():
    import socket, platform, datetime, os
    visit_counter["index"] += 1
    return render_template_string(
        HTML,
        python_version=platform.python_version(),
        hostname=socket.gethostname(),
        deploy_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        environment="Production" if app.config.get("ENV") == "production" else "Development",
        visit_count=visit_counter["index"],
        cpu_count=os.cpu_count() or 1,
    )


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/api/info")
def api_info():
    import socket, platform, os, datetime
    return {
        "version": "2.0",
        "status": "running",
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count() or 1,
        "visit_count": visit_counter["index"],
        "deploy_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.route("/api/reset")
def api_reset():
    visit_counter.clear()
    return {"status": "success", "message": "计数器已重置"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
