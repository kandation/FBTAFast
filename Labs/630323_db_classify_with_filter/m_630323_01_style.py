import json


def find_max_dataft(dataft_list):
    max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
    max_index = max_indexx.index(max(max_indexx))
    return dataft_list[max_index].attrib['data-ft']




def dataparse(ft, doc):
    parse_data = {
        'dataft-raw': '',
        'dataft-type': '',
        'instruct': []
    }

    js = json.loads(ft, encoding='utf8')

    tag_style = js.get('attached_story_attachment_style')

    ppps = [ 'share', 'video_inline', 'animated_image_share',
             'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
            'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note', 'fallback']
    attachment_other = ['unavailable', 'multi_share', 'photo_link_share', 'group_sell_product_item', 'question', 'video',
                     'file_upload', 'story_list', 'image_share', 'group', 'stream_publish']

    if tag_style:
        # ตอนนี้เราสนใจแค่ภาพ หรืออัลบัม
        style_tag_photo = ['photo', 'cover_photo', 'profile_media']
        style_tag_album = ['album', 'new_album']

        if tag_style in style_tag_photo:
            return 'photo'
        if tag_style in style_tag_album:
            return 'album'


    else:
        pass

    # if tag_style in ppps and tag_style is not None:
    #     if tag_style == 'album' or tag_style == 'new_album':
    #         parse_data['dataft-raw'] = js
    #         parse_data['dataft-type'] = tag_style
    #         # collection.update_one({'_id': doc.get('_id')}, {'$set': {'dataft': parse_data}})
    #
    # if tag_style in attachment_other and tag_style is not None:
    #     if tag_style == 'image_share':
    #         print(js)
    # # if k not in ppps+attmaen_othrt and k is not None:
    # #     print(js)


