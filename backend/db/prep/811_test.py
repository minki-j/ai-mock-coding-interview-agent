import unittest



class Test(unittest.TestCase):
    def test_1(self):
        solution = Solution()
        self.assertEqual(
            set(
                solution.subdomainVisits(
                    [
                        "900 google.mail.com",
                        "50 yahoo.com",
                        "1 intel.mail.com",
                        "5 wiki.org",
                    ]
                )
            ),
            set(
                [
                    "901 mail.com",
                    "50 yahoo.com",
                    "900 google.mail.com",
                    "5 wiki.org",
                    "5 org",
                    "1 intel.mail.com",
                    "951 com",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
