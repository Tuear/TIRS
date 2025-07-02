from server.app import app


def start_flask_server():
    print("-----------------------启动导师智能推荐系统后端服务----------------------------")
    # 注意：use_reloader=False 防止重载时创建多个事件循环
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    start_flask_server()