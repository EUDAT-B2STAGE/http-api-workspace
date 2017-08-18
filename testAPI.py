import unittest
import requests
import urllib
import os
import sys

TEST_URL = "http://localhost:5000/api/api/workspace/"
#TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = sys.path[0]
MYWORKSPACE = 'mycol/'
MYFILE = 'test_upload.txt'
MY_RENAMED_FILE = "renamed_test_upload.txt"

class testAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Test Dir: ', TEST_DIR)
        print('Base test URL: ', TEST_URL)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_aa_create_workspace(self):
        req_url = TEST_URL
        payload = {'collection_name': MYWORKSPACE}
        r = requests.post(req_url, params=payload)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_ba_put_file(self):
        req_url = TEST_URL + urllib.quote_plus(MYWORKSPACE)
        upload_file = os.path.join(TEST_DIR,MYFILE)
        file_to_upload = {'file': open(upload_file, 'rb')}
        r = requests.put(req_url, files=file_to_upload)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_ca_get_file(self):
        relative_url = MYWORKSPACE + MYFILE
        req_url = TEST_URL + urllib.quote_plus(relative_url)
        r = requests.get(req_url)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_da_renaming_file(self):
        req_url = TEST_URL + urllib.quote_plus(MYWORKSPACE)
        payload = {"current_file_name": MYFILE,
                   "new_file_name": MY_RENAMED_FILE
                   }
        r = requests.patch(req_url, json=payload)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_ea_delete_file(self):
        relative_url = MYWORKSPACE + MY_RENAMED_FILE
        req_url = TEST_URL + urllib.quote_plus(relative_url)
        r = requests.delete(req_url)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_fa_delete_workspace(self):
        req_url = TEST_URL
        payload = {'collection_name': MYWORKSPACE}
        r = requests.delete(req_url, params=payload)
        print(r.text)
        self.assertEqual(200, r.status_code)

'''
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(testAPI('test_create_workspace'))
    test_suite.addTest(testAPI('test_put_file'))
    test_suite.addTest(testAPI('test_get_file'))
    test_suite.addTest(testAPI('test_renaming_file'))
    #test_suite.addTest(testAPI('test_delete_file'))
    return test_suite
'''

if __name__ == '__main__':
    #runner = unittest.TextTestRunner()
    #runner.run(suite())
    unittest.main()
