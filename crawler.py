import requests as rq
from bs4 import BeautifulSoup as bs
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))  # Download stopwords
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"}
page = rq.get('https://www.imdb.com/chart/top/', headers=header)
soup = bs(page.text, 'html.parser')
movie_links = [a['href'] for a in soup.find_all('a', class_="ipc-title-link-wrapper")]

with open('plot_summaries.txt', 'w+', encoding='utf-8') as f:
    for link in movie_links:
        new_page = rq.get('https://m.imdb.com/' + f"{link[:17]}" + 'plotsummary/?ref_=tt_stry_pl', headers=header)
        new_soup = bs(new_page.text, 'html.parser')
        plot_summaries_1 = new_soup.find(class_='sc-a885edd8-9 dcErWY')
        plot_summaries = new_soup.find_all(attrs={'data-testid': "sub-section-summaries"})
        if not plot_summaries:
            new_page = rq.get('https://m.imdb.com/' + f"{link[:18]}" + 'plotsummary/?ref_=tt_stry_pl', headers=header)
            plot_summaries_1 = new_soup.find(class_='sc-a885edd8-9 dcErWY')
            plot_summaries = new_soup.find_all(attrs={'data-testid': "sub-section-summaries"})
        if plot_summaries:
            plat_text_1 = plot_summaries_1.get_text(strip=True, separator='\n')
            plot_text = [p.get_text(strip=True, separator='\n') for p in plot_summaries]
            plot_text_no_punct = [pt.translate(str.maketrans('', '', string.punctuation)) for pt in plot_text]
            words = plot_text_no_punct
            filtered_words = [[word for word in w.split() if word.lower() not in stop_words] for w in words]
            filtered_plot_text = [' '.join(fw) for fw in filtered_words]
            f.write(f'{plat_text_1};{" ".join(filtered_plot_text)};\n')
