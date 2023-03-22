#url for Huntington: https://magicseaweed.com/Huntington-Pier-Surf-Report/286/#Sunday1809
#url for Doheny: https://magicseaweed.com/Doheny-State-Beach-Surf-Report/2588/

import surfsender as ss

def main(url):
    html = ss.html_retriever(url)
    for i in ss.extract_all_surf_data(html):
        print(i)

if __name__ == "__main__":
    
    url = input("Type in a url for your beach: ")
    main(url)