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
from xml.dom.minidom import Node, parse, parseString
import xml.etree.ElementTree as ET



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
    
    def _preprocessing(self, doc_id,tag_path, content):
        return (doc_id, tag_path, self.doc_preprocessing(content))

    # def pre_process(self, content, use_parallel_computing=False):
    #     if not use_parallel_computing:
    #          return self.doc_preprocessing(content)
            

    #     # For parallel computing
    #     print("Using pool to preprocess documents...")
    #     num_processes = os.cpu_count()
    #     with Pool(num_processes) as executor:
    #         results = executor.map(
    #             lambda doc: (self.doc_preprocessing(doc)),
    #             content
    #         )

    #     return results
                
    def fetch_articles(self, path):
        dom = parse(path)
        return dom.getElementsByTagName('article')
   

    def browse_article(self, articles, Document, preprocessor, documents, granularity, use_parallel_computing) -> list:
        """
        Parcourir un article et extraire son texte.
        """
        data = []
        for article in articles:
            doc_data = {}
            doc_id = ''
            if article.getElementsByTagName('title'):
                title_element = article.getElementsByTagName('title')[0]
                sibling = title_element.nextSibling
                while sibling and sibling.nodeType != sibling.ELEMENT_NODE:
                    sibling = sibling.nextSibling
                if sibling and sibling.tagName == 'id':
                    doc_id = sibling.firstChild.nodeValue if sibling.firstChild else ''

            self.recursive_element_extraction(article, doc_data, granularity)

            # Prétraiter et créer des objets Document pour chaque balise
            for tag_path, text_content in doc_data.items():
                updated_tag_path = self.format_tag_path(tag_path)
                doc_tokens = preprocessor.doc_preprocessing(text_content)
                # Ajoutez doc_id et tag_path à l'objet Document
                doc = Document(doc_id, doc_tokens, updated_tag_path, tag_path)
                documents.append(doc)

                # Ajoutez les données dans la liste de résultats
                data.append({
                    'doc_id': doc_id,
                    'tag_path': updated_tag_path,
                    'content': doc_tokens
                })

        return data



    def recursive_element_extraction(self, element, doc_data, granularity, current_path='', index=1):
        """
        Fonction récursive pour extraire les données des éléments et de leurs enfants.
        """
        tag_name = element.nodeName
        tag_path = f"{current_path}/{tag_name}[{index}]"

        text_content = self.extract_text_from_element(element).strip()
        doc_data[tag_path] = text_content

        for child_index, child in enumerate(element.childNodes, start=1):
            if child.nodeType == Node.ELEMENT_NODE:
                self.recursive_element_extraction(child, doc_data, granularity, tag_path, index=child_index)
                
    def extract_text_from_element(self, element):
        """
        Fonction récursive pour extraire le texte de tous les éléments et de leurs enfants.
        """
        text = ''
        for child in element.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                text += self.extract_text_from_element(child)
            elif child.nodeType == Node.TEXT_NODE:
                text += child.nodeValue + ' '
        return text
    
    def format_tag_path(self, tag_path):
        """
        Formater le chemin de la balise avec le format row[2] pour chaque tag.
        """
        formatted_path = tag_path
        for match in re.finditer(r'/(\w+)(\[\d+\])?', tag_path):
            tag_name = match.group(1)
            position = match.group(2) or '[1]'
            formatted_path = formatted_path.replace(match.group(), f'/{tag_name}{position}')

        return formatted_path