from parsel import Selector
import json
from typing import List, Optional


def find_max_dataft(dataft_list):
    mx_lenght = [len(x) for x in dataft_list]
    mx = mx_lenght.index(max(mx_lenght))
    return dataft_list.pop(mx)


def find_dataft(m_source):
    bs = Selector(m_source)
    dataft_list: List[Optional[Selector]] = bs.css("*::attr(data-ft)")
    dataft_list = dataft_list.getall()

    data_ft_raw = {
        'dataft-raw': {},
        'dataft-type': 'n/a'
    }

    tag_style_simplify = 'n/a'

    if len(dataft_list) > 0:
        ft = find_max_dataft(dataft_list)
        js = json.loads(ft, encoding='utf8')

        tag_style = js.get('attached_story_attachment_style')

        if tag_style:
            # ตอนนี้เราสนใจแค่ภาพ หรืออัลบัม
            style_tag_photo = ['photo', 'cover_photo', 'profile_media']
            style_tag_album = ['album', 'new_album']

            if tag_style in style_tag_photo:
                tag_style_simplify = 'photo'
            if tag_style in style_tag_album:
                tag_style_simplify = 'album'

        data_ft_raw['dataft-raw'] = js
        data_ft_raw['dataft-type'] = tag_style_simplify

    return data_ft_raw
