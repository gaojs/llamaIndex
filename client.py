import os
import gradio as gr
import shutil
import requests


with gr.Blocks() as demo:
    gr.Markdown('<img src="favicon.ico" width="100" height="50">')
    gr.Markdown('')
    tabs = gr.State([{"name": "index",}])
    tabs_data = {"index": [], }
    state_tab = gr.State("index")  # 用于记录当前 Tab 名字
    state_chat = gr.State([])    # 用于记录当前聊天记录

    def add_tabs(tabs, new_tabs_name):
        return [{"name": new_tabs_name,}]+tabs , ""

    def upload_files(fileobjs,new_tab_name):
        path = "./data/"+ new_tab_name+"/"
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        for file in fileobjs:
            shutil.copyfile(file.name, path+ os.path.basename(file))
        return

    def load_tab_data(tab_name):
        return tabs_data.get(tab_name, [])

    @gr.render(inputs=tabs)
    def render_todos(tabs_list):
        for tab in tabs_list:
            tab_name = tab["name"]
            with gr.Tab(tab_name) as ttab:
                chatbot = gr.Chatbot(latex_delimiters=[{ "left": "$$", "right": "$$", "display": True },
                                                       { "left": "$", "right": "$", "display": False }])  # 对话框
                msg = gr.Textbox(show_label=False, placeholder="输入消息...")  # 输入文本框

                def respond(message,chat_history,cur_tab):
                    url = "http://127.0.0.1:5601/query"
                    params = {'name':cur_tab,'text': message}
                    # 发送 GET 请求
                    response = requests.get(url, params=params)
                    # 检查请求状态
                    if response.status_code == 200:
                        response_msg = response.text
                    else:
                        response_msg = "请求失败"
                    chat_history.append((message, response_msg))
                    tabs_data[cur_tab] = chat_history
                    return "", chat_history
                ttab.select(lambda name=tab_name: (name, load_tab_data(name)), None, [state_tab, chatbot])
            msg.submit(respond, [msg, chatbot, state_tab], [msg, chatbot])

        with gr.Tab("添加知识库"):
            with gr.Column():
                new_tab_name = gr.Textbox(label="输入新知识库的名称：", placeholder="请输入新知识库标题")
                upload_button = gr.Files(label="上传知识库文件")
                add_button = gr.Button("创建知识库")
            upload_button.upload(upload_files, [upload_button,new_tab_name])
            add_button.click(add_tabs, [tabs, new_tab_name], [tabs, new_tab_name])


if __name__ == "__main__":
    demo.launch(server_name="localhost",server_port=1234,allowed_paths=["/"])



