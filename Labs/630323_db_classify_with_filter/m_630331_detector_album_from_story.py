def detector():
    sel = Selector(res.text)
    k = sel.css('#objects_container').css('a > img').xpath('.//..')
    if session.get_title() not in page_error_topic:
        try:
            check_link = k[0].attrib
        except:
            print(doc_post)
            print(session.get_title())
            exit()

    """ ถ้าเป็นอับัมรูป มันจะมี role="presentation" นอกนั้นให้เดาเแ็น pcb แต่ถ้าเป็น สนแฟะรนื 6 ก็ oa"""
    # TODO : ให้กลับไปตรวจสอบข้อมูลในDB ว่าจะเป็นประเภทอะไรกันแน่ จากนั้น ก็ค่อยลงมือทำตัวเก็บภาพแบบทีละ 12
    """ ซึ่งจากการคำนวนแล้ว มันสามารถแบ่งรูปไปให้แต่ละ cluster ช่วยโหลดได้ ความเร็วก็จะเพิ่มขึ้นมาก
    แต่ว่าการจะดาวน์โหลดรูปภาพ ควรมีการจัดเก็บด้วยว่า ไม่ใช้อัลบัมที่ซ้ำ จะไได้ไม่ต้องโหลดมาเยอะๆ"""

    """
    หารูปภาพได้แล้ว แต่ยังมีปัญหากับ top-level อยู่ เช่นอัลบัมที่ตัวเองแชร์ เจ้า tlstory มันดันเป็นของตัวเอง
    ไม่ไใช่อัลบัมที่แท้จริง  
    วิธีแก้ก็ ปรับอัลกอให้เข้า original post ไปเลย
    ส่วนวิธีการสำรวจ ไม่ควรใช้ตัวนี้สำรวจ แต่ควรจะ filter หาอัลบัมซ้ำตั้งแต่ขั้นตอน 03 load story แล้ว
    ก็ไปเป็น method  ใหม่ซะนะ
    """
    """
    ปกติแล้วเราจะรู้จำนวนภาพในอัลบัมอยู่แล้ว การทราบ  more_item ก็ไม่จำเป็นเท่าไร
    อีกทั้งการตรวจประเภทอัลบัม นั้นทำมาตั้งนานแล้ว แทบจะเจอข้อมูลแล้วโดยนให้ find12img ทำงานได้เลย

    """
    if '/a.' in check_link.get('href'):
        url_new = f'https://m.facebook.com/media/set/?set=a.{pp}&type=1'
        find12img(url_new)
        # print(check_link)
    elif 'pcb.' in check_link.get('href'):
        url_new = f'https://m.facebook.com/media/set/?set=pcb.{pp}&type=1'
        find12img(url_new)

    else:

        print(check_link)