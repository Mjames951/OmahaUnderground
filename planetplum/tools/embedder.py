# using OPENGRAPH: https://pypi.org/project/opengraph/

from opengraph import opengraph

# stolen from: https://github.com/discourse/discourse/blob/64171730827c58df26a7ad75f0e58f17c2add118/lib/onebox/engine/band_camp_onebox.rb#L14
def bandcamp(url):
    video = opengraph.OpenGraph(url)
    if video.is_valid():
        try:

            escaped_src = video.video

            html = f'''<iframe src="{escaped_src}" style="margin: .5rem auto; text-align: center; display:block;" width="{video['video:width']}" height="{video['video:height']}" scrolling="no" frameborder="0" allowfullscreen></iframe>'''
            return html
        except:
            return ""
    
