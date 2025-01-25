import unittest

from scraper import filter

class TestFilter(unittest.TestCase):
    def test_check_art_type(self):
        pub1 = {'artType': "Aviso de Licitação"}
        pub2 = {'artType': "Aviso de Anulação"}
        
        self.assertTrue(filter.check_art_type(pub1, "Aviso de Licitação", "Extrato de Contrato"))
        self.assertFalse(filter.check_art_type(pub2, "Aviso de Licitação", "Extrato de Contrato"))
        
    def test__check_all(self):
        self.assertTrue(filter._check_all(["a", "b", "c"], ["a", "b", "c", "d"]))
        self.assertTrue(filter._check_all(["a", "b", "c"], ["a", "b", "c"]))
        self.assertTrue(filter._check_all([], ["a", "b", "c"]))
        
        self.assertFalse(filter._check_all(["a", "b", "c"], ["a", "b"]))
        
    def test__check_any(self):
        self.assertTrue(filter._check_any(["a", "b", "e"], ["a", "b", "c", "d"]))
        
        self.assertFalse(filter._check_any(["aa", "bb", "cc"], ["a", "b", "c", "d"]))
        
        self.assertTrue(filter._check_any([], ["a", "b", "c", "d"]))
        
    
    def test__check_not_any(self):
        self.assertTrue(filter._check_not_any(["e", "f",], ["a", "b", "c", "d"]))
        
        self.assertFalse(filter._check_not_any(["a", "bb", "cc"], ["a", "b", "c", "d"]))
        
        self.assertTrue(filter._check_not_any([], ["a", "b", "c", "d"]))
        
        
    def test_check_hierarchy_list(self):
        r1, r2, r3 = filter.check_hierarchy_list({'hierarchyList':["a", "b","c"]}, ["a", "d", "e"], ["c", "f"], ["a", "b"])
        # r1 -> True
        # r2 -> False
        # r3 -> True
        self.assertTrue(r1)
        self.assertFalse(r2)
        self.assertTrue(r3)
        
        r1, r2, r3 = filter.check_hierarchy_list({'hierarchyList':["a", "b","c"]}, [], [], []) # no filters
        # r1 -> True
        # r2 -> True
        # r3 -> True
        self.assertTrue(r1)
        self.assertTrue(r2)
        self.assertTrue(r3)
        
        r1, r2, r3 = filter.check_hierarchy_list({'hierarchyList':["a", "b","c"]}, ["a", "d", "e"], ["c", "f"], ["a", "b", "d"])
        # r1 -> True
        # r2 -> True
        # r3 -> False
        self.assertTrue(r1)
        self.assertFalse(r2)
        self.assertFalse(r3)
         