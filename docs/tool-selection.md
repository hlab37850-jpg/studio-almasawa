# اختيار الأدوات وخطة التحقق

> تمت مراجعة المصادر العامة وملفات README/LICENSE في 16 نوفمبر 2026. لم تُشغّل الأدوات داخل بيئة المشروع. لا تتاح لهذه الجلسة طرفية Codex لفحص GPU أو الشبكة أو تثبيت الحزم؛ لذلك لا تُسجّل أي أداة على أنها اختُبرت عمليًا.

## الاختيارات الأولية

| الطبقة | الاختيار | المبرر والقيود |
|---|---|---|
| TTS الافتراضي | edge-tts Python | أصوات عربية عصبية متعددة بلا مفتاح، ويدعم WordBoundary. لكنه يتصل بخدمة Microsoft Edge عبر واجهة غير رسمية قابلة للتغيير؛ ليس نموذجًا مفتوحًا أو محليًا. الترخيص البرمجي LGPLv3 في معظمه. |
| TTS محلي | XTTS-v2 | يدعم العربية ضمن 17 لغة. ترخيص الأوزان Coqui Public Model License (CPML)، ويجب مراجعة شروطه قبل الاستخدام التجاري؛ لم تُختبر جودة العربية أو الأداء محليًا. |
| بديل محلي خفيف | Piper | توجد أصوات عربية ar_JO (Kareem). مستودع rhasspy الأصلي مؤرشف منذ 6 أكتوبر 2025؛ ترخيص كل وزن صوتي مستقل ويجب فحص MODEL_CARD. |
| TTS غير تجاري | MMS-TTS | يدعم العربية ولغات كثيرة، لكن بطاقة النموذج CC-BY-NC-4.0؛ لا يصلح للمسار التجاري. |
| تشكيل | CAMeL Tools + Mishkal | CAMeL Tools تحت MIT، وMishkal مشروع تشكيل عربي تحت GPL بحسب README. كلاهما يحتاج اختبارًا ومراجعة بشرية؛ pronunciation.md هو المرجع النهائي. |
| توليد فيديو | Wan2.1 T2V-1.3B | بطاقة النموذج تعلن 8.19GB VRAM و480p، والأوزان Apache-2.0. أفضل مرشح مبدئي عند توفر NVIDIA GPU مناسب، وليس وعدًا بإمكان التشغيل قبل فحص الجهاز. |
| توليد صور | FLUX.1-schnell | 12B parameters، Apache-2.0، 1–4 خطوات. يحتاج ذاكرة كبيرة؛ لا يوجد تحقق محلي من VRAM. |
| بديل صور | SDXL | CreativeML Open RAIL++-M؛ راجع قيود الترخيص قبل النشر التجاري. |
| تركيب | Remotion + FFmpeg | Remotion للمشاهد والنصوص، FFmpeg للدمج والصوت والترميز. Remotion ليس OSI open-source، لكنه مجاني للأفراد والفرق حتى 3 أشخاص وفق شروطه. تحقق من الأهلية. |
| المحاذاة | edge-tts WordBoundary ثم faster-whisper | توقيتات الكلمات من المزود أولًا، وfaster-whisper للتحقق المستقل باستخدام word_timestamps. WhisperX بديل للمحاذاة لكنه يحتاج اختبار موارد وتوافق. |

## مراجعة المرشحين

### الصوت
- edge-tts: https://github.com/rany2/edge-tts — مكتبة العميل LGPLv3 في معظم الملفات، وتدعم WordBoundary. اعتمادها على خدمة Microsoft غير الرسمية خطر تشغيلي؛ يجب اختبار قائمة الأصوات والاتصال والتوليد العربي في بيئة التنفيذ.
- XTTS-v2: https://huggingface.co/coqui/XTTS-v2 — العربية ضمن اللغات المدعومة، لكن الأوزان CPML وليست ترخيصًا مفتوحًا قياسيًا. لا تعتمد قبل مراجعة الشروط.
- Piper: https://github.com/rhasspy/piper — المستودع الأصلي مؤرشف، ويذكر ar_JO/Kareem. افحص ترخيص ملف الصوت نفسه.
- MMS-TTS: https://huggingface.co/facebook/mms-tts — CC-BY-NC-4.0، مستبعد من الاستخدام التجاري.
- CAMeL Tools: https://github.com/CAMeL-Lab/camel_tools — MIT؛ حزمة NLP عربية، لا نفترض أن كل مكون فيها يشكل النص دون أخطاء.
- Mishkal: https://github.com/linuxscout/mishkal — README يذكر GPL وأداة تشكيل عربية.

### الفيديو والصور
- Wan2.1: https://github.com/Wan-Video/Wan2.1 — T2V-1.3B يعلن 8.19GB VRAM و480p أكثر استقرارًا؛ بطاقة الأوزان https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B تعرض Apache-2.0.
- Wan2.2: لا يعتمد إصدار قبل فحص بطاقة أوزان محددة ومتطلبات الذاكرة والترخيص.
- LTX-Video: https://github.com/Lightricks/LTX-Video — مستودع 0.9.x يعلن أنه لم يعد تحت تطوير نشط؛ الشيفرة Apache-2.0 والأوزان لها تراخيص منفصلة. LTX-2.5 أحدث وله Community License منفصل، فلا نفترض أنه Apache.
- CogVideoX: https://github.com/zai-org/CogVideo — الشيفرة Apache-2.0؛ بعض أوضاع 5B تتطلب ذاكرة GPU مرتفعة جدًا (مثال SAT BF16 76GB في README). افحص ترخيص checkpoint المحدد.
- HunyuanVideo: https://github.com/Tencent-Hunyuan/HunyuanVideo — متطلبات README: 45GB VRAM لـ544×960 و60GB لـ720×1280 في الإعداد المشار إليه.
- FLUX.1-schnell: https://github.com/black-forest-labs/flux — 12B وApache-2.0. FLUX.1-dev ليس بديلًا مماثلًا؛ ترخيصه Non-Commercial.
- SDXL: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 — CreativeML Open RAIL++-M.

المستويات التي يجب تسميتها بوضوح في التقارير:
A) توليد فيديو حقيقي بنموذج Text-to-Video أو Image-to-Video.
B) صور مولدة ثم تحريك كاميرا Ken Burns بـFFmpeg؛ هذا ليس توليد فيديو.
C) لقطات stock مرخصة؛ لا تعتمد على Pexels/Pixabay API لأنهما يحتاجان مفتاحًا. أي مفتاح مجاني خيار اختياري يتطلب موافقة.

### التركيب والمحاذاة
- Remotion: https://www.remotion.dev/docs/license/pricing — مجاني للأفراد والفرق حتى 3 أشخاص وفق الأهلية؛ ليس OSI open-source. إذا لم تنطبق الأهلية، توقف واطلب قرارًا قبل الاستبدال.
- FFmpeg: https://ffmpeg.org/legal.html — LGPL/GPL حسب البناء والـ codecs؛ افحص ffmpeg -L وffmpeg -buildconf للنسخة المستخدمة.
- faster-whisper: https://github.com/SYSTRAN/faster-whisper — يدعم word_timestamps=True.
- WhisperX: https://github.com/m-bain/whisperX — بديل محاذاة، لم يتم اختبار إصدار أو نموذج بعد.

### SawtakArabi
- Starter موجود: https://github.com/SawtakArabi/arabic-video-starter — README وLICENSE تمت مراجعتهما، MIT. يستخدم مشروع Remotion وأمثلة للهجات، لكن README يذكر أن الصوت يأتي عبر Sawtak skill أو MCP ويستهلك رصيد Sawtak؛ لذلك لا نعتمد توليده الصوتي.
- Skill موجود: https://github.com/SawtakArabi/skill — MIT، لكن README يطلب SAWTAK_API_KEY وحسابًا ورصيدًا. مستبعد من المسار الافتراضي، ولن نضيف المفتاح أو نستخدم الخدمة.

## بنية المزودات المقترحة
- TTSProvider: EdgeTTSProvider + LocalXTTSProvider/PiperProvider + MockTTSProvider.
- VideoProvider: WanVideoProvider + KenBurnsVideoProvider + MockVideoProvider.
- ImageProvider: FluxImageProvider/SDXLImageProvider + MockImageProvider.
- كل ناتج يسجل provider وmodel وlicense وseed وprompt وis_mock. لا يسمح للـ mock أن يدعي توليدًا حقيقيًا.

## ما لم يتم التحقق منه
- GPU/VRAM/CUDA/القرص/الشبكة في بيئة التنفيذ.
- تشغيل edge-tts أو XTTS أو Piper فعليًا وجودة الصوت العربي.
- توليد صورة أو فيديو، أو إنشاء MP4، أو فحص ffprobe/Whisper/Remotion.
- لا توجد package.json أو pyproject.toml أو lockfiles في نقطة البداية.

## مصادر إضافية
https://github.com/rany2/edge-tts
https://huggingface.co/coqui/XTTS-v2
https://github.com/rhasspy/piper
https://huggingface.co/facebook/mms-tts
https://github.com/CAMeL-Lab/camel_tools
https://github.com/linuxscout/mishkal
https://github.com/Wan-Video/Wan2.1
https://github.com/Lightricks/LTX-Video
https://github.com/zai-org/CogVideo
https://github.com/Tencent-Hunyuan/HunyuanVideo
https://github.com/black-forest-labs/flux
https://ffmpeg.org/legal.html
https://github.com/SYSTRAN/faster-whisper
https://github.com/SawtakArabi/arabic-video-starter
https://github.com/SawtakArabi/skill
