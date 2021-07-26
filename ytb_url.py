from youtube_search import YoutubeSearch


class Video:
    def __init__(self, title, duration, url_suffix):
        self.title = title
        self.duration = duration
        self.url_suffix = url_suffix
        self.url = 'https://www.youtube.com/' + url_suffix


def get_urls(r, n_v):
    results_list = YoutubeSearch(r, max_results=n_v).to_dict()
    titles = []
    urls = []
    videos = []
    for vid in results_list:
        title = vid['title']
        titles.append(title)
        url = 'https://www.youtube.com/' + vid['url_suffix']
        urls.append(url)
        video = Video(title, vid['duration'], vid['url_suffix'])
    return titles, urls
