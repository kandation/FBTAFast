# Type of Album
ปกติเฟสบุ๊คจะมีประเภทอัลบัมอยู่ 3 แบบ คื pcb, oa ,a  ซึ่ง
~~~~
pcb = อัลบัมรูปที่เป็นส่วนหนึ่งของอับบัม 
เช่น https://www.facebook.com/NhatNguyetKimVuong/posts/2806391479408259

a คือ อัลบัมภาพที่เป็นการสร้างจาก ฟังก์ชั่น Create Album จริงๆ

oa ไม่รู้เหมือนกัน น่าจะเป็น Oathen Alblum มั้ง แต่พบอยู่ในอัลบัมที่สร้างในกลุ่ม

piaarp อันนี้อยู่ใน Fueature album
และประเภทอื่นๆอีกมากมาย ซึ่งคิดว่าไม่น่าสงผลกับ การสำรวจเท่าไร
~~~~

และนอกจากนั้น หากสำรวจใน data-ft  จะมีการบอกใบ้ถึง อัลบัมนั้นๆด้วย จะพบใน `page_insights` กรณีที่มาจากเพจ
และเมื่อมองไปข้างใน
~~~~json
"page_insights" : {
                "147627388735633" : {
                    "page_id" : "147627388735633", 
                    "actor_id" : "100000695314425", 
                    "attached_story" : {
                        "page_id" : "147627388735633", 
                        "actor_id" : "147627388735633", 
                        "dm" : {
                            "isShare" : NumberInt(0), 
                            "originalPostOwnerID" : NumberInt(0)
                        }, 
                        "psn" : "EntAlbumViewCreationStory", 
                        "post_context" : {
                            "object_fbtype" : NumberInt(25), 
                            "publish_time" : NumberInt(1581125812), 
                            "story_name" : "EntAlbumViewCreationStory", 
                            "story_fbid" : [
                                "1521932781305080"
                            ]
                        }, 
                        "role" : NumberInt(1), 
                        "sl" : NumberInt(9)
                    }, 
                    "dm" : {
                        "isShare" : NumberInt(0), 
                        "originalPostOwnerID" : NumberInt(0)
                    }, 
                    "psn" : "EntLikeEdgeStory", 
                    "role" : NumberInt(1), 
                    "sl" : NumberInt(9)
                }
            }, 
            "tn" : "-R"
~~~~

ตรง `post_context.object_fbtype` นั้นระบุเลขที่มีความเกี่ยวข้องกับประเภทอัลบัมไว้ คือ
~~~~
pcb = 266
a = 25
oa = ??
~~~~

# เริ่มต้นการสำรวจ
หากว่าไม่รู้ว่าจะเปิดประเด็นยังไง เริ่มแรกเมื่อเรารู้ประเภทของอัลบัมแล้ว สิ่งต่อไปคือการสังเกตว่า รูปภาพที่เปิดไปมันเชื่อมโยงด้วย param แบบไหน
แน่นอนว่า กดเข้าไปดูรูปภาพนใน www-url  เลย แล้วก็สั่งเกตเอา

จากนั้น ให้ลองดูว่ามันจะสามารถโหลดด้วยกระบวนการใดได้บ้าง lazy load หรือต้องใช้ static