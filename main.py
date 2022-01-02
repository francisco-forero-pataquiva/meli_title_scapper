from requests_html import HTMLSession
import pandas as pd
from unidecode import unidecode

s = HTMLSession()

def get_titles(counter, store_id):
  r =s.get(f'https://listado.mercadolibre.cl/_Desde_{counter}_CustId_{store_id}_NoIndex_True')
  results=r.html.find('.ui-search-item__group--title')
  keyword_list = [(x.text.lower().split()) for x in results]
  flat_keyword_list = [item for sublist in keyword_list for item in sublist]
  unaccented_list = [unidecode(x) for x in flat_keyword_list]
  if not unaccented_list:
    return False
  else:
    return unaccented_list

def main(): 
  store_id = input('Store ID:')
  n= -49  
  final_list =[]
  while n < 501:
    n = n+50  
    if get_titles(n,store_id) == False:
        flat_flat_list = [item for sublist in final_list for item in sublist]
        return flat_flat_list
    else:
      final_list.append(get_titles(n,store_id))
      
if __name__ == '__main__':
  print('Getting titles from store...')
  title_words = pd.DataFrame(main(), columns=["synonyms"])
  if title_words.empty:
    print('Error: empty dataframe')
  else:
    print('Normalizing text!')
    title_words.insert(0,"key","key")
    title_words.insert(1,"word","title_words")
    title_words.to_csv('title_words_watson.csv', index=False, header=False)
    print('Csv created successfully!')