import csv

import requests

URL = 'https://www.producthunt.com/frontend/graphql'


def get_website(links) -> str:
    '''Getting website from results'''
    results = []
    for item in links:
        if item['storeName'] == 'Website':
            return item['websiteName']
    return ''

def item_to_result(item: dict) -> dict:
    '''Converting item to result dict'''
    links = item.get('links', [])
    url = get_website(links)

    result = {
        'id': item['id'],
        'base_url': f'https://www.producthunt.com/posts/{item["slug"]}',
        'name': item['name'],
        'tagline': item['tagline'],
        'url': url,
        'description': item['description'],
        'updated_at': item['updatedAt'],
    }
    return result

def get_payload() -> str:
    '''Payload loading helper'''
    with open('payload.gql', 'r') as f:
        return f.read()

def get_response(cursor=None) -> dict:
    '''Getting response from ProductHunt GraphQL endpoint'''
    paylaod = get_payload()
    print("Getting cursor: {}".format(cursor))
    response = requests.post(URL, json={'query': paylaod, 'variables': {'cursor': cursor, 'kind': 'POPULAR'}})
    return response.json()


def get_N_pages(n: int) -> list:
    '''Getting N pages of results'''
    results = []
    current_cursor = None

    for i in range(n):
        response = get_response(current_cursor)
        for item in response['data']['homefeed']['edges'][0]['node']['items']:
            if not item.get('name'):
                continue
            results.append(item_to_result(item))
        current_cursor = response['data']['homefeed']['pageInfo']['endCursor']
    
    return results

if __name__ == '__main__':
    results = get_N_pages(100)

    # Writing results to csv
    with open('results.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader()
        for result in results:
            print(result)
            w.writerow(result)
