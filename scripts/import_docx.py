"""Read-only DOCX ingestion. Output is immutable by source-content hash; no translation generation."""
import datetime, pathlib, zipfile, xml.etree.ElementTree as ET, json, hashlib, re, sys, collections
ROOT=pathlib.Path(__file__).resolve().parent.parent
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def digest(s): return hashlib.sha256(s.encode()).hexdigest()
def read(p):
    r=ET.fromstring(zipfile.ZipFile(p).read('word/document.xml'))
    rows=[]
    for t in r.findall('.//w:tbl',NS):
        rr=[[ ''.join(x.text or '' for x in c.findall('.//w:t',NS)) for c in row.findall('w:tc',NS)] for row in t.findall('w:tr',NS)]
        if rr and rr[0][0].strip().upper()=='ID': rows.extend(c for c in rr[1:] if len(c)>=4)
    return rows, [''.join(x.text or '' for x in p.findall('.//w:t',NS)) for p in r.findall('.//w:p',NS)]
CATEGORIES=['Patient Details','Pain','Time / Onset','Systems Review','Allergies','Medications','Medical Background','Pregnancy / Gynaecology','Neurological / Stroke','Examination / Procedures','Interpreter / Help','Other Questions']
SYSTEMS={'GEN':'General','CVS':'Cardiovascular','RESP':'Respiratory','GI':'Gastrointestinal','GU':'Genitourinary','NEURO':'Neurological','ENT':'ENT','MSK':'Musculoskeletal','SKIN':'Skin','EYE':'Eyes','TRAUMA':'Trauma'}
def classify(i,s,c):
    prefix=re.match('[A-Z]+',i)
    if prefix and prefix[0] in SYSTEMS: return ('Neurological / Stroke' if prefix[0]=='NEURO' else 'Systems Review', SYSTEMS[prefix[0]])
    if i.startswith('NEW-INST'): return ('Interpreter / Help' if i.endswith('046') else 'Examination / Procedures','Instructions')
    if i in ['1'] or 'interpreter' in c.lower(): return ('Interpreter / Help','Communication')
    if '_' in i or i in ['7.b','9']: return ('Time / Onset','Timing')
    if i.startswith(('10.','11.')) or i=='12':return ('Pain','Assessment')
    if i.startswith('24.'):return ('Pregnancy / Gynaecology','Pregnancy')
    if i.startswith('28'):return ('Allergies','Allergies')
    if i.startswith('29'):return ('Medications','Medication history')
    if i.startswith(('2.','5.')) or i in ['3','4']:return ('Patient Details','Details')
    if i.startswith(('25.','26.','27.','23')):return ('Medical Background','History')
    if 'neuro' in c.lower() or i=='8':return ('Neurological / Stroke','Assessment')
    if 'symptoms' in c.lower():return ('Systems Review','General')
    if s.endswith('?'):return ('Other Questions','General')
    return ('Examination / Procedures','Explanation')
def response(i,s,c):
    if i=='11.a':return 'pain'
    if i in ['onset_question','duration_question','10.c','7.b','9']:return 'duration'
    if i=='onset_character_question':return 'choice'
    if i=='24.1':return 'date'
    if i in ['4','24.3','25.2']:return 'number'
    if i in ['sudden','gradual']:return 'label'
    if i in ['30']:return 'number'
    if i=='14.2':return 'boolean'
    if i=='32.b':return 'text'
    if i=='1' or ('_' in i and i not in ['onset_question','duration_question','onset_character_question']):return 'label'
    if c.startswith('Patient'):return 'statement'
    if i=='12' or re.match(r'^(What|Where|How|When|Please write|Can you write)',s):return 'text'
    if s.endswith('?'):return 'boolean'
    return 'instruction'
LANGS=[('Albanian','sq','Shqip'),('Amharic','am','አማርኛ'),('Arabic','ar','العربية'),('Bengali','bn','বাংলা'),('Bosnian','bs','Bosanski'),('Czech','cs','Čeština'),('Farsi','fa','فارسی'),('French','fr','Français'),('German','de','Deutsch'),('Greek','el','Ελληνικά'),('Gujarati','gu','ગુજરાતી'),('Hindi','hi','हिन्दी'),('Hungarian','hu','Magyar'),('Irish','ga','Gaeilge'),('Italian','it','Italiano'),('Japanese','ja','日本語'),('Korean','ko','한국어'),('Kurdish_Sorani','ckb','کوردی'),('Lingala','ln','Lingála'),('Lithuanian','lt','Lietuvių'),('Macedonian','mk','Македонски'),('Mandarin_Chinese','zh-CN','简体中文'),('Pashto','ps','پښتو'),('Polish','pl','Polski'),('Portuguese','pt','Português'),('Punjabi','pa','ਪੰਜਾਬੀ'),('Romanian','ro','Română'),('Russian','ru','Русский'),('Slovak','sk','Slovenčina'),('Somali','so','Soomaali'),('Spanish','es','Español'),('Swahili','sw','Kiswahili'),('Tamil','ta','தமிழ்'),('Traditional_Chinese','zh-TW','繁體中文'),('Turkish','tr','Türkçe'),('Ukrainian','uk','Українська'),('Urdu','ur','اردو'),('Vietnamese','vi','Tiếng Việt')]
def main():
    global ROOT
    folder=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '..'); masterfile=next(folder.glob('*English_Master*.docx'))
    fingerprint={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.docx')}
    baseline=ROOT/'review/import-inputs.json'
    if '--stage' in sys.argv:
        ROOT=ROOT/'review'/'import-candidates'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        (ROOT/'review').mkdir(parents=True,exist_ok=True)
    elif baseline.exists():
        previous=json.loads(baseline.read_text(encoding='utf-8'))
        current={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'public/data').glob('*.json')}
        if previous['sources']!=fingerprint or previous['runtime']!=current:
            raise ValueError('Source or canonical data changed. Refusing overwrite. Run import_docx.py SOURCE --stage, validate and review the candidate, then explicitly promote it.')
    rows,paras=read(masterfile); counts=collections.Counter(r[0] for r in rows)
    if any(v!=1 for v in counts.values()):raise ValueError('Duplicate Master IDs; import stopped')
    phrases=[]
    for i,s,c,*_ in rows:
        cat,sub=classify(i,s,c);phrases.append(dict(id=i,english=s,sourceHash=digest(s),category=cat,subcategory=sub,speaker=c,responseType=response(i,s,c),requiresMapping='requires translation ID mapping' in c or 'provisional ID' in c))
    version=digest(json.dumps(phrases,ensure_ascii=False))[:16]; master=dict(version=version,phrases=phrases,categories=CATEGORIES)
    target=ROOT/'public/data';target.mkdir(parents=True,exist_ok=True); archive=ROOT/'review'/version;archive.mkdir(parents=True,exist_ok=True)
    (archive/'master-source.json').write_text(json.dumps(dict(filename=masterfile.name,rows=rows,documentText=paras),ensure_ascii=False,indent=2),encoding='utf-8')
    lookup={p['id']:p for p in phrases}; languages=[]; reports=[]
    for name,code,native in LANGS:
        files=list(folder.glob('*Independent_'+name+'_Translation*.docx'))
        if not files:continue
        p=files[0];lr,lp=read(p);entries={};issues=[];lc=collections.Counter(r[0] for r in lr)
        for r in lr:
            i,s,c,t,*notes=r;errors=[];m=lookup.get(i)
            if not m:errors.append('unknown-id')
            else:
                if s!=m['english']:errors.append('english-source-mismatch')
                if c!=m['speaker']:errors.append('speaker-context-mismatch')
                if m['requiresMapping']:errors.append('explicit-id-mapping-required')
            if lc[i]>1:errors.append('duplicate-id')
            if not t.strip():errors.append('empty')
            # Intentional b/strong/em/br context markup is retained in the archive; never rendered as HTML.
            if re.search(r'<\s*(script|iframe|img|svg)|on\w+\s*=|javascript:',t,re.I):errors.append('unsafe-markup')
            scripts=[]
            if code in ['ar','fa','ur','ps','ckb'] and t and not re.search('[\u0600-\u06ff]',t):scripts.append('unexpected-script-review')
            if errors or scripts:issues.append(dict(id=i,errors=errors,warnings=scripts))
            if m and not errors:entries[i]=dict(text=t,sourceHash=m['sourceHash'],speaker=m['speaker'],responseType=m['responseType'],status='AI draft',source=p.name,lastUpdated=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat())
        raw=json.dumps(dict(filename=p.name,rows=lr,documentText=lp),ensure_ascii=False,indent=2)
        out=archive/(code+'-'+digest(raw)[:12]+'.json')
        if not out.exists():out.write_text(raw,encoding='utf-8')
        bundle=dict(code=code,masterVersion=version,version=digest(raw)[:16],entries=entries)
        (target/(code+'.json')).write_text(json.dumps(bundle,ensure_ascii=False),encoding='utf-8')
        languages.append(dict(code=code,name=name.replace('_',' '),native=native,dir='rtl' if code in ['ar','fa','ur','ps','ckb'] else 'ltr',available=len(entries),total=len(phrases),status='AI draft',version=bundle['version']))
        reports.append(dict(language=code,sourceRows=len(lr),acceptedForReview=len(entries),humanVerified=0,missing=[i for i in lookup if i not in entries],issues=issues))
    (target/'master.json').write_text(json.dumps(master,ensure_ascii=False),encoding='utf-8')
    (target/'languages.json').write_text(json.dumps(languages,ensure_ascii=False),encoding='utf-8')
    (ROOT/'review/translation-report.json').write_text(json.dumps(dict(masterVersion=version,masterRows=len(rows),languages=reports),ensure_ascii=False,indent=2),encoding='utf-8')
    runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in target.glob('*.json')}
    (ROOT/'review/import-inputs.json').write_text(json.dumps(dict(sources=fingerprint,runtime=runtime),indent=2),encoding='utf-8')
    print(f'Imported {len(rows)} authoritative phrases, {len(languages)} language bundles. Human verified: 0. See review/translation-report.json')
if __name__=='__main__':main()
