import os,tempfile,unittest,base64
os.environ['HADIRIN_DATA']=tempfile.mkdtemp()
from fastapi.testclient import TestClient
from app import app,db,now
class Flow(unittest.TestCase):
 def test_flow(self):
  a=TestClient(app); b=TestClient(app)
  self.assertEqual(a.get('/api/me').status_code,401)
  self.assertEqual(a.post('/api/setup',json={'name':'Admin','email':'admin@test.id','password':'TestPassword123'}).status_code,200)
  self.assertEqual(a.post('/api/setup',json={'name':'Admin','email':'a@b.c','password':'TestPassword123'}).status_code,409)
  self.assertEqual(a.post('/api/login',json={'email':'admin@test.id','password':'bad'}).status_code,401)
  self.assertEqual(a.post('/api/login',json={'email':'admin@test.id','password':'TestPassword123'}).status_code,200)
  self.assertEqual(a.post('/api/users',json={'name':'User','email':'user@test.id','password':'TestPassword123'}).status_code,200)
  b.post('/api/login',json={'email':'user@test.id','password':'TestPassword123'})
  self.assertEqual(b.get('/api/users').status_code,403)
  s=a.get('/api/settings').json();s['workdays']=list(range(7));a.put('/api/settings',json=s)
  payload={'lat':s['lat'],'lon':s['lon'],'accuracy':10,'photo':'data:image/jpeg;base64,'+base64.b64encode(b'\xff\xd8\xfftest').decode(),'consent':True}
  self.assertEqual(b.post('/api/checkin',json={**payload,'lat':0}).status_code,422)
  self.assertEqual(b.post('/api/checkin',json=payload).status_code,200)
  self.assertEqual(b.post('/api/checkin',json=payload).status_code,409)
  aid=b.get('/api/attendance').json()[0]['id']
  self.assertEqual(b.get('/api/photos/'+str(aid)).status_code,200)
  self.assertEqual(b.get('/api/export').status_code,403)
  self.assertEqual(a.post('/api/analyze').status_code,422)
  self.assertEqual(a.post('/api/logout',headers={'Origin':'https://evil.example'}).status_code,403)
  self.assertEqual(a.get('/api/export').status_code,200)
if __name__=='__main__':unittest.main()
