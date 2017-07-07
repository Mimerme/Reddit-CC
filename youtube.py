import xml.etree.ElementTree as ET
import youtube_dl.youtube_dl.YoutubeDL as ydl
#for encoding parameters
import urllib
#for making the actuall requests
import urllib2
from pycaption import WebVTTReader

#Gets Youtube's Automatic Captions
def get_automatic_captions(video_id):
    ydl_opts = {
        "writeautomaticsub": True,
        "skip_download": True
    }
    parsed = WebVTTReader().read(ydl(ydl_opts).download(["http://www.youtube.com/watch?v=" + video_id]))
    tmp_string = ""
    #Only supports en-US for now
    for caption in parsed.get_captions("en-US"):
        tmp_string = tmp_string + caption.get_text() + " "
    return tmp_string


#Gets possible captions and returns the first result (it should be the default caption i hope)
def get_caption_first_language(videoid):
    list_response = urllib2.urlopen("http://video.google.com/timedtext?type=list&v=" + videoid)
    caption_list_xml = ET.fromstring(list_response.read())
    #Gets first node of track under transcript list
    caption_attrib =  caption_list_xml[0].attrib
    return caption_attrib['lang_code'], caption_attrib['name']

#Gets the manually added captions
def get_captions_no_quota(video_id, include_timestamp=False, include_duration=False):
    caption_language, caption_name = get_caption_first_language(video_id)
    tmp_string = ""
    caption_name = urllib.quote(caption_name)
    response = urllib2.urlopen("http://video.google.com/timedtext?lang=" + caption_language + "&name=" + caption_name + "&v=" + video_id)
    if(response.info().type == "text/xml"):
        captions_xml = ET.fromstring(response.read())
        for caption in captions_xml.iter():
            if(caption.text == None):
                continue
            if include_timestamp:
                tmp_string = tmp_string + (caption.get("start") + "s ") 
            if include_duration:
                tmp_string = tmp_string + (caption.get("dur") + "s ")
            if(include_duration or include_timestamp):
                colon = ":"
            else:
                colon = ""
            tmp_string += colon + unicode(caption.text) + "\n"
        return tmp_string
    else:
        return False