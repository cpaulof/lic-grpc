import unittest
import datetime
from unittest.mock import Mock, patch

import config

config.DATABASE_URL = config.DATABASE_URL.replace("db.", "test_db.")

from database import service


class TestService(unittest.TestCase):
    def test_create_pub_from_do3(self):
        pub = {"pubName":"DO3","urlTitle":"aviso-de-licitacao-587161876","numberPage":"231","subTitulo":"","titulo":"",
                "title":"AVISO DE LICITAÇÃO","pubDate":"30/09/2024",
                "content":"AVISO DE LICITAÇÃO PREGÃO ELETRÔNICO Nº 5/2024 O MUNICÍPIO DE ALEXÂNIA, Estado de Goiás, torna público, para conhecimento dos interessados, que realizará licitação, na modalidade PREGÃO, em sua forma ELETRÔNICA, com critério de julgamento menor preço global, objetivando a contratação de empresa especializada para a execução de recapeamento asfáltico em vias públicas do Município de Alexânia/GO. In...",
                "editionNumber":"189","hierarchyLevelSize":3,"artType":"Aviso de Licitação",
                "pubOrder":"DO300075:00008:00035:00000:00000:00000:00000:00000:00000:00000:00079:00000",
                "hierarchyStr":"Prefeituras/Estado de Goiás/Prefeitura Municipal de Alexânia",
                "hierarchyList":["Prefeituras","Estado de Goiás","Prefeitura Municipal de Alexânia"]}
        serv = service.Service()
        self.assertTrue(serv.create_pub_from_do3(pub))
    
    def test_get_publication_by_url(self):
        url = 'aviso-de-licitacao-587161876'
        serv = service.Service()
        r = serv.get_publication_by_url(url)
        r2 = serv.get_publication_by_url("asdasda")
        self.assertIsInstance(r, service.models.Publication)
        self.assertIsInstance(r2, None.__class__)
        
        