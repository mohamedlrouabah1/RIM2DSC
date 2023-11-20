import copyreg
import glob
import os
import re
import types
from multiprocessing import Pool
from typing import Any
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
# from nltk.corpus import stopwords
from string import punctuation
from tqdm import tqdm
from utilities.config import DATA_FOLDER, STOPWORDS_DIR
from xml.dom.minidom import parse



def _pickle_method(method):
    attached_object = method.im_self or method.im_class
    func_name = method.im_func.func_name

    if func_name.startswith('pre_'):
        func_name = filter(lambda method_name: method_name.startswith('_') and method_name.endswith(func_name), dir(attached_object))[0] # type: ignore

    return (getattr, (attached_object, func_name))
        
copyreg.pickle(types.MethodType, _pickle_method)
class TextPreprocessor:
    # get stopwords from stopwords package
    # os.path.join(os.path.dirname(__file__), STOPWORDS_DIR)
    # xml_files = glob.glob(os.path.join(DATA_FOLDER, "*.xml"))
    def _identity(x): # type: ignore
        return x

    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer=None, collection_pattern=None):
        if exclude_stopwords:
            #self.stopwords = set(stopwords.words('english') + list(punctuation))
            with open(STOPWORDS_DIR, 'r') as f:
                self.stopwords = set(f.read().splitlines() + list(punctuation))
        else:
            self.stopwords = set()

        # if exclude_digits:
        #     self.is_valid_token = lambda w: w.isalpha() and w not in self.stopwords
        # else:
        #     self.is_valid_token = lambda w: w not in self.stopwords
        

        # if tokenizer == "regex":
        #     # self.tokenize = lambda text: re.findall(r"\b\w+(?:'\w+)?\b", text)
        # else: 
        #     #tokenizer == "nltk"
        #     # self.tokenize = lambda text: word_tokenize(text)

        # lamda function don't work with // computation bc its use pickle
        # if lemmer and stemmer:
        #     self.lemmatizer = WordNetLemmatizer()
        #     self.stemmer = PorterStemmer()
        #     self.normalize = lambda w : self.stemmer.stem(self.lemmatizer.lemmatize(w))
        # elif lemmer:
        #     self.lemmatizer = WordNetLemmatizer()
        #     self.normalize = lambda w : self.lemmatizer.lemmatize(w)
        # elif stemmer:
        #     self.stemmer = PorterStemmer()
        #     self.normalize = lambda w : self.stemmer.stem(w)
        # else:
        #     self.normalize = lambda w : w
        if lemmer:
            self.lemmatizer = WordNetLemmatizer()
            self.lemmatizing = self.lemmatizer.lemmatize
        else:
            self.lemmatizing = TextPreprocessor._identity

        if stemmer:
            self.stemmer = PorterStemmer()
            self.stemming = self.stemmer.stem
        else:
            self.stemming = TextPreprocessor._identity

        if collection_pattern:
            self.collection_pattern = collection_pattern
        else:
            self.collection_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)

    def normalize(self, w):
        return self.stemming(self.lemmatizing(w)) # type: ignore
    
    def tokenize(self, w):
        return word_tokenize(w)
    
    def is_valid_token(self, w):
        return w.isalpha() and w not in self.stopwords


    def load_and_lower_text_collection(self, path) -> str:
        """
        Read the document collection from a file.
        Handles both regular and gzipped files.

        Returns:
            str: the document collection as a lowered 
                 string
        """
        with open(path, 'r', encoding='utf-8') as f:
            document_collection_str = f.read().lower()
        return document_collection_str
    
    def doc_preprocessing(self, doc):
        return [
            self.normalize(token)
            for token in self.tokenize(doc)
            if self.is_valid_token(token)
        ]
    
    def _preprocessing(self, doc_id, content):
        return (doc_id, self.doc_preprocessing(content))

    def pre_process(self, documents,tag_names, use_parallel_computing=False):
        if not use_parallel_computing:
            return [
                (doc['doc_id'], self.doc_preprocessing(doc['title'] + " " + doc['abstract'] + " " + doc['body'] + " " + doc['section'] + " " + doc['paragraph']))
                for doc in documents
            ]
            # return [
            #     (
            #         doc.get('doc_id', ''),
            #         self.doc_preprocessing(
            #             ' '.join(doc.get(tag, '') for tag in tag_names)
            #         )
            #     )
            #     for doc in documents
            # ]


        # For parallel computing
        print("Using pool to preprocess documents...")
        num_processes = os.cpu_count()
        with Pool(num_processes) as executor:
            results = executor.map(lambda doc: (doc['doc_id'], self.doc_preprocessing(doc['title'] + " " + doc['abstract'] + " " + doc['body'] + " " + doc['section'] + " " + doc['paragraph'])), documents)

        return list(results)


    def fetch_articles(self, path):
        dom = parse(path)
        return dom.getElementsByTagName('article')
   
    
    def browse_article(self, path, Document, preprocessor,documents, granurality) -> list:
        """
        Browse an article and extract its text.
        """
        data = []
        articles = self.fetch_articles(path)
        for article in articles:
            title = ''
            doc_id = ''
            body = ''
            abstract=''
            section=''
            paragraph=''
            granurality = granurality            
            # Extract title and id
            if article.getElementsByTagName('title'):
                title_element = article.getElementsByTagName('title')[0]
                title = title_element.firstChild.nodeValue if title_element.firstChild else '' # type: ignore
                sibling = title_element.nextSibling
                while sibling and sibling.nodeType != sibling.ELEMENT_NODE:
                    sibling = sibling.nextSibling
                if sibling and sibling.tagName == 'id':
                    doc_id = sibling.firstChild.nodeValue if sibling.firstChild else ''

            # Extract body similar to above or as per your XML structure
            if article.getElementsByTagName('bdy'):
                body_element = article.getElementsByTagName('bdy')[0]
                body = body_element.firstChild.nodeValue if body_element.firstChild else '' # type: ignore
                
            # Extract sections and paragraphs
            if article.getElementsByTagName('section'):
                section_element = article.getElementsByTagName('section')[0]
                section = section_element.firstChild.nodeValue if section_element.firstChild else '' # type: ignore
            
            # Extract abstract
            if article.getElementsByTagName('abstract'):
                abstract_element = article.getElementsByTagName('abstract')[0]
                abstract = abstract_element.firstChild.nodeValue if abstract_element.firstChild else '' # type: ignore
            
            # Extract paragraphs
            if article.getElementsByTagName('p'):
                paragraph_element = article.getElementsByTagName('p')[0]
                paragraph = paragraph_element.firstChild.nodeValue if paragraph_element.firstChild else '' # type: ignore
            
            # Combine title and body, preprocess, and create Document objects
            combined_text = f"{doc_id} {title} {abstract} {body} {section} {paragraph}"
            doc_tokens = preprocessor.doc_preprocessing(combined_text)
            documents.append(Document(doc_id, doc_tokens))

            data.append({'doc_id': doc_id, 'title': title, 'body': body, 'abstract': abstract, 'section': section, 'paragraph': paragraph})
        return data

    
    # def browse_article(self, path, Document, preprocessor, documents, granularity_info) -> tuple:
    #     """
    #     Browse an article and extract its text.
    #     """
    #     data = []
    #     articles = self.fetch_articles(path)
    #     tag_names = set()  # Collect unique tag names

    #     for article in articles:
    #         title = ''
    #         doc_id = ''
    #         body = ''
    #         abstract = ''
    #         section = ''
    #         paragraph = ''
    #         granularity_info = None  # Initialize granularity information

    #         # Extract title and id
    #         if article.getElementsByTagName('title'):
    #             title_element = article.getElementsByTagName('title')[0]
    #             title = title_element.firstChild.nodeValue if title_element.firstChild else ''  # type: ignore
    #             sibling = title_element.nextSibling
    #             while sibling and sibling.nodeType != sibling.ELEMENT_NODE:
    #                 sibling = sibling.nextSibling
    #             if sibling and sibling.tagName == 'id':
    #                 doc_id = sibling.firstChild.nodeValue if sibling.firstChild else ''

    #         # Extract body similar to above or as per your XML structure
    #         if article.getElementsByTagName('bdy'):
    #             body_element = article.getElementsByTagName('bdy')[0]
    #             body = body_element.firstChild.nodeValue if body_element.firstChild else ''  # type: ignore

    #         # Extract sections and paragraphs
    #         for elem in article.childNodes:
    #             if elem.nodeType == elem.ELEMENT_NODE:
    #                 tag_name = elem.tagName.lower()
    #                 tag_names.add(tag_name)  # Add the tag name to the set

    #                 # Update granularity info for sections
    #                 if tag_name.startswith('section'):
    #                     granularity_level = int(tag_name[len('section'):])
    #                     section = f"{tag_name} {granularity_level}"
    #                     granularity_info = (tag_name, granularity_level)

    #                 # Extract abstract
    #                 elif tag_name == 'abstract':
    #                     abstract_element = article.getElementsByTagName('abstract')[0]
    #                     abstract = abstract_element.firstChild.nodeValue if abstract_element.firstChild else ''  # type: ignore

    #                 # Extract paragraphs and other tags
    #                 elif tag_name in ['p', 'other_tag']:  # Add more tag names as needed
    #                     paragraph_element = article.getElementsByTagName(tag_name)[0]
    #                     paragraph = paragraph_element.firstChild.nodeValue if paragraph_element.firstChild else ''  # type: ignore

    #         # Combine title and body, preprocess, and create Document objects
    #         combined_text = f"{doc_id} {title} {abstract} {body} {section} {paragraph}"
    #         doc_tokens = preprocessor.doc_preprocessing(combined_text)

    #         # Append Document object with granularity info to the documents list
    #         documents.append(Document(doc_id, doc_tokens, granularity_info=granularity_info))

    #         data.append({'doc_id': doc_id, 'title': title, 'body': body, 'abstract': abstract, 'section': section, 'paragraph': paragraph})

    #     return data, list(tag_names)  # Return both data and tag_names