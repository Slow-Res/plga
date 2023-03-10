import difflib
import json
import re
import eel
from github import Github   

import concurrent.futures
import time
import io


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_usernames(txt_file = 'usernames.txt'):
    try: 
        with open(txt_file) as f:
            contents = f.read()
            contents = contents.strip().split()
        return contents
    except Exception as err:
        print(err)

def get_repo(username,repo_name):
    try:
        repo_url = f"{username}/{repo_name}"
        #repo_url = "Slow-Res/covid-19"
        access_token = "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"
        g = Github(access_token)
        repo = g.get_repo(repo_url)
        return repo
    except Exception as e :
        print(e)
        url = ("https://github.com/" + repo_url)
        print(f"{bcolors.FAIL} FAILED TO GET REPO TO {url} \n{bcolors.ENDC}")
        print(f"{bcolors.FAIL} {url} \n{bcolors.ENDC}")

def get_all_repo_files(repo,formats = ['js','html','css','py','jsx'] , exclude = ['.venv', 'env', '.env', 'venv' , '__pycache__','node_modules']):
    try:
        if not repo:
            return []
        
        root_directory = repo.get_contents('')
        file_paths = {}
        while root_directory:
            file_or_dir = root_directory.pop(0)    
            if file_or_dir.type == 'file' and "." in file_or_dir.name and file_or_dir.name.split('.')[1].lower() in formats :
                file_content = file_or_dir.decoded_content.decode()
                file_paths[file_or_dir.path] = file_content
                # import json
                # with open('result.json', 'w') as fp:
                #     json.dump(file_paths, fp)

                
            # if the file_or_dir is a directory, get its contents and add them to the root_directory list
            elif file_or_dir.type == 'dir' and file_or_dir.name.lower() not in exclude :
                root_directory.extend(repo.get_contents(file_or_dir.path))
        return file_paths
    except Exception as err:
        print(err)

def calculate_similarity(code1, code2):

    import copydetect
    from copydetect import CopyDetector
 

    fp1 = copydetect.CodeFingerprint(code1, 25, 1)
    fp2 = copydetect.CodeFingerprint(code2, 25, 1)
    token_overlap, similarities, slices = copydetect.compare_files(fp1, fp2)

    return similarities

def do_compare(data_username1,data_username2):

    user1_files = data_username1['files']
    user2_files = data_username2['files']

    try:
        for key in user1_files.keys():
            if key in user2_files:
                code1 =[key , user1_files[key]]
                code2 =[key , user2_files[key]]

                result_compare = calculate_similarity(code1,code2)
                if result_compare[0] > 0.8 or result_compare[1] > 0.8:

                    print(f"""
                    RESULT OF COMPARE BETWEEN  {data_username1['name']} {data_username2['name']}
                    https://github.com/{data_username1['name']}/{data_username1['repo']}/blob/main/{key}
                    https://github.com/{data_username2['name']}/{data_username2['repo']}/blob/main/{key}
                    SIMILARITY : {result_compare}
                    
                    
                    """)
                
    except:
        print("ERROR IN COMPARING")

def get_candidate_files(candidate_name,repo_name):
    candidate_repo = get_repo(candidate_name,repo_name)
    candidate_files = get_all_repo_files(candidate_repo)

    wanted_user_data = {}
    wanted_user_data['files'] = candidate_files
    wanted_user_data['name'] = candidate_name
    wanted_user_data['repo'] = repo_name

    return wanted_user_data


def start(username ,repo):
    wanted_username = username
    repo_name = repo
    repo = get_repo(wanted_username,repo_name)
    wanted_user_files = get_all_repo_files(repo) # dict

    wanted_user_data = {}
    wanted_user_data['files'] = wanted_user_files
    wanted_user_data['name'] = username
    wanted_user_data['repo'] = repo_name




    our_candidates = get_usernames()
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_candidate_files, name , repo_name) for name in our_candidates]
        for idx ,f in enumerate(concurrent.futures.as_completed(results)):
            do_compare(wanted_user_data,f.result())


 

 

st = time.perf_counter()
start("zekraquraan","HR-management-system")
end = time.perf_counter()

print(f"TIME TO FINISH {end -st}" )


"""
#print(json.dumps(files, indent=6))

# @eel.expose
# def can_be_called_in_js(data):
#     pass



# eel.init('GUI/')
# eel.start('index.html') 
"""
