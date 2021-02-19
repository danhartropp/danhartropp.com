import re
from os import listdir

target = '\*\*\*main\*\*\*[\s\S]*\*\*\*endmain\*\*\*'

with open('../index.html') as f:
    index_page = f.read()
    
for page in listdir('../read'):
    print('read/' + page)
    with open('../read/' + page, 'r+') as f:
        oldpage = f.read()
        f.seek(0)
        content = re.findall(target, oldpage)[0]
        newpage = re.sub(target,content,index_page)
        f.write(newpage)
        f.truncate()