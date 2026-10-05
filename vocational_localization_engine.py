"""
AI-Powered Multilingual Content Localization Engine for Vocational Training
Hackathon Prototype - MVP Implementation

Features:
- Multi-format content translation (text, audio, video subtitles)
- Domain-specific terminology handling
- Cultural adaptation
- Speech-to-text and text-to-speech
- Quality feedback loop
- LMS API integration capability
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Note: In production, install: googletrans==4.0.0rc1, gtts, speechrecognition, pydub
# For this prototype, we'll simulate the core logic with mock implementations

class ContentType(Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    ASSESSMENT = "assessment"
    DOCUMENT = "document"

class Language(Enum):
    """22 Indian Official Languages + English"""
    HINDI = "hi"
    ENGLISH = "en"
    BENGALI = "bn"
    TELUGU = "te"
    MARATHI = "mr"
    TAMIL = "ta"
    GUJARATI = "gu"
    KANNADA = "kn"
    MALAYALAM = "ml"
    ODIA = "or"
    PUNJABI = "pa"
    ASSAMESE = "as"
    URDU = "ur"
    SANSKRIT = "sa"
    KASHMIRI = "ks"
    KONKANI = "kok"
    MANIPURI = "mni"
    NEPALI = "ne"
    BODO = "brx"
    DOGRI = "doi"
    MAITHILI = "mai"
    SANTALI = "sat"
    SINDHI = "sd"

@dataclass
class VocationalDomain:
    """Domain-specific terminology and context"""
    name: str
    keywords: List[str]
    terminology: Dict[str, Dict[str, str]]  # {english_term: {lang: translation}}
    
class DomainVocabularyBank:
    """Manages domain-specific terminology across languages"""
    
    def __init__(self):
        self.domains = self._initialize_domains()
    
    def _initialize_domains(self) -> Dict[str, VocationalDomain]:
        """Initialize with sample vocational domains"""
        return {
            "healthcare": VocationalDomain(
                name="Healthcare",
                keywords=["patient", "diagnosis", "treatment", "hospital", "medicine"],
                terminology={
                    "patient": {"hi": "रोगी", "ta": "நோயாளி", "te": "రోగి"},
                    "nurse": {"hi": "नर्स", "ta": "செவிலியர்", "te": "నర్సు"},
                    "hospital": {"hi": "अस्पताल", "ta": "மருத்துவமனை", "te": "ఆసుపత్రి"},
                }
            ),
            "manufacturing": VocationalDomain(
                name="Manufacturing",
                keywords=["machine", "production", "assembly", "quality", "safety"],
                terminology={
                    "machine": {"hi": "मशीन", "ta": "இயந்திரம்", "te": "యంత్రం"},
                    "safety": {"hi": "सुरक्षा", "ta": "பாதுகாப்பு", "te": "భద్రత"},
                    "quality": {"hi": "गुणवत्ता", "ta": "தரம்", "te": "నాణ్యత"},
                }
            ),
            "agriculture": VocationalDomain(
                name="Agriculture",
                keywords=["crop", "fertilizer", "irrigation", "harvest", "soil"],
                terminology={
                    "crop": {"hi": "फसल", "ta": "பயிர்", "te": "పంట"},
                    "soil": {"hi": "मिट्टी", "ta": "மண்", "te": "నేల"},
                    "fertilizer": {"hi": "उर्वरक", "ta": "உரம்", "te": "ఎరువు"},
                }
            ),
            "it": VocationalDomain(
                name="Information Technology",
                keywords=["software", "programming", "database", "network", "server"],
                terminology={
                    "software": {"hi": "सॉफ्टवेयर", "ta": "மென்பொருள்", "te": "సాఫ్ట్‌వేర్"},
                    "database": {"hi": "डेटाबेस", "ta": "தரவுத்தளம்", "te": "డేటాబేస్"},
                    "network": {"hi": "नेटवर्क", "ta": "வலையமைப்பு", "te": "నెట్‌వర్క్"},
                }
            )
        }
    
    def get_domain(self, domain_name: str) -> Optional[VocationalDomain]:
        return self.domains.get(domain_name.lower())
    
    def detect_domain(self, content: str) -> Optional[str]:
        """Detect vocational domain from content"""
        content_lower = content.lower()
        max_matches = 0
        detected_domain = None
        
        for domain_name, domain in self.domains.items():
            matches = sum(1 for keyword in domain.keywords if keyword in content_lower)
            if matches > max_matches:
                max_matches = matches
                detected_domain = domain_name
        
        return detected_domain if max_matches > 0 else None

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    domain: Optional[str]
    confidence_score: float
    cultural_adaptations: List[str]
    timestamp: str

class CulturalAdaptationEngine:
    """Handles cultural context and regional adaptation"""
    
    def __init__(self):
        self.cultural_rules = self._initialize_cultural_rules()
    
    def _initialize_cultural_rules(self) -> Dict[str, List[Dict]]:
        """Cultural adaptation rules by language/region"""
        return {
            "hi": [
                {"pattern": "Mr.", "replacement": "श्री", "context": "formal_address"},
                {"pattern": "Mrs.", "replacement": "श्रीमती", "context": "formal_address"},
            ],
            "ta": [
                {"pattern": "Mr.", "replacement": "திரு", "context": "formal_address"},
                {"pattern": "Mrs.", "replacement": "திருமதி", "context": "formal_address"},
            ],
            "te": [
                {"pattern": "Mr.", "replacement": "శ్రీ", "context": "formal_address"},
                {"pattern": "Mrs.", "replacement": "శ్రీమతి", "context": "formal_address"},
            ]
        }
    
    def adapt_content(self, text: str, target_lang: str) -> tuple[str, List[str]]:
        """Apply cultural adaptations to translated content"""
        adaptations = []
        adapted_text = text
        
        rules = self.cultural_rules.get(target_lang, [])
        for rule in rules:
            if rule["pattern"] in adapted_text:
                adapted_text = adapted_text.replace(rule["pattern"], rule["replacement"])
                adaptations.append(f"Applied {rule['context']} adaptation")
        
        return adapted_text, adaptations

class TranslationEngine:
    """Core translation engine with domain awareness"""
    
    def __init__(self):
        self.vocab_bank = DomainVocabularyBank()
        self.cultural_engine = CulturalAdaptationEngine()
        self.translation_memory = {}  # Cache for consistency
        self.feedback_data = []
    
    def translate(self, text: str, target_lang: str, source_lang: str = "en", 
                  domain: Optional[str] = None) -> TranslationResult:
        """
        Translate content with domain-specific accuracy
        In production: Use Google Translate API, Azure Translator, or custom models
        """
        # Detect domain if not provided
        if not domain:
            domain = self.vocab_bank.detect_domain(text)
        
        # Simulate translation (in production, call actual translation API)
        translated_text = self._perform_translation(text, target_lang, source_lang, domain)
        
        # Apply cultural adaptations
        adapted_text, adaptations = self.cultural_engine.adapt_content(
            translated_text, target_lang
        )
        
        # Calculate confidence score (simulated)
        confidence = self._calculate_confidence(text, domain)
        
        result = TranslationResult(
            original_text=text,
            translated_text=adapted_text,
            source_lang=source_lang,
            target_lang=target_lang,
            domain=domain,
            confidence_score=confidence,
            cultural_adaptations=adaptations,
            timestamp=datetime.now().isoformat()
        )
        
        # Store in translation memory
        self._update_translation_memory(text, target_lang, adapted_text)
        
        return result
    
    def _perform_translation(self, text: str, target_lang: str, 
                            source_lang: str, domain: Optional[str]) -> str:
        """
        Perform actual translation
        Production: Integrate with Google Translate, Azure, or custom NMT models
        """
        # Check translation memory first
        cache_key = f"{text}_{target_lang}"
        if cache_key in self.translation_memory:
            return self.translation_memory[cache_key]
        
        # Apply domain-specific terminology
        processed_text = text
        if domain:
            domain_obj = self.vocab_bank.get_domain(domain)
            if domain_obj:
                for eng_term, translations in domain_obj.terminology.items():
                    if eng_term in processed_text and target_lang in translations:
                        processed_text = processed_text.replace(
                            eng_term, translations[target_lang]
                        )
        
        # Simulate translation (in production, call actual API)
        # For demo, we'll return a formatted version
        simulated_translation = f"[{target_lang.upper()}] {processed_text}"
        
        return simulated_translation
    
    def _calculate_confidence(self, text: str, domain: Optional[str]) -> float:
        """Calculate translation confidence score"""
        base_confidence = 0.85
        
        # Higher confidence if domain detected
        if domain:
            base_confidence += 0.10
        
        # Adjust based on text length and complexity
        if len(text.split()) < 10:
            base_confidence += 0.05
        
        return min(base_confidence, 0.99)
    
    def _update_translation_memory(self, source: str, lang: str, translation: str):
        """Update translation memory for consistency"""
        cache_key = f"{source}_{lang}"
        self.translation_memory[cache_key] = translation
    
    def collect_feedback(self, translation_id: str, rating: int, 
                        corrections: Optional[str] = None):
        """Collect user feedback for continuous improvement"""
        feedback = {
            "translation_id": translation_id,
            "rating": rating,
            "corrections": corrections,
            "timestamp": datetime.now().isoformat()
        }
        self.feedback_data.append(feedback)
        return feedback

class SpeechProcessor:
    """Handle speech-to-text and text-to-speech"""
    
    def __init__(self):
        self.supported_languages = [lang.value for lang in Language]
    
    def speech_to_text(self, audio_file: str, language: str = "en") -> str:
        """
        Convert speech to text
        Production: Use Google Speech-to-Text, Azure Speech Services, or Whisper API
        """
        # Simulated STT result
        return f"[STT Result for {language}]: Transcribed audio content from {audio_file}"
    
    def text_to_speech(self, text: str, language: str = "en", 
                       output_file: str = "output.mp3") -> str:
        """
        Convert text to speech
        Production: Use gTTS, Azure TTS, or Google TTS
        """
        # Simulated TTS generation
        return f"Generated audio file: {output_file} for language {language}"

class ContentProcessor:
    """Process different content types"""
    
    def __init__(self, translation_engine: TranslationEngine):
        self.translation_engine = translation_engine
        self.speech_processor = SpeechProcessor()
    
    def process_document(self, content: str, target_langs: List[str], 
                        domain: Optional[str] = None) -> Dict[str, TranslationResult]:
        """Process and translate text documents"""
        results = {}
        for lang in target_langs:
            results[lang] = self.translation_engine.translate(
                content, lang, domain=domain
            )
        return results
    
    def process_audio(self, audio_file: str, target_langs: List[str],
                     source_lang: str = "en") -> Dict[str, Dict]:
        """Process audio content: STT -> Translate -> TTS"""
        # Step 1: Speech to Text
        transcribed_text = self.speech_processor.speech_to_text(audio_file, source_lang)
        
        results = {}
        for lang in target_langs:
            # Step 2: Translate
            translation = self.translation_engine.translate(transcribed_text, lang)
            
            # Step 3: Text to Speech
            output_file = f"translated_audio_{lang}.mp3"
            audio_output = self.speech_processor.text_to_speech(
                translation.translated_text, lang, output_file
            )
            
            results[lang] = {
                "transcription": transcribed_text,
                "translation": translation,
                "audio_file": audio_output
            }
        
        return results
    
    def process_video_subtitles(self, subtitle_file: str, target_langs: List[str],
                                domain: Optional[str] = None) -> Dict[str, str]:
        """Process and translate video subtitles (SRT format)"""
        # In production: Parse SRT, translate segments, regenerate SRT
        results = {}
        for lang in target_langs:
            results[lang] = f"Generated subtitle file: subtitles_{lang}.srt"
        return results
    
    def process_assessment(self, questions: List[Dict], target_langs: List[str],
                          domain: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Translate assessment questions and options"""
        results = {}
        
        for lang in target_langs:
            translated_questions = []
            for q in questions:
                translated_q = {
                    "id": q["id"],
                    "question": self.translation_engine.translate(
                        q["question"], lang, domain=domain
                    ).translated_text,
                    "options": [
                        self.translation_engine.translate(opt, lang, domain=domain).translated_text
                        for opt in q.get("options", [])
                    ],
                    "correct_answer": q.get("correct_answer")
                }
                translated_questions.append(translated_q)
            
            results[lang] = translated_questions
        
        return results

class LMSIntegrationAPI:
    """API integration capabilities for LMS platforms"""
    
    def __init__(self, content_processor: ContentProcessor):
        self.content_processor = content_processor
        self.api_endpoints = {
            "ncvet": "https://api.ncvet.gov.in/v1",
            "msde": "https://api.msde.gov.in/v1",
            "skill_india": "https://api.skillindia.gov.in/v1"
        }
    
    def create_translation_job(self, content: Dict, target_langs: List[str],
                              content_type: str) -> Dict:
        """Create a batch translation job"""
        job = {
            "job_id": f"JOB_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "content_type": content_type,
            "target_languages": target_langs,
            "status": "processing",
            "created_at": datetime.now().isoformat()
        }
        return job
    
    def get_job_status(self, job_id: str) -> Dict:
        """Check translation job status"""
        return {
            "job_id": job_id,
            "status": "completed",
            "progress": 100,
            "completed_languages": ["hi", "ta", "te"]
        }
    
    def export_to_lms(self, content: Dict, format: str = "scorm") -> Dict:
        """Export translated content in LMS-compatible format"""
        return {
            "format": format,
            "package_url": f"https://storage.example.com/packages/{format}_package.zip",
            "metadata": {
                "languages": content.get("languages", []),
                "duration": "2 hours",
                "accessibility": "WCAG 2.1 AA compliant"
            }
        }

class LocalizationPipeline:
    """Complete end-to-end localization pipeline"""
    
    def __init__(self):
        self.translation_engine = TranslationEngine()
        self.content_processor = ContentProcessor(self.translation_engine)
        self.lms_api = LMSIntegrationAPI(self.content_processor)
    
    def localize_training_module(self, module_data: Dict) -> Dict:
        """
        Localize complete training module
        
        Args:
            module_data: {
                "title": str,
                "content": str,
                "domain": str,
                "target_languages": List[str],
                "includes_audio": bool,
                "includes_video": bool,
                "assessment": List[Dict]
            }
        """
        results = {
            "module_id": f"MOD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "original_title": module_data["title"],
            "domain": module_data["domain"],
            "localizations": {}
        }
        
        target_langs = module_data["target_languages"]
        
        # Translate main content
        content_translations = self.content_processor.process_document(
            module_data["content"],
            target_langs,
            domain=module_data["domain"]
        )
        
        # Translate assessments if present
        assessment_translations = {}
        if "assessment" in module_data:
            assessment_translations = self.content_processor.process_assessment(
                module_data["assessment"],
                target_langs,
                domain=module_data["domain"]
            )
        
        # Compile results
        for lang in target_langs:
            results["localizations"][lang] = {
                "content": asdict(content_translations[lang]),
                "assessment": assessment_translations.get(lang, []),
                "accessibility_features": {
                    "tts_enabled": True,
                    "screen_reader_compatible": True,
                    "keyboard_navigation": True
                }
            }
        
        return results
    
    def get_analytics(self) -> Dict:
        """Get analytics on translation quality and usage"""
        return {
            "total_translations": len(self.translation_engine.translation_memory),
            "average_confidence": 0.92,
            "feedback_count": len(self.translation_engine.feedback_data),
            "supported_languages": len(Language),
            "supported_domains": len(self.translation_engine.vocab_bank.domains)
        }

# =============================================================================
# DEMO / TESTING CODE
# =============================================================================

def run_demo():
    """Demonstrate the localization engine capabilities"""
    
    print("=" * 70)
    print("AI-POWERED MULTILINGUAL VOCATIONAL TRAINING LOCALIZATION ENGINE")
    print("Hackathon MVP Prototype")
    print("=" * 70)
    print()
    
    # Initialize the pipeline
    pipeline = LocalizationPipeline()
    
    # Sample training module
    sample_module = {
        "title": "Basic Patient Care in Nursing",
        "content": """
        Patient care is the foundation of nursing practice. A nurse must always 
        monitor the patient's vital signs, administer medicine as prescribed, 
        and maintain a clean and safe hospital environment. Safety protocols 
        must be followed at all times to prevent infections and ensure quality care.
        """,
        "domain": "healthcare",
        "target_languages": ["hi", "ta", "te"],
        "assessment": [
            {
                "id": "Q1",
                "question": "What is the primary responsibility of a nurse?",
                "options": [
                    "Patient care and monitoring",
                    "Hospital administration",
                    "Medical diagnosis",
                    "Surgery assistance"
                ],
                "correct_answer": 0
            }
        ]
    }
    
    print("📚 SAMPLE TRAINING MODULE:")
    print(f"Title: {sample_module['title']}")
    print(f"Domain: {sample_module['domain']}")
    print(f"Target Languages: {', '.join(sample_module['target_languages'])}")
    print()
    
    print("🔄 Processing localization...")
    print()
    
    # Process the module
    results = pipeline.localize_training_module(sample_module)
    
    print("✅ LOCALIZATION COMPLETE!")
    print(f"Module ID: {results['module_id']}")
    print()
    
    # Display results for each language
    for lang, localization in results["localizations"].items():
        print(f"\n{'=' * 70}")
        print(f"📍 LANGUAGE: {lang.upper()}")
        print(f"{'=' * 70}")
        
        content_result = localization["content"]
        print(f"\n📄 Translated Content:")
        print(f"   Original: {content_result['original_text'][:100]}...")
        print(f"   Translated: {content_result['translated_text'][:100]}...")
        print(f"   Confidence: {content_result['confidence_score']:.2%}")
        print(f"   Domain: {content_result['domain']}")
        
        if content_result['cultural_adaptations']:
            print(f"   Cultural Adaptations: {', '.join(content_result['cultural_adaptations'])}")
        
        # Show assessment translation
        if localization["assessment"]:
            print(f"\n📝 Assessment Translation:")
            q = localization["assessment"][0]
            print(f"   Question: {q['question'][:80]}...")
            print(f"   Options: {len(q['options'])} translated")
        
        # Show accessibility features
        print(f"\n♿ Accessibility Features:")
        for feature, enabled in localization["accessibility_features"].items():
            status = "✓" if enabled else "✗"
            print(f"   {status} {feature.replace('_', ' ').title()}")
    
    # Show analytics
    print(f"\n{'=' * 70}")
    print("📊 SYSTEM ANALYTICS")
    print(f"{'=' * 70}")
    analytics = pipeline.get_analytics()
    for key, value in analytics.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Demonstrate feedback collection
    print(f"\n{'=' * 70}")
    print("🔁 CONTINUOUS IMPROVEMENT - FEEDBACK SYSTEM")
    print(f"{'=' * 70}")
    feedback = pipeline.translation_engine.collect_feedback(
        translation_id=results['module_id'],
        rating=4,
        corrections="Excellent translation quality"
    )
    print(f"   Feedback collected: Rating {feedback['rating']}/5")
    print(f"   Timestamp: {feedback['timestamp']}")
    
    # Show LMS integration capabilities
    print(f"\n{'=' * 70}")
    print("🔌 LMS INTEGRATION API")
    print(f"{'=' * 70}")
    print("   Supported Platforms:")
    for platform, endpoint in pipeline.lms_api.api_endpoints.items():
        print(f"   • {platform.upper()}: {endpoint}")
    
    export_result = pipeline.lms_api.export_to_lms(
        {"languages": sample_module['target_languages']},
        format="scorm"
    )
    print(f"\n   Export Format: {export_result['format'].upper()}")
    print(f"   Package URL: {export_result['package_url']}")
    print(f"   WCAG Compliance: {export_result['metadata']['accessibility']}")
    
    print(f"\n{'=' * 70}")
    print("✨ PROTOTYPE DEMONSTRATION COMPLETE")
    print(f"{'=' * 70}")
    print("\n🚀 PRODUCTION ROADMAP:")
    print("   1. Integrate Google Translate / Azure Translator API")
    print("   2. Implement Whisper API for speech recognition")
    print("   3. Add custom NMT models for domain-specific accuracy")
    print("   4. Build web dashboard for content management")
    print("   5. Implement SCORM/xAPI packaging")
    print("   6. Add quality assurance workflow")
    print("   7. Deploy on cloud infrastructure (AWS/Azure/GCP)")
    print("   8. Connect to real NCVET/MSDE platforms")
    print()

if __name__ == "__main__":
    run_demo()
