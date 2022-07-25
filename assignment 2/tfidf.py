import re
import math

docs = []
stopwords = []
#number of times a term appears in a doc
term_occurs = {}
#total number of terms per doc
doc_term_cnt = {}
#TF for each distinct term in a doc
tf = {}
#number of docs each word is found in
doc_num_words = {}
#IDF for each distinct term in a doc
idf = {}
#TF-IDF score for each distinct term in a doc
tfidf = {}

# -------- set up --------
def get_filenames(file):
    with open(file) as f:
        content = f.readlines()
        for st in content:
            st = st.strip()
            docs.append(st)

# ======== PREPROCESSING ========

# -------- clean --------
def clean():
    for doc in docs: #each doc
        new_lines = []
        with open(doc) as f:
            content = f.readlines()
            for line in content: #each line in a doc
                line_list = line.split()
                new_line = ''
                for word in line_list: #each word in a line in a doc
                    if 'http://' not in word and 'https://' not in word and word not in stopwords:
                        regex = re.compile('[^a-zA-Z0-9_]')
                        word = regex.sub('', word)
                        word = word.lower()
                        word = get_root(word)
                        new_line = new_line + ' ' + word
                new_lines.append(new_line.strip())

        new_file = 'preproc_' + doc
        with open(new_file,'w') as f:
            for thing in new_lines:
                f.write(f'{thing}\n')

# -------- get stopwords --------
def remove_stops(file):
    with open(file) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            stopwords.append(line)

# -------- stemming and lemmatization --------
def get_root(word):
    if (len(word) > 4):
        root = re.sub('(ing)$|(ly)$|(ment)$','',word)
        return root
    else:
        return word

# ======== COMPUTING TF-IDF SCORES ========

# -------- computing term frequency (tf) --------
def get_doc_term_cnt():
    for doc in docs:
        doc = 'preproc_' + doc
        with open(doc) as f:
            content = f.read()
            word_lst = content.split()
            doc_term_cnt[doc] = len(word_lst)

def get_term_occurrences():
    for doc in docs:
        doc = 'preproc_' + doc
        with open(doc) as f:
            curr_doc = {}
            content = f.read()
            word_lst = content.split()
            for word in word_lst:
                word_cnt = 0
                if word in curr_doc:
                    word_cnt = curr_doc[word]
                curr_doc[word] = word_cnt + 1
            term_occurs[doc] = curr_doc

def compute_term_freq():
    for doc,terms in term_occurs.items():
        curr_doc = {}
        for word,cnt in terms.items():
            word_tf = cnt / doc_term_cnt[doc]
            curr_doc[word] = word_tf
        tf[doc] = curr_doc

# -------- computing inverse document frequency (idf) --------
def get_doc_num_words():
    for doc,dict in tf.items(): #for each document in tf
        for word in dict: #for each word in a document
            word_cnt = 0
            if word not in doc_num_words: #if word is not already in doc_num_words
                for document in tf: #go through every document again
                    if word in tf[document]: #if it exists in a document increase its count
                        word_cnt += 1
                doc_num_words[word] = word_cnt

def compute_inv_doc_freq():
    for doc in docs:
        doc = 'preproc_' + doc
        with open(doc) as f:
            curr_doc = {}
            content = f.read()
            word_lst = content.split()
            for word in word_lst:
                word_idf = len(docs) / doc_num_words[word]
                word_idf = math.log(word_idf) + 1
                curr_doc[word] = word_idf
            idf[doc] = curr_doc

# -------- calculate tf-idf score --------
def calculate_tfidf():
    for doc,tf_dict in tf.items():
        idf_dict = idf[doc]
        curr_dict = {}
        for word in tf_dict:
            tfidf_word = tf_dict[word] * idf_dict[word]
            tfidf_word = round(tfidf_word, 2)
            curr_dict[word] = tfidf_word
        tfidf[doc] = curr_dict

def output_most_important():
    for doc in docs:
        pre_doc = 'preproc_' + doc
        dict = tfidf[pre_doc]
        sorted_dict = sorted(dict.items(), key=lambda x:x[1], reverse=True)
        first_five = sorted_dict[0:5]

        tfidf_doc = 'tfidf_' + doc
        with open(tfidf_doc,'w') as file:
            file.write(f'{first_five}')




# -------- main function --------
def main():
    get_filenames('tfidf_docs.txt')
    remove_stops('stopwords.txt')
    clean()
    get_doc_term_cnt()
    get_term_occurrences()
    compute_term_freq()
    get_doc_num_words()
    compute_inv_doc_freq()
    calculate_tfidf()
    output_most_important()

main()