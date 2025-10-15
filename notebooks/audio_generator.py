
#!/usr/bin/env python3
"""
Audio Generator Script for HealthEquity Case Study
Generates Spanish and Tagalog audio files using TTS (Text-to-Speech).
"""

import os
import sys
import argparse
from pathlib import Path
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from TTS.api import TTS
except ImportError:
    print("Installing TTS...")
    os.system("pip install TTS")
    from TTS.api import TTS


class HealthEquityAudioGenerator:
    """Audio generator using TTS library for HealthEquity case study."""
    
    def __init__(self, output_dir: str = "health_audio_output"):
        """
        Initialize the HealthEquity Audio Generator.
        
        Args:
            output_dir: Directory to save generated audio files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize TTS model
        try:
            logger.info("Loading TTS model...")
            self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
            logger.info("TTS model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load TTS model: {str(e)}")
            raise
        
        # Spanish healthcare questions
        self.spanish_questions = [
            "¿Cuáles son mis valores de presión arterial hoy?",
            "¿Cuáles fueron los valores de la última semana?", 
            "¿Cuál es la tendencia de mis valores?",
            "¿Cuáles son los rangos normales para una persona como yo?",
            "Por favor tome su medicamento según lo recetado por su médico.",
            "Su cita está programada para mañana a las 2 PM.",
            "Por favor ayune durante 8 horas antes de su análisis de sangre.",
            "Su seguro cubre este procedimiento completamente.",
            "Por favor traiga su tarjeta de seguro y identificación con foto.",
            "El médico lo verá en la habitación 205."
        ]
        
        # Tagalog healthcare questions (manually translated)
        self.tagalog_questions = [
            "Ano ang aking mga blood pressure values ngayon?",
            "Ano ang mga values noong nakaraang linggo?",
            "Ano ang trend ng aking mga values?",
            "Ano ang normal ranges para sa isang taong katulad ko?",
            "Mangyaring inumin ang inyong gamot ayon sa inireseta ng inyong doktor.",
            "Ang inyong appointment ay nakatakda bukas ng 2 PM.",
            "Mangyaring mag-ayuno ng 8 oras bago ang inyong blood test.",
            "Ang inyong insurance ay sumasaklaw sa procedure na ito nang lubusan.",
            "Mangyaring dalhin ang inyong insurance card at photo ID.",
            "Ang doktor ay makikita kayo sa room 205."
        ]
        
        logger.info(f"HealthEquity Audio Generator initialized. Output directory: {self.output_dir}")
    
    def generate_spanish_audio(self, custom_questions: List[str] = None) -> List[str]:
        """
        Generate Spanish audio files.
        
        Args:
            custom_questions: Optional list of custom Spanish questions
            
        Returns:
            List of generated audio file paths
        """
        questions = custom_questions if custom_questions else self.spanish_questions
        generated_files = []
        
        logger.info(f"Generating {len(questions)} Spanish audio files...")
        
        for i, question in enumerate(questions, 1):
            try:
                filename = f"spanish_q{i:03d}.wav"
                filepath = self.output_dir / filename
                
                self.tts.tts_to_file(text=question, speaker="es", file_path=str(filepath))
                generated_files.append(str(filepath))
                logger.info(f"✅ Generated {filename}")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate audio for Spanish question {i}: {str(e)}")
        
        return generated_files
    
    def generate_tagalog_audio(self, custom_questions: List[str] = None) -> List[str]:
        """
        Generate Tagalog audio files.
        
        Args:
            custom_questions: Optional list of custom Tagalog questions
            
        Returns:
            List of generated audio file paths
        """
        questions = custom_questions if custom_questions else self.tagalog_questions
        generated_files = []
        
        logger.info(f"Generating {len(questions)} Tagalog audio files...")
        
        for i, question in enumerate(questions, 1):
            try:
                filename = f"tagalog_q{i:03d}.wav"
                filepath = self.output_dir / filename
                
                # Use English speaker for Tagalog (no specific Tagalog speaker available)
                self.tts.tts_to_file(text=question, speaker="en", file_path=str(filepath))
                generated_files.append(str(filepath))
                logger.info(f"✅ Generated {filename}")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate audio for Tagalog question {i}: {str(e)}")
        
        return generated_files
    
    def generate_all_audio(self) -> Dict[str, List[str]]:
        """
        Generate both Spanish and Tagalog audio files.
        
        Returns:
            Dictionary with lists of generated files for each language
        """
        results = {
            'spanish': [],
            'tagalog': []
        }
        
        logger.info("Starting audio generation for all languages...")
        
        # Generate Spanish audio
        results['spanish'] = self.generate_spanish_audio()
        
        # Generate Tagalog audio
        results['tagalog'] = self.generate_tagalog_audio()
        
        total_files = len(results['spanish']) + len(results['tagalog'])
        logger.info(f"✅ Audio generation completed! Generated {total_files} files total.")
        
        return results
    
    def generate_custom_audio(self, spanish_texts: List[str] = None, tagalog_texts: List[str] = None) -> Dict[str, List[str]]:
        """
        Generate audio files from custom text inputs.
        
        Args:
            spanish_texts: List of Spanish texts to convert to audio
            tagalog_texts: List of Tagalog texts to convert to audio
            
        Returns:
            Dictionary with lists of generated files for each language
        """
        results = {
            'spanish': [],
            'tagalog': []
        }
        
        if spanish_texts:
            logger.info(f"Generating custom Spanish audio for {len(spanish_texts)} texts...")
            results['spanish'] = self.generate_spanish_audio(spanish_texts)
        
        if tagalog_texts:
            logger.info(f"Generating custom Tagalog audio for {len(tagalog_texts)} texts...")
            results['tagalog'] = self.generate_tagalog_audio(tagalog_texts)
        
        return results


def load_texts_from_file(file_path: str) -> List[str]:
    """
    Load texts from a file (one per line).
    
    Args:
        file_path: Path to text file
        
    Returns:
        List of texts
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        texts = [line.strip() for line in content.split('\n') if line.strip()]
        logger.info(f"Loaded {len(texts)} texts from {file_path}")
        return texts
        
    except Exception as e:
        logger.error(f"Error loading texts from file: {str(e)}")
        return []


def main():
    """Main function to run the audio generator."""
    parser = argparse.ArgumentParser(description='HealthEquity Audio Generator - Generate Spanish/Tagalog audio files')
    parser.add_argument('--output', '-o', default='health_audio_output',
                       help='Output directory for audio files (default: health_audio_output)')
    parser.add_argument('--spanish-file', '-sf', help='Text file containing Spanish texts (one per line)')
    parser.add_argument('--tagalog-file', '-tf', help='Text file containing Tagalog texts (one per line)')
    parser.add_argument('--spanish-texts', '-st', nargs='+', help='List of Spanish texts')
    parser.add_argument('--tagalog-texts', '-tt', nargs='+', help='List of Tagalog texts')
    parser.add_argument('--languages', '-l', nargs='+', choices=['spanish', 'tagalog'], 
                       default=['spanish', 'tagalog'], help='Languages to generate (default: both)')
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = HealthEquityAudioGenerator(output_dir=args.output)
        
        # Determine what to generate
        spanish_texts = None
        tagalog_texts = None
        
        if args.spanish_file:
            spanish_texts = load_texts_from_file(args.spanish_file)
        elif args.spanish_texts:
            spanish_texts = args.spanish_texts
        
        if args.tagalog_file:
            tagalog_texts = load_texts_from_file(args.tagalog_file)
        elif args.tagalog_texts:
            tagalog_texts = args.tagalog_texts
        
        # Generate audio files
        if spanish_texts or tagalog_texts:
            # Custom texts provided
            results = generator.generate_custom_audio(
                spanish_texts=spanish_texts if 'spanish' in args.languages else None,
                tagalog_texts=tagalog_texts if 'tagalog' in args.languages else None
            )
        else:
            # Use default healthcare questions
            results = {}
            if 'spanish' in args.languages:
                results['spanish'] = generator.generate_spanish_audio()
            if 'tagalog' in args.languages:
                results['tagalog'] = generator.generate_tagalog_audio()
        
        # Print results
        print("\n" + "="*60)
        print("HEALTHEQUITY AUDIO GENERATION RESULTS")
        print("="*60)
        
        total_files = 0
        for language, files in results.items():
            print(f"\n{language.upper()} Audio Files ({len(files)} files):")
            for file in files:
                filename = Path(file).name
                print(f"  ✅ {filename}")
                total_files += 1
        
        print(f"\n📁 All files saved in: {generator.output_dir}")
        print(f"📊 Total audio files generated: {total_files}")
        
    except Exception as e:
        logger.error(f"Audio generation failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()