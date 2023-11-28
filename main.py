# WordleAssist by Art@AbingtonPro.com Nov 27, 2023
#   Python program to assist solving Wordle games
#   Allows user to add words as possible solutions
#   Provides a frequency counter to track how many times a word is a winner

# For Apple, change line 23 to 
#   os.system('clear')
# For Windoes, change line 23 to 
#   os.system('cls')

import time
import os
import pandas as pd
from   termcolor import colored
import shutil
import requests
import socket
import webbrowser
remote_server = "1.1.1.1"

#function clear_console()
def clear_console():
  os.system('cls')

#function internet_avail:
def internet_avail(hostname):
  try:
    # See if we can resolve the host name - tells us if there is a DNS listening
    host = socket.gethostbyname(hostname)
    # Connect to the host - tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
    pass  # We ignore any errors, returning False
    return False

#function get_yskip function
#Usage example:    test = get_yn( 4, 'Would you like to continue?', 'light_cyan')
#Available colors: black,red,green,yellow,blue,magenta,cyan,white,light_grey,light_cyan,
#                  dark_grey,light_red,light_green,light_yellow,light_blue,light_magenta
def get_yskip(indent, question, colr ):
  spc = ''
  for q in range(indent):
    spc = spc + ' '

  spc2 = spc + '  '
  txt = spc + question + ' '
  txtq = colored(txt, color=colr)
  txt = spc2 + 'Please enter only "Y" or "N" '
  txte = colored(txt, color='light_red')
  ok_skip = ('Y', 'y')

  print(txtq, end='')
  ans_yn = input()
  if ans_yn in ok_skip:
    rtrn = 'Y'
  else:
    rtrn = 'N'

  return rtrn
#END of get_yskip function

#START of get_yn function
#Usage example:    test = get_yn( 4, 'Would you like to continue?', 'light_cyan')
#Available colors: black,red,green,yellow,blue,magenta,cyan,white,light_grey,light_cyan,
#                  dark_grey,light_red,light_green,light_yellow,light_blue,light_magenta
def get_yn(indent, question, colr ):
  spc = ''
  for q in range(indent):
    spc = spc + ' '

  spc2 = spc + '  '
  txt = spc + question + ' '
  txtq = colored(txt, color=colr)
  txt = spc2 + 'Please enter only "Y" or "N" '
  txte = colored(txt, color='light_red')
  ok_ans = ('Y', 'y','N','n')

  print(txtq, end='')
  while True:
    ans_yn = input()
    if ans_yn in ok_ans:
      break
    else:
      print(txte, end='')

  ans_yn = ans_yn.upper()

  return ans_yn
#END of get_yn function

#START of exp_list function - expand list
def exp_list(list):
  len_list = len(list)
  str = ''
  if len_list > 0:
    for x in list:
      str = str + " " + x
  else:
    str = '-'
  return str
#END of exp_list function

#START of get_clue function - to get search clues for menu choice 3
def get_clue(pos):
  seq = ['Enter 1st clue: ', 'Enter 2nd clue: ', 'Enter 3rd clue: ', 'Enter 4th clue: ', 'Enter 5th clue: ']
  while True:
    tx = seq[pos]
    tx = '      ' + tx
    txt = colored(tx, color='light_green')
    print(txt, end='')
    clue = input()

    if clue == '':
      clue = "QUIT"
      break

    lclue = len(clue)
    clue = clue.upper()

    if lclue != 2:
      txt = colored('        Must be a letter followed by a number 1 to 5: ', color='light_red')
      print(txt)
    else:
      #get current number positions from list_3
      len3 = len(list_3)
      list_3nos = []
      for n in range(len3):
        clu = list_3[n]
        clu2 = clu[1:2]
        cln_add = [clu2]
        list_3nos = list_3nos + cln_add

      clue1 = clue[0:1]
      clue2 = clue[1:2]
      clue = clue1 + clue2
      if clue2 in list_3nos:
        txt = colored('        There cannot be two letters in the same', color='light_red')
        print(txt)
        txt = '        position. There is already a clue for ' + clue2 + '.'
        txt = colored(txt, color='light_red')
        print(txt)
        print('        Enter a different search clue. To remove a ')
        print('        clue, clear List 3 using menu choice 4.')
        print()
      else:
        if clue1 not in letters or clue2 not in nums:
          if clue1 not in letters:
            txt = colored('        1st character must be a letter, try again: ', color='light_red')
            print(txt)
          if clue2 not in nums:
            if clue1 in letters:
              txt = colored('        2nd character must be a number 1 to 5, try again: ', color='light_red')
              print(txt)
        else:
          break

  return clue
#END of get_clue function

#define lists
letters = 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
nums = '1','2','3','4','5'
menu_options = ('1','2','3','4','5','6','7','8','X','x')
menu4_options = ('N','n','q','1','2','3')
list_1 = []  #gray letters
list_2 = []  #yellow letters with position numbers
list_2y = [] #yellow letters
list_3 = []  #green letters with position numbers
list_4 = []  #green letters with position plus yellow letters
results = pd.DataFrame(columns=['IDX','WORD'])

#START OF MAIN PROGRAM LOOP
while True:
  clear_console()
  data = pd.read_csv('mainlist.csv')
  total_words = str(len(data.index))
  internet_status = internet_avail(remote_server)

  lst_1 = exp_list(list_1)
  lst_2 = exp_list(list_2)
  lst_3 = exp_list(list_3)
  print()
  text = colored('                        MAIN MENU', color='light_yellow')
  print(text)
  text = colored('                      Wordle! Assist', color='light_green')
  print(text)
  text = colored('                  ' + total_words + ' words in main list ', color='light_cyan')
  print(text)
  text = colored('  ========================================================== ', color='light_yellow')
  print(text)
  print()
  text = colored('    How to play:  ', color='light_green')
  text2 = colored('After entering a guess in Wordle!, enter  ', color='light_cyan')
  text = text + text2
  print(text)
  text = colored('       any gray, yellow, and green letters in menu choices ', color='light_cyan')
  print(text)
  text = colored('       1, 2, and 3 below.  Repeat as you add more guesses.', color='light_cyan')
  print(text)
  print()
  print('      1 - Enter ', end='')
  text = colored('grayed out ', color='dark_grey')
  print(text, end='')
  print('letters')
  text = colored(lst_1, color='light_cyan')
  print('            List 1: ' + text)
  print()
  print('      2 - Enter ', end='')
  text = colored('yellow ', color='light_yellow')
  print(text, end='')
  print('letters')
  text = colored(lst_2, color='light_cyan')
  print('            List 2: ' + text)
  print()
  print('      3 - Find matching words ')
  text = colored(lst_3, color='light_cyan')
  print('            List 3: ' + text)
  print()
  print('      4 - Start new game (or clear list 1, 2 or 3)')
  print()
  print('      5 - Add new words to the master word list')
  if not internet_status:
    text = colored( '          Internet not connected, will not check words.', color='light_magenta' )
    print(text)

  print()
  print("      6 - Look up a word's meaning")
  if not internet_status:
    text = colored( '          Internet not connectd, lookup not available.', color='light_magenta' )
    print(text)

  print()
  print('      7 - Remove a word from master word list')
  print()
  print('      8 - Launch Wordle! game in Web Browser')
  print()
  print('      X - Exit')
  print()
  print('          Choice: ', end='')

  while True:
    user_input = input()
  
    if user_input in menu_options:
      break

    else: 
      text = colored('          Not a valid choice, try again ', color='red')
      print(text, end='')

  #START MENU CHOICE 1 - ENTER GRAY LETTERS
  if user_input == '1':
    clear_console()
    print()
    text = colored('               Enter ', color='light_yellow')
    print(text, end='')
    text = colored('Grayed Out ', color='dark_grey')
    print(text, end='')
    text = colored('Letters', color='light_yellow')
    print(text)
    text = colored('    ==============================================', color='light_yellow')
    print(text)
    print()
    print('      Current List 1: ' + lst_1)
    print()

    text = colored('      Enter one or more letters without spaces.', color='light_cyan')
    print(text)
    text = colored('      [Enter] only to exit.', color='light_cyan')
    print(text)
    print()
    print('      Letter(s): ', end='')

    while True:

      my_str = input()
      if my_str == '':
        text = colored('        Nothing entered, returning to main menu', color='dark_grey')
        print(text)
        time.sleep(1)
        break

      else:
        my_str = my_str.upper()
        if my_str.isalpha():
          list_1.extend(my_str)
          print()
          txt = '      ' + my_str + ' added to List 1, returning to main menu'
          text = colored(txt, color='light_green')
          print(text)
          break

        else:
          txt = '        "' + my_str + '" has a space or number, try again: '
          text = colored(txt, color='light_red')
          print(text, end='')

    time.sleep(1)
    clear_console()
  #END MENU CHOICE 1 - ENTER GRAY LETTERS
  
  #START MENU CHOICE 2 - ENTER YELLOW LETTERS
  if user_input == '2':
    clear_console()
    print()
    text = colored('           Enter Yellow Letters and Their Positions', color='light_yellow')
    print(text)
    text = colored(lst_2, color='light_cyan')
    print('             List 2: ' + text)
    text = colored('  ============================================================', color='light_yellow')
    print(text)
    print('')
    text = colored('letter', color='light_yellow')
    print('    Enter a yellow ' + text + ' and the position it occupies as a')
    print('    number (1-5) with no space between the letter and number.')
    print('')
    text = colored('letters', color='light_yellow')
    print('    Enter as many ' + text + ' as you have available.')
    print('')
    print('    To return to the main menu, press [Enter] only.')
    print('')
    text = colored('      Enter a letter and number: ', color='light_cyan')
    print(text, end='')

    while True:
      user_input = input()
      lenu = len(user_input)
      user_input = user_input.upper()

      if lenu == 0:
        print()
        text = colored('      Nothing entered, returning to main menu ...', color='dark_grey')
        print(text)
        time.sleep(1)
        break
      else:

        if lenu != 2:
          text = colored('        Must be 2 characters, a letter followed by a number.', color='light_red')
          print(text)
          text = colored('      Try again: ', color='light_cyan')
          print(text, end='')
        else:
          first = user_input[0:1]
          second = user_input[1:2]
      
          if first in letters and second in nums:
            list_temp = [user_input]
            list_2 = list_2 + list_temp

            if first not in list_2:
              list_2y.extend(first)

            print('        ' + user_input + ' entered ')
            print()
            text = colored('      Enter another letter and number: ', color='light_cyan')
            print(text, end='')

          else:
            text = colored('        Must be a letter followed by a number (1-5).', color='light_red')
            print(text)
            text = colored('      Try again: ', color='light_cyan')
            print(text, end='')

  #END MENU CHOICE 2 - ENTER YELLOW LETTERS

  # START MENU CHOICE 3 - FIND WORDS THAT MATCH SEARCH CLUES
  if user_input == '3':

    clear_console()
    results = results[0:0]
    print()
    txt = colored('          Find Words That Match Search Clues', color='light_yellow')
    print(txt)
    txt = colored('  ==================================================', color='light_yellow')
    print(txt)
    print()
    txt = colored('green', color='light_green')
    txt = '    Enter ' + txt + ' letters and their position as a '
    print(txt)
    print('    number (1-5) with no space between the letter')
    print('    and the number. When you are finished, press')
    print('    [Enter] only.')
    print()
    print('    Only enter new green letter clues. If there are ')
    print('    no green letters to add, just press [Enter].')
    print()
    lst_3 = exp_list(list_3)
    txt = colored(lst_3, color='light_cyan')
    txt = '    Current clues (List 3) for green letters: ' + txt
    print(txt)
    
    ln = 0

    while True:
      print()
      clue0 = get_clue(ln)
      ln = ln + 1
      if clue0 == 'QUIT':
        quit = 'QUIT'
        break
      else:
        list_temp = [clue0]
        list_3 = list_3 + list_temp
        txt = '        ' + colored(str(clue0), color='light_cyan') + ' entered'
        print(txt)
      if ln >= 5:
        break

    k = 0
    
    #add new list_3 entries to list_4
    len3 = len(list_3)
    for m in range(len3):
      gr_ltr = list_3[m]
      if gr_ltr not in list_4:
        add_list = [gr_ltr]
        list_4 = list_4 + add_list

    #add new yellow letters from list_2y to list_4
    len2y = len(list_2y)
    for m in range(len2y):
      yw_ltr = list_2y[m]
      if yw_ltr not in list_4:
        add_list = [yw_ltr]
        list_4 = list_4 + add_list

    lst_4 = exp_list(list_4)
    
    txt = '    Words matching these clues:'
    txt = colored(txt, color='light_yellow')
    txt2 = colored(lst_4, color='light_cyan')
    txt = txt + txt2
    print()
    print(txt)
    txt = '  ============================================= '
    txt = colored(txt, color='light_yellow')
    print(txt)
    txt = colored('      #      WORD   FREQUENCY', color='light_cyan')
    print(txt)

    data = pd.read_csv('mainlist.csv')

    rows = len(data)
    lnl3 = len(list_3)
    lnl4 = len(list_4)
    wordlen = 5

    for i in range(rows):
      word = data.WORD[i]
      numpassed = 0

      # Test against list_1 gray letters
      possible = 'y'
      for j in range(wordlen):
        gltr = word[j]
        if gltr in list_1:
          possible = 'n'

      # if still possible = y, perform yellow tests, otherwise move on to next word
      if possible == 'y':
        stest = []  # will build test array for next check search test stest
        h = 1
        for x in range(5):
          ltrpos = word[x] + str(h)
          lp = [ltrpos]
          stest = stest + lp
          if ltrpos in list_2:
            possible = 'n'
          h = h + 1

        # if still possible = y, perform search tests on list_4 or move on to next word
        if possible == 'y':
          
          for j in range(lnl4):
            sltr = list_4[j]
            lens = len(sltr)

            if lens == 1 and sltr in word:
              numpassed = numpassed + 1

            if lens == 2:
              lpos1 = sltr[0:1]
              lpos2 = sltr[1:2]
              lpostest = lpos1 + lpos2

              if lpostest in stest:
                numpassed = numpassed + 1

          if numpassed == lnl4:
            possible = 'y'
          else:
            possible = 'n'

      if possible == 'y':
        freq = data.FREQ[i]
        k = k + 1
        if k < 10:
          spc = ' '
        else:
          spc = ''

        add = {'IDX': k, 'WORD': word}
        results = results._append(add, ignore_index=True)
        freqi = int(freq)
        freqstr = str(freqi)
        print('   ', spc, k, '   ', word, '     ', freqstr)

    if not list_1 and not list_2 and not list_4:
      print()
      text1 = colored('     No clues were entered for menu choice 1, 2, or 3', color='light_red')
      text2 = colored('     so the entire word list matched.  Please enter ', color='light_red')
      text3 = colored('     at least one clue. ', color='light_red')
      text4 = colored('       Press [Enter] to return to menu: ', color='dark_grey')
      print(text1)
      print(text2)      
      print(text3)
      print()
      print(text4, end='')
    else:
      print()
      txt = colored('   If one of these words solves the game, enter the ', color='light_cyan')
      txt2 = colored('#', color='light_yellow')
      txt3 = colored('.', color='light_cyan')
      txt = txt + txt2 + txt3
      print(txt)
      txt = colored('   If you solved it with a ', color='light_cyan')
      txt2 = colored('new word', color='light_green')
      txt3 = colored(', enter ', color='light_cyan')
      txt4 = colored('0 ', color='light_green')
      txt5 = colored('to record it.', color='light_cyan')
      txt = txt + txt2 + txt3 + txt4 + txt5
      print(txt)
      txt = colored('   Press "[Enter] only" to search for more matches. ', color='light_cyan')
      print(txt)
      txt = colored('     Choice: ', color='light_yellow')
      print(txt, end='')

    while True:
      is_number = 'n'
      choice = input()
    
      if choice == "":
        break

      try:
        ansi = int(choice)
        is_number = 'y'
      except:
        txt = '       Must be a number between 1 and ' + str(k) + ', try again: '
        txt = colored(txt, color='light_red')
        print(txt, end='')
        is_number = 'n'
    
      if is_number == 'y':
        ansi = int(choice)
        if ansi >= 0 and ansi <= k:
          break
        else:
          txt = '      Must be a number between 1 and ' + str(k) +  ', try again: '
          txt = colored(txt, color='light_red')
          print(txt, end='')

    while True:
      if choice == '': 
        break
      else:

        is_valid = "n"
        while True:
          try:
            ansi = int(choice)
            if ansi >= 0 and ansi <= k:
              solution = choice
              break
            else:
              choice = input()

          except:
            txt = '     Must be a number between 1 and ' + str(k) + ', try again: '
            txt = colored(txt, color='light_red')
            print(txt, end='')

        if solution == '0':
          print()
          print('   You chose to enter a new solution word.')
          print('   Enter the word, or press [Enter] only to skip: ', end='')
          while True:
            new_word = input()
            if new_word == '':
              add_word = 'n'
            else:
              add_word = 'y'

            lnw = len(new_word)
            if lnw == 5:
              new_word = new_word.upper()
              break
            else:
              txt = colored('    New word must be 5 characters, try again: ', color='light_red')
              print(txt, end='')

          if add_word == 'y':
            if new_word in data.WORD.values:
              txt = '      ' + new_word + ' already exists in main list'
              text = colored(txt, color='light_magenta')
              print(text)
              add_word = 'n'
              sel_word = new_word
              
              # increment FREQ of word, get index, then get freq, add 1, then replace and update file
              cur_freq = data.loc[data['WORD'] == new_word, 'FREQ'].iloc[0]
              cur_freqi = int(cur_freq)
              new_freqi = cur_freqi + 1
              new_freq = str(new_freqi)
              idx = data[data['WORD'] == new_word].index.values
              idxi = idx[0]
              idxi = int(idxi)
              data.at[idxi, 'FREQ'] = new_freq

              newdata = data.sort_values("WORD")
              newlist = newdata.to_csv('data2.csv', index=False)

              cwd = os.getcwd()
              des = cwd + "\\mainlist.csv"
              fo = open(des, "wb")
              fo.close()
              src = cwd + "\\data2.csv"
              shutil.copy(src, des)

              txt = colored('   The word frequency has been updated in the database. ', color='light_green')
              print(txt)

            else:
              freq = "1"
              new_row = pd.Series([new_word, freq], index=data.columns)
              data = data._append(new_row, ignore_index=True)
              txt = '      "' + new_word + '" added to Main Word List'
              text = colored(txt, color='light_green')
              print(text)
              word_added = 'y'
              sel_word = new_word

              # sort and write dataframe to new file
              newdata = data.sort_values("WORD")
              newlist = newdata.to_csv('data2.csv', index=False)

              cwd = os.getcwd()
              des = cwd + "\\mainlist.csv"
              src = cwd + "\\data2.csv"
              shutil.copy(src, des)

          txt = 'line 504 new word ' + new_word
          #input(txt)

        else:
          sel_word = results.loc[results['IDX'] == ansi, 'WORD'].iloc[0]

          #increment FREQ of word, get index, then get freq, add 1, then replace and update file
          cur_freq = data.loc[data['WORD'] == sel_word, 'FREQ'].iloc[0]
          cur_freqi = int(cur_freq)
          new_freqi = cur_freqi + 1
          new_freq = str(new_freqi)
          idx = data[data['WORD'] == sel_word].index.values
          idxi = idx[0]
          idxi = int(idxi)
          data.at[idxi, 'FREQ'] = new_freq

          newdata = data.sort_values("WORD")
          newlist = newdata.to_csv('data2.csv', index=False)

          cwd = os.getcwd()
          des = cwd + "\\mainlist.csv"
          fo = open(des, "wb")
          fo.close()
          src = cwd + "\\data2.csv"
          shutil.copy(src, des)

          print()
          text = '   You selected ' + sel_word + ' as the Wordle solution. '
          txt = colored(text, color='light_green')
          print(txt)
          txt = colored('   The word frequency has been updated in the database. ', color='light_green')
          print(txt)

          print()
          txt = colored('   Definition from FreeDictionary.org:', color='light_cyan')
          print(txt)

        # now print definition
        if not internet_status:
          text = '     Internet not available, not able to provide a definition for ' + sel_word
          txt = colored(text, color='light_magenta')
          print(txt)
          txt = colored('       Press [Enter] to return to menu ', color='dark_grey')
          print(txt, end='')
          break

        else:
          
          uri = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + sel_word
          response = requests.get(uri)
          xtra_pause = 'y'

          if 'No Definitions Found' in response.text:
            text = '      FreeDictionary.org has no definition for ' + sel_word
            txt = colored(text, color='light_magenta')
            print(txt)
            print()
            xtra_pause = 'y'

          else:
            text = (response.text).split('[')

            for index in range(len(text)):
              part = text[index]

              if 'noun' in part:
                j = index + 1
                dfn = text[j]
                defpart = dfn.split(':')
                meaning = defpart[1]
                lng = len(meaning)

                if lng >= 55:
                  lng = 55

                meaning = meaning[1:lng]

                txt = colored('      Noun:      ', color='light_green')
                print(txt + meaning)
                print()

              if 'verb' in part:
                j = index + 1
                dfn = text[j]
                defpart = dfn.split(':')
                meaning = defpart[1]
                lng = len(meaning)

                if lng >= 55:
                  lng = 55

                meaning = meaning[1:lng]
                txt = colored('      Verb:      ', color='light_green')
                print(txt + meaning)
                print()

              if 'adverb' in part:
                j = index + 1
                dfn = text[j]
                defpart = dfn.split(':')
                meaning = defpart[1]
                lng = len(meaning)

                if lng >= 55:
                  lng = 55

                meaning = meaning[1:lng]
                txt = colored('      Adverb:    ', color='light_green')
                print(txt + meaning)
                print()

              if 'adjective' in part:
                j = index + 1
                dfn = text[j]
                defpart = dfn.split(':')
                meaning = defpart[1]
                lng = len(meaning)

                if lng >= 55:
                  lng = 55

                meaning = meaning[1:lng]
                txt = colored('      Adjective: ', color='light_green')
                print(txt + meaning)
                print()

          if xtra_pause == 'y':
            txt = colored('   Do you want to start a new game (clear lists)?: ', color='light_yellow')
            print(txt, end='')
            new_game = ['y', 'Y', 'n', 'N']
            while True:
              user_input = input()
              if user_input in new_game:
                user_input = user_input.upper()
                if user_input == 'Y':
                  list_1 = []
                  list_2 = []
                  list_2y = []
                  list_3 = []
                  list_4 = []
                  break
                else:
                  break

              else:
                txt = colored('     Must be Y or N, try again: ', color='light_red')
                print(txt, end='')                

          break

    print()
    txt = colored('      Returning to menu.', color='dark_grey')
    print(txt)
    xtra_pause = 'n'
    time.sleep(1)
  # END MENU CHOICE 3 - FIND WORDS THAT MATCH SEARCH CLUES

  # START MENU CHOICE 4 - CLEAR LISTS
  if user_input == '4':
    clear_console()
    print()
    text = colored('            Clear Letter Lists', color='light_yellow')
    print(text)
    text = colored('  =========================================', color='light_yellow')
    print(text)
    print()
    print('      List 1: ', end='')
    text = colored(lst_1, color='light_cyan')
    print(text)
    print('      List 2: ', end='')
    text = colored(lst_2, color='light_cyan')
    print(text)
    print('      List 3: ', end='')
    text = colored(lst_3, color='light_cyan')
    print(text)
    print()
    print('      N - Start new game (clear all lists)')
    print()
    print('      1 - Clear List 1 only')
    print()
    print('      2 - Clear List 2 only')
    print()
    print('      3 - Clear List 3 only')
    print()
    print('      [Enter] only - Return to main menu')
    print()

    text =colored('        Choice: ', color='light_yellow')
    print(text, end='')

    while True:
      user_input = input()
      if user_input == '':
        user_input = 'q'
  
      if user_input in menu4_options:
        break

      else: 
        text = colored('          Not a valid choice, try again ', color='red')
        print(text, end='')

    if user_input == 'q':
      text = colored('        Nothing entered, returning to main menu', color='dark_grey')
      print()
      print(text)
      time.sleep(2)

    if user_input == '1':
      print()
      print ('        Clearing List 1')
      list_1 = []
      time.sleep(2)      

    if user_input == '2':
      print()
      print ('        Clearing List 2')
      list_2 = []
      list_2y = []
      list_4 = []
      time.sleep(2)      

    if user_input == '3':
      print()
      print ('        Clearing List 3')
      list_3 = []
      list_4 = []
      time.sleep(2)      

    if user_input == 'N' or user_input == 'n':
      print()
      print ('        Clearing all lists')
      list_1 = []
      list_2 = []
      list_2y = []
      list_3 = []
      list_4 = []
      time.sleep(2)      

    clear_console()
  # END MENU CHOICE 4 - CLEAR LISTS

  # START MENU CHOICE 5 ADD NEW WORDS TO MAINLIST
  if user_input == '5':
    clear_console()
    word_added = 'N'
    print()
    data = pd.read_csv('mainlist.csv')

    text = colored('             Add Words to Main Word List', color='light_yellow')
    print(text)
    text = colored('  ===================================================', color='light_yellow')
    print(text)

    while True:
      print()
      text = colored('    Enter a new word or [Enter] only to quit: ', color='light_cyan')
      print(text, end='')
      user_input = input()
      #enter_only = "N"

      if user_input == '':
        print()
        text = colored('      [Enter] only pressed, returning to main menu', color='dark_grey')
        print(text)
        time.sleep(1)
        break

      else:
        lenu = len(user_input)
        if lenu != 5:
          text = colored('      Must be 5 characters, try again: ', color='light_red')
          print(text)

        else:
          user_input = user_input.upper()

          if user_input in data.WORD.values:
            cur_freq = data.loc[data['WORD'] == user_input, 'FREQ'].iloc[0]
            cur_freqi = int(cur_freq)
            cur_freq_str = str(cur_freqi)
            txt = '      ' + user_input + ' already exists in word list with a frequency of ' + cur_freq_str + '.'
            text = colored(txt, color='light_magenta')
            print(text)

            ans_inc = get_yskip(6, 'Increment frequency by 1? Y=yes, [Enter]=skip : ', 'dark_grey')

            if ans_inc == 'Y':
              new_freqi = cur_freqi + 1
              new_freq = str(new_freqi)
              idx = data[data['WORD'] == user_input].index.values
              idxi = idx[0]
              idxi = int(idxi)
              data.at[idxi, 'FREQ'] = new_freq
              word_added = 'Y'
              txt = colored('      Frequency incremented by 1', color='light_green')
              print(txt)
          else:
            ansa = 'Y'
            ans_add = ['Y', 'y']

            if not internet_status:
              txt = colored('      Internet not available, check spelling. ', color='light_red')
              print(txt)
              txt = colored('      Do you still want to add? ', color='light_red')
              print(txt, end='')
              ansa = input()

            else:
              uri = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + user_input
              response = requests.get(uri)

              if 'No Definitions Found' in response.text:
                txt = colored('      Word not found at FreeDictionary.org. ', color='light_red')
                print(txt)
                txt = colored('      Do you still want to add? ', color='light_red')
                print(txt, end='')
                ansa = input()
              else:
                ansa = 'y'

            if ansa in ans_add:
              print()
              print('      If this was a winning word, you should answer "Y"')
              print('      to set the frequecy to 1, otherwise answer "N".')
              ans_inc = get_yn(4, 'Do you want to set the frequency to 1? ', 'light_cyan')
              if ans_inc == 'Y':
                freq = '1'
              else:
                freq = '0'

              new_row = pd.Series([user_input, freq], index=data.columns)
              data = data._append(new_row, ignore_index=True)
              txt = '      "' + user_input + '" added to Main Word List'
              text = colored(txt, color='light_green')
              print(text)
              if freq == '1':
                txt = colored('      Frequency set to 1', color='light_green')
                print(txt)

              word_added = 'Y'
            else:
              txt = '      "' + user_input + '" NOT added to Main Word List'
              text = colored(txt, color='light_magenta')
              print(text)

    if word_added == 'Y':
      # sort and write dataframe to new file
      print()
      text = colored('      Sorting updated word list . . . ', color='dark_grey')
      print(text)
      newdata = data.sort_values("WORD")
      newlist = newdata.to_csv('data2.csv', index=False)

      cwd = os.getcwd()
      des = cwd + "\\mainlist.csv"
      src = cwd + "\\data2.csv"
      shutil.copy(src, des)

      text = colored('      Writing sorted list to file . . . ', color='dark_grey')
      print(text)

      time.sleep(1)
      clear_console()
  # END MENU CHOICE 5 - ADD NEW WORDS TO MAIN LIST

  if user_input == '6':
    # START MENU CHOICE 6 - LOOK UP A WORD'S MEANING
    clear_console()
    print()
    txt = colored('          Look up a definition from FreeDictionary.org', color='light_yellow')
    print(txt)
    txt = colored('  ===========================================================', color='light_yellow')
    print(txt)
    print()

    while True:

      if not internet_status:
        text = colored('     Internet not available, press [Enter] to return to menu', color='light_red')
        print(text, end='')
        word = input()
        break

      else:
        txt = colored('    Enter a word or [Enter] to exit: ', color='light_cyan')
        print(txt, end='')
        word = input()

      if word == '':
        break

      else:

        uri = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + word
        response = requests.get(uri)

        if 'No Definitions Found' in response.text:
          txt = colored('      Word not found, try again: ', color='light_red')
          print(txt)
          print()

        else:
          text = (response.text).split('[')
          print()

          for index in range(len(text)):
            part = text[index]

            if 'noun' in part:
              j = index + 1
              dfn = text[j]
              defpart = dfn.split(':')
              meaning = defpart[1]
              lng = len(meaning)

              if lng >= 70:
                nd = 60
              else:
                nd = lng - 10

              meaning = meaning[1:nd]

              txt = colored('      Noun:      ', color='light_green')
              print(txt + meaning)
              print()

            if 'verb' in part:
              j = index + 1
              dfn = text[j]
              defpart = dfn.split(':')
              meaning = defpart[1]
              lng = len(meaning)

              if lng >= 70:
                nd = 60
              else:
                nd = lng - 10

              meaning = meaning[1:nd]
              txt = colored('      Verb:      ', color='light_green')
              print(txt + meaning)
              print()

            if 'adverb' in part:
              j = index + 1
              dfn = text[j]
              defpart = dfn.split(':')
              meaning = defpart[1]
              lng = len(meaning)

              if lng >= 70:
                nd = 60
              else:
                nd = lng - 10

              meaning = meaning[1:nd]
              txt = colored('      Adverb:    ', color='light_green')
              print(txt + meaning)
              print()

            if 'adjective' in part:
              j = index + 1
              dfn = text[j]
              defpart = dfn.split(':')
              meaning = defpart[1]
              lng = len(meaning)

              if lng >= 70:
                nd = 60
              else:
                nd = lng - 10

              meaning = meaning[1:nd]
              txt = colored('      Adjective: ', color='light_green')
              print(txt + meaning)
              print()

    print()

    time.sleep(1)
    clear_console()
    # END MENU CHOICE 6 - LOOK UP A WORD'S MEANING

  if user_input == '7':
    # START MENU CHOICE 7 - ADD WORD TO MAIN LIST
    clear_console()
    word_removed = 'N'
    print()
    data = pd.read_csv('mainlist.csv')

    text = colored('           Remove a Word from Main Word List', color='light_yellow')
    print(text)
    text = colored('  ===================================================', color='light_yellow')
    print(text)

    text = colored('  Hint: To remove a word that you just added, use the', color='light_green')
    print(text)
    text = colored('  up arrow to scroll through recent keyboard entries.', color='light_green')
    print(text)

    while True:
      print()
      text = colored('    Word to remove or [Enter] only to quit: ', color='light_cyan')
      print(text, end='')
      user_input = input()

      if user_input == '':
        print()
        text = colored('    [Enter] only pressed, returning to main menu.', color='dark_grey')
        print(text)
        time.sleep(1)
        break

      else:
        user_input = user_input.upper()
        if user_input in data.WORD.values:
          data2 = data[data.WORD != user_input]
          data = data2
          txt = '      "' + user_input + '" removed from Main Word List'
          text = colored(txt, color='light_green')
          print(text)
          word_removed = 'Y'

        else:
          txt = '      "' + user_input + '" not in Main Word List'
          text = colored(txt, color='light_red')
          print(text)

    if word_removed == 'Y':
      # sort and write dataframe to new file
      print()
      text = colored('      Sorting updated word list . . . ', color='dark_grey')
      print(text)
      newlist = data.to_csv('data2.csv', index=False)

      cwd = os.getcwd()
      des = cwd + "\\mainlist.csv"
      src = cwd + "\\data2.csv"
      shutil.copy(src, des)

      text = colored('      Writing sorted list to file . . . ', color='dark_grey')
      print(text)

    clear_console()
  # END MENU CHOICE 7 - ADD WORD TO MAIN LIST
  
  # START MENU CHOICE 8 - LAUNCH WORDLE GAME IN BROWSER
  if user_input == '8':
    webbrowser.open('https://wordlegame.org')

  # END MENU CHOICE 8 - LAUNCH WORDLE GAME IN BROWSER
  
  # START MENU CHOICE X - EXIT PROGRAM
  if user_input == 'X' or user_input == 'x':
    print()
    text = colored('          Exiting program, Goodbye. ', color='light_cyan')
    print(text)
    print()
    time.sleep(1)
    break
  # END MENU CHOICE X - EXIT PROGRAM

# END OF MAIN PROGRAM LOOP
exit()    
