import unittest
import json
import requests


class TestApi(unittest.TestCase):

    host_url = 'http://localhost:8081'

    list_response = {
        "results": [
            {
                "bio": "I have over 20 years of experience running People/HR teams and creating company cultures. I believe that great cultures drive great businesses. I love to help companies leverage their values to create and maintain great cultures to drive their business.",
                "id": "cindyhall",
                "name": "Cindy Hall",
                "picture": "https://ti.bolster.com/a/5ffe2989cbf0a1006f2593de/1611263724"
            },
            {
                "bio": "Technical leader and problem solver with over 25-years of experience developing software and leading high-performing teams.",
                "id": "samnewton",
                "name": "Sam Newton",
                "picture": "https://ti.bolster.com/a/630e328375b819c626b18685/1665609168"
            },
            {
                "bio": "Experienced B2B Marketing Leader. Passionate about technology, collaboration, leadership and learning.",
                "id": "noahbraxton",
                "name": "Noah Braxton",
                "picture": "https://ti.bolster.com/a/630e328375b819c626b18685/1665609168"
            },
            {
                "bio": "Founder/CEO with 25+ years of experience",
                "id": "michaelboyd",
                "name": "Michael Boyd",
                "picture": "https://ti.bolster.com/a/630e328375b819c626b18685/1665609168"
            },
            {
                "bio": "25 years of experience working on security/privacy issues, data governance issues, and protecting and improving data through industry policy, regulatory policy relations, and technical solutions.",
                "id": "dandutch",
                "name": "Dan Dutch",
                "picture": "https://ti.bolster.com/a/630e328375b819c626b18685/1665609168"
            }
        ]
    }

    get_candidate_cindy = {
        "results": {
            "bio": "I have over 20 years of experience running People/HR teams and creating company cultures. I believe that great cultures drive great businesses. I love to help companies leverage their values to create and maintain great cultures to drive their business.",
            "experience": [
                {
                    "company": "Bolster",
                    "dates": "2020|",
                    "description": "New startup to connect on-demand executives with startups and scaleups.",
                    "title": "Co-founder"
                },
                {
                    "company": "Acme Widgets",
                    "dates": "2019|2020",
                    "description": "Fractional and advisory Chief People Officer ",
                    "title": "Chief People Officer"
                },
                {
                    "company": "Sonantic, Inc.",
                    "dates": "2008|2019",
                    "description": "Led HR for Sonantic's global business organization across 35 Countries in Europe, Middle East, and Africa. Directly supported Sonantic's President of EMEA, setting and delivering a People strategy for the region.",
                    "title": "Chief People Officer"
                }
            ],
            "name": "Cindy Hall",
            "picture": "https://ti.bolster.com/a/5ffe2989cbf0a1006f2593de/1611263724"
        }
    }

    put_candidate_cindy = [
        {"company": "Bolstear", "dates": "2020|",
         "description": "New startup to connect on-demand executives with startups and scaleups.",
         "title": "Co-founder"},
        {"company": "Acme Widgets", "dates": "2019|2020",
         "description": "Fractional and advisory Chief People Officer ", "title": "Chief People Officer"},
        {"company": "Sonantic, Inc.", "dates": "2008|2019",
         "description":
         "Led HR for Sonantic's global business organization across 35 Countries in Europe, Middle East, and Africa. Directly supported Sonantic's President of EMEA, setting and delivering a People strategy for the region.",
         "title": "Chief People Officer"}]

    def test_candidate_list(self):
        response = requests.get(
            self.host_url + "/candidates",
        )
        self.assertDictEqual(response.json(), self.list_response, "GET candidate list")

    def test_candidate_get(self):
        response = requests.get(
            self.host_url + "/candidate/cindyhall",
        )
        self.assertDictEqual(response.json(), self.get_candidate_cindy, "GET candidate cindyhall")

    def test_candidate_put(self):
        response = requests.put(
            self.host_url + "/candidate/cindyhall",
            json={"experience": self.put_candidate_cindy},
        )
        self.assertDictEqual(response.json(), {'results': 'ok'}, "PUT candidate cindyhall")


if __name__ == '__main__':
    unittest.main()
