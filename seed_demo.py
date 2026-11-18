"""Synthetic demonstration data. Never writes the operational database."""
import os
from pathlib import Path
os.environ['HADIRIN_DATA']=str(Path(__file__).parent/'demo_data')
from app import db, hashpw, now, TZ
from datetime import timedelta
import random,json,math
r=random.Random(42)
with db() as c:
 if c.execute('SELECT count(*) FROM users').fetchone()[0]:raise SystemExit('Database demo sudah berisi data. Tidak ditimpa.')
 c.execute('INSERT INTO users(name,email,password,role,code) VALUES(?,?,?,?,?)',('Admin Demo','admin@demo.local',hashpw('DemoHadirin2026!'),'admin','DEMO-ADMIN'))
 for i in range(1,6):
  c.execute('INSERT INTO users(name,email,password,role,code) VALUES(?,?,?,?,?)',(f'Karyawan Demo {i}',f'user{i}@demo.local',hashpw('DemoHadirin2026!'),'user',f'DEMO-{i}'))
  uid=c.execute('SELECT last_insert_rowid()').fetchone()[0]
  for d in range(35):
   t=(now()-timedelta(days=40-d)).replace(hour=8,minute=0,second=0,microsecond=0)+timedelta(minutes=r.randint(-20,20) if d<28 else r.choice([0,5,120,180]))
   dist=r.uniform(5,50) if d<28 else r.uniform(50,190);late=max(0,(t.hour*60+t.minute)-490);h=t.hour+t.minute/60
   f=[late,math.sin(2*math.pi*h/24),math.cos(2*math.pi*h/24),math.sin(2*math.pi*t.weekday()/7),math.cos(2*math.pi*t.weekday()/7),dist,0,0,1]
   c.execute('INSERT INTO attendance(user_id,day,at,lat,lon,accuracy,distance,late,photo,location,features) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(uid,t.date().isoformat(),t.isoformat(),-7.3305,110.5084,10,dist,late,'DEMO_NO_PHOTO','Kantor Demo',json.dumps(f)))
print('175 catatan SINTETIS dibuat pada demo_data. Bukan hasil penelitian.')
print('Login: admin@demo.local / DemoHadirin2026!')
print('Windows PowerShell: $env:HADIRIN_DATA="demo_data"; .venv\\Scripts\\python -m uvicorn app:app')
