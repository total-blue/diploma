from urllib.parse import urlencode
import requests
import time
import json
from extramodule.clint.textui import colored, puts
import random


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
    try:
        response = requests.get(
            'https://api.vk.com/method/users.get',
            {'user_ids': adress,
            'access_token': token,
            'v': 5.103}
            )
        id = response.json()['response'][0]['id']
    except KeyError:
        print('Invalid id!')
    else:
        return id

def getFriendsIDs(id):
    response = requests.get(
        'https://api.vk.com/method/friends.get',
        {'user_id' : id,
        'access_token': token,
        'v': 5.103}
        )
    friends = response.json()['response']['items']
    friends_sep = []
    friends = [str(x) for x in friends]
    while friends:
        if len(friends) > 300:
            friends_sep.append(','.join(friends[:301]))
            friends = friends[301:]
        else:
            friends_sep.append(','.join(friends))
            break
    friends = ','.join(friends_sep)
    return friends_sep


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
    if friends == []:
        return groups
    else:
        res = user_groups[:]
        for group in user_groups:
            puts(getattr(colored, random.choice(colored.COLORS))('\rProcessing...'), newline=False)
            while True:
                try:
                    for friends in friends_sep:
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
                                if not group in res:
                                    break
                                res.remove(group)
                                break
                except KeyError:
                    if response.json()['error']['error_code'] == 6:
                        time.sleep(0.1)
                    else:
                        print('Another exc')
                        break
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
                    puts(getattr(colored, random.choice(colored.COLORS))('\rProcessing...'), newline=False)
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
                except Exception as exc:
                    if 'error' in response.json() and response.json()['error']['error_code'] == 6:
                        time.sleep(0.1)
                    elif response.json()['response'][0]['deactivated'] == 'banned':
                        dictionary['name'] = r['name']
                        dictionary['gid'] = r['id']
                        dictionary['members_count'] = 'banned'
                        list.append(dictionary)
                        break
                    else:
                        print('Unknown exc', exc)
                        break
                else:
                    break
        json.dump(list, f, ensure_ascii=False, indent = 2)

if __name__ == '__main__':
    adress = input('Enter short adress: ')
    user_id = getUserID(adress)
    #print(user_id)
    if user_id:
        friends_sep = getFriendsIDs(user_id)
        user_groups = getUserGroups(user_id)
        #print(user_groups)
        res = getXorGroups(user_groups, friends_sep)
        dumper()
        print('\nDone!')
