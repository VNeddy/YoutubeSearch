1. 使用pip安装相关moudle
2. `pyi-makespec -D manage.py`
3. urls.py中添加
```python
from django.conf.urls import static
from django.conf import settings

urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
4. manage.spec中添加
```
datas=[(r'C:\Users\harry\Desktop\youtubeSearch\static',r'.\static'), (r'C:\Users\harry\Desktop\youtubeSearch\templates', r'.\templates')],
```
5. `pyinstaller manage.spec`
6. 拷贝config.txt和key到./dist/manage/
7. 创建 YoutubeSearch.py
```python
import os

os.system('manage.exe runserver 127.0.0.1:12345 --noreload')
```
8. 打包
`pyinstaller -F -i youtube_search.ico .\YoutubeSearch.py`
9. 将YoutubeSearch.exe拷贝到manage文件夹
10. 双击YoutubeSearch.exe运行