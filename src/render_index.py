import json
import os

# Portable by design: BASE is always the directory this script itself lives in, so the build
# works unmodified wherever the project folder is unzipped/cloned -- it does not depend on any
# particular machine's absolute path. Run as `python3 render_index.py` from anywhere; it resolves
# its own location first.
BASE = os.path.dirname(os.path.abspath(__file__))

phrases = open(f'{BASE}/DATA_PHRASES.r6.json', encoding='utf-8').read()
langs = open(f'{BASE}/DATA_LANGS.json', encoding='utf-8').read()
meta = open(f'{BASE}/DATA_META.r6.json', encoding='utf-8').read()
sys_en = open(f'{BASE}/systems.en.json', encoding='utf-8').read()
sys_langs_text = open(f'{BASE}/systems.languages.json', encoding='utf-8').read()
sys_langs = json.loads(sys_langs_text)
# Time/Onset module (redesigned elapsed-time onset/duration capture): a single combined file
# with the English baseline plus all 36 languages' AI-draft strings -- small enough (16 short
# strings per language) that one file is more maintainable than 36 separate ones, unlike the
# 96-question Systems translations. Same embed-at-build-time, no-runtime-fetch approach.
time_onset_text = open(f'{BASE}/time_onset_translations.json', encoding='utf-8').read()

# Systems-module translations are embedded directly in the page, exactly like the legacy
# phrasebook's PHRASES data -- NOT fetched over the network at runtime. This is built here, at
# render time, from the per-language systems.translations.<code>.json files (kept on disk
# separately for version control/maintainability, per the "separate file per language"
# requirement) so there is a single source of truth and no risk of the embedded copy drifting
# from those files. Only `status: "draft"` languages contribute content; `pending` languages
# are intentionally left out of SYS_TR entirely (sysGetTranslation treats "no entry" as
# "missing", never as a silent English fallback).
sys_tr = {}
for lang_entry in sys_langs['languages']:
    if lang_entry['status'] == 'draft' and lang_entry.get('file'):
        lang_file = json.load(open(f"{BASE}/{lang_entry['file']}", encoding='utf-8'))
        sys_tr[lang_entry['code']] = lang_file['questions']
sys_tr_text = json.dumps(sys_tr, ensure_ascii=False)

tmpl = open(f'{BASE}/template.html', encoding='utf-8').read()

# Minify-safe inline: these are JSON text blobs inserted verbatim inside <script type="application/json"> tags.
# The only character that must never appear raw is "</script" (JSON strings won't contain it from our data).
def safe(s):
    return s.replace('</script', '<\\/script')

out = tmpl
out = out.replace('__DATA_PHRASES__', safe(phrases))
out = out.replace('__DATA_LANGS__', safe(langs))
out = out.replace('__DATA_META__', safe(meta))
out = out.replace('__DATA_SYS_EN__', safe(sys_en))
out = out.replace('__DATA_SYS_LANGS__', safe(sys_langs_text))
out = out.replace('__DATA_SYS_TR__', safe(sys_tr_text))
out = out.replace('__DATA_TIME_ONSET__', safe(time_onset_text))

assert '__DATA_' not in out, 'unreplaced placeholder remains'

open(f'{BASE}/index.html', 'w', encoding='utf-8').write(out)
print('index.html written,', len(out), 'bytes')
print(f'Embedded {len(sys_tr)} drafted Systems languages directly in the page:', sorted(sys_tr.keys()))
