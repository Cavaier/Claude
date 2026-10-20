# Video (Seedance) and voice-over (ElevenLabs)

## Video (Seedance 2.5, BytePlus ModelArk)
- **Model and key:** model `dreamina-seedance-2-5-260628`, env `SEEDANCE_API_KEY` only. Never print keys. API: `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks`, poll `GET …/tasks/<id>`.
- **Draft:** text prompt + `first_frame` image (base64 data URL), `duration 5`, `draft true`, `resolution "480p"`, `generate_audio true` (always sound), `watermark false`. Never send `ratio`.
- **Final:** `content:[{type:"draft_task", draft_task:{id}}]` with the resolution Eli writes. Do NOT add `generate_audio`, because the API rejects it on draft_task and the final inherits the draft's sound. A silent draft can't become a sound final. 720p was once refused for draft_task; if that happens, tell Eli.
- **Motion:** gentle slow motion only, and the jewelry keeps its shape and count. No sparkles or flares.
- **Motion feedback, step by step (saves credits):** when Eli says a video moves too much, only take the motion down one step, never to almost still. When he says it doesn't move, only take it up one step, never to twisting. The target is always in between: clearly visible, continuous movement (hand glides or settles, fabric and light move) with no wrist twist or rotation. Before choosing a take, compare its motion with the take he rejected and pick one that sits between it and the opposite extreme. Don't overcorrect.
- **Pipeline:**
  - `split.js` makes `_bg.png` (the photo for Seedance) and `_ov.png` (the text layer). `compose.sh` lays the text over the clip at 1080×1920 and keeps the audio.
  - On card layouts, only the photo moves, inside its fixed frame (ffmpeg overlay at the photo box).
  - The static stays live as its own ad.
  - No custom SOUND ON/OFF button on video artboards (Eli said no). Videos keep the native `controls`, whose speaker icon unmutes.
- **Helper sessions:** new env vars only show up in new sessions. Run Seedance and Frame.io jobs in a fresh helper session (`create_session`, same env and branch) with the full task in its first prompt, then read the result with `list_events`.


## Voice-over (ElevenLabs)
- **Key:** env `ELEVENLABS_API_KEY` only, in a helper session. Never print, log or commit it. API `https://api.elevenlabs.io/v1`, header `xi-api-key`.
- **Settings:** model `eleven_multilingual_v2`, stability 0.55, similarity 0.8, style 0.15, speaker boost, output `mp3_44100_128` (192 needs the Creator tier). The plan is pay-as-you-go.
- **Voices tried (W418 C2 trial):** Arabella `Z3R5wn05IrDiVCyEkUrK` (gentle, the pick), Veda Sky `8quEMRkSpwEaWBzHvTLv`, Relaxing Rachel `ROMJ9yK1NAMuu1ggrjDW`. Use the one Eli picks for future VO ads.
- **Voice notes / UGC (Eli, W436 C3):** a friend's WhatsApp-style voice message must sound real, never like a narrator. Arabella and the eleven_v3 takes sounded fake and robotic. Eli's pick: **Jessa** `yj30vwTGJxSHezdAGsv9` on `eleven_v3_conversational` (stability 0.3, similarity 0.75, speaker boost; no style, no audio tags). Keep natural pauses (cap at 0.6 s), light phone EQ. Scripts must make sense as a real message (no "just bought it" + "never take it off"; no pushy "just get it"; an ending like "I'll send you the link" works).
- **Mix:** tighten pauses (silenceremove, 0.28 s), voice starts at 0.3 s, loudnorm -16 LUFS, the clip's own sound stays underneath at about a third, and the last frame holds until the voice ends. Files go in `bfcm26/video/vo/`.
- **Scripts:** keep them short enough to fit the clip (about 2.3 words a second), true claims only, English.

