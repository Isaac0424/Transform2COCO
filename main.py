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
                    temp_name = json_file.split(".")
                    file_names.append(temp_name[0]+"."+temp_name[1])
                    paths.append(file_name)

    
    for id, path in enumerate(paths):
        temp_dict = dict()
        image_width,image_height = Read_Jason(path,id)
        temp_dict["file_name"]=file_names[id]
        temp_dict["height"]=image_height
        temp_dict["width"]=image_width
        temp_dict["id"]=id
        list_images.append(temp_dict)



def Read_Jason(json_file_name,image_id):
    # JSON 파일 읽기
    with open(json_file_name, 'r') as f:
        data = json.load(f)
    # 데이터 수정
    
    for i in data['row']:
        temp_dict_annotation=dict()
        # [id, image_id, bbox(top left x, top left y, width, height), category_id]
        id = i['id']
        point1 = list(map(int,i['points1'].split(",")))
        point2 = list(map(int,i['points2'].split(",")))
        point3 = list(map(int,i['points3'].split(",")))
        point4 = list(map(int,i['points4'].split(",")))
        min_x = min(point1[0],point2[0],point3[0],point4[0])
        min_y = min(point1[1],point2[1],point3[1],point4[1])
        max_x = max(point1[0],point2[0],point3[0],point4[0])
        max_y = max(point1[1],point2[1],point3[1],point4[1])
        bbox_width = max_x-min_x
        bbox_height = max_y-min_y
        category_id = categories.index(i['attributes2'])
        if category_id == 13:
            #성인 어린이 통합 =>보행자
            category_id=12

        temp_dict_annotation["id"] = id
        temp_dict_annotation["image_id"] = image_id
        temp_dict_annotation["bbox"] = [min_x,min_y,bbox_width,bbox_height]
        temp_dict_annotation["category_id"]=category_id

        list_annotations.append(temp_dict_annotation)
    
    return i['width'],i['height']
    # # JSON 파일에 저장
    # with open(json_file_name, 'w') as f:
    #     json.dump(data, f, indent=4)

if __name__ == "__main__":
    dictionary = dict()         # 
    list_annotations=list() #어노테이션 정보 저장.()
    file_names = list()         #image file의 이름을 저장하는 리스트  
    list_category = list()  #category 정보를 json에 쓰기편하게 
    list_images = list()

    categories = ["경차/세단","SUV/승합차","트럭","버스","통학버스","경찰차","구급차","소방차","기타특장차(견인차, 쓰레기차, 크레인 등)","오토바이","자전거","전동이동체","성인","어린이"]
    after_modify_categories = ["경차/세단","SUV/승합차","트럭","버스","통학버스","경찰차","구급차","소방차","기타특장차(견인차, 쓰레기차, 크레인 등)","오토바이","자전거","전동이동체","보행자"]

    for idx,categ in enumerate(after_modify_categories):
        temp_dict = dict()
        temp_dict["supercategory"] ="obstacle"
        temp_dict["id"]=idx
        temp_dict["name"]=categ
        list_category.append(temp_dict)


    
    # 읽을 폴더의 경로를 지정합니다.
    folder_path_ = '/home/armstrong/주간_성남_01'
    Read_folder_list(folder_path_)

    dictionary["images"]=list_images
    dictionary["categories"]=list_category
    dictionary["annotations"]=list_annotations
    print(dictionary)

    json_name = "./annotations.json"
    
    with open(json_name,'w') as f:
        json.dump(dictionary,f,indent=4,ensure_ascii=False)
