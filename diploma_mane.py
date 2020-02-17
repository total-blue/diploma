from urllib.parse import urlencode
import requests
import time
import json


#adress = 'eshmargunov'
app_id = 7315243
auth_url = 'https://oauth.vk.com/authorize'
params = {
    'client_id': app_id,
    'display': 'page',
    'scope': ('friends', 'groups', 'users'),
    'response_type': 'token',
    'v': 5.103
    }
#print('?'.join((AUTH_URL, urlencode(params))))
token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

def getUserID(adress):
    response = requests.get(
        'https://api.vk.com/method/users.get',
        {'user_ids': adress,
        'access_token': token,
        'v': 5.103}
        )
    id = response.json()['response'][0]['id']
    return id

def getFriendsIDs(id):
    response = requests.get(
        'https://api.vk.com/method/friends.get',
        {'user_id' : id,
        'access_token': token,
        'v': 5.103}
        )
    friends = response.json()['response']['items']
    friends = [str(x) for x in friends]
    friends = ','.join(friends)
    return friends

def getUserGroups(id):
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        {'user_id' : id,
        'access_token': token,
        'v': 5.103}
        )
    groups = response.json()['response']['items']
    return groups

def getXorGroups(groups, friends):
    res = user_groups[:]
    for i, group in enumerate(user_groups):
        print(f'\r {i / (len(friends) / 100)}', end='')
        while True:
            try:
                response = requests.get(
                    'https://api.vk.com/method/groups.isMember',
                    {'access_token': token,
                    'v': 5.103,
                    'user_ids': friends,
                    'group_id': group,
                    'extended': 1
                    })
                responses = response.json()['response']
                for resp in responses:
                    if resp['member'] == 1:
                        res.remove(group)
                        break
            except KeyError:
                time.sleep(0.4)
            else:
                break
                responses = response.json()['response']

    return res

def dumper(filename='groups.json'):
    with open(filename, 'w') as f:
        list = []
        for group in res:
            while True:
                try:
                    response = requests.get(
                        'https://api.vk.com/method/groups.getById',
                        {'access_token': token,
                        'v': 5.103,
                        'group_id': group,
                        'fields': 'members_count'}
                        )
                    r = response.json()['response'][0]
                    dictionary = {}
                    dictionary['name'] = r['name']
                    dictionary['gid'] = r['id']
                    dictionary['members_count'] = r['members_count']
                    list.append(dictionary)
                except KeyError:
                    time.sleep(0.4)
                else:
                    break
        json.dump(list, f, ensure_ascii=False, indent = 2)

if __name__ == '__main__':
    adress = input('Enter short adress: ')
    user_id = getUserID(adress)
    friends = getFriendsIDs(user_id)
    user_groups = getUserGroups(user_id)
    res = getXorGroups(user_groups, friends)
    dumper()
