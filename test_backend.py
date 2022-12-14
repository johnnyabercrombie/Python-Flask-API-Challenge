import unittest

from app import load_api_data, users

class TestAPIBackend(unittest.TestCase):

    def test_load_api_data(self):
        load_api_data()
        self.assertIn("cindyhall", users)
        self.assertIn("samnewton", users)
        self.assertNotIn("fakeuser", users)

    def test_load_api_data_missing_user_file(self):
        with self.assertRaisesRegex(FileNotFoundError, "The user file is missing"):
            load_api_data(users_file="missing.tsv")

    def test_load_api_data_missing_experience_file(self):
        with self.assertRaisesRegex(FileNotFoundError, "The experience file is missing"):
            load_api_data(experience_file="missing.tsv")

    def test_load_api_data_missing_user_data_point(self):
        with self.assertRaisesRegex(ValueError, "The user file is missing a data point"):
            load_api_data(users_file="users_file_with_error.tsv")

    def test_load_api_data_missing_experience_data_point(self):
        with self.assertRaisesRegex(ValueError, "The experience file is missing a data point"):
            load_api_data(experience_file="experience_file_with_error.tsv")

    def test_load_api_data_bad_primary_key_specified(self):
        with self.assertRaisesRegex(ValueError, "Invalid primary key was specified"):
            load_api_data(primary_key="test")


if __name__ == "__main__":
    unittest.main()
