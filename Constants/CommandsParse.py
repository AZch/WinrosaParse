class Beton():
    picks = 'picks'
    archive = 'archive'
    xpathPicks = "//*[@class='sport tte soc' or " \
                "@class='location' or " \
                "@class='event_main' or " \
                "@class='event_aux' or " \
                "@class='outcome tte' or " \
                "@class='stake' or " \
                "@class='odds' or " \
                "@class='book' or " \
                "@class='header_inactive']"
    xpathArchive = "//*[@class='subs_table_picks']/table/tbody/tr/td"

resourceNames = [{'name': 'betonsuccess.ru', 'class': Beton}]