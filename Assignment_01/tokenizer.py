import re
def sentence_tokenizer(paragraph):
  pattern='[\u0964!?.][^0-9.0-9]'
  sentences=re.split(pattern,paragraph)
  ends=re.findall(pattern,paragraph)
  res=[]
  for sentence in sentences: 
    if ends==[]:
      break
    end=ends.pop(0)
    res.append(sentence.strip() + end)
  return res


def word_tokenizer(sentence):
    url_pattern = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Phone numbers (with optional +91 or +९१)
    phone_pattern = r'(?:\+?[0-9\u0966-\u096F]{1,3}[\s-]?)?[0-9\u0966-\u096F]{10}'

    # Time format: 10:30 or १०:३०
    time_pattern = r'[0-9\u0966-\u096F]{1,2}:[0-9\u0966-\u096F]{2}'

    # Decimal and whole numbers
    latin_number = r'[0-9]+(?:\.[0-9]+)?'
    devnag_number = r'[\u0966-\u096F]+(?:\.[\u0966-\u096F]+)?'

    # Punctuation
    punctuation = r'[!?\.\u0964\,"\'\+-]'

    # Hindi / Devanagari words
    hindi_word = fr'[\u0900-\u0963\u0965-\u096F]+[^!?\.\u0964\,"\'\+-]'
    english_word = r'[a-zA-Z]+'


    # Emojis (basic unicode emoji range)
    emoji_pattern = r'[\U0001F300-\U0001FAFF\U00002700-\U000027BF]'

    # Final combined pattern
    pattern = fr'{email_pattern}|{url_pattern}|{phone_pattern}|{time_pattern}|{latin_number}|{devnag_number}|{punctuation}|{hindi_word}|{emoji_pattern}|{english_word}'

    return re.findall(pattern, sentence)



