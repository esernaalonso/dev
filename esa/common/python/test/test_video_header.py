# import urllib2
#
# class HeadRequest(urllib2.Request):
#     def get_method(self):
#         return "HEAD"
#
# url = "http://www.db.insideanim.com/media/campus/tmp/creatures01_lsn01_sbt01_the_basis_of_animal_behavior.flv"
# # url = "http://mydomain.com/thevideofile.mp4"
# head = urllib2.urlopen(HeadRequest(url))
# head.read()          # This will return empty string and closes the connection
# # print head.headers.maintype
# # print head.headers.subtype
# # print head.headers.type
# print head.headers

import pymediainfo
url = "http://www.db.insideanim.com/media/campus/tmp/creatures01_lsn01_sbt01_the_basis_of_animal_behavior.flv"

media_info = pymediainfo.MediaInfo.parse(url)
for track in media_info.tracks:
    if track.track_type == 'Video':
        print track.bit_rate, track.bit_rate_mode, track.codec
