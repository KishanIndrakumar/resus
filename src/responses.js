import {translation} from './core.js';
export function optionClinicallyApproved(e){return e?.status==='Human verified'&&e.humanVerified===true&&e.clinicallyApproved===true&&!!e.approval?.reviewer&&!!e.approval?.date&&!!e.approval?.evidence&&!!e.approval?.policyVersion;}
export function responseSpec(registry,p){const s=registry?.phrases?.[p.id];return s&&s.sourceHash===p.sourceHash&&s.speaker===p.speaker?s:{control:'unavailable',options:[],rationale:'Response audit is missing or stale.'};}
export function optionLabel({registry,candidates,master,bundle,language,mode,preview=false},id){
 const d=registry?.definitions?.[id];if(!d)return null;
 if(language==='en')return {text:d.english,kind:'English source',id};
 if(d.kind==='numeral')return {text:d.english,kind:'Language-neutral numeral',id};
 const locale=registry.locales[language],entry=locale?.entries?.[id];
 if(locale&&locale.bundleVersion!==bundle?.version)return null;
 if(entry){if(mode==='clinical'&&!optionClinicallyApproved(entry))return null;const proof=entry.provenance,p=master.phrases.find(p=>p.id===proof.phraseId);const parent=p&&translation(bundle,p,mode);if(parent&&p.sourceHash===proof.sourceHash){const parts=parent.split('/').map(v=>v.trim());const expected=proof.segmentIndex==null?parent:parts.length===4?parts[proof.segmentIndex]:null;if(expected===entry.text)return {text:entry.text,kind:mode==='clinical'?'Documented approved label':'Reused source label — unverified',id};}return null;}
 const candidate=preview&&mode==='review'&&candidates?.registryVersion===registry.version&&locale?.issues?.[id]?candidates.locales?.[language]?.[id]:null;
 if(candidate&&candidate.status==='AI draft'&&candidate.humanVerified===false&&candidate.clinicallyApproved===false&&candidate.text?.trim())return {text:candidate.text,kind:'Unverified AI option draft',id};
 return null;
}
export function optionMeaning(registry,id){const d=registry?.definitions?.[id];return d?.meaning||d?.english||null;}
export function responseValue(registry,id,patientText){const label=optionMeaning(registry,id);if(!label)throw Error('Unknown option ID');const legacy={'answer.yes':0,'answer.no':1,'answer.unknown':2,'answer.not_understood':3};const d=registry.definitions[id];return {optionId:id,label,patientLabel:patientText,...(id in legacy?{key:legacy[id]}:{}),...(d.kind==='numeral'?{value:String(d.value)}:{value:id})};}
export function permittedOption(spec,id){return spec.options.includes(id);}
