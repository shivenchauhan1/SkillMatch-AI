import unittest
from src.matcher import extract_skills,flatten_skills,load_catalogues,analyze_profile,similarity_score
class MatcherTests(unittest.TestCase):
 def test_extract_skill(self):
  cat,_=load_catalogues(); found=extract_skills("I use Python, SQL and pandas.",flatten_skills(cat))
  self.assertIn("python",found); self.assertIn("sql",found); self.assertIn("pandas",found)
 def test_empty_similarity(self): self.assertEqual(similarity_score("","Data Analyst"),0.0)
 def test_role_analysis(self):
  result=analyze_profile("Python SQL pandas Excel","Data Analyst")
  self.assertIn("sql",result["matched_skills"]); self.assertGreaterEqual(result["skill_coverage"],0); self.assertLessEqual(result["skill_coverage"],100)
if __name__=="__main__": unittest.main()
