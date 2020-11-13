from datetime import date, datetime

gemara_lesson_link = 'https://edu-il.zoom.us/wc/join/2960827055'
torah_leeson_link_dov = 'https://edu-il.zoom.us/wc/join/3935560602'
torah_leeson_link_rabinak = 'https://edu-il.zoom.us/wc/join/3422464676?pwd=aUlOWFFjUEx0ak5yalFpTjBHdU1Xdz09'
programming_lesson_link = 'https://edu-il.zoom.us/wc/join/7184928368?pwd=cmZ5Sm9BdXdtWEcrcFBWN0pRRlZjUT09'
math_lesson_link = 'https://edu-il.zoom.us/wc/join/3198379053?pwd=elcrU1Nxb3hpaGNOQzVBNzhiOHR4Zz09'
physics_lesson_link = 'https://zoom.us/wc/join/98729071010?pwd=ajVBbU13bHBqdmhCemlqQWV2aEZFUT09'
english_lesson_link = 'https://edu-il.zoom.us/wc/join/6259151077'
history_lesson_link_itsik = 'https://edu-il.zoom.us/wc/join/3136023920'
# history_lesson_link_tsipi = 'https://chperber.my.webex.com/meet/chperber'
hebrew_lesson_link = 'https://us04web.zoom.us/wc/join/77765386769?pwd=UE51NmNjL2Y1elNlMW0rcXJyUkNWZz09'
literature_lesson_link = 'https://edu-il.zoom.us/wc/join/9655244107?pwd=c1h5RGNyYUs5QndDUHpqTFMyUmFqUT09'


monday = date.today().weekday() == 0
tuesday = date.today().weekday() == 1
wednesday = date.today().weekday() == 2
thursday = date.today().weekday() == 3
sunday = date.today().weekday() == 6


def schedule():
    if sunday:
        return '''\n08:45-10:15: hebrew
10:30-12:00: gemara
12:30-14:00: math
14:30-16:00: english
16:15-17:45: programming
17:55-18:40: programming\n'''
    elif monday:
        return '''\n08:45-10:15: gemara
10:30-11:15: history
11:15-12:00: literature
12:30-13:15: torah dov
13:15-14:00: english
18:30-19:30: programming\n'''
    elif tuesday:
        return '''\n08:45-10:15: history tsipi
10:30-11:15: torah rabinak
11:15-12:00: history itsik
12:30-14:00: physics
14:30-16:00: physics\n'''
    elif wednesday:
        return '''\n08:45-10:15: math
10:30-11:15: literature
11:15-12:00: gemara
12:30-14:00: programming
14:30-16:00: programming\n'''
    elif thursday:
        return '''\n08:45-10:15: gemara
10:30-11:15: gemara
12:30-14:00: physics
14:30-16:00: physics\n'''
    else:
        return ''


def which_lesson(lesson):
    hour_min = datetime.now().strftime('%H:%M')

    lessons = {
        sunday and hour_min >= '08:42' and hour_min <= '10:15': hebrew_lesson_link,
        sunday and hour_min >= '10:27' and hour_min <= '12:00': gemara_lesson_link,
        sunday and hour_min >= '12:27' and hour_min <= '14:00': math_lesson_link,
        sunday and hour_min >= '14:27' and hour_min <= '16:00': english_lesson_link,
        sunday and hour_min >= '16:12' and hour_min <= '17:45': programming_lesson_link,
        sunday and hour_min >= '17:52' and hour_min <= '18:40': programming_lesson_link,

        monday and hour_min >= '08:42' and hour_min <= '10:15': gemara_lesson_link,
        monday and hour_min >= '10:27' and hour_min <= '11:15': history_lesson_link_itsik,
        monday and hour_min > '11:15' and hour_min <= '12:00': literature_lesson_link,
        monday and hour_min >= '12:27' and hour_min < '13:15': torah_leeson_link_dov,
        monday and hour_min >= '13:15' and hour_min <= '14:00': english_lesson_link,

        # tuesday and hour_min >= '08:42' and hour_min <= '10:15': history_lesson_link_tsipi,
        tuesday and hour_min >= '10:27' and hour_min < '11:15': torah_leeson_link_rabinak,
        tuesday and hour_min >= '11:15' and hour_min <= '12:00': history_lesson_link_itsik,
        tuesday and hour_min >= '12:27' and hour_min <= '14:00': physics_lesson_link,
        tuesday and hour_min >= '14:27' and hour_min <= '16:00': physics_lesson_link,

        wednesday and hour_min >= '08:42' and hour_min <= '10:15': math_lesson_link,
        wednesday and hour_min >= '10:27' and hour_min < '11:15': literature_lesson_link,
        wednesday and hour_min >= '11:15' and hour_min <= '12:00': gemara_lesson_link,
        wednesday and hour_min >= '12:27' and hour_min <= '14:00': programming_lesson_link,
        wednesday and hour_min >= '14:27' and hour_min <= '16:00': programming_lesson_link,

        thursday and hour_min >= '08:42' and hour_min <= '10:15': gemara_lesson_link,
        thursday and hour_min >= '10:27' and hour_min <= '11:15': gemara_lesson_link,
        thursday and hour_min >= '12:27' and hour_min <= '14:00': physics_lesson_link,
        thursday and hour_min >= '14:27' and hour_min <= '16:00': physics_lesson_link,
    }
    return lessons.get(lesson, False)
