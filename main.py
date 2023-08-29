import json
import os


def Read_folder_list(root_folder_path):
    # os.listdir() 함수를 사용하여 폴더 내의 모든 파일과 폴더 이름을 가져옵니다.
    file_and_folder_names = os.listdir(root_folder_path)
    #최종 경로들
    paths = []
    for folder_name in file_and_folder_names:
        direction_folders = os.listdir(root_folder_path+"/"+folder_name)
        for direction_folder in direction_folders:
            json_files = os.listdir(root_folder_path+"/"+folder_name+"/"+direction_folder)
            for json_file in json_files:
                file_name = root_folder_path+"/"+folder_name+"/"+direction_folder+"/"+json_file
                if os.path.isfile(os.path.join(file_name)):
                    paths.append(file_name)
    
    Read_Jason(paths[0])

    
    # for name in file_and_folder_names:
    #     if os.path.isfile(os.path.join(folder_path, name)):
    #         files.append(name)
    #     else:
    #         folders.append(name)
    



def Read_Jason(json_file_name):
    # JSON 파일 읽기
    with open(json_file_name, 'r') as f:
        data = json.load(f)
    # 데이터 수정
    for i in data['row']:
        print(i['id'])

    # # JSON 파일에 저장
    # with open(json_file_name, 'w') as f:
    #     json.dump(data, f, indent=4)

if __name__ == "__main__":
    # 읽을 폴더의 경로를 지정합니다.
    folder_path_ = '/home/armstrong/주간_성남_01'

    Read_folder_list(folder_path_)
