1. 使用pip安装相关moudle
2. pyi-makespec -D manage.py
3. urls.py中添加
from django.conf.urls import static
from django.conf import settings
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
4. manage.spec中添加
datas=[(r'\\Mac\Home\Downloads\youtubeSearch\static',r'.\static'), (r'\\Mac\Home\Downloads\youtubeSearch\templates', r'.\templates')],
5. pyinstaller manage.spec
6. 拷贝config.txt到./dist/manage/
7. 创建 ./dist/manage/YoutubeSearch.py
import os
os.system('manage.exe runserver 127.0.0.1:12345 --noreload')
8.打包
pyinstaller -F .\YoutubeSearch.py
8. 将YoutubeSearch.exe拷贝到manage文件夹
9. 双击YoutubeSearch.exe运行