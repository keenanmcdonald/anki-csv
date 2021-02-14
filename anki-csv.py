import os
import csv
import genanki
import datetime

vocab_dir = './'
model_id = 20201207145042
model = genanki.Model(
    model_id,
    'IMMERSION CLUB',
    fields=[
        {'name': 'English'},
        {'name': 'PartOfSpeech'},
        {'name': 'Japanese'},
        {'name': 'Example'},
        {'name': 'Lesson'},
        {'name': 'Audio'},
        {'name': 'Episode'},
        {'name': 'Course'},

    ],
    templates=[{
        'name': '{{English}}',
        'qfmt': '''
            <div class="lesson">
                {{Course}}, Episode {{Episode}}, Lesson {{Lesson}}
            </div>
            <div class="content">
                {{cloze::Example}}
                <br/>
                <div class="pos">
                    ({{PartOfSpeech}})
                </div>
            </div>
            ''',
        'afmt': '''
            <div class="lesson">
                {{Course}}, Episode {{Episode}}, Lesson {{Lesson}}
            </div>
            <div class="content">
                {{cloze::Example}}
                <br/>
                <div class="pos">
                    ({{PartOfSpeech}})
                </div>
                <hr id="answer">
                <div class="inf">
                    {{Japanese}} | {{English}}
                </div>
                <br/>
                <div class="pronunciation">
                    {{Audio}}
                </div>
            </div>
            ''',
    }],
    css= '''
        .card{
            text-align:center;
            font-size:28px;
            background-color:#292F36;
            font-family: sans-serif;
            color: #feffff;
        }
        .content{
            margin-top: 16%;
        }
        .cloze{
            color: #52c3e2 !important;
        }
        .inf *{
            color: #52c3e2;
        } 
        .pos{
            margin-top: 8px;
        }
        .lesson{
            text-align: left;            
            font-size: 16px;
            margin-bottom: 20px;
        }
        ''',
    model_type=1,
)

def sortRows(data):
    lessons = {}
    headers = data[0]
    for row in data[1:]:
        sortedRow = {}
        for i in range(len(row)):
            sortedRow[headers[i].lower()] = row[i]
        if (sortedRow['lesson'] in lessons):
            lessons[sortedRow['lesson']].append(sortedRow)
        else:
            lessons[sortedRow['lesson']] = [sortedRow]
    return lessons

for filename in os.listdir(vocab_dir):
    if filename.endswith('.csv'):
        with open(os.path.join(vocab_dir, filename)) as vocab_file:
            filename = filename[:-4]
            reader = csv.reader(vocab_file, delimiter=',')
            data = list(reader)

            lessons = sortRows(data)
            print(lessons)

            for lesson, cards in lessons.items():
                print(cards[0]['episode'], lesson)
                deck = genanki.Deck(
                    model_id,
                    'Immersion Club::' + cards[0]['course'] + '::Episode ' + f"{int(cards[0]['episode']):02d}" + '::Lesson ' + f'{int(lesson):02d}'
                )
                audio_filenames = []
                i = 0
                for card in cards:
                    note = genanki.Note(
                        model=model,
                        fields=[
                            card['infinitive'],
                            card['part of speech'],
                            card['japanese'], 
                            card['example'], 
                            card['lesson'],
                            '[sound:' + card['audio'] + ']' if ('audio' in card) else '',
                            card['episode'],
                            card['course']
                        ],
                        sort_field = int(card['episode']) * 10000 + int(lesson) * 100 + i
                    )
                    deck.add_note(note)
                    if ('audio' in card and not card['audio'] == ''):
                        audio_filenames.append('./audio_files/' + card['audio'])
                    i+=1

                package = genanki.Package(deck)

                package.media_files = audio_filenames
                
                package.write_to_file('./vocab-decks/' + filename + '_Lesson_' + lesson + '.apkg')
