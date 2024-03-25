import os
import time
import json
import time
import re
import shutil
import requests
import ffmpeg
import xml.etree.ElementTree as ET

jav_api_url = "https://javapi.myth815.com/api/movies/"
requests.packages.urllib3.disable_warnings()

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

def generate_nfo_file(jav_api_check_result, jav_file):
    jav_file_info = ffmpeg.probe(jav_file)
    # 创建根元素
    root_node = ET.Element("movie")
    ET.SubElement(root_node, 'plot').text = 'plot'
    ET.SubElement(root_node, 'customrating').text = 'JP-18+'
    ET.SubElement(root_node, 'lockdata').text = False
    ET.SubElement(root_node, 'dateadded').text = 'now'
    ET.SubElement(root_node, 'title').text = 'title'
    ET.SubElement(root_node, 'originaltitle').text = 'originaltitle'
    ET.SubElement(root_node, 'director').text = 'director'
    ET.SubElement(root_node, 'year').text = 'year'
    ET.SubElement(root_node, 'sorttitle').text = 'sorttitle'
    ET.SubElement(root_node, 'mpaa').text = 'JP-18+'
    ET.SubElement(root_node, 'premiered').text = 'premiered'
    ET.SubElement(root_node, 'releasedate').text = 'releasedate'
    ET.SubElement(root_node, 'runtime').text = 'runtime'
    ET.SubElement(root_node, 'genre').text = 'genre1'
    ET.SubElement(root_node, 'genre').text = 'genre2'
    ET.SubElement(root_node, 'genre').text = 'genre3'
    ET.SubElement(root_node, 'studio').text = 'studio'
    ET.SubElement(root_node, 'tag').text = 'tag1'
    ET.SubElement(root_node, 'tag').text = 'tag2'
    ET.SubElement(root_node, 'tag').text = 'tag3'
    art_node = ET.SubElement(root_node, 'art')
    ET.SubElement(art_node, 'poster').text = 'poster'
    ET.SubElement(art_node, 'fanart').text = 'fanart1'
    ET.SubElement(art_node, 'fanart').text = 'fanart2'
    ET.SubElement(art_node, 'fanart').text = 'fanart3'
    ET.SubElement(root_node, 'isuserfavorite').text = False
    ET.SubElement(root_node, 'playcount').text = 0
    ET.SubElement(root_node, 'watched').text = False
    ET.SubElement(root_node, 'lastplayed').text = ''
    resume_node = ET.SubElement(root_node, 'resume')
    ET.SubElement(resume_node, 'position').text = 0.0
    ET.SubElement(resume_node, 'total').text = 0.0
    actor_node = ET.SubElement(root_node, 'actor')
    ET.SubElement(actor_node, 'name').text = 'name'
    ET.SubElement(actor_node, 'type').text = 'Actor'
    ET.SubElement(actor_node, 'thumb').text = 'thumb'
    file_info_node = ET.SubElement(root_node, 'fileinfo')
    stream_details_node = ET.SubElement(file_info_node, 'streamdetails')
    video_node = ET.SubElement(stream_details_node, 'video')
    ET.SubElement(video_node, 'codec').text = 'codec'
    ET.SubElement(video_node, 'micodec').text = 'micodec'
    ET.SubElement(video_node, 'bitrate').text = 'bitrate'
    ET.SubElement(video_node, 'width').text = 'width'
    ET.SubElement(video_node, 'height').text = 'height'
    ET.SubElement(video_node, 'aspect').text = 'aspect'
    ET.SubElement(video_node, 'aspectratio').text = 'aspectratio'
    ET.SubElement(video_node, 'framerate').text = 29.97
    ET.SubElement(video_node, 'language').text = 'language'
    ET.SubElement(video_node, 'scantype').text = 'scantype'
    ET.SubElement(video_node, 'default').text = True
    ET.SubElement(video_node, 'forced').text = False
    ET.SubElement(video_node, 'duration').text = 123
    ET.SubElement(video_node, 'durationinseconds').text = 123
    audio_node = ET.SubElement(stream_details_node, 'audio')
    ET.SubElement(audio_node, 'codec').text = 'codec'
    ET.SubElement(audio_node, 'micodec').text = 'micodec'
    ET.SubElement(audio_node, 'bitrate').text = 'bitrate'
    ET.SubElement(audio_node, 'language').text = 'language'
    ET.SubElement(audio_node, 'scantype').text = 'scantype'
    ET.SubElement(audio_node, 'channels').text = 2
    ET.SubElement(audio_node, 'samplingrate').text = 48000
    ET.SubElement(audio_node, 'default').text = True
    ET.SubElement(audio_node, 'forced').text = False
    ET.SubElement(root_node, 'poster').text = 'poster'
    ET.SubElement(root_node, 'thumb').text = 'thumb'
    ET.SubElement(root_node, 'fanart').text = 'fanart'
    ET.SubElement(root_node, 'maker').text = 'maker'
    ET.SubElement(root_node, 'label').text = ''
    ET.SubElement(root_node, 'num').text = 'num'
    ET.SubElement(root_node, 'release').text = 'release'
    ET.SubElement(root_node, 'cover').text = 'cover'
    ET.SubElement(root_node, 'website').text = 'website'
    # 创建ElementTree对象
    xml_tree = ET.ElementTree(root_node)

    # 保存XML文件，指定编码为utf-8，并添加XML声明
    xml_tree.write("users.xml", encoding='utf-8', xml_declaration=True, standalone="yes")

def handle_success_file(jav_api_check_result, full_path, file_name_lower):
    # 生成NFO文件
    generate_nfo_file(jav_api_check_result, file_name_lower)
    
    # 将文件拷贝到对应的目录
    print("success handle file : " + file_name_lower)
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

def get_jav_info(name):
    session = requests.session()
    session.keep_alive = False
    response = session.get(jav_api_url + name, verify=False)
    return response.json()

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
                    # check if exsit in jav info data
                    jav_api_check_result = get_jav_info(vaildate_file_name)
                    if 'error' in jav_api_check_result and jav_api_check_result['error'] == 'Not Found':
                        pass
                    else:
                        handle_success_file(jav_api_check_result, full_path, output_dir + "/" + vaildate_file_name + "." + file_ext)
                    
                # handle the file
                pass
            else:
                # delete the file
                pass
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
        time.sleep(update_interval)

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