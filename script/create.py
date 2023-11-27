import os
import yaml
from slugify import slugify

DEFAULT_INFO_DATA = {
    'id': 'Default',
    'slug': '',
    'title': '',
    'next': 'Default',
    'previous': 'Default',
    'createdBy': 'Default',
    'updatedBy': 'Default',
    'lastUpdatedTime': 'Default',
    'createdTime': 'Default'
}

def get_input_data():
    _type = input("Enter 1. Library | 2. Blogs: ")
    _cate = input("Enter category: ")
    _name = input("Enter blog name: ")
    _next = input("Enter next blog id: ")
    _previous = input("Enter previous blog id: ")
    
    parent_folder = 'library' if _type == '1' else 'blogs'
    path_to_folder = os.path.join(parent_folder, _cate)
    
    return path_to_folder, _name, _next, _previous

if __name__ == '__main__':
    path_to_parent, name, next_id, previous_id = get_input_data()
    slug = slugify(name)
    DEFAULT_INFO_DATA['slug'] = slug
    DEFAULT_INFO_DATA['next'] = next_id
    DEFAULT_INFO_DATA['previous'] = previous_id
    DEFAULT_INFO_DATA['title'] = name
    
    with open('./BUILD', "r") as file:
        number_post = file.readlines()[0]
    
    idx = '0' * (4 - len(number_post)) + number_post
    
    folder_path = os.path.join(path_to_parent, f'{idx}_{slug}')
    os.makedirs(folder_path)
    
    with open(os.path.join(folder_path, "info.yaml"), "w") as yaml_file:
        yaml.dump({'data': DEFAULT_INFO_DATA}, yaml_file)
        
    with open(os.path.join(folder_path, "README.md"), "w") as readme_file:
        readme_file.writelines("add your content here....")