
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


def get_repo(username,repo_name):

        except Exception as e :
        print(e)
        url = ("https://github.com/" + repo_url)
        print(f"{bcolors.FAIL} FAILED TO GET REPO TO {url} \n{bcolors.ENDC}")
        print(f"{bcolors.FAIL} {url} \n{bcolors.ENDC}")

    try:
        repo_url = f"{username}/{repo_name}"
        #repo_url = "Slow-Res/covid-19"
        access_token = "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"
        g = Github(access_token)
        repo = g.get_repo(repo_url)
        return repo


def get_usernames(txt_file = 'usernames.txt'):
    try: 
        with open(txt_file) as f:
            contents = f.read()
            contents = contents.strip().split()
        return contents
    except Exception as err:
        print(err)


