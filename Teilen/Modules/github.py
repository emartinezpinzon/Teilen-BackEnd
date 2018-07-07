import requests
class Github:
    def __init__():
        self.url=''
    @staticmethod
    def listarRepos(token):
        headers = {'Authorization':'token '+token}

        repositorios = requests.get('https://api.github.com/user/repos',headers=headers)
        return repositorios.json()

