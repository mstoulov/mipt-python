from bs4 import BeautifulSoup
import requests
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from pprint import pprint


async def find_link(text):
    # create url
    url = 'https://www.google.com/search?channel=fs&client=ubuntu&q=cppreference+' + text
    # define headers
    headers = {'User-Agent': 'Generic user agent'}
    # get page
    page = requests.get(url, headers=headers)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    # pprint(soup)
    # print()
    # print()
    for link in soup.find_all('a'):
        string = str(link.get('href'))
        if 'https://en.cppreference.com' in string:
            string = string[string.find('https://en.cppreference.com'):]
            ind = string.rfind('/')
            ind1 = string[ind::].find('&')
            ind2 = string[ind::].find('%')
            ind = ind + min(ind1 if ind1 != -1 else len(string),
                            ind2 if ind2 != -1 else len(string))
            return string[:ind]


async def find_header(name):
    url = str(await find_link(name)) + '/any'
    headers = {'User-Agent': 'Generic user agent'}
    try:
        page = requests.get(url, headers=headers, allow_redirects=True)
    except:
        return 'not found'
    soup = str(BeautifulSoup(page.text, 'html.parser'))
    while 'Defined in header' not in soup:
        if url.find('/') == -1:
            return 'not found'
        url = url[:url.rfind('/')]
        try:
            page = requests.get(url, headers=headers, allow_redirects=True)
        except:
            return 'not found'
        soup = str(BeautifulSoup(page.text, 'html.parser'))

    string = soup[soup.find('Defined in header'):]
    string = string[:string.find('</div>')]
    string = string[string.find(';') + 1:string.find('&gt')]
    return 'Defined in header <' + string + '>'


async def handle(msg):
    print(msg)
    # These are some useful variables
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Log variables
    print(content_type, chat_type, chat_id)
    pprint(msg)
    username = msg['chat']['first_name']
    # Check that the content type is text and not the starting
    if content_type == 'text':
        if msg['text'] != '/start':
            text = msg['text']
            # it's better to strip and lower the input
            text = text.strip()
            ans = await find_header(text.lower())
            await bot.sendMessage(chat_id, ans)


TOKEN = '5368574939:AAHWRJ_xvP7rKzrYlR__OUhuLL8MQtVrptI'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

loop.run_forever()
