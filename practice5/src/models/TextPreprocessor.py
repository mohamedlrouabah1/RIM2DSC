from collections import defaultdict
import copyreg
import os
import re
import types
import xml.dom.minidom as minidom
from sys import stderr
from multiprocessing import Pool
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
from string import punctuation
from tqdm import tqdm
from utilities.config import STOPWORDS_DIR, START_TAG
from xml.dom.minidom import Node, parse, parseString


def _pickle_method(method):
    attached_object = method.im_self or method.im_class
    func_name = method.im_func.func_name

    if func_name.startswith('pre_'):
        func_name = filter(
            lambda method_name: method_name.startswith('_') 
            and
            method_name.endswith(func_name),
            dir(attached_object)
            )[0]

    return (getattr, (attached_object, func_name))
        
copyreg.pickle(types.MethodType, _pickle_method)


class TextPreprocessor:
    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer=None, collection_pattern=None):
        self.tag_id_counter = 0
        if exclude_stopwords:
            with open(STOPWORDS_DIR, 'r') as f:
                self.stopwords = set(f.read().splitlines() + list(punctuation))
        else:
            self.stopwords = set()        

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
            self.collection_pattern = re.compile(r'<article><id>(.*?)</id>(.*?)</article>', re.DOTALL)

    def _identity(x):
        return x

    def _normalize(self, w):
        return self.stemming(self.lemmatizing(w)) # type: ignore
    
    def _tokenize(self, w):
        return word_tokenize(w)
    
    def _is_valid_token(self, w):
        return w.isalpha() and w not in self.stopwords


    def load_and_lower_text_collection(self, path) -> str:
        """
        Read the document collection from a file.

        Returns:
            str: the document collection as a lowered string
        """
        with open(path, 'r', encoding='utf-8') as f:
            document_collection_str = f.read().lower()
        return document_collection_str
    
    def doc_preprocessing(self, doc:list) -> list:
        return [
            self._normalize(token)
            for token in self._tokenize(doc)
            if self._is_valid_token(token)
        ]
    
    def _preprocessing(self, doc_id,tag_path, content):
        return (doc_id, tag_path, self.doc_preprocessing(content))


    def pre_process(self, content, use_parallel_computing=False):
        if not use_parallel_computing:
             return self.doc_preprocessing(content)
            
        # For parallel computing
        print("Using pool to preprocess documents...")
        num_processes = os.cpu_count()
        with Pool(num_processes) as executor:
            results = executor.map(
                lambda doc: (self.doc_preprocessing(doc)),
                content
            )

        return results   
    
    
    def recursive_element_extraction(self, element, current_path='', index=1):
        """
        Extrait récursivement les données des éléments et de leurs enfants.
        """
        tag_name = element.nodeName
        tag_path = f"{current_path}/{tag_name}[{index}]"
        doc_data = {}

        # Générer un identifiant unique pour le chemin de balise
        self.tag_id_counter += 1

        text_content = self._extract_text_from_element(element).strip()
        doc_data[tag_path] = text_content

        for child_index, child in enumerate(element.childNodes, start=1):
            if child.nodeType == Node.ELEMENT_NODE:
                doc_data.update(
                    self.recursive_element_extraction(child, tag_path, index=child_index)
                )
        
        return doc_data
                

    def _extract_text_from_element(self, element) -> list:
        """
        Fonction récursive pour extraire le texte de tous les éléments et de leurs enfants.

        Return:
            list(str): liste de tokens
        """
        text = ''
        for child in element.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                text += self._extract_text_from_element(child)
            elif child.nodeType == Node.TEXT_NODE:
                text += child.nodeValue + ' '
        return text
    
    def format_xpath(self, xpath):
        """
        Formater le chemin de la balise avec le format row[2] pour chaque tag.
        """
        formatted_path = xpath
        for match in re.finditer(r'/(\w+)(\[\d+\])?', xpath):
            tag_name = match.group(1)
            position = match.group(2) or '[1]'

            formatted_path = formatted_path.replace(match.group(), f'/{tag_name}{position}')

        return formatted_path
    
    def fetch_articles(self, xml_path) -> minidom.Document:
        xml_files = [f for f in os.listdir(xml_path) if f.lower().endswith('.xml')]
        articles = []
        for xml_file in tqdm(xml_files, desc="loading --- fetching ---- articles"):
            file_path = os.path.join(xml_path, xml_file)
            id = xml_file.split('.')[0]
            dom = parse(file_path).getElementsByTagName(START_TAG)
            articles += [(id, dom)]
        return articles


    def browse_article(self, xml_files, preprocessor) -> list:
        data = []
        unique_doc_ids = set()
        old_doc_id = ''
        for doc_id, tags_list in tqdm(xml_files, desc="browse ---- xml_files"):
            for article in tqdm(tags_list, desc="browse ---- tags"):
                print(article, file=stderr)
                doc_data = self.recursive_element_extraction(article)
                metadata = []
                seen_xpaths = set()
    
                for xpath, text_content in doc_data.items():
                    if xpath not in seen_xpaths:
                        seen_xpaths.add(xpath)
                        updated_xpath = self.format_xpath(xpath)
                        doc_tokens = preprocessor.doc_preprocessing(text_content)
                        metadata.append((self.tag_id_counter, updated_xpath, doc_tokens))
                        self.tag_id_counter += 1

        print(f"Number of unique documents: {len(unique_doc_ids)}", file=stderr)
        print(f"Number of documents: {len(data)}", file=stderr)
        print(data, file=stderr)
        return data
    
    
    # fetch for each file in the zip file
    # def fetch_articles(self, path):
    #     articles=[]
    #     with zipfile.ZipFile(path, 'r') as zip_file:
    #         # Iterate through each file in the ZIP archive
    #         for file_info in tqdm(zip_file.infolist(), desc="loading --- fetching ---- articles"):
    #             with zip_file.open(file_info.filename) as xml_file:
    #                 # Parse each XML document
    #                 xml_content = xml_file.read()
    #                 # print(f"XML Content for {file_info.filename}:\n{xml_content}")
    #                 dom = parse(BytesIO(xml_content)).getElementsByTagName('article')
    #                 articles.append(dom)
                    
    #     return articles

    # def browse_article(self, articles, preprocessor) -> list:
    #     """
    #     Browse an article and extract its text.
    #     """
    #     data = []
    #     for xml_article in articles:
    #         # Directly use the provided structured XML document
    #         elements = [f"{xml_article.tagName}/{element.tagName}" for element in xml_article.childNodes if element.nodeType == element.ELEMENT_NODE]
    #         data.extend(elements)
    #     return data
    
    
    
    # browse for each file in the zip file
    # def browse_article(self, articles_list, preprocessor):
    #     """
    #     Browse through a list of articles and extract relevant information.
    #     """
    #     data = []

    #     for articles in tqdm(articles_list , desc="browse ---- articles"):
    #         for article in articles:
    #             doc_id = ''
    #             content = ''

    #             # Extract doc_id
    #             title_elements = article.getElementsByTagName('title')
    #             if title_elements:
    #                 title_element = title_elements[0]
    #                 sibling = title_element.nextSibling
    #                 while sibling and sibling.nodeType != sibling.ELEMENT_NODE:
    #                     sibling = sibling.nextSibling
    #                 if sibling and sibling.tagName == 'id':
    #                     doc_id = sibling.firstChild.nodeValue if sibling.firstChild else ''

    #             # Extract content
    #             content = self._extract_text_from_element(article)
    #             doc_tokens = preprocessor.doc_preprocessing(content)

    #             data.append({'doc_id': doc_id, 'content': doc_tokens})

    #     return data
    
    
    
    
    
    
        # def browse_article(self, articles, Document, preprocessor, documents, granularity, use_parallel_computing) -> list:
    #     """
    #     Browse an article and extract its text.
    #     """
    #     data = []
    #     for article in articles:
    #         title = ''
    #         doc_id = ''
    #         body = ''
    #         abstract = ''
    #         section = ''
    #         paragraph = ''

    #         # Extract title and id
    #         title_elements = article.getElementsByTagName('title')
    #         if title_elements:
    #             title_element = title_elements[0]
    #             title = title_element.firstChild.nodeValue if title_element.firstChild else ''  # type: ignore
    #             sibling = title_element.nextSibling
    #             while sibling and sibling.nodeType != sibling.ELEMENT_NODE:
    #                 sibling = sibling.nextSibling
    #             if sibling and sibling.tagName == 'id':
    #                 doc_id = sibling.firstChild.nodeValue if sibling.firstChild else ''

    #         # Extract body similar to above or as per your XML structure
    #         body_elements = article.getElementsByTagName('bdy')
    #         if body_elements:
    #             for body_element in body_elements:
    #                 body += body_element.firstChild.nodeValue if body_element.firstChild else ''  # type: ignore

    #         # Extract sections and paragraphs
    #         section_elements = article.getElementsByTagName('section')
    #         if section_elements:
    #             for section_element in section_elements:
    #                 section += section_element.firstChild.nodeValue if section_element.firstChild else ''  # type: ignore

    #         # Extract abstract
    #         abstract_elements = article.getElementsByTagName('abstract')
    #         if abstract_elements:
    #             for abstract_element in abstract_elements:
    #                 abstract += abstract_element.firstChild.nodeValue if abstract_element.firstChild else ''

    #         # Extract paragraphs
    #         paragraph_elements = article.getElementsByTagName('p')
    #         if paragraph_elements:
    #             for paragraph_element in paragraph_elements:
    #                 paragraph += paragraph_element.firstChild.nodeValue if paragraph_element.firstChild else ''  # type: ignore

    #         # Combine title and body, preprocess, and create Document objects
    #         combined_text = f"{title} {abstract} {body} {section} {paragraph}"
    #         doc_tokens = preprocessor.doc_preprocessing(combined_text)
    #         documents.append(Document(doc_id, doc_tokens))

    #         data.append({'doc_id': doc_id, 'title': title, 'body': body, 'abstract': abstract, 'section': section,
    #                     'paragraph': paragraph})
    #     return data
    