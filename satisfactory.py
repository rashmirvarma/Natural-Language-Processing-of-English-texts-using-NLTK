##Author: Rashmi Varma
##Created: November 16, 2017

try:
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import sent_tokenize
    from nltk.corpus import cmudict
    from bs4 import BeautifulSoup
    import urllib2
    import re
    import matplotlib.pyplot as plt
    import numpy as np
except:
    ImportError

def main():
    flag = 0
    url = "http://www.gutenberg.org/ebooks/search/?query="

    while flag == 0:      
        print " \n\n 1. Score of a book\n 2. Exit"
        choice = int(raw_input("\nYour choice:"))
        if choice == 1:
            category = int(raw_input("\nPlease choose category to proceed with scoring: \n1. Animal \n2. Children's Bookshelf \n3. Classics Bookshelf \n4. Countries Bookshelf \n5. Crime Bookshelf \n6. Education Bookshelf \
            \n7. Emmy's Picks \n8. Fiction Bookshelf \n9. Fine arts Bookshelf \n10. General Works Bookshelf \n11. Geography Bookshelf \n12. History Bookshelf \n13. Language and Literature Bookshelf \n14. Law Bookshelf \
            \n15. Music Bookshelf \n16. Periodicals Bookshelf \n17. Psychology and Philosophy Bookshelf \n18. Religion Bookshelf \n19. Science Bookshelf \
            \n20. Social Sciences Bookshelf \n21. Technology Bookshelf \n22. Wars Bookshelf \n23. Quit \nYour choice::" ))
            if category == 23:
                break
            else:
                selectedCategoryUrl = createUrl(category, url)
                if selectedCategoryUrl == "Null":
                   break
                else:
                    bookTitles = []
                    bookScores = []
                    numberBooks = int(raw_input("\nPlease enter the number of books you want to see the result for:"))
                    names, links = scrapBooks(selectedCategoryUrl, numberBooks)
                    bookTitles, bookScores = scrapLinks(names, links)
                    print("\nWould you like to see the graph for the books selected by you?")
                    print("1. Yes \n2. No ")
                    gChoice = int(raw_input("Choice - "))

                    if gChoice == 1:
                        print "lp"
                        print bookTitles
                        print bookScores
                        createGraph(bookTitles, bookScores)
                        
                    elif gChoice == 2:
                        break
                    else:
                        print "Incorrect Choice"

                
                    
        if choice ==2:
            break
        

def createGraph(bookTitles, bookScores):
    try:
        fig,ax = plt.subplots(1,1,figsize=(12,3))


        y = bookScores
        x = np.arange(len(bookScores))

        ax.set_xticks(x)
        labels = [item.get_text() for item in ax.get_xticklabels()]
        for i in range(0, len(bookTitles)):
            labels[i] = bookTitles[i] 

            
                 
            
            
        plt.gcf().subplots_adjust(bottom=0.10)

        ax.set_xticklabels(labels, minor = False, rotation=0)
        plt.xlabel('Book Name')
        plt.ylabel('FRES Score')  
        plt.title('Book Name V/S FRES Score graph')               
        ax.scatter(x,y)
        plt.tick_params(labelsize=5)
 
        plt.show()

 
    except:
        print "The number of books selected consists of one or more audio books. Please try again with a different category or number combination"


def createUrl(choice, url):

    if choice == 1:
        link = url + "animal"
    elif choice == 2:
        link = url + "children"
    elif choice == 3:
        link = url + "classics"
    elif choice == 4:
        link = url + "countries"
    elif choice == 5:
        link = url + "crime"
    elif choice == 6:
        link = url + "education"
    elif choice == 7:
        link = url + "emmy"
    elif choice == 8:
        link = url + "fiction"
    elif choice == 9:
        link = url + "fine+arts"
    elif choice == 10:
        link = url + "general+works"
    elif choice == 11:
        link = url + "geography"
    elif choice == 12:
        link = url + "history"
    elif choice == 13:
        link = url + "language+and+literature"
    elif choice == 14:
        link = url + "law"
    elif choice == 15:
        link = url + "music"
    elif choice == 16:
        link = url + "periodicals"
    elif choice == 17:
        link = url + "psychology+and+philosophy"
    elif choice == 18:
        link = url + "religion"
    elif choice == 19:
        link = url + "science"
    elif choice == 20:
        link = url + "social+sciences"
    elif choice == 21:
        link = url + "technology"
    elif choice == 22:
        link = url + "wars"
    else:
        link = "Null"
    return link

def scrapBooks(selectedCategory, numberBooks):
    data = []
    relevantData = []
    links = []
    relevantLinks = []
    mainLink = "http://www.gutenberg.org"

    try:
        page = urllib2.urlopen(selectedCategory)
        soup = BeautifulSoup(page, 'html.parser')

        for everyline in soup.find_all('li', attrs={'class': 'booklink' }):

            if hasattr(everyline, "text"):
                t = everyline.text
                t = t.strip()

                data.append(t)
            for a in everyline.find_all('a', href=True):
                links.append(mainLink + a['href'])
        for i in range(0, numberBooks):
            relevantData.append(data[i])
            relevantLinks.append(links[i])

    
        return (relevantData, relevantLinks)
    except:
        print "Something went wrong while scraping this book"

def scrapLinks(names,links):
    score = []
    title = []
    
    for i in range(0, len(links)):
        url = links[i]
        try:
            scrape = scrapRelevantLinks(url,names[i])
            book_name = scrape[0]
            fres_score = scrape[1]
            title.append(book_name)
            score.append(fres_score)
        except:
            print "One or more of the books selected may have been an audio book. Please try some other category or a smaller number"
    return title,score


def scrapRelevantLinks(url,names):
    url_scrape = ""
    name_link = []
    url_final = url

    try:
        page1 = urllib2.urlopen(url_final)
        soup1 = BeautifulSoup(page1, 'html.parser')
        
        # Removing the script content
        for script in soup1(["script", "style"]):
            script.extract()  # rip it out

        cols = soup1.find_all('table', attrs={'class': 'files'})                    
        for link in cols:
            for m in link.find_all('a'):
                temp_link = m.get('href')  
                if m.text in "Plain Text UTF-8":
                    url_scrape = temp_link
                

        
        url_scrape = "http:"+url_scrape
        
        page2 = urllib2.urlopen(url_scrape)
        soup2 = BeautifulSoup(page2, 'html.parser')
        
        # Removing the script content
        for script in soup2(["script", "style"]):
            script.extract()  # rip it out                    
    
        cleaned_data = soup2.text.encode('ascii', 'ignore')
        
        
        index = str(soup2).find("Author:")
        index = index + 8
        index_new_line = str(soup2).find('\n', index)
       
        author = "Anonymous"
        
        if index != -1 and index_new_line != -1:
            author = str(soup2)[index: index_new_line+1]                   
            
            fres = fres_score(cleaned_data)
                
            print "\nBook Title: {}\nAuthor: {}FRES score: {}\nSchool level: {}\n\n".format(names,author.title(),str(fres[0]),str(fres[1]))
##            print names+"\t"+author.title()+str(fres[0])+str(fres[1])
            
            return names, str(fres[0])
            
    except urllib2.HTTPError:
        print("You may have selected an audio book!")
        return -1
    
    except:
        print("You may have selected an audio book!")
        return -1
            

def cleanText(text):
    paras = (line.strip() for line in text.splitlines())
    chunks = (words.strip() for line in paras for words in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    try:
        return re.sub("[,;@#?:/\-+!&()$]+\ *", " ", text.encode('ascii', 'ignore')).lower()
    except:
        print("There is some issue with the RegEx library")
def fres_score(sentance):
    number_of_syllables = 0
    tokenizer = RegexpTokenizer('\w+')
    x = tokenizer.tokenize(sentance)
    number_of_words = len(x)
 
    
    y = sent_tokenize(sentance)
    number_of_sentances = len(y)
    
    d = cmudict.dict()
    for word in x:
        
        try:
            number_of_syllables = number_of_syllables + [len(list(z for z in a if z[-1].isdigit())) for a in d[word.lower()]][0]
        except KeyError:
            number_of_syllables = number_of_syllables + syllables(word)
    
    
    fres_score = 206.835-(1.015*(number_of_words/float(number_of_sentances)))-(84.6*(number_of_syllables/float(number_of_words)))
    flesch_grade = (0.39*(number_of_words/float(number_of_sentances))) + (11.8*(number_of_syllables/float(number_of_words)))-15.59
    
    
    return (fres_score, flesch_grade)
def syllables(word):
    # referred from stack overflow 'Count the number of syllables in a word'
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count 

main()
