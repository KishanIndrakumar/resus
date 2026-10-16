export type ReviewStatus='AI draft'|'AI reviewed'|'Human verified'|'Missing'|'Requires review';
export type ResponseType='boolean'|'pain'|'number'|'date'|'duration'|'choice'|'text'|'instruction'|'statement'|'label';
export interface Phrase {id:string;english:string;sourceHash:string;category:string;subcategory:string;speaker:string;responseType:ResponseType;requiresMapping:boolean}
export interface MappingState {translationExists:boolean;sourceIdMatches:boolean;sourceEnglishMatches:boolean;speakerContextMatches:boolean;mappingVerified:boolean;humanVerified:boolean;linguisticReviewStatus:string;clinicallyApproved:boolean;blockReasons:string[]}
export interface Entry extends Partial<MappingState> {text:string;sourceHash:string;speaker:string;responseType:ResponseType;status:ReviewStatus;source:string;sourceId?:string;mappingEvidenceId?:string;reviewLabel?:string;lastUpdated?:string;approval?:{reviewer:string;date:string;policyVersion:string;evidence:string}}
export interface LanguageBundle {code:string;masterVersion:string;version:string;entries:Record<string,Entry>;availability?:Record<string,MappingState>}
export interface Coverage {availableForReview:number;missing:number;blockedByMappingIssue:number;humanVerified:number;clinicallyApproved:number}
export interface Language {code:string;name:string;native:string;dir:'ltr'|'rtl';available:number;total:number;coverage?:Coverage;status:ReviewStatus|'Unverified — review draft';version:string}
export interface SessionAnswer {phraseId:string;english:string;category:string;system:string;language:string;label:string;optionId?:string;unitOptionId?:string;responseControl?:string;patientLabel?:string;key?:0|1|2|3;value?:string;unit?:string;approximate?:boolean;exact?:boolean}
export type TimingSlot='onset'|'duration'|'character';
export interface Session {responses:Record<string,SessionAnswer>;recent:string[];asked:Record<string,{language:string;available:boolean}>;timings:Record<string,Partial<Record<TimingSlot,SessionAnswer>>>}

export interface ResponseSpec {id:string;sourceHash:string;speaker:string;control:ResponseType|'unavailable';options:string[];units?:string[];fixedUnit?:string;defaultUnit?:string;numberStep:string;rationale:string}
export interface ResponseOption {id:string;english:string;audience?:'clinician-interface'|'patient-interface'|'patient-answer';kind?:'numeral';value?:number;meaning?:string}
export interface OptionLabel {text:string;status:ReviewStatus;humanVerified:boolean;clinicallyApproved:boolean;provenance:Record<string,unknown>;approval?:Entry['approval']}
export interface ResponseRegistry {schemaVersion:number;masterVersion:string;version:string;definitions:Record<string,ResponseOption>;phrases:Record<string,ResponseSpec>;locales:Record<string,{code:string;bundleVersion:string;dir:'ltr'|'rtl';entries:Record<string,OptionLabel>;issues:Record<string,{status:string;reason:string}>}>}
