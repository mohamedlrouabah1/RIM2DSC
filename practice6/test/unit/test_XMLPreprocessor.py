
import sys
import xml.dom.minidom
from models.xml.XMLPreprocessor import XMLPreprocessor


STOPWORDS_DIR = "utilities/stopwords"

class TestXMLPreprocessor:
    XMLPreprocessor = XMLPreprocessor(exclude_stopwords=False)

    def test_fetch_articles_return_types(self): 
        xml_doc = self._get_1_xml_doc()
        assert type(xml_doc) == type(())
        assert type(xml_doc[0]) == type("")
        assert type(xml_doc[1]) == type(xml.dom.minidom.Document())
        
    
    def test_fetch_articles_tag_article(self):
        xml_doc = self._get_1_xml_doc()[1]
        xml_real = self._get_minidom_1_xml_to_str()

        assert len(xml_doc.getElementsByTagName("article")) == 1
        assert len(xml_doc.getElementsByTagName("p")) == 4

        article = xml_doc.getElementsByTagName("article")[0]
        real_article = xml_real.getElementsByTagName("article")[0]

    def test_fetch_articles_tag_article_childs(self):
        article = self._get_1_xml_doc()[1].getElementsByTagName("article")[0]
        assert len(article.childNodes) == 9 # i.e space count as black text node


    def test_browse_article(self):
        article = [self._get_1_xml_doc()]
        xml_element = TestXMLPreprocessor.XMLPreprocessor.pre_process(article)[0].content

        assert len(xml_element.childs) == 4
        assert len(xml_element.content) == 5
        assert xml_element.id == "1:/article[1]"
        assert xml_element.childs["/article[1]/p[3]"].get_xpath() == "/article[1]/p[3]"
        assert xml_element.childs["/article[1]/p[3]"].get_doc_id() == "1"









    def _get_1_xml_doc(self) -> xml.dom.minidom.Document:
        XMLPreprocessor = TestXMLPreprocessor.XMLPreprocessor
        xml_doc = XMLPreprocessor._fetch_articles("test/unit/test_data/xml_doc")[0]
        return xml_doc

    def _get_minidom_1_xml_to_str(self) ->  xml.dom.minidom.Document:
        doc = xml.dom.minidom.Document()

        article_element = doc.createElement("article")
        doc.appendChild(article_element)

        # Création des éléments <p> avec du texte et balises imbriquées
        paragraph1 = doc.createElement("p")
        paragraph1.appendChild(doc.createTextNode("Ceci est un "))
        em1 = doc.createElement("em")
        em1.appendChild(doc.createTextNode("paragraphe"))
        paragraph1.appendChild(em1)
        paragraph1.appendChild(doc.createTextNode("."))
        article_element.appendChild(paragraph1)

        paragraph2 = doc.createElement("p")
        paragraph2.appendChild(doc.createTextNode("Ceci est un "))
        b1 = doc.createElement("b")
        b1.appendChild(doc.createTextNode("autre paragraphe"))
        paragraph2.appendChild(b1)
        paragraph2.appendChild(doc.createTextNode("."))
        article_element.appendChild(paragraph2)

        paragraph3 = doc.createElement("p")
        paragraph3.appendChild(doc.createTextNode("Ceci est un "))
        em2 = doc.createElement("em")
        em2.appendChild(doc.createTextNode("paragraphe"))
        paragraph3.appendChild(em2)
        paragraph3.appendChild(doc.createTextNode(" avec un "))
        a1 = doc.createElement("a")
        a1.setAttribute("href", "http://www.google.fr")
        a1.appendChild(doc.createTextNode("lien"))
        paragraph3.appendChild(a1)
        paragraph3.appendChild(doc.createTextNode("."))
        article_element.appendChild(paragraph3)

        # Création de la section avec du texte et imbrications
        section_element = doc.createElement("section")
        section_element.appendChild(doc.createTextNode("Une section"))
        div1 = doc.createElement("div")
        div1.appendChild(doc.createTextNode("imbrication 1"))
        div1.appendChild(doc.createElement("div"))
        div2 = doc.createElement("div")
        div2.appendChild(doc.createTextNode("imbrication 2"))
        div2.appendChild(doc.createElement("div"))
        div2.appendChild(doc.createElement("div"))
        div2.appendChild(doc.createElement("div"))
        div2.appendChild(doc.createElement("div"))
        div3 = doc.createElement("p")
        div3.appendChild(doc.createTextNode("imbrication 3"))
        div2.appendChild(div3)
        div2.appendChild(doc.createTextNode("encore du texte..."))
        section_element.appendChild(div1)
        section_element.appendChild(div2)
        section_element.appendChild(doc.createTextNode("Fin de la section."))
        article_element.appendChild(section_element)

        return doc
