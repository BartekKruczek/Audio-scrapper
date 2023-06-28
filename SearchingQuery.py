from youtubesearchpython import PlaylistsSearch


def search_youtube_playlists(query):
    playlists_search = PlaylistsSearch(
        query, limit=10, language="pl"
    )  # Ograniczamy do 10 wyników
    result = playlists_search.result()

    for playlist in result["result"]:
        title = playlist["title"]
        link = playlist["link"]
        print(f"Title: {title}")
        print(f"Link: {link}")
        print()


# Przykładowe zapytania
search_youtube_playlists("Podcasty")
