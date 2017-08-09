import unittest
import requests
import urllib
import os
import sys

TEST_URL = "http://localhost:5000/api/api/workspace/"
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = sys.path[0]

class testAPI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_workspace(self):
        req_url = TEST_URL
        col_name = 'mycol3/'
        payload = {'collection_name': col_name}
        r = requests.post(req_url, params=payload)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_put_file(self):
        req_url = TEST_URL + urllib.quote_plus('mycol/')
        upload_file = os.path.join(TEST_DIR,'test_upload.txt')
        file_to_upload = {'file': open(upload_file, 'rb')}
        r = requests.put(req_url, files=file_to_upload)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_get_file(self):
        req_url = TEST_URL + urllib.quote_plus('mycol/test_upload.text')
        r = requests.get(req_url)
        print(r.text)
        self.assertEqual(200, r.status_code)

    def test_renaming_file(self):
        req_url = TEST_URL + urllib.quote_plus('mycol/')
        payload = {"current_file_name": "test_upload.txt",
                   "new_file_name": "renamed_test_upload.txt"
                   }
        r = requests.patch(req_url, json=payload)
        print(r.text)
        self.assertEqual(200, r.status_code)


    if __name__ == '__main__':
       unittest.main()
