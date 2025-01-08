import os
import shutil
import requests
import gradio as gr


# 创建一个 Gradio 应用程序的容器，命名为 demo
with gr.Blocks() as demo:
    # Markdown组件用于显示文本或HTML内容。
    gr.Markdown('<img src="favicon.ico" width="100" height="50">')
    # State组件用于存储和管理应用的状态。
    tabs_data = {"index": [], }  # 存储每个Tab的数据（名称和聊天记录）
    tabs = gr.State([{"name": "index"}])  # 存储 Tab 的列表，State对象
    state_tab = gr.State("index")  # 用于记录当前 Tab 名字

    # 添加新标签页
    def add_tabs(tables, new_tab_name):
        if not new_tab_name.strip():  # 检查名称是否为空
            return tables, new_tab_name
        # 返回新的标签列表，并清空输入框
        return tables+[{"name": new_tab_name}], ""

    # 上传文件
    def upload_files(files, new_tab_name):
        if not new_tab_name.strip():  # 如果名称为空（去除前后空格后）
            return gr.Text(value="警告：请先输入新知识库的名称，再上传文件！", visible=True)
        path = "./data/" + new_tab_name + "/"
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        for file in files:
            shutil.copyfile(file.name, path + os.path.basename(file))
        return gr.Text(value="文件上传成功", visible=False)

    # 加载标签页数据
    def load_tab_data(tab_name):
        return tabs_data.get(tab_name, [])

    # 处理用户输入，发送请求并更新聊天记录
    def request(message, chat_history, cur_tab):
        url = "http://127.0.0.1:5678/query"
        params = {'name': cur_tab, 'text': message}
        # 发送 GET 请求
        response = requests.get(url, params=params)
        # 检查请求状态
        if response.status_code == 200:
            response_msg = response.text
        else:
            response_msg = "请求失败"
        chat_history.append(gr.ChatMessage(role="user", content=message))
        chat_history.append(gr.ChatMessage(role="assistant", content=response_msg))
        tabs_data[cur_tab] = chat_history
        # 清空输入框，并返回新的聊天记录
        return "", chat_history

    @gr.render(inputs=tabs)
    def render_todos(tabs_list):
        with gr.Tab("添加知识库"):
            with gr.Column():
                tab = gr.Textbox(label="输入新知识库的名称：", placeholder="请输入新知识库标题")
                files = gr.Files(label="上传知识库文件")
                button = gr.Button("创建知识库")
                alert = gr.Text(visible=False)  # 用于显示警告信息
            files.upload(upload_files, [files, tab], [alert])
            button.click(add_tabs, [tabs, tab], [tabs, tab])

        # 循环遍历tabs_list
        for tab in tabs_list:
            tab_name = tab["name"]
            # 为每个标签页创建一个Tab
            with gr.Tab(tab_name) as gtab:
                chatbot = gr.Chatbot(type='messages',  # 对话框，默认tuples元组方式，推荐messages方式
                                     latex_delimiters=[{"left": "$$", "right": "$$", "display": True},
                                                       {"left": "$", "right": "$", "display": False}])
                msg = gr.Textbox(show_label=False, placeholder="输入消息...")  # 输入文本框
                gtab.select(lambda name=tab_name: (name, load_tab_data(name)), None, [state_tab, chatbot])
            msg.submit(request, [msg, chatbot, state_tab], [msg, chatbot])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=1234, allowed_paths=["/"])