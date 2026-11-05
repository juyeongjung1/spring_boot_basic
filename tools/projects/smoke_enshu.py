"""演習13アプリの起動、HTTP画面、入力チェック、DB登録・削除を確認する。

あらかじめJDK21でpackageし、教材のspring_exercise DBを初期化しておく。
開始用プロジェクトはTODOを保った初期画面までを検証する。
認証の変更時は EXERCISE_DB_USER / EXERCISE_DB_PASSWORD を設定する。
"""
from pathlib import Path
import argparse
import http.cookiejar
import json
import math
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
import time

ROOT=Path(__file__).resolve().parents[2]


def sql(query,config):
    env=dict(os.environ,MYSQL_PWD=config['exercise_password'])
    result=subprocess.run([config['mysql'],'-h',config['mysql_host'],'-P',str(config['mysql_port']),'-u',config['exercise_user'],'--default-character-set=utf8mb4','-N','-B',config['exercise_database']],input=query.encode('utf-8'),capture_output=True,env=env)
    if result.returncode:raise RuntimeError(result.stderr.decode('utf-8',errors='replace'))
    return result.stdout.decode('utf-8').strip()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None


def check_app(app,config,port):
    # 使用中の別アプリへ誤ってテスト要求を送らない。
    import socket
    with socket.socket() as probe:probe.bind(('127.0.0.1',port))
    ENV=config
    OUT=config["log_dir"]
    JAVA=config["java"]
    def query(text):return sql(text,config)
    stage=int(app.name.rsplit('_',1)[1]);answer=app.parent.name=='enshu_answer'
    jar=app/'target'/(app.name+'-0.0.1-SNAPSHOT.jar')
    record={'project':str(app.relative_to(ROOT)),'checks':[]}
    with zipfile.ZipFile(jar) as z:
        assert 'BOOT-INF/lib/spring-boot-4.0.2.jar' in z.namelist()
        classes=[n for n in z.namelist() if n.startswith('BOOT-INF/classes/') and n.endswith('Application.class')]
        assert len(classes)==1
        assert int.from_bytes(z.read(classes[0])[6:8],'big')==65
    record['java_class_major']=65;record['spring_boot']='4.0.2'
    if stage==3:
        with zipfile.ZipFile(jar) as z:assert 'BOOT-INF/lib/modelmapper-3.2.6.jar' in z.namelist()
        record['modelmapper']='3.2.6'
    url=f'http://127.0.0.1:{port}'
    client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),NoRedirect())
    log=OUT/(app.name+'-http.log')
    def request(path,data=None):
        req=urllib.request.Request(url+path,data=urllib.parse.urlencode(data).encode() if data is not None else None)
        try:r=client.open(req,timeout=20)
        except urllib.error.HTTPError as error:r=error
        return r.code,r.read().decode('utf-8',errors='replace'),r.headers
    def verify(label,path,data=None,contains=(),status=200):
        code,body,headers=request(path,data)
        assert code==status,(app.name,label,code,body[:250])
        assert all(v in body for v in contains),(app.name,label,contains,body[:250])
        record['checks'].append({'step':label,'path':path,'status':code})
        return body
    args=[JAVA,'-Xmx384m','-Dfile.encoding=UTF-8','-jar',str(jar),'--server.address=127.0.0.1',f'--server.port={port}',f"--spring.datasource.url=jdbc:mysql://{ENV['mysql_host']}:{ENV['mysql_port']}/{ENV['exercise_database']}?serverTimezone=Asia/Tokyo",f"--spring.datasource.username={ENV['exercise_user']}",f"--spring.datasource.password={ENV['exercise_password']}"]
    name=f'SB4_TEST_{stage}_'+uuid.uuid4().hex[:12]
    owns_fixture_name=False
    proc=None
    try:
        with log.open('wb') as output:
            proc=subprocess.Popen(args,cwd=app,stdout=output,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
            until=time.monotonic()+180
            while True:
                if proc.poll() is not None:raise RuntimeError('起動失敗: '+log.read_text(encoding='utf-8',errors='replace')[-3500:])
                try:
                    code,body,_=request('/')
                    if code==200:break
                    if code>=500:raise RuntimeError('初期画面HTTP '+str(code)+': '+log.read_text(encoding='utf-8',errors='replace')[-2500:])
                except urllib.error.URLError:pass
                if time.monotonic()>until:raise RuntimeError('起動待ちタイムアウト: '+app.name)
                time.sleep(.5)
            verify('初期画面','/',contains=('html',))
            if not answer:
                record['exercise_todo_preserved']=True
            elif stage==1:
                verify('設問と解答','/',contains=('演習1.1.','correct'))
            elif stage==2:
                for route in ['/bmi','/bmi2']:
                    body=verify('BMI計算',route,{'height':160,'weight':64},contains=('BMI結果',))
                    assert math.isclose(float(re.search(r'<p>([0-9.]+)</p>',body)[1]),25.0,abs_tol=1e-10)
            else:
                seed=query('SELECT id,name,password,salary FROM employee ORDER BY id LIMIT 1').split('\t')
                ident,employee,password,salary=seed
                prefix='/emp' if stage in (4,5) else ''
                if stage==4:
                    verify('ログイン入力チェック','/login3',{'id':'','password':''},contains=('社員番号を入力してください','パスワードを入力してください'))
                    verify('ログインとセッション','/login2',{'id':ident,'password':password},contains=(employee,))
                elif stage==5:
                    verify('ログイン入力チェック','/login',{'id':'','password':''},contains=('社員番号を入力してください','パスワードを入力してください'))
                    verify('ログインとセッション','/login',{'id':ident,'password':password},status=302)
                verify('全件検索',prefix+'/findAll',contains=(employee,))
                if stage==5:
                    verify('Thymeleaf共通レイアウト',prefix+'/findAll',contains=('<header>','<footer>','<th>給与</th>'))
                    other=query('SELECT id,password FROM employee WHERE id <> 1001 ORDER BY id LIMIT 1').split('\t')
                    verify('一般社員ログイン','/login',{'id':other[0],'password':other[1]},status=302)
                    body=verify('一般社員の給与列非表示',prefix+'/findAll')
                    assert '<th>給与</th>' not in body
                    verify('管理者セッションに戻す','/login',{'id':ident,'password':password},status=302)
                verify('主キー検索',prefix+'/showFindById?id='+ident,contains=(employee,))
                if stage in (3,4,5):
                    verify('給与検索',prefix+'/showFindBySalary?salary='+salary,contains=(employee,))
                    verify('名前検索',prefix+'/showFindByName?name='+urllib.parse.quote(employee),contains=(employee,))
                if stage in (4,5):
                    verify('登録入力チェック',prefix+'/insertEmp',{'name':'','password':'','salary':'-1'},contains=('名前を入力してください','パスワードを入力してください','1以上の数値を入力してください'))
                if stage>=6:
                    joined=query('SELECT e.id,e.name,l.name,l.id FROM employee e JOIN location l ON e.location_id=l.id ORDER BY e.id LIMIT 1').split('\t')
                    jid,jname,location,location_id=joined
                    verify('外部参照の表示','/showFindById?id='+jid,contains=(jname,location))
                    verify('存在しない社員の表示','/showFindByIdSafe?id=999999',contains=('該当する社員情報は存在しません',))
                    verify('勤務地選択肢','/showInputView',contains=(location,))
                    if stage==6:verify('JPQL関連検索','/findHighSalary?salary=0&locationName='+urllib.parse.quote(location),contains=(jname,))
                if stage==7:
                    verify('Bootstrap共通レイアウト','/4',contains=('container','社員番号で検索',employee))
                    verify('Bootstrap静的CSS','/css/bootstrap.min.css',contains=('Bootstrap',))
                data={'name':name,'password':'smokePass1','salary':271828}
                if stage>=6:data['locationId']=location_id
                assert query("SELECT COUNT(*) FROM employee WHERE name='"+name+"'")=='0'
                owns_fixture_name=True
                verify('社員登録',prefix+'/insertEmp',data,status=302 if stage in (5,7) else 200)
                added=query("SELECT id FROM employee WHERE name='"+name+"'")
                assert added.isdigit(),(app.name,'登録結果なし')
                if stage>=6:assert query('SELECT location_id FROM employee WHERE id='+added)==location_id
                verify('登録した社員の再検索',prefix+'/showFindById?id='+added,contains=(name,))
                if stage<7:
                    verify('社員削除',prefix+'/delete/'+added,status=302)
                    assert query('SELECT COUNT(*) FROM employee WHERE id='+added)=='0'
    finally:
        try:
            if owns_fixture_name:query("DELETE FROM employee WHERE name='"+name+"'")
        finally:
            if proc is not None and proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=15)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    record['passed']=True
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home',type=Path,default=os.getenv('JAVA_HOME'),help='JDK21の場所（既定: JAVA_HOME）')
    parser.add_argument('--mysql',default=shutil.which('mysql') or 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe',help='mysqlクライアント')
    parser.add_argument('--mysql-host',default='127.0.0.1')
    parser.add_argument('--mysql-port',type=int,default=3306)
    parser.add_argument('--port-start',type=int,default=18200)
    parser.add_argument('--output',type=Path,default=ROOT/'output/verification/projects/enshu-smoke.json')
    args=parser.parse_args()
    if not args.java_home:parser.error('--java-home または JAVA_HOME でJDK21を指定してください')
    if not 1<=args.port_start<=65523:parser.error('--port-start は1〜65523を指定してください')
    java=args.java_home/'bin'/('java.exe' if os.name=='nt' else 'java')
    version=subprocess.run([str(java),'-version'],capture_output=True,text=True,check=True)
    if not re.search(r'version "21[."]',version.stderr+version.stdout):parser.error('JDK21を指定してください')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    logs=args.output.parent/'enshu-http-logs';logs.mkdir(exist_ok=True)
    config=dict(java=str(java.resolve()),mysql=args.mysql,mysql_host=args.mysql_host,mysql_port=args.mysql_port,exercise_database='spring_exercise',exercise_user=os.getenv('EXERCISE_DB_USER','spring_exercise_user'),exercise_password=os.getenv('EXERCISE_DB_PASSWORD','password'),log_dir=logs)
    results=[]
    apps=[app for group in ['enshu_answer','enshu_exercise'] for app in sorted((ROOT/'projects'/group).iterdir()) if (app/'src').exists()]
    for index,app in enumerate(apps):
        print('確認開始',app.name,flush=True)
        try:results.append(check_app(app,config,args.port_start+index))
        except Exception as error:
            results.append({'project':str(app.relative_to(ROOT)),'passed':False,'error':str(error)})
            args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            raise
        args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('合格',app.name,len(results[-1]['checks']),'確認',flush=True)
