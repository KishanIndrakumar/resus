// UI references only. No canonical phrases, translations or clinical interpretations are changed.
export const DIRECTIONS='Directions / Instructions';
export const DIRECTION_IDS=['NEW-INST-013','NEW-INST-014','NEW-INST-015','NEW-INST-016','NEW-INST-017','NEW-INST-018','NEW-INST-019','NEW-INST-020','NEW-INST-021','50','54','55.a','55.b','55.c','51.b'];
// Explicit timing eligibility by phrase ID, rather than a category/text heuristic.
// This is workflow configuration for governance review, not a clinical validation claim.
export const SYMPTOM_IDS=new Set([
 'GEN01','GEN02','GEN03','GEN04','GEN05','GEN06',
 'CVS01','CVS02','CVS03','CVS04','CVS05','CVS06','CVS07','CVS08',
 'RESP01','RESP02','RESP03','RESP04','RESP05','RESP06',
 'GI01','GI02','GI03','GI04','GI05','GI06','GI07','GI08','GI09','GI10','GI11','GI12a','GI12b','GI13',
 'GU01','GU02','GU03','GU04','GU05','GU06','GU07a','GU07b','GU08','GU09',
 'NEURO01','NEURO04','NEURO05','NEURO06','NEURO07a','NEURO07b','NEURO08a','NEURO08b','NEURO08c','NEURO09','NEURO10','NEURO11','NEURO12','NEURO13','NEURO14',
 'ENT01','ENT02','ENT03','ENT04','ENT05','ENT06','ENT07','ENT08','ENT09','ENT10',
 'MSK01','MSK02','MSK03','MSK04a','MSK04b','MSK05','MSK06','MSK07',
 'SKIN01','SKIN02','SKIN03','SKIN04','SKIN05','SKIN06','SKIN07','SKIN08',
 'EYE01','EYE02','EYE03','EYE04','EYE05','EYE07',
 'TRAUMA05','TRAUMA06','TRAUMA07a','TRAUMA07b','TRAUMA07c','TRAUMA08a','TRAUMA08b',
 '8','10.a','13','14.1','14.2','15','16.1','16.2','17','18','19','20','21','22.1','22.2','22.3','22.4'
]);
export const TIMING_SLOTS={onset:'onset_question',duration:'duration_question',character:'onset_character_question'};
export const RESPONSE_MEANINGS=['Yes','No',"I don’t know","I don’t understand"];
export function categories(master){const result=[...master.categories];result.splice(result.indexOf('Examination / Procedures')+1,0,DIRECTIONS);return result;}
export function categoryPhrases(phrases,category,system=''){
 return phrases.filter(p=>p.id!=='11.b'&&p.responseType!=='label'&&(category===DIRECTIONS?DIRECTION_IDS.includes(p.id):p.category===category||(category==='Systems Review'&&p.category==='Neurological / Stroke'&&p.subcategory==='Neurological'))&&(!system||p.subcategory===system));
}
export function systemKey(p){return p.category+' / '+p.subcategory;}
export function responseState(answer){if(!answer)return 'unanswered';if(answer.optionId==='answer.not_understood'||answer.key===3)return 'not-understood';if(answer.optionId==='answer.unknown'||answer.optionId==='timing.not_sure'||answer.key===2||answer.value==='not_sure')return 'unknown';if(answer.optionId==='answer.yes'||answer.key===0)return 'positive';if(answer.optionId==='answer.no'||answer.key===1)return 'negative';return 'recorded';}
export function needsTiming(id,answer){return SYMPTOM_IDS.has(id)&&['positive','unknown'].includes(responseState(answer));}
export function answerCount(session){return Object.keys(session.responses).length+Object.values(session.timings).reduce((sum,slots)=>sum+Object.keys(slots).length,0);}
export function makeAnswer(phrase,language,value){return {...value,phraseId:phrase.id,english:phrase.english,category:phrase.category,system:phrase.subcategory,language};}
export function saveAnswer(session,phrase,language,value,target=null,slot=null){const answer=makeAnswer(phrase,language,value);if(target){if(!SYMPTOM_IDS.has(target)||!TIMING_SLOTS[slot]||TIMING_SLOTS[slot]!==phrase.id)throw Error('Invalid symptom timing association');session.timings[target]??={};session.timings[target][slot]=answer;}else session.responses[phrase.id]=answer;return answer;}
export function removeAnswer(session,id){delete session.responses[id];/* Timing remains explicitly linked, visible and removable; never silently reassigned. */}
export function removeTiming(session,id,slot){if(session.timings[id]){delete session.timings[id][slot];if(!Object.keys(session.timings[id]).length)delete session.timings[id];}}
export function sessionRows(session,phrases){return phrases.filter(p=>session.asked[p.id]||session.responses[p.id]||session.timings[p.id]).map(p=>({phrase:p,answer:session.responses[p.id],asked:session.asked[p.id],timings:session.timings[p.id]||{}}));}
export function summaryText(session,phrases){const rows=sessionRows(session,phrases);let group='';const lines=['Resus.ie — factual conversation summary','Communication record only; no clinical interpretation.'];for(const row of rows){const key=systemKey(row.phrase);if(group!==key){lines.push('',key);group=key}lines.push(row.phrase.english+' — '+(row.answer?.label||'Unanswered (opened only)')+(responseState(row.answer)==='not-understood'?' [communication issue; not a clinical answer]':'')+(row.answer?' ['+row.answer.language+']':''));for(const [slot,a] of Object.entries(row.timings))lines.push('  '+slot+': '+a.label+' ['+a.language+']');}return lines.join('\n');}
