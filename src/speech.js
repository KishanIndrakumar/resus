import {chooseVoice} from './core.js';

// Keep speak() synchronous with the user's tap. Voice discovery never auto-plays.
export function createSpeech({synthesis,Utterance,onStatus=()=>{},schedule=setTimeout,unschedule=clearTimeout}){
 let active=null,timer=null,lastCode=null,awaitingVoices=false;
 const supported=!!synthesis&&typeof Utterance==='function';
 function voices(){if(!supported)return [];try{return synthesis.getVoices()||[]}catch{return []}}
 function stop(){if(timer!==null){unschedule(timer);timer=null;}const hadActive=!!active;active=null;if(supported&&(hadActive||synthesis.speaking||synthesis.pending))synthesis.cancel();if(hadActive)onStatus('Speech stopped.');}
 function refresh(){const available=voices();if(awaitingVoices&&lastCode&&chooseVoice(available,lastCode)){awaitingVoices=false;onStatus('A matching voice is now available. Tap Play to hear the question.');}return available;}
 function status(code){const available=voices();const voice=chooseVoice(available,code);return {supported,count:available.length,voice};}
 function play(value,code){
  if(!value)return false;stop();lastCode=code;
  if(!supported){onStatus('This browser does not support speech playback. Try the phone’s main browser or use an interpreter.');return false;}
  const available=refresh(),voice=chooseVoice(available,code);
  if(!voice){awaitingVoices=true;onStatus(available.length?'No suitable installed voice is available for this language on this device. Install its speech voice in the device settings, then tap Play again.':'This browser has not supplied any speech voices yet. Wait a moment and tap Play again. If this persists, check the device speech voices or try its main browser.');return false;}
  awaitingVoices=false;
  // Retain the utterance until end/error/stop, including on mobile engines.
  const u=new Utterance(value);active=u;u.lang=voice.lang.replaceAll('_','-');u.voice=voice;u.rate=0.9;let started=false;
  const description=`Voice: ${voice.name}. ${voice.localService?'Device voice; an installed voice is required for offline playback.':'This device voice may require an internet connection.'}`;
  u.onstart=()=>{if(active!==u)return;started=true;if(timer!==null)unschedule(timer);timer=null;onStatus('Playing. '+description);};
  u.onend=()=>{if(active!==u)return;active=null;if(timer!==null)unschedule(timer);timer=null;onStatus('Playback finished. Tap Play to replay.');};
  u.onerror=e=>{if(active!==u)return;active=null;if(timer!==null)unschedule(timer);timer=null;const messages={'not-allowed':'The browser blocked speech. Tap Play again in the phone’s main browser and check its audio permissions.','language-unavailable':'The device speech engine cannot speak this language. Install its speech voice or use an interpreter.','voice-unavailable':'The selected device voice is unavailable. Check the installed speech voices.','network':'The device voice needs a network connection. Connect or install an offline voice.','audio-busy':'The device audio is busy. Finish other audio and tap Play again.','audio-hardware':'The browser cannot access audio output. Check the device audio settings.','synthesis-unavailable':'The device speech engine is unavailable. Check the device text-to-speech settings.','synthesis-failed':'The device speech engine could not play this question. Check its installed voice and try again.'};if(!['canceled','interrupted'].includes(e.error))onStatus(messages[e.error]||`Speech playback failed (${e.error||'unknown error'}). Check device volume and installed speech voices.`);};
  try{if(synthesis.paused)synthesis.resume();onStatus('Starting speech. '+description);synthesis.speak(u);if(active===u&&!started)timer=schedule(()=>{timer=null;if(active===u&&!started&&!synthesis.speaking)onStatus('Speech has not started. Check device volume, audio output and the installed language voice, then tap Play again.');},5000);return true;}catch{active=null;onStatus('The browser could not start speech. Check the device speech settings and tap Play again.');return false;}
 }
 if(supported){synthesis.addEventListener?.('voiceschanged',refresh);refresh();}
 return {play,stop,refresh,status};
}
