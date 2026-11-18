import os,tempfile,unittest,json
from unittest.mock import patch
os.environ['HADIRIN_DATA']=tempfile.mkdtemp()
os.environ.pop('GROQ_API_KEY',None)
from fastapi.testclient import TestClient
from app import app,db,now
class AgentTest(unittest.TestCase):
 def test_agent(self):
  admin=TestClient(app);emp=TestClient(app)
  admin.post('/api/setup',json={'name':'Admin','email':'admin@test.id','password':'Password123!'})
  admin.post('/api/login',json={'email':'admin@test.id','password':'Password123!'})
  admin.post('/api/users',json={'name':'Person Secret','email':'user@test.id','password':'Password123!'})
  emp.post('/api/login',json={'email':'user@test.id','password':'Password123!'})
  day=now().date().isoformat()
  with db() as c:
   for uid in [1,2]:c.execute('INSERT INTO attendance(user_id,day,at,late,features) VALUES(?,?,?,?,?)',(uid,day,now().isoformat(),10*uid,'[]'))
  b={'start_date':day,'end_date':day,'question':'Buat laporan','use_groq':False}
  x=emp.post('/api/assistant/report',json=b);self.assertEqual(x.status_code,200);self.assertEqual(x.json()['summary']['records'],1)
  self.assertEqual(x.json()['source'],'local')
  self.assertEqual(len(admin.get('/api/assistant/history').json()),0)
  self.assertEqual(emp.post('/api/assistant/report',json=b).status_code,429)
  self.assertEqual(admin.post('/api/assistant/report',json={**b,'start_date':'2027-01-01','end_date':'2026-01-01'}).status_code,422)
  class Mock:
   def raise_for_status(self):pass
   def json(self):return {'choices':[{'message':{'content':'Rapport de test'}}]}
  with patch.dict(os.environ,{'GROQ_API_KEY':'fake-test-key'}),patch('app.httpx.post',return_value=Mock()) as post:
   x=admin.post('/api/assistant/report',json={**b,'use_groq':True});self.assertEqual(x.status_code,200);self.assertEqual(x.json()['source'],'groq');self.assertEqual(x.json()['summary']['records'],2)
   payload=json.dumps(post.call_args.kwargs['json']);self.assertNotIn('Person Secret',payload);self.assertNotIn('user@test.id',payload);self.assertNotIn('password',payload.lower())
  with db() as c:c.execute("DELETE FROM audit WHERE action='assistant_request'")
  import httpx
  with patch.dict(os.environ,{'GROQ_API_KEY':'fake-test-key'}),patch('app.httpx.post',side_effect=httpx.TimeoutException('failed')):
   x=admin.post('/api/assistant/report',json={**b,'use_groq':True});self.assertEqual(x.status_code,200);self.assertEqual(x.json()['source'],'local');self.assertTrue(x.json()['warning'])
  self.assertEqual(len(emp.get('/api/assistant/history').json()),1)
  self.assertEqual(len(admin.get('/api/assistant/history').json()),2)
  self.assertEqual(TestClient(app).get('/api/assistant/status').status_code,401)
if __name__=='__main__':unittest.main()
