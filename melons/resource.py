import json
import os


def set_resource_test():
    # cur_user = get_object_or_404(User, username='test50')
    # cur_user_profile = get_object_or_404(UserProfile, user=cur_user)
    print(__file__)
    script_dir = os.getcwd()
    print(script_dir)
    file_path = os.path.join(script_dir, r'\static\resource_json.json')
    print(file_path)

    with open(file_path, 'r') as file:
        json_file = json.load(file)
        resource = json_file['resource']
        print(resource)
        print(__file__)

    #    cur_user_profile.resource = resource
    #    cur_user_profile.save()


set_resource_test()