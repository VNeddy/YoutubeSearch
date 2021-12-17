# -*- coding: utf-8 -*-
import datetime
import os
import sys

import dateutil
import pandas as pd
import numpy as np
import time

from googleapiclient.discovery import build
from django.shortcuts import render
from googleapiclient.errors import HttpError

from youtubeSearch.search_forms import SearchForm

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = ["AIzaSyB6CTCSehDLueyPNQJSceaiLOPex4D9_HM", "AIzaSyBH71H1mVIttpQ7aJDed9kZAa5B_E0MBmg",
                 "AIzaSyADrqKHpaDe2c1cPC4dLzZTlFhBCZW9iOw", "AIzaSyA0TaQGt_5VLGVOsyeuX-RnUK1fn0lyxnk",
                 "AIzaSyAbiadD2bHYoEZ9ekbcsc3uHMmqpMF2mD0", "AIzaSyDAWBROSjGvZu5tNqVwn3Jq3rTOipIr1Dw"]


# 接收POST请求数据
def search_post(request):
    if request.method == "GET":
        form = SearchForm()
        return render(request, "search.html")
    else:
        form = SearchForm(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            ctx = {}
            args = []
            developer_key_list = ["AIzaSyB6CTCSehDLueyPNQJSceaiLOPex4D9_HM", "AIzaSyBH71H1mVIttpQ7aJDed9kZAa5B_E0MBmg",
                                  "AIzaSyADrqKHpaDe2c1cPC4dLzZTlFhBCZW9iOw", "AIzaSyA0TaQGt_5VLGVOsyeuX-RnUK1fn0lyxnk",
                                  "AIzaSyAbiadD2bHYoEZ9ekbcsc3uHMmqpMF2mD0", "AIzaSyDAWBROSjGvZu5tNqVwn3Jq3rTOipIr1Dw"]
            link = "查询失败，请重试！！！"
            with open("config.txt", "r") as f:
                for line in f.readlines():
                    args.append(line.strip('\n'))
            proxy_host = args[0]
            proxy_port = args[1]
            data = form.cleaned_data  # 校验成功的值，会放在cleaned_data里。
            keyword = data.pop('keyword')
            order = data.pop('order')
            scope_start = data.pop('scope_start')
            scope_end = data.pop('scope_end')
            max_result = data.pop('maxResult')
            start_time = time.time()
            while developer_key_list:
                try:
                    developer_key = developer_key_list.pop()
                    is_succeed = youtube_search(developer_key, proxy_host, proxy_port, keyword,
                                                order, scope_start, scope_end, max_result)
                    break
                except HttpError as e:
                    if "quota" in e.content:
                        if developer_key_list:
                            continue

            if is_succeed:
                link = keyword + "-result.xlsx";
                ctx['rlt'] = "查询成功，耗时" + str(round(time.time() - start_time)) + "秒，点击链接下载："
                ctx['rlt1'] = link
            else:
                ctx['rlt1'] = link
            return render(request, "result.html", ctx)
        else:
            errors = form.errors.get("keyword")
        return render(request, "result.html", {"rlt": errors})


def youtube_search(developer_key, proxy_host, proxy_port, key_word, order, scope_start, scope_end, max_result):
    os.environ["http_proxy"] = "http://" + proxy_host + ":" + proxy_port
    os.environ["https_proxy"] = "https://" + proxy_host + ":" + proxy_port
    file_name = key_word + "-result.xlsx"
    f_excel = pd.ExcelWriter(file_name)
    data_excel = []
    scope_start = int(scope_start)
    scope_end = int(scope_end)
    item_list = ["Youtube Id", "主页Link", "粉丝数", "最低views", "最高views", "平均views", "平均likes", "平均comments",
                 "国家", "简介", "注册时间", "1个月内上传视频数", "平均播放量（发布1天内）", "平均播放量（发布1-7天）",
                 "平均播放量（发布1-2周）", "平均播放量（发布2-3周）", "平均播放量（发布3周-1月）", "平均播放量（发布1-2个月）",
                 "平均播放量（发布2-3个月）", "平均播放量（发布3-6个月）"]

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=developer_key)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=key_word,
        part='id,snippet',
        maxResults=max_result,
        order=order
    ).execute()

    channels = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result.get('id', '').get('kind', '') == 'youtube#video' and search_result.get('snippet', '') \
                .get('channelId', '') not in channels:
            channels.append('%s' % (search_result['snippet']['channelId']))

    # 根据channelId获取youtuber信息
    channels_response = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=','.join(channels)
    ).execute()
    for channels_result in channels_response.get('items', []):
        li_data = []
        video_ids = []
        video_ids_1 = []
        video_ids_2 = []
        video_ids_3 = []
        video_ids_4 = []
        video_ids_5 = []
        video_ids_6 = []
        video_ids_7 = []
        video_ids_8 = []
        one_month_video_ids = []
        lowest_views = sys.maxsize
        highest_views = 0
        view_count = 0
        like_count = 0
        comment_count = 0
        view_count_1 = 0
        view_count_2 = 0
        view_count_3 = 0
        view_count_4 = 0
        view_count_5 = 0
        view_count_6 = 0
        view_count_7 = 0
        view_count_8 = 0

        channel_id = channels_result.get('id', '')
        channel_name = channels_result.get('snippet', '').get('title', '')
        channel_description = channels_result.get('snippet', '').get('description', '')
        channel_country = channels_result.get('snippet', '').get('country', '')
        if len(channels_result.get('snippet', '').get('publishedAt', '')) > 20:
            channel_published_at = datetime.datetime.strptime(channels_result['snippet']['publishedAt'],
                                                              "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)
        elif len(channels_result.get('snippet', '').get('publishedAt', '')) == 20:
            channel_published_at = datetime.datetime.strptime(channels_result['snippet']['publishedAt'],
                                                              "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=8)
        else:
            channel_published_at = ''
        channel_view_count = channels_result.get('statistics', '').get('viewCount', '')
        channel_subscriber_count = channels_result.get('statistics', '').get('subscriberCount', '')
        channel_video_count = channels_result.get('statistics', '').get('videoCount', '')
        channel_url = "https://www.youtube.com/channel/" + channel_id + "/about"
        # 获取该youtuber全部playlist
        playlists_response = youtube.playlists().list(
            part="contentDetails",
            channelId=channel_id,
            maxResults=100
        ).execute()
        # 获取该youtuber全部视频列表
        # upload播放列表
        playlist_items_response = youtube.playlistItems().list(
            part='contentDetails,status',
            playlistId=channels_result.get('contentDetails', '').get('relatedPlaylists', '').get('uploads', ''),
            maxResults=100
        ).execute()
        for playlist_items_result in playlist_items_response.get('items', []):
            if playlist_items_result.get('status', '').get('privacyStatus', '') == 'public':
                video_published_at = playlist_items_result.get('contentDetails', '').get('videoPublishedAt', '')
                video_time = datetime.datetime.strptime(video_published_at, "%Y-%m-%dT%H:%M:%SZ") \
                             + datetime.timedelta(hours=8)
                now_time = datetime.datetime.now()
                # 范围内的视频列表
                if scope_start == 1:
                    if now_time - dateutil.relativedelta.relativedelta(months=scope_start) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(months=scope_end) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids:
                        # 保存在scope内的视频
                        video_ids.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                else:
                    if now_time - dateutil.relativedelta.relativedelta(days=scope_start) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(months=scope_end) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids:
                        # 保存在scope内的视频
                        video_ids.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 一个月内的视频列表
                if now_time < video_time + dateutil.relativedelta.relativedelta(months=1) and \
                        playlist_items_result.get('contentDetails', '').get('videoId', '') not in one_month_video_ids:
                    one_month_video_ids.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布1天内
                if now_time < video_time + dateutil.relativedelta.relativedelta(days=1) and \
                        playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_1:
                    video_ids_1.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布1-7天
                if now_time - dateutil.relativedelta.relativedelta(days=1) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(days=7) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_2:
                    video_ids_2.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布1-2周
                if now_time - dateutil.relativedelta.relativedelta(days=7) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(days=14) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_3:
                    video_ids_3.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布2-3周
                if now_time - dateutil.relativedelta.relativedelta(days=14) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(days=21) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_4:
                    video_ids_4.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布3周-1月
                if now_time - dateutil.relativedelta.relativedelta(days=21) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(months=1) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_5:
                    video_ids_5.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布1-2个月
                if now_time - dateutil.relativedelta.relativedelta(months=1) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(months=2) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_6:
                    video_ids_6.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布2-3个月
                if now_time - dateutil.relativedelta.relativedelta(months=2) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(months=3) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_7:
                    video_ids_7.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                # 发布3-6个月
                if now_time - dateutil.relativedelta.relativedelta(months=3) > video_time > \
                        now_time - dateutil.relativedelta.relativedelta(months=6) \
                        and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_8:
                    video_ids_8.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))

        # 其余播放列表
        for playlists_result in playlists_response.get('items', []):
            if playlists_result.get('kind', '') == 'youtube#playlist':
                playlist_items_response = youtube.playlistItems().list(
                    part='contentDetails,status',
                    playlistId=playlists_result.get('id', ''),
                    maxResults=100
                ).execute()

            for playlist_items_result in playlist_items_response.get('items', []):
                if playlist_items_result.get('status', '').get('privacyStatus', '') == 'public':
                    video_published_at = playlist_items_result.get('contentDetails', '').get('videoPublishedAt', '')
                    video_time = datetime.datetime.strptime(video_published_at,
                                                            "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=8)
                    now_time = datetime.datetime.now()
                    # 范围内的视频列表
                    if scope_start == 1:
                        if now_time - dateutil.relativedelta.relativedelta(months=scope_start) > video_time > \
                                now_time - dateutil.relativedelta.relativedelta(months=scope_end) \
                                and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids:
                            # 保存在scope内的视频
                            video_ids.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    else:
                        if now_time - dateutil.relativedelta.relativedelta(days=scope_start) > video_time > \
                                now_time - dateutil.relativedelta.relativedelta(months=scope_end) \
                                and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids:
                            # 保存在scope内的视频
                            video_ids.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 一个月内的视频列表
                    if now_time < video_time + dateutil.relativedelta.relativedelta(months=1) and \
                            playlist_items_result.get('contentDetails', '').get('videoId',
                                                                                '') not in one_month_video_ids:
                        one_month_video_ids.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布1天内
                    if now_time < video_time + dateutil.relativedelta.relativedelta(days=1) and \
                            playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_1:
                        video_ids_1.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布1-7天
                    if now_time - dateutil.relativedelta.relativedelta(days=1) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(days=7) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_2:
                        video_ids_2.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布1-2周
                    if now_time - dateutil.relativedelta.relativedelta(days=7) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(days=14) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_3:
                        video_ids_3.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布2-3周
                    if now_time - dateutil.relativedelta.relativedelta(days=14) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(days=21) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_4:
                        video_ids_4.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布3周-1月
                    if now_time - dateutil.relativedelta.relativedelta(days=21) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(months=1) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_5:
                        video_ids_5.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布1-2个月
                    if now_time - dateutil.relativedelta.relativedelta(months=1) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(months=2) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_6:
                        video_ids_6.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布2-3个月
                    if now_time - dateutil.relativedelta.relativedelta(months=2) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(months=3) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_7:
                        video_ids_7.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))
                    # 发布3-6个月
                    if now_time - dateutil.relativedelta.relativedelta(months=3) > video_time > \
                            now_time - dateutil.relativedelta.relativedelta(months=6) \
                            and playlist_items_result.get('contentDetails', '').get('videoId', '') not in video_ids_8:
                        video_ids_8.append(playlist_items_result.get('contentDetails', '').get('videoId', ''))

        # 计算平均值
        avg_view_count = 0
        avg_like_count = 0
        avg_comment_count = 0
        avg_view_count_1 = 0
        avg_view_count_2 = 0
        avg_view_count_3 = 0
        avg_view_count_4 = 0
        avg_view_count_5 = 0
        avg_view_count_6 = 0
        avg_view_count_7 = 0
        avg_view_count_8 = 0

        # 一次最多查询50个
        if len(video_ids) > 50:
            x = 50
            split_list = lambda video_ids, x: [video_ids[i:i + x] for i in range(0, len(video_ids), x)]
            final_list = split_list(video_ids, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    if int(videos_result.get('statistics', '').get('viewCount', 0)) < lowest_views:
                        lowest_views = int(videos_result.get('statistics', '').get('viewCount', 0))
                    if int(videos_result.get('statistics', '').get('viewCount', 0)) > highest_views:
                        highest_views = int(videos_result.get('statistics', '').get('viewCount', 0))
                    view_count += int(videos_result.get('statistics', '').get('viewCount', 0))
                    like_count += int(videos_result.get('statistics', '').get('likeCount', 0))
                    comment_count += int(videos_result.get('statistics', '').get('commentCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids)
            ).execute()
            for videos_result in videos_response.get('items', []):
                if int(videos_result.get('statistics', '').get('viewCount', 0)) < lowest_views:
                    lowest_views = int(videos_result.get('statistics', '').get('viewCount', 0))
                if int(videos_result.get('statistics', '').get('viewCount', 0)) > highest_views:
                    highest_views = int(videos_result.get('statistics', '').get('viewCount', 0))
                view_count += int(videos_result.get('statistics', '').get('viewCount', 0))
                like_count += int(videos_result.get('statistics', '').get('likeCount', 0))
                comment_count += int(videos_result.get('statistics', '').get('commentCount', 0))
        if len(video_ids) != 0:
            avg_view_count = round(view_count / len(video_ids))
            avg_like_count = round(like_count / len(video_ids))
            avg_comment_count = round(comment_count / len(video_ids))

        if len(video_ids_1) > 50:
            x = 50
            split_list = lambda video_ids_1, x: [video_ids_1[i:i + x] for i in range(0, len(video_ids_1), x)]
            final_list = split_list(video_ids_1, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_1 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_1)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_1 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_1) != 0:
            avg_view_count_1 = round(view_count_1 / len(video_ids_1))

        if len(video_ids_2) > 50:
            x = 50
            split_list = lambda video_ids_2, x: [video_ids_2[i:i + x] for i in range(0, len(video_ids_2), x)]
            final_list = split_list(video_ids_2, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_2 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_2)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_2 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_2) != 0:
            avg_view_count_2 = round(view_count_2 / len(video_ids_2))

        if len(video_ids_3) > 50:
            x = 50
            split_list = lambda video_ids_3, x: [video_ids_3[i:i + x] for i in range(0, len(video_ids_3), x)]
            final_list = split_list(video_ids_3, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_3 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_3)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_3 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_3) != 0:
            avg_view_count_3 = round(view_count_3 / len(video_ids_3))

        if len(video_ids_4) > 50:
            x = 50
            split_list = lambda video_ids_4, x: [video_ids_4[i:i + x] for i in range(0, len(video_ids_4), x)]
            final_list = split_list(video_ids_4, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_4 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_4)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_4 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_4) != 0:
            avg_view_count_4 = round(view_count_4 / len(video_ids_4))

        if len(video_ids_5) > 50:
            x = 50
            split_list = lambda video_ids_5, x: [video_ids_5[i:i + x] for i in range(0, len(video_ids_5), x)]
            final_list = split_list(video_ids_5, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_5 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_5)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_5 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_5) != 0:
            avg_view_count_5 = round(view_count_5 / len(video_ids_5))

        if len(video_ids_6) > 50:
            x = 50
            split_list = lambda video_ids_6, x: [video_ids_6[i:i + x] for i in range(0, len(video_ids_6), x)]
            final_list = split_list(video_ids_6, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_6 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_6)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_6 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_6) != 0:
            avg_view_count_6 = round(view_count_6 / len(video_ids_6))


        if len(video_ids_7) > 50:
            x = 50
            split_list = lambda video_ids_7, x: [video_ids_7[i:i + x] for i in range(0, len(video_ids_7), x)]
            final_list = split_list(video_ids_7, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_7 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_7)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_7 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_7) != 0:
            avg_view_count_7 = round(view_count_7 / len(video_ids_7))

        if len(video_ids_8) > 50:
            x = 50
            split_list = lambda video_ids_8, x: [video_ids_8[i:i + x] for i in range(0, len(video_ids_8), x)]
            final_list = split_list(video_ids_8, x)
            for list in final_list:
                videos_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(list)
                ).execute()
                for videos_result in videos_response.get('items', []):
                    view_count_8 += int(videos_result.get('statistics', '').get('viewCount', 0))
        else:
            videos_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids_8)
            ).execute()
            for videos_result in videos_response.get('items', []):
                view_count_8 += int(videos_result.get('statistics', '').get('viewCount', 0))
        if len(video_ids_8) != 0:
            avg_view_count_8 = round(view_count_8 / len(video_ids_8))

        li_data.append(channel_name)
        li_data.append(channel_url)
        li_data.append(channel_subscriber_count)
        if lowest_views == sys.maxsize:
            lowest_views = 0
        li_data.append(lowest_views)
        li_data.append(highest_views)
        li_data.append(avg_view_count)
        li_data.append(avg_like_count)
        li_data.append(avg_comment_count)
        li_data.append(channel_country)
        li_data.append(channel_description)
        li_data.append(channel_published_at)
        li_data.append(len(one_month_video_ids))
        li_data.append(avg_view_count_1)
        li_data.append(avg_view_count_2)
        li_data.append(avg_view_count_3)
        li_data.append(avg_view_count_4)
        li_data.append(avg_view_count_5)
        li_data.append(avg_view_count_6)
        li_data.append(avg_view_count_7)
        li_data.append(avg_view_count_8)

        data_excel.append(li_data)

    data_df = pd.DataFrame(data_excel)
    data_df.columns = item_list
    data_df.index = np.arange(1, len(data_df) + 1)
    data_df.to_excel(f_excel, float_format='%.5f')
    f_excel.save()
    return True
