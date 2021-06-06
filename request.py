from pytest_bdd import given, when, then, parsers
from pytest_bdd import scenarios
import requests
import base64

GUTHUB_API = 'https://api.github.com'

# Below 2 auth are not valid anymore and to be updated as per current user
USER = 'andrey-dmitriev'
TOKEN = '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'

HEADERS = {'Authorization': 'token ' + TOKEN}

# Basic Auth is deprecated by Github
# See https://developer.github.com/changes/2020-02-14-deprecating-password-auth/
def test_github_response():
    response = requests.get(GUTHUB_API + '/user', headers=HEADERS)
    print('user logs in to GitHub using basic authentication and response is ' + str(response.status_code))
    assert response.status_code == 200

def github_create_repo(repo):

    print('user creates repository with name ' + repo)
    body = {'name': repo, 'auto_init': True}
    response = requests.post(GUTHUB_API + '/user/repos', headers=HEADERS, json = body)
    print(' and response is ' + str(response.status_code))
    #print('\n' + str(response.content))
    assert response.status_code == 201

def github_list_branches(repo):
    print('user list branches for repo ' + repo)
    #GET /repos/{owner}/{repo}/branches
    response = requests.get(GUTHUB_API + '/repos/' + USER + '/' + repo +'/branches')
    print(' and response is ' + str(response.status_code))
    assert response.status_code == 200

def github_get_sha(repo):
    response = requests.get(GUTHUB_API + '/repos/' + USER + '/' + repo +'/branches')
    assert response.status_code == 200
    for item in response.json():
        if item['name'] == 'main':
            sha = item['commit'].get('sha')
    return sha

# https://developer.github.com/enterprise/2.10/v3/git/refs/#create-a-reference
# https://github.community/t/github-api-to-create-a-branch/14216
def github_create_branch(branch):
    print('user creates branch ' + branch)
    body = { 'ref': 'refs/heads/' + branch, 'sha': sha}
    # POST /repos/:owner/:repo/git/refs
    response = requests.post(GUTHUB_API + '/repos/' + USER + '/' + REPO +'/git/refs', headers=HEADERS, json = body)
    print(' and response is ' + str(response.status_code))
    #print('\n' + str(response.content))
    assert response.status_code == 201


# https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents
def github_commit_file(branch):
    print('user commit a file to the branch ' + branch)
    sample_string = 'some content'
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    body = { 'message':'committing autogenerated file', 'content': base64_string,'branch':branch}
    
    # PUT /repos/{owner}/{repo}/contents/{path}
    response = requests.put(GUTHUB_API + '/repos/' + USER + '/' + REPO +'/contents/' + 'path', headers=HEADERS, json = body)
    print(' and response is ' + str(response.status_code))
    #print('\n' + str(response.content))
    assert response.status_code == 201

# https://docs.github.com/en/rest/reference/pulls#create-a-pull-request
def github_create_pull_request():
    print('user creates pull request to main branch')
    
    # POST /repos/{owner}/{repo}/pulls
    body = { 'title':'New pull request','head': BRANCH, 'base': 'main'}
    
    response = requests.post(GUTHUB_API + '/repos/' + USER + '/' + REPO +'/pulls', headers=HEADERS, json = body)
    
    print(' and response is ' + str(response.status_code))
    #print('\n' + str(response.content))
    assert response.status_code == 201

def github_delete_repo(repo):
    print('user deletes a branch ' + BRANCH)
    response = requests.delete(GUTHUB_API + '/repos/' + USER + '/' + repo, headers=HEADERS)
    print(' and response is ' + str(response.status_code))
    #print('\n' + str(response.content))
    assert response.status_code == 204

REPO = 'test4'
BRANCH = 'testBranch'
test_github_response()
github_create_repo(REPO)
github_list_branches(REPO)
sha = github_get_sha(REPO)
github_create_branch(BRANCH)
github_commit_file(BRANCH)
github_create_pull_request()
github_delete_repo(REPO)