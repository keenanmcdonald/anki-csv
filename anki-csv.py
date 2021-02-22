import os
import os.path
import csv
import genanki
import datetime
import hashlib

vocab_dir = './vocab-list'
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
    episodes = {}
    headers = data[0]
    for row in data[1:]:
        sortedRow = {}
        for i in range(len(row)):
            sortedRow[headers[i].lower()] = row[i]
        
        if (sortedRow['episode'] in episodes):
            if (sortedRow['lesson'] in episodes[sortedRow['episode']]):
                episodes[sortedRow['episode']][sortedRow['lesson']].append(sortedRow)
            else:
                episodes[sortedRow['episode']][sortedRow['lesson']] = [sortedRow]
        else:
            episodes[sortedRow['episode']] = {}
    return episodes

decks = []
audio_files = []


for filename in os.listdir(vocab_dir):
    if filename.endswith('.csv'):
        with open(os.path.join(vocab_dir, filename)) as vocab_file:
            filename = filename[:-4]
            reader = csv.reader(vocab_file, delimiter=',')
            data = list(reader)

            episodes = sortRows(data)

            for episode, lessons in episodes.items():
                for lesson, cards in lessons.items():
                    deck_name = 'Immersion Club::' + cards[0]['course'] + '::Episode ' + f"{int(cards[0]['episode']):02d}" + '::Lesson ' + f'{int(lesson):02d}'
                    deck_id = hash(deck_name)
                    deck = genanki.Deck(
                        deck_id,
                        deck_name
                    )
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
                            path = './audio_files/' + card['audio']
                            if (os.path.exists(path)):
                                audio_files.append(path)
                            else:
                                print('FILE NOT FOUND: ' + 'episode ' +  card['episode'] + ':  ' + path)
                        i+=1
                    decks.append(deck)

print(audio_files)
package = genanki.Package(decks)
package.media_files = audio_files

if not os.path.exists('vocab-decks'):
    os.makedirs('vocab-decks')

package.write_to_file('./vocab-decks/' + filename + '.apkg')

