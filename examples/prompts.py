"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
#!/usr/bin/env python3
import textwrap

FA_TOKENS = {
    "arabic": ("السؤال:", "الإجابة:"),
    "bengali": ("প্র:", "উ:"),
    "cantonese": ("問題：", "答案:"),
    "czech": ("Otázka:", "Odpověď:"),
    "dutch": ("Vraag:", "Antwoord:"),
    "english": ("Q:", "A:"),
    "french": ("Q :", "R :"),
    "hebrew": ("שאלה", "תשובה"),
    "hindi": ("सवाल:", "जवाब:"),
    "italian": ("D:", "R:"),
    "indonesian": ("T:", "J:"),
    "farsi": ("سؤال:", "جواب:"),
    "german": ("F:", "A:"),
    "japanese": ("質問：", "回答："),
    "khmer": ("សំណួរ៖", "ចម្លើយ៖"),
    "korean": ("질문:", "답:"),
    "malay": ("Soalan:", "Jawapan:"),
    "marathi": ("प्रश्न:", "उत्तर:"),
    "polish": ("Pytanie:", "Odpowiedź:"),
    "portuguese": ("Pergunta:", "Resposta:"),
    "romanian": ("Întrebare:", "Răspuns:"),
    "russian": ("Вопрос:", "Ответ:"),
    "simplified_mandarin": ("问题：", "答案："),
    "spanish": ("Pregunta:", "Respuesta:"),
    "swedish": ("Fråga:", "Svar:"),
    "tagalog": ("T:", "S:"),
    "thai": ("คำถาม:", "คำตอบ:"),
    "traditional_mandarin": ("問題：", "答案："),
    "turkish": ("S:", "C:"),
    "vietnamese": ("H:", "Đ:"),
    "urdu": ("سوال:", "جواب:"),
}

fewshot = {
    "arabic": textwrap.dedent(
        """
            {% for x in few_shot -%}
            يرجى الإجابة عن السؤال التالي بإيجاز قدر الإمكان. يجب أن تكون الإجابة في شكل {{ x["output_type"] }}
            السؤال: {{ x["question"] }}
            الإجابة: {{ x["answer"] }}

            {% endfor -%}
            يرجى الإجابة عن السؤال التالي بإيجاز قدر الإمكان. يجب أن تكون الإجابة في شكل {{ output_type }}.
            السؤال: {{ question }}
            الإجابة:"""
    ),
    "bengali": textwrap.dedent(
        """
            {% for x in few_shot -%}
            প্র: {{ x["question"] }} শুধু একটি{{ x["output_type"] }}দাও
            উ: {{ x["answer"] }}
            {% endfor -%}

            প্র: {{ question }} শুধু একটি{{ output_type }}দাও
            উ:"""
    ),
    "cantonese": textwrap.dedent(
        """
            {% for x in few_shot -%}
            問題：{{ x["question"] }}只係產生一個{{ x["output_type"] }}就得。同埋要用廣東話口語回答。
            答案：{{ x["answer"] }}

            {% endfor -%}

            問題：{{ question }}只係產生一個{{ output_type }}就得。同埋要用廣東話口語回答。
            答案："""
    ),
    "czech": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Odpověz na otázku stručně a jasně. Odpovědí může být jen {{ x["output_type"] }}
            Otázka: {{ x["question"] }}
            Odpověď: {{ x["answer"] }}

            {% endfor -%}
            Odpověz na otázku stručně a jasně. Odpovědí může být jen {{ output_type }}.
            Otázka: {{ question }}
            Odpověď:"""
    ),
    "dutch": textwrap.dedent(
        """\
            Beantwoord de volgende vraag zo kort en bondig mogelijk.

            {% for x in few_shot -%}
            Vraag: {{ x["question"] }} Antwoord met alleen een {{ x["output_type"] }}.
            Antwoord: {{ x["answer"] }}
            {% endfor -%}

            Vraag: {{ question }} Antwoord met alleen {{ output_type }}.
            Antwoord:"""
    ),
    "english": textwrap.dedent(
        """\
            Answer the given question as concisely as possible.

            {% for x in few_shot -%}
            Q: {{ x["question"] }} Produce only a {{ x["output_type"] }}.
            A: {{ x["answer"] }}

            {% endfor -%}

            Q: {{ question }} Produce only {{ output_type }}.
            A:"""
    ),
    "farsi": textwrap.dedent(
        """
            {% for x in few_shot -%}
            به این سؤال تا حد امکان دقیق پاسخ دهید
            سؤال: {{ x["question"] }} فقط با {{ x["output_type"] }} پاسخ دهید.
            جواب: {{ x["answer"] }}

            {% endfor -%}
            به این سؤال تا حد امکان دقیق پاسخ دهید
            سؤال: {{ question }} فقط با {{ output_type }} پاسخ دهید.
            جواب:"""
    ),
    "french": textwrap.dedent(
        """\
            {% for x in few_shot -%}
            Q : {{ x["question"] }} Ta réponse doit être du type : {{ x["output_type"] }}.
            R : {{ x["answer"] }}

            {% endfor -%}

            Q : {{ question }} Ta réponse doit être du type : {{ output_type }}.
            R :"""
    ),
    "hebrew": textwrap.dedent(
        """
            {% for x in few_shot -%}
            יש לענות על השאלה הבאה בקצרה ככל הניתן.
            שאלה: {{ x["question"] }} התשובה צריכה להיות {{ x["output_type"] }}.
            תשובה: {{ x["answer"] }}

            {% endfor -%}
            יש לענות על השאלה הבאה בקצרה ככל הניתן.
            שאלה: {{ question }} התשובה צריכה להיות {{ output_type }}.
            תשובה:"""
    ),
    "german": textwrap.dedent(
        """\
            Bitte beantworte die folgende Frage so kurz und knapp wie möglich.

            {% for x in few_shot -%}
            F: {{ x["question"] }} Gib deine Antwort nur als {{ x["output_type"] }}.
            A: {{ x["answer"] }}

            {% endfor -%}

            F: {{ question }} Schreibe deine Antwort als {{ output_type }}.
            A:"""
    ),
    "hindi": textwrap.dedent(
        """
            {% for x in few_shot -%}
            सवाल: {{ x["question"] }} जवाब में सिर्फ़ {{ x["output_type"] }} बताओ.
            जवाब: {{ x["answer"] }}
            {% endfor -%}

            सवाल: {{ question }} जवाब में सिर्फ़ {{ output_type }} बताओ.
            जवाब:"""
    ),
    "indonesian": textwrap.dedent(
        """
            {% for x in few_shot -%}
            T: Jawab dengan {{ x["output_type"] }} saja. {{ x["question"] }}
            J: {{ x["answer"] }}

            {% endfor -%}

            T: Jawab dengan {{ output_type }} saja. {{ question }}
            J:"""
    ),
    "italian": textwrap.dedent(
        """\
            {% for x in few_shot -%}
            Rispondi alla seguente domanda in modo chiaro e conciso.
            D: {{ x["question"] }} Produci solo risposte del seguente tipo: {{ x["output_type"] }}.
            R: {{ x["answer"] }}

            {% endfor -%}

            D: {{ question }} Produci solo risposte del seguente tipo: {{ output_type }}.
            R:"""
    ),
    "japanese": textwrap.dedent(
        """\
            {% for x in few_shot -%}
            質問：{{ x["question"] }}{{ x["output_type"] }}だけを答えてください。
            回答：{{ x["answer"] }}

            {% endfor -%}

            質問：{{ question }}{{ output_type }}だけを答えてください。
            回答："""
    ),
    "khmer": textwrap.dedent(
        """
            {% for x in few_shot -%}
            សូម​ឆ្លើ​យសំណួរ​ខាងក្រោម​ដោយស​ង្ខេប និងច្បាស់លាស់​​តាម​ដែល​អាច​ធ្វើទៅបាន។
            សំណួរ៖ {{ x["question"] }} សរសេរចម្លើយរបស់អ្នកជា {{ x["output_type"] }}។
            ចម្លើយ៖ {{ x["answer"] }}

            {% endfor -%}
            សូម​ឆ្លើ​យសំណួរ​ខាងក្រោម​ដោយស​ង្ខេប និងច្បាស់លាស់​​តាម​ដែល​អាច​ធ្វើទៅបាន។
            សំណួរ៖ {{ question }}. សរសេរចម្លើយរបស់អ្នកជា {{ output_type }}។
            ចម្លើយ៖"""
    ),
    "korean": textwrap.dedent(
        """\
            {% for x in few_shot -%}
            질문: {{ x["question"] }}{{ x["output_type"] }}(으)로 간단히 대답해줘.
            답: {{ x["answer"] }}

            {% endfor -%}

            질문: {{ question }}{{ output_type }}(으)로 간단히 대답해줘.
            답:"""
    ),
    "malay": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Sila jawab soalan yang berikut secara ringkas dan padat.
            Soalan: {{ x["question"] }} Tulis jawapan anda sebagai {{ x["output_type"] }}
            Jawapan: {{ x["answer"] }}

            {% endfor -%}
            Sila jawab soalan yang berikut secara ringkas dan padat.
            Soalan: {{ question }}. Tulis jawapan anda sebagai {{ output_type }}.
            Jawapan:"""
    ),
    "marathi": textwrap.dedent(
        """
            {% for x in few_shot -%}
            प्रश्न: {{ x["question"] }} {{ x["output_type"] }} सांगा.
            उत्तर: {{ x["answer"] }}

            {% endfor -%}

            प्रश्न: {{ question }} {{ output_type }} सांगा.
            उत्तर:"""
    ),
    "polish": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Odpowiedz możliwie krótko na następujące pytanie.
            Pytanie: {{ x["question"] }} Oczekiwana odpowiedź to {{ x["output_type"] }}
            Odpowiedź: {{ x["answer"] }}

            {% endfor -%}
            Odpowiedz możliwie krótko na następujące pytanie.
            Pytanie: {{ question }} Oczekiwana odpowiedź to {{ output_type }}.
            Odpowiedź:"""
    ),
    "portuguese": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Pergunta: {{ x["question"] }} A resposta deve ser somente do seguinte tipo: {{ x["output_type"] }}.
            Resposta: {{ x["answer"] }}
            {% endfor -%}

            Pergunta: {{ question }} A resposta deve ser somente do seguinte tipo: {{ output_type }}.
            Resposta:"""
    ),
    "romanian": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Te rog să răspunzi la următoarea întrebare cât mai concis posibil.
            Întrebare: {{ x["question"] }} Răspunsul trebuie să fie {{ x["output_type"] }}
            Răspuns: {{ x["answer"] }}

            {% endfor -%}
            Te rog să răspunzi la următoarea întrebare cât mai concis posibil.
            Întrebare: {{ question }}. Răspunsul trebuie să fie {{ output_type }}.
            Răspuns:"""
    ),
    "russian": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Вопрос: {{ x["question"] }} Дай ответ в формате: {{ x["output_type"] }}.
            Ответ: {{ x["answer"] }}

            {% endfor -%}

            Вопрос: {{ question }} Дай ответ в формате: {{ output_type }}.
            Ответ:"""
    ),
    "simplified_mandarin": textwrap.dedent(
        """
            {% for x in few_shot -%}
            问题：{{ x["question"] }}只产生一个{{ x["output_type"] }}即可。
            答案：{{ x["answer"] }}

            {% endfor -%}

            问题：{{ question }}只产生一个{{ output_type }}即可。
            答案："""
    ),
    "spanish": textwrap.dedent(
        """\
            {% for x in few_shot -%}
            Pregunta: {{ x["question"] }} La respuesta debe ser del siguiente tipo: {{ x["output_type"] }}.
            Respuesta: {{ x["answer"] }}

            {% endfor -%}

            Pregunta: {{ question }} La respuesta debe ser del siguiente tipo: {{ output_type }}.
            Respuesta:"""
    ),
    "swedish": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Svara på den här frågan så kort och koncist som möjligt.
            Fråga: {{ x["question"] }} Svara med {{ x["output_type"] }}
            Svar: {{ x["answer"] }}

            {% endfor -%}
            Svara på den här frågan så kort och koncist som möjligt.
            Fråga: {{ question }}. Svara med {{ output_type }}.
            Svar:"""
    ),
    "tagalog": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Sagutin ang tanong ng pinakatumpak na sagot. Nasa {{ x["output_type"] }} na format lamang dapat ang sagot.
            T: {{ x["question"] }}.
            S: {{ x["answer"] }}

            {% endfor -%}
            Sagutin ang tanong ng pinakatumpak na sagot. Nasa {{ output_type }} na format lamang dapat ang sagot.
            T: {{ question }}.
            S:"""
    ),
    "thai": textwrap.dedent(
        """
            {% for x in few_shot -%}
            ช่วยตอบคำถามนี้แบบสั้นๆ หน่อย
            คำถาม: {{ x["question"] }}เขียนคำตอบเป็น{{ x["output_type"] }}
            คำตอบ: {{ x["answer"] }}

            {% endfor -%}
            ช่วยตอบคำถามนี้แบบสั้นๆ หน่อย
            คำถาม: {{ question }}เขียนคำตอบเป็น{{ output_type }}
            คำตอบ:"""
    ),
    "traditional_mandarin": textwrap.dedent(
        """
            {% for x in few_shot -%}
            問題：{{ x["question"] }} 只產生一個{{ x["output_type"] }}即可。
            答案：{{ x["answer"] }}

            {% endfor -%}

            問題：{{ question }} 只產生一個{{ output_type }}即可。
            答案："""
    ),
    "turkish": textwrap.dedent(
        """
            {% for x in few_shot -%}
            Lütfen aşağıdaki soruyu mümkün olan en kısa şekilde cevaplayın. Cevap bir {{ x["output_type"] }} olmalıdır.
            S: {{ x["question"] }}.
            C: {{ x["answer"] }}

            {% endfor -%}
            Lütfen aşağıdaki soruyu mümkün olan en kısa şekilde cevaplayın. Cevap bir {{ output_type }} olmalıdır.
            S: {{ question }}.
            C:"""
    ),
    "urdu": textwrap.dedent(
        """
            {% for x in few_shot -%}
            دیئے گئے سوال کا ہر ممکن حد تک مختصر جواب دیں۔
            سوال: {{ x["question"] }} صرف {{ x["output_type"] }} تیارکریں۔
            جواب: {{ x["answer"] }}

            {% endfor -%}
            دیئے گئے سوال کا ہر ممکن حد تک مختصر جواب دیں۔
            سوال: {{ question }} صرف {{ output_type }} تیارکریں۔
            جواب:"""
    ),
    "vietnamese": textwrap.dedent(
        """
            {% for x in few_shot -%}
            H: {{ x["question"] }} Chỉ nêu {{ x["output_type"] }}.
            Đ: {{ x["answer"] }}

            {% endfor -%}

            H: {{ question }} Chỉ nêu {{ output_type }}.
            Đ:"""
    ),
}

fewshot_examples = {
    "arabic": [
        {"question": "كم مرة فازت مصر بكأس الأمم الأفريقية لكرة القدم؟", "answer": "7", "output_type": "رقم"},
        {"question": " متى تم افتتاح المتحف المصري بالقاهرة؟", "answer": "1902", "output_type": "تاريخ"},
        {"question": " من الذي بنى الجامع الأزهر؟", "answer": "جوهر الصقلي", "output_type": "اسم"},
        {"question": "أين ولد العالم المصري أحمد زويل؟", "answer": "دمنهور", "output_type": "مكان"},
        {"question": "من هو أول رئيس لمصر؟", "answer": "محمد نجيب", "output_type": "اسم"},
        ],
    "bengali" : [
        {"question": "বাংলাদেশের জনসংখ্যা কত?",  "answer": "17.12", "output_type": "সংখ্যা"},
        {"question": "ভারতের কোন রাজ্যে জনঘনত্ব সর্বাধিক?",  "answer": "উত্তরপ্রদেশ", "output_type": "নাম"},
        {"question": "পশ্চিমবঙ্গের সাক্ষরতার হার কত?", "answer": "76.26", "output_type": "সংখ্যা"},
        {"question": "পশ্চিমবঙ্গের প্রথম মুখ্যমন্ত্রী কে? ", "answer": "প্রফুল্লচন্দ্র ঘোষ",  "output_type": "নাম"},
        {"question": "পশ্চিমবঙ্গের জনঘনত্ব কত?", "answer": "1029", "output_type": "সংখ্যা"},
        ],
    "cantonese" : [
        {"question": "王菲係邊一年出道？", "answer": "1989", "output_type": "數字"},
        {"question": "香港係2024年巴黎奧運攞到幾面金牌？", "answer": "2", "output_type": "數字"},
        {"question": "人生嘅意義係乜？", "answer": "42", "output_type": "數字"},
        {"question": "李小龍係邊一年出世？ ", "answer": "1940", "output_type": "數字"},
        {"question": "周星馳係2004年電影《功夫》入面叫咩名？", "answer": "阿星", "output_type": "名"},
        ],
    "czech" : [
        {"question": "Ve kterém roce vyhrál český národní hokejový tým turnaj na Zimních olympijských hrách v Naganu?", "answer": "1998", "output_type": "číslo"},
        {"question": "Ve kterém městě se narodil skladatel Bedřich Smetana?", "answer": "Litomyšl", "output_type": "místo"},
        {"question": "Který den byl vyhlášen samostatný československý stát?", "answer": "28. října 1918", "output_type": "datum"},
        {"question": "Jak se jmenoval panovník, který v roce 1348 založil Pražskou univerzitu, dnes známou pod názvem Univerzita Karlova?", "answer": "Karel IV", "output_type": "jméno"},
        {"question": "Jak se nazývá současný největší výrobce automobilů v Česku, který sídlí v Mladé Boleslavi?", "answer": "Škoda Auto", "output_type": "název"},
        ],
    "dutch" : [
        {"question": "Op welke datum werd Nederland bevrijd van de Duitsers in de tweede wereld oorlog?", "answer": "5 mei 1945", "output_type": "datum"},
        {"question": "Voor hoeveel verschillende landen heeft Johan Cruiff professioneel gevoetbald?", "answer": "3", "output_type": "getal"},
        {"question": "Uit welke taal stamt de bekendste informele bijnaam van de stad Amsterdam?", "answer": "Hebreeuws", "output_type": "woord"},
        {"question": "Hoeveel jaar was Beatrix koningin van Nederland?", "answer": "33", "output_type": "getal"},
        {"question": "Hoe heet het derde kind van André Hazes?", "answer": "Roxeanne Hazes", "output_type": "naam"},
        ],
    "english": [
        {
            "question": "What is the human life expectancy in the United States in 2019?",
            "answer": "78",
            "output_type": "number",
        },
        {
            "question": "Who was president of the United States in 1955?",
            "answer": "Dwight D. Eisenhower",
            "output_type": "name",
        },
        {"question": "What is the square root of four?", "answer": "2", "output_type": "Number"},
        {"question": "When was Benitto Mussolini born?", "answer": "July 29, 1883", "output_type": "date"},
        {"question": "When were the Olympics held in Barcelona, ​​Spain?", "answer": "1992", "output_type": "year"},
    ],
    "farsi": [
        {"question": "لطفاً به این سؤال تا حد امکان مختصر پاسخ دهید. محمدرضا پهلوی، شاه ایران، در چه سالی به دنیا آمده است؟", "answer": "۱۹۱۹", "output_type": "عدد"},
        {"question": "لطفاً به این سؤال تا حد امکان مختصر پاسخ دهید. نخستین رئیس‌جمهور ایران بعد از انقلاب اسلامی چه کسی بود؟", "answer": "ابوالحسن بنی‌صدر", "output_type": "نام"},
        {"question": "لطفاً به این سؤال تا حد امکان مختصر پاسخ دهید. پروین اعتصامی، شاعر مشهور ایرانی، در چه تاریخی درگذشت؟", "answer": "۲۸ فروردین ۱۳۴۵", "output_type": "تاریخ"},
        {"question": "لطفاً به این سؤال تا حد امکان مختصر پاسخ دهید. انفجاری که در سال ۱۳۶۰ منجر به مرگ برخی از چهره‌های سیاسی ایران شد در کجا رخ داد؟", "answer": "مکان", "output_type": "دفتر حزب جمهوری اسلامی"},
        {"question": "لطفاً به این سؤال تا حد امکان مختصر پاسخ دهید. ناصر حجازی در چند دوره از جام جهانی فوتبال شرکت کرده است؟", "answer": "عدد", "output_type": "۴"},
        ],
    "french": [
        {"question": "Combien d'ingrédients trouve-t-on dans un quatre-quart ?", "answer": "4", "output_type": "nombre"},
        {"question": "Qui est élu président de la République française en 1995 ?", "answer": "Jacques Chirac", "output_type": "nom"},
        {"question": "Quelle est la date du début de la Révolution Française ?", "answer": "1789", "output_type": "date"},
        {"question": "Qui était le président de la République française de 1981 à 1995 ?", "answer": "François Mitterrand", "output_type": "nom complet"},
        {"question": "Combien de médailles d'or la France a-t-elle remportées lors des Jeux Olympiques de Paris 2024 ?", "answer": "16", "output_type": "nombre"},
        ],
    "german": [
        {"question": "Wie lautet die Hauptstadt von Thüringen?", "answer": "Erfurt", "output_type": "Namen"},
        {"question": "Wie viele Kantone hat die Schweiz?", "answer": "26", "output_type": "Zahl"},
        {"question": "In welchem Jahr gewann Lena Mayer-Landrut den Eurovision Song Contest?", "answer": "2010", "output_type": "Zahl"},
        {"question": "Wer war 1970 deutscher Bundespräsident?", "answer": "Gustav Heinemann", "output_type": "Namen"},
        {"question": "Wie heißt das 2016 fertiggestellte Konzerthaus in Hamburg?", "answer": "Elbphilharmonie", "output_type": "Namen"},
        ],
    "hebrew": [
        {"question": "מי היה ראש הממשלה הראשון של מדינת ישראל?", "answer": "דוד בן-גוריון", "output_type": "שם של אדם"},
        {"question": "מתי הוקמה מדינת ישראל?", "answer": "14 במאי 1948", "output_type": "תאריך"},
        {"question": "לפי ספר בראשית, כמה גרסאות יש לסיפור בריאת העולם?", "answer": "שתיים", "output_type": "מספר"},
        {"question": "מי זכה במקום הראשון בגמר העונה הראשונה של התוכנית ״כוכב נולד״?", "answer": "נינט טייב", "output_type": "שם של אדם"},
        {"question": "באיזו חברה יצא אלבומו השני של דורי בן-זאב?", "answer": "התקליט", "output_type": "שם של חברה"},
        ],
    "hindi": [
        {"question": "भारत के पहले प्रधानमंत्री का क्या नाम था?", "answer": "पंडित जवाहर लाल नेहरू", "output_type": "नाम"},
        {"question": "हिन्दी वर्णमाला में कितने वर्ण होता हैं?", "answer": "52", "output_type": "संख्या"},
        {"question": "भारत में वोट देने की कम से कम उम्र क्या है?", "answer": "21", "output_type": "संख्या "},
        {"question": "ताज महल कहाँ स्थित है?", "answer": "आगरा", "output_type": "शहर"},
        {"question": "भारत के किस राज्य को फलों का कटोरा कहा जाता है? ", "answer": "हिमाचल प्रदेश", "output_type": "नाम"},
        ],
    "indonesian": [
        {"question": "Ada berapa shio dalam zodiak China?", "answer": "12", "output_type": "angka"},
        {"question": "Siapa presiden pertama Republik Indonesia?", "answer": "Soekarno", "output_type": "nama"},
        {"question": "Berapa tinggi Gunung Rinjani?", "answer": "3.726 mdpl", "output_type": "angka"},
        {"question": "Di mana Bandara I Gusti Ngurah Rai?", "answer": "Bali", "output_type": "lokasi"},
        {"question": "Berapa titik didih air?", "answer": "100", "output_type": "angka"},
        ],
    "italian": [
        {"question": "Quando si festeggia Ferragosto?", "answer": "15 agosto", "output_type": "data"},
        {"question": "Quando ha vinto l'Italia per l'ultima volta i mondiali di calcio?", "answer": "2006", "output_type": "data"},
        {"question": "Quale moneta aveva l'Italia prima dell'euro?", "answer": "Lira", "output_type": "nome"},
        {"question": "Come si chiama il primo Presidente della Repubblica italiana?", "answer": "Enrico De Nicola", "output_type": "nome"},
        {"question": "Quando è la Festa della Repubblica in Italia?", "answer": "2 giugno", "output_type": "data"},
        ],
    "japanese": [
        {"question": "日本で一番高い山はなんですか？", "answer": "富士山", "output_type": "名前"},
        {"question": "士急ハイランドはどこにありますか？", "answer": "山梨県富士吉田市", "output_type": "場所"},
        {"question": "あきたこまちが開発されたのは何年ですか？", "answer": "1984", "output_type": "数字"},
        {"question": "枕草子の作者は誰ですか？", "answer": "清少納言", "output_type": "名前"},
        {"question": "日本で一番長い川はなんですか？", "answer": "信濃川", "output_type": "名前"},
        ],
    "khmer": [
        {"question": "តើប្រទេសកម្ពុជាធ្វើជាម្ចាស់ផ្ទះក្នុងការប្រកួតកីឡាប្រជាជាតិអាស៊ីអាគ្នេយ៍នៅឆ្នាំណា?", "answer": "2023", "output_type": "លេខ"},
        {"question": "តើបាវចនារបស់ព្រះរាជាណាចក្រកម្ពុជាមានអ្វីខ្លះ?", "answer": "ជាតិ សាសនា ព្រះមហាក្សត្រ", "output_type": "ពាក្យ"},
        {"question": "តើប្រទេសកម្ពុជាមានផ្ទៃដីសរុបចំនួនប៉ុន្មានគីឡូម៉ែត្រការ៉េ?", "answer": "181035", "output_type": "លេខ"},
        {"question": "តើការបោះឆ្នោត​ជ្រើសរើសតាំតំណាងរាស្រ្ដអាណត្តិទី៧ប្រព្រឹត្តិទៅនៅថ្ងៃខែឆ្នាំណា?​", "answer": "23/07/2023", "output_type": "កាលបរិច្ឆេទ"},
        {"question": "តើប្រទេសកម្ពុជាមានប្រាសាទសរុបចំនួនប៉ុន្មាន?", "answer": "1080", "output_type": "លេខ"},
        ],
    "korean": [
        {"question": "한라산의 높이는?", "answer": "1,947m", "output_type": "숫자"},
        {"question": "대한민국 대통령의 임기는?", "answer": "5년", "output_type": "숫자"},
        {"question": "현재 대한민국 대통령은?", "answer": "윤석열", "output_type": "이름"},
        {"question": "2028년 올림픽은 어디서 개최되나요?", "answer": "로스엔젤레스", "output_type": "장소"},
        {"question": "하버드 대학교는 몇 년도에 설립됐나요?", "answer": "1636", "output_type": "숫자"},
        ],
    "malay": [
        {"question": "Berapakah jalur yang terdapat pada bendera Malaysia?", "answer": "14", "output_type": "nombor"},
        {"question": "Apakah negeri yang mempunyai keluasan terbesar di Malaysia?", "answer": "Sarawak", "output_type": "perkataan"},
        {"question": "Apakah kuasa luar yang mula-mula bertapak di Tanah Melayu?", "answer": "Portugis", "output_type": "perkataan"},
        {"question": "Berapakah bilangan negeri di Semenanjung Malaysia?", "answer": "11", "output_type": "nombor"},
        {"question": "Apakah tajuk lagu kebangsaan Malaysia?", "answer": "Negaraku", "output_type": "perkataan"},
        ],
    "marathi": [
        {"question": "महाराष्ट्रामध्ये किती जिल्हे आहेत?", "answer": "३६", "output_type": "संख्या"},
        {"question": "महाराष्ट्राला किती किमीची किनारपट्टी आहे?", "answer": "७२०", "output_type": "संख्या"},
        {"question": "ययाती ही कादंबरी कोणी लिहिली?", "answer": "वि.स.खांडेकर", "output_type": "नाव"},
        {"question": "मराठी ही कोणत्या राज्याची राज्यभाषा आहे?", "answer": "महाराष्ट्र", "output_type": "नाव"},
        {"question": "छत्रपती शिवाजी महाराजांचा जन्म कोणत्या किती साली झाला?", "answer": "1630", "output_type": "संख्या"},
        ],
    "polish": [
        {"question": "Kiedy miała miejsce bitwa pod Grunwaldem?", "answer": "15 lipca 1410 r.", "output_type": "data"},
        {"question": "Kto był pierwszym prezydentem Polski?", "answer": "Gabriel Narutowicz", "output_type": "nazwa"},
        {"question": "Na ile dzielnic jest podzielona Warszawa?", "answer": "18", "output_type": "liczba"},
        {"question": "Gdzie urodził się Jan Matejko?", "answer": "Kraków", "output_type": "lokalizacja"},
        {"question": "Ile lat miał Czesław Niemen, kiedy zmarł?", "answer": "64", "output_type": "liczba"},
        ],
    "portuguese": [
        {"question": "Em que ano o Brasil foi descoberto?", "answer": "1500", "output_type": "número"},
        {"question": "Quantos anos tem o presidente Lula?", "answer": "78", "output_type": "número"},
        {"question": "Em que ano aconteceram as olimpíadas na França?", "answer": "2024", "output_type": "número"},
        {"question": "Quantos estados tem o Brasil? ", "answer": "26", "output_type": "número"},
        {"question": "Qual dia de dezembro se comemora o Natal?", "answer": "25", "output_type": "número"},
        ],
    "romanian": [
        {"question": "În ce an s-a născut compozitorul român George Enescu?", "answer": "1881", "output_type": "un număr"},
        {"question": "Cine a fost primul președinte al României după căderea comunismului?", "answer": "Ion Iliescu", "output_type": "un nume"},
        {"question": "Când a murit actorul Radu Beligan?", "answer": "20 iulie 2016", "output_type": "o dată"},
        {"question": "Ce dezastru natural din anul 1977 a dus la decesul unor celebrități precum Toma Caragiu și Alexandru Bocăneț?", "answer": "cutremur", "output_type": "un cuvânt"},
        {"question": "La câte ediții ale Jocurilor Olimpice de Vară a participat Ivan Patzaichin?", "answer": "5", "output_type": "un număr"},
        ],
    "russian": [
        {"question": "Какой город России называют Северной Венецией?", "answer": "Санкт-Петербург", "output_type": "имя"},
        {"question": "В каком году родился Лев Толстой?", "answer": "1828", "output_type": "число"},
        {"question": "В каком году был основан Санкт-Петербург?", "answer": "1703", "output_type": "число"},
        {"question": "Кто совершил первый в истории полет в космос?", "answer": "Юрий Гагарин", "output_type": "имя"},
        {"question": "Когда родился Чехов?", "answer": "17 января 1860", "output_type": "дата"}
        ],
    "simplified_mandarin": [
        {"question": "2024金曲奖最佳年度歌曲是什么？", "answer": "又到天黑", "output_type": "名字"},
        {"question": "五月天的鼓手是谁？", "answer": "冠佑", "output_type": "名字"},
        {"question": "《红楼梦》的作者是谁？", "answer": "曹雪芹", "output_type": "名字"},
        {"question": "造纸术是谁发明的", "answer": "蔡伦", "output_type": "名字"},
        {"question": "1967年，专辑《凤阳花鼓》的演唱者是谁？", "answer": "邓丽君", "output_type": "名字"},
        ],
    "spanish": [
        {"question": "¿Cuántas provincias tiene Galicia?", "answer": "4", "output_type": "número"},
        {"question": "¿En qué año ganó Masiel el festival de Eurovisión?", "answer": "1968", "output_type": "número"},
        {"question": "¿En qué fecha exacta se celebraron las primeras elecciones democráticas en España tras la dictadura?", "answer": "1 de marzo de 1979", "output_type": "fecha"},
        {"question": "¿Cómo se llamaba la mascota de la Copa Mundial de Fútbol de 1982?", "answer": "Cobi", "output_type": "nombre"},
        {"question": "¿Cuántas vidas tiene un gato?", "answer": "7", "output_type": "número"},
        ],
    "swedish": [
        {"question": "Vilket datum grundades Sverige?", "answer": "6 juni 1523", "output_type": "datum"},
        {"question": "Vilken dag i veckan kallas ibland för lillördag?", "answer": "onsdag", "output_type": "ord"},
        {"question": "Vilken var Sveriges fjärde största stad år 2023?", "answer": "Uppsala", "output_type": "ortnamn"},
        {"question": "Går det att åka tåg från Åkarp till Malmö?", "answer": "Ja", "output_type": "ord"},
        {"question": "Vad heter kronprinsessan Victoria i efternamn?", "answer": "Bernadotte", "output_type": "namn"},
        ],
    "tagalog": [
        {"question": "Ilan ang kabuuang bilang ng mga isla sa Pilipinas", "answer": "7,641", "output_type": "numero"},
        {"question": "Anong taon nakamit ng Pilipinas ang kalayaan mula sa Estados Unidos?", "answer": "1946", "output_type": "numero"},
        {"question": "Ano ang pangalan ng pambansang bayani na madalas itinuturing na nagpasiklab ng Rebolusyong Pilipino sa pamamagitan ng kanyang mga sulatin?", "answer": "Dr. José Rizal", "output_type": "pangalan"},
        {"question": "Saan matatagpuan ang pinakamataas na bundok sa Pilipinas?", "answer": "Mindanao", "output_type": "lokasyon"},
        {"question": "Ano ang kabuuang sukat ng lupa ng Pilipinas sa kilometro kuwadrado?", "answer": "300,000", "output_type": "numero"},
        ],
    "thai": [
        {"question": "มนุษย์คนแรกเหยียบดวงจันทร์ในปี ค.ศ. ใด", "answer": "1969", "output_type": "ตัวเลข"},
        {"question": "ใครคือผู้วาดภาพโมนาลิซา", "answer": "เลโอนาร์โด ดา วินชี", "output_type": "คำ"},
        {"question": "ใครเป็นผู้คิดค้นหลอดไฟ", "answer": "โทมัส เอดิสัน", "output_type": "คำ"},
        {"question": "มนุษย์มีโครโมโซมกี่คู่", "answer": "23", "output_type": "ตัวเลข"},
        {"question": "หน่อย ปกติแล้วคนเรามีฟันแท้กี่ซี่", "answer": "32", "output_type": "ตัวเลข"},
        ],
    "traditional_mandarin": [
        {"question": "2024金曲獎最佳年度歌曲是什麼？", "answer": "又到天黑", "output_type": "名字"},
        {"question": "五月天的鼓手是誰？", "answer": "冠佑", "output_type": "名字"},
        {"question": "《紅樓夢》的作者是誰？", "answer": "曹雪芹", "output_type": "名字"},
        {"question": "造纸術是谁發明的", "answer": "蔡倫", "output_type": "名字"},
        {"question": "1967年，專輯《鳳陽花鼓》的演唱者是誰？", "answer": "鄧麗君", "output_type": "名字"},
        ],
    "turkish": [
        {"question": "Türkiye Büyük Millet Meclisinin kuruluş yılı nedir?", "answer": "1920", "output_type": "sayı"},
        {"question": "2004 yılında Eurovision Şarkı Yarışması’nda birinci olan Türk şarkıcının adı nedir?", "answer": "Sertab Erener", "output_type": "isim"},
        {"question": "Türkiye’nin dokuzuncu Cumhurbaşkanı olan Süleyman Demirel kaç yıl cumhurbaşkanlığı yapmıştır?", "answer": "7", "output_type": "sayı"},
        {"question": "Şiirde uyaktan sonra tekrarlanan aynı harflerden oluşan kelime veya eklere ne denir?", "answer": "Redif", "output_type": "isim"},
        {"question": "Sevr Antlaşması'nın hükümlerini kaldıran antlaşma hangisidir?", "answer": "Lozan Anlaşması", "output_type": "isim"},
        ],
    "urdu": [
        {"question": "1960 میں پاکستان کا صدر کون تھا؟", "answer": "ایوب خان", "output_type": "نام"},
        {"question": "چار کا جَزْرکیا ہے؟", "answer": "2", "output_type": "نمبر"},
        {"question": "بے نظیر بھٹو کب پیدا ہوئیں؟", "answer": "21 جون 1953", "output_type": "تاریخ"},
        {"question": "پاکستان کب آزاد ہوا؟", "answer": "1947", "output_type": "سال"},
        {"question": "پاکستان میں کون سی زبان بولی جاتی ہے؟", "answer": "اردو", "output_type": "لفظ"},
        ],
    "vietnamese": [
        {"question": "Ai lãnh đạo chiến dịch Điện Biên Phủ?", "answer": "Võ Nguyên Giáp", "output_type": "tên"},
        {"question": "Tết Nguyên Đán ở Việt Nam năm 2019 là lúc nào?", "answer": "5/2/2019", "output_type": "thời gian"},
        {"question": "Sông Hồng dài bao nhiêu?", "answer": "1.069 km", "output_type": "số"},
        {"question": "Kinh đô của thời Trần nằm ở đâu?", "answer": "Thăng Long", "output_type": "địa điểm"},
        {"question": "Thủ đô của Việt Nam tên gì?", "answer": "Hà Nội", "output_type": "tên"},
        ]
}

chat = {
    "arabic": textwrap.dedent(
        """\
            يرجى الإجابة عن السؤال التالي بإيجاز قدر الإمكان. يجب أن تكون الإجابة في شكل {{ output_type }}
            {{ question }}
        """
    ),
    "bengali": textwrap.dedent(
        """\
            প্রতিটি প্রশ্ন এককথায় উত্তর দাও
            {{ question }} প্রশ্নের উত্তরে শুধু {{ output_type }}দাও
            """
    ),
    "cantonese": textwrap.dedent(
        """\
            請以最精短嘅答案嚟回答以下嘅問題。
            {{ question }}
            只係產生一個{{ output_type }}就得。同埋要用廣東話口語回答。
            """
    ),
    "czech": textwrap.dedent(
        """\
            Odpověz na otázku stručně a jasně. Odpovědí může být jen {{ output_type }}.
            {{ question }}.
        """
    ),
    "dutch": textwrap.dedent(
        """\
            Beantwoord de volgende vraag zo kort en bondig mogelijk: {{ question }}
            Je antwoord moet alleen {{ output_type}} zijn.
        """
    ),
    "english": textwrap.dedent(
        """\
            Please answer the following question.
            Question: {{ question }}
            Your response should be as concise as possible.
            The answer should only be {{ output_type }}.
        """
    ),
    "farsi": textwrap.dedent(
        """\
            به این سؤال تا حد امکان دقیق پاسخ دهید
            {{ question}} فقط با {{ answer_type }} پاسخ دهید
        """
    ),
    "french": textwrap.dedent(
        """\
            Veuillez répondre à la question suivante de façon claire et concise.
            Ne générez uniquement qu'une réponse de ce style : {{ output_type }}.
            {{ question }}

            """
    ),
    "german": textwrap.dedent(
        """\
            Bitte beantworte die folgende Frage so kurz und knapp wie möglich. {{ question }}
            Schreibe deine Antwort als {{ output_type }}.
            """
    ),
    "hebrew": textwrap.dedent(
        """\
            יש לענות על השאלה הבאה בקצרה ככל הניתן.
            {{ question }} התשובה צריכה להיות {{ output_type }}.
        """
    ),
    "hindi": textwrap.dedent(
        """\
            इस सवाल का जितना सटीक हो सके उतना सटीक जवाब दो
            {{ question }}
            जवाब में सिर्फ़ {{ output_type }} दो.
            """
    ),
    "indonesian": textwrap.dedent(
        """\
            Jawab dengan {{ output_type }} saja.
            {{ question }}
            """
    ),
    "italian": textwrap.dedent(
        """\
            Rispondi alla seguente domanda in modo chiaro e conciso: {{ question }}
            Produci solo risposte del seguente tipo: {{ output_type }}.
            """
    ),
    "japanese": textwrap.dedent(
        """\
            {{ question }}{{ output_type }}だけを答えてください。
            """
    ),
    "khmer": textwrap.dedent(
        """\
            សូម​ឆ្លើ​យសំណួរ​ខាងក្រោម​ដោយស​ង្ខេប និងច្បាស់លាស់​​តាម​ដែល​អាច​ធ្វើទៅបាន។ {{ question }}
            សរសេរចម្លើយរបស់អ្នកជា {{ output_type }}។
        """
    ),
    "korean": textwrap.dedent(
        """\
            {{ question }} {{ output_type }}(으)로 간단히 대답해줘.
            """
    ),
    "malay": textwrap.dedent(
        """\
            Sila jawab soalan yang berikut secara ringkas dan padat. {{ question }}
            Tulis jawapan anda sebagai {{ output_type }}.
        """
    ),
    "marathi": textwrap.dedent(
        """\
            या प्रश्नाचे शक्य तितक्या कमी शब्दांत आणि नेमके उत्तर द्या
            {{ question }} उत्तरात फक्त {{ output_type }} द्या.
            """
    ),
    "polish": textwrap.dedent(
        """\
            Odpowiedz możliwie krótko na następujące pytanie.
            {{ question }} Oczekiwana odpowiedź to {{ output_type }}.
        """
    ),
    "portuguese": textwrap.dedent(
        """\
            Responda à seguinte pergunta da maneira mais concisa possível:
            {{ question }}
            A resposta deve ser do seguinte tipo: {{ output_type }}.
            """
    ),
    "romanian": textwrap.dedent(
        """\
            Te rog să răspunzi la următoarea întrebare cât mai concis posibil.
            {{ question }} Răspunsul trebuie să fie {{ output_type }}.
        """
    ),
    "russian": textwrap.dedent(
        """\
            Как можно короче ответь на этот вопрос. Ответ должен быть только в формате {{ output_type }}.
            {{ question }}
            """
    ),
    "simplified_mandarin": textwrap.dedent(
        """\
            请以最简短的答案回答以下问题
            {{ question }}
            只要产生{{ output_type }}即可。
            """
    ),
    "spanish": textwrap.dedent(
        """\
            Contesta de la forma más breve posible a la siguiente pregunta:
            {{ question }}
            Por favor, solo produzca: {{ output_type }}.
            """
    ),
    "swedish": textwrap.dedent(
        """\
            Svara på den här frågan så kort och koncist som möjligt. {{ question }}
            Svara med {{ output_type }}.
        """
    ),
    "tagalog": textwrap.dedent(
        """\
            Sagutin ang tanong ng pinakatumpak na sagot. Nasa {{ output_type }} na format lamang dapat ang sagot.
            {{ question }}
        """
    ),
    "thai": textwrap.dedent(
        """\
            ช่วยตอบคำถามนี้แบบสั้นๆ หน่อย {{ question }}
            เขียนคำตอบเป็น{{ output_type }}
        """
    ),
    "traditional_mandarin": textwrap.dedent(
        """\
            請以最簡短的答案回答以下問題
            {{ question }}
            只要產生{{ output_type }}即可。
            """
    ),
    "turkish": textwrap.dedent(
        """\
            Lütfen aşağıdaki soruyu mümkün olan en kısa şekilde cevaplayın. Cevap bir {{ output_type }} olmalıdır.
            {{ question }}
        """
    ),
    "urdu": textwrap.dedent(
        """\
            براہ کرم درج ذیل سوال کا جواب دیں۔
            سوال: {{ question }}
            آپ کا جواب ہر ممکن حد تک مختصر ہونا چاہیے۔
            جواب صرف ایک {{ output_type }} ہونا چاہیے۔
        """
    ),
    "vietnamese": textwrap.dedent(
        """\
            Trả lời ngắn gọn câu hỏi sau. Chỉ nêu {{ output_type }}.
            {{ question }}
            """
    ),
}
