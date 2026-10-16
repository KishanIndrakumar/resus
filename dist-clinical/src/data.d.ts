export type ReviewStatus='AI draft'|'AI reviewed'|'Human verified'|'Missing'|'Requires review';
export type ResponseType='boolean'|'pain'|'number'|'date'|'duration'|'choice'|'text'|'instruction'|'statement'|'label';
export interface Phrase {id:string;english:string;sourceHash:string;category:string;subcategory:string;speaker:string;responseType:ResponseType;requiresMapping:boolean}
export interface Entry {text:string;sourceHash:string;speaker:string;responseType:ResponseType;status:ReviewStatus;source:string;lastUpdated?:string;approval?:{reviewer:string;date:string;policyVersion:string;evidence:string}}
export interface LanguageBundle {code:string;masterVersion:string;version:string;entries:Record<string,Entry>}
export interface Language {code:string;name:string;native:string;dir:'ltr'|'rtl';available:number;total:number;status:ReviewStatus;version:string}
export interface SessionAnswer {phraseId:string;english:string;category:string;system:string;language:string;label:string;patientLabel?:string;key?:0|1|2|3;value?:string;unit?:string;approximate?:boolean;exact?:boolean}
export type TimingSlot='onset'|'duration'|'character';
export interface Session {responses:Record<string,SessionAnswer>;recent:string[];asked:Record<string,{language:string;available:boolean}>;timings:Record<string,Partial<Record<TimingSlot,SessionAnswer>>>}
