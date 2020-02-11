from urllib.parse import urlencode
import requests
import time
import json


if __name__ == '__main__':
    adress = 'eshmargunov'

    APP_ID = 7315243
    AUTH_URL = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': APP_ID,
        'display': 'page',
        'scope': ('friends', 'groups', 'users'),
        'response_type': 'token',
        'v': 5.103
    }
    #print('?'.join((AUTH_URL, urlencode(params))))
    TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

    response = requests.get(
        'https://api.vk.com/method/users.get',
        {'user_ids': adress,
        'access_token': TOKEN,
        'v': 5.103}
        )
    USER_ID = response.json()['response'][0]['id']
    print(USER_ID)

    response = requests.get(
        'https://api.vk.com/method/friends.get',
        {'user_id' : USER_ID,
        'access_token': TOKEN,
        'v': 5.103}
        )
    FRIENDS = response.json()['response']['items']

    response = requests.get(
        'https://api.vk.com/method/groups.get',
        {'user_id' : USER_ID,
        'access_token': TOKEN,
        'v': 5.103}
        )
    USER_GROUPS = response.json()['response']['items']
    print(USER_GROUPS)
    print((FRIENDS))
    res = USER_GROUPS[:]


    for group in USER_GROUPS:
        for friend in FRIENDS:
            print('*')
            time.sleep(0.3)
            response = requests.get(
                'https://api.vk.com/method/groups.isMember',
                {'access_token': TOKEN,
                'v': 5.103,
                'user_id': friend,
                'group_id': group
                }
                )
            print(response.json()['response'])
            if response.json()['response']:
                res.remove(group)
                break

    list = []

    with open('groups.json', 'w') as f:
        for group in res:
            response = requests.get(
                'https://api.vk.com/method/groups.getById',
                {'access_token': TOKEN,
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
        json.dump(list, f, indent = 2)






'''    for group in USER_GROUPS:
        for friend in FRIENDS:
            time.sleep(0.3)
            print('*')
            response = requests.get(
                'https://api.vk.com/method/groups.isMember',
                {'group_id': group,
                'user_id' : USER_ID,
                'access_token': TOKEN,
                'v': 5.103}
                )
            print(response.json(), group, friend)'''
