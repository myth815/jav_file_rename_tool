import os
import time
import json
import time
import re
import shutil

def log_message(message):
    """Log messages with timestamp."""
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def log_error(message):
    """Log error messages with timestamp."""
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {message}")
    exit(1)

def validate_string(s):
    pattern = r'^[a-zA-Z]+-\d+$'
    if re.match(pattern, s):
        return True
    else:
        return False

def validate_file_less_space(file_name):
    # 定义正则表达式：(\D+)(\d+)
    # \D+ 匹配一个或多个非数字字符
    # \d+ 匹配一个或多个数字
    # 使用括号创建捕获组，以便在替换时引用
    pattern = r'(\D+)(\d+)'
    # 使用 \1 和 \2 引用两个捕获组，中间插入连字符 '-'
    result = re.sub(pattern, r'\1-\2', file_name)
    if validate_string(result):
        return result
    else:
        return ''

def remove_suffix(file_name, remove_suffix_list):
    for suffix in remove_suffix_list:
        if file_name.endswith(suffix):
            file_name = file_name[:-len(suffix)]
            file_name = remove_suffix(file_name, remove_suffix_list)
    return file_name

def remove_prefix(file_name, remove_prefix_list):
    for prefix in remove_prefix_list:
        if file_name.startswith(prefix):
            file_name = file_name[len(prefix):]
            file_name = remove_prefix(file_name, remove_prefix_list)
    return file_name

def handle_success_file(full_path, file_name_lower):
    # 将文件拷贝到对应的目录
    shutil.move(full_path, file_name_lower)
    pass

def handle_unsuccess_file(full_path, file_name_lower):
    # 将文件拷贝到对应的目录
    pass

def handle_file(file_name, remove_prefix_list, remove_suffix_list):
    file_name_lower = file_name.lower()
    file_name_lower = remove_prefix(file_name_lower, remove_prefix_list)
    file_name_lower = remove_suffix(file_name_lower, remove_suffix_list)
    if not validate_string(file_name_lower):
        if validate_file_less_space(file_name_lower):
            # 定义正则表达式：(\D+)(\d+)
            # \D+ 匹配一个或多个非数字字符
            # \d+ 匹配一个或多个数字
            # 使用括号创建捕获组，以便在替换时引用
            pattern = r'(\D+)(\d+)'
            # 使用 \1 和 \2 引用两个捕获组，中间插入连字符 '-'
            result = re.sub(pattern, r'\1-\2', file_name_lower)
            if validate_string(result):
                return result
                pass
            else:
                return None
        else:
            # 其他可能的问题
            pass
    else:
        return file_name_lower
        pass

def walk_workspace(workspace, output_dir, min_file_size, handle_file_extends, remove_prefix_list, remove_suffix_list):
    for root, dirs, files in os.walk(workspace):
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            file_ext = file_ext.replace('.', '')
            file_size = os.path.getsize(os.path.join(root, file))
            full_path = os.path.join(root, file)
            if file_ext in handle_file_extends and file_size > min_file_size:
                vaildate_file_name = handle_file(file_name, remove_prefix_list, remove_suffix_list)
                if vaildate_file_name:
                    handle_success_file(full_path, output_dir + "/" + vaildate_file_name + "." + file_ext)
                # handle the file
                pass
            else:
                # delete the file
                pass
    # set an timer for watching the workspace
    time.sleep(10)
    walk_workspace(workspace, output_dir, min_file_size, handle_file_extends, remove_prefix_list, remove_suffix_list)
    pass

def start_work(config_file):
    # check workspace
    workspace = config_file.get('workspace')
    if not (os.path.exists(workspace) and os.path.isdir(workspace)):
        log_error("Workspace is error, check the config file")
    output_dir = config_file.get('output_dir')
    if not (os.path.exists(output_dir) and os.path.isdir(output_dir)):
        log_error("Output directory is error, check the config file")
    handle_file_extends = config_file.get('handle_file_extends')
    remove_prefix_list = config_file.get('remove_prefix')
    remove_suffix_list = config_file.get('remove_suffix')
    update_interval = config_file.get('update_interval')
    min_file_size = config_file.get('min_file_size')
    while True:
        walk_workspace(workspace, output_dir, min_file_size, handle_file_extends, remove_prefix_list, remove_suffix_list)
        log_message("Sleeping for next update cycle.")
        # time.sleep(update_interval)

def read_config_file():
    config_file_path = 'config.json'
    if os.path.exists(config_file_path):
        with open(config_file_path, encoding="utf-8") as config_file:
            try:
                json_config_object = json.load(config_file)
                return json_config_object
            except json.JSONDecodeError as e:
                log_error(f"JSON decode error in config file: {e}")
                return None
            except Exception as e:
                log_error(f"Error reading config file: {e}")
                return None
    else:
        log_message("Config file not exist")
        return None
    
def __main__():
    config_file = read_config_file()
    if not config_file:
        return
    start_work(config_file)
    
__main__()