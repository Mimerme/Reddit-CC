import xml.etree.ElementTree as ET
import youtube_dl.youtube_dl.YoutubeDL as ydl
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

#Gets the manually added captions
def get_captions_no_quota(video_id, include_timestamp=False, include_duration=False):
    tmp_string = ""
    response = urllib2.urlopen("http://video.google.com/timedtext?lang=en&v=" + video_id)
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