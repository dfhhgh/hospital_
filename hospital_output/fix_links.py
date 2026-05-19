import glob

for f in glob.glob('templates/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    old1 = "url_for('main.home')"
    old2 = "url_for(\"main.home\")"
    new1 = "url_for('main.home_page')"
    new2 = "url_for(\"main.home_page\")"
    
    if old1 in content or old2 in content:
        content = content.replace(old1, new1).replace(old2, new2)
        with open(f, 'w', encoding='utf-8') as out:
            out.write(content)
        print('Updated ' + f)