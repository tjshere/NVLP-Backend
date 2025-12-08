from django.core.management.base import BaseCommand
from adaptive_engine.models import AdaptiveRule


class Command(BaseCommand):
    help = 'Load neuro rules into the database'

    # Define the AI rules data
    AI_RULES_DATA = {
        "AI_SENSORY_REDUCE": {
            "trigger": "learner_profile.contains('autistic_profile') || sensory_overload_detected == true",
            "action": "reduce_sensory_input",
            "modifiers": {
                "visual_contrast": "neutral",
                "audio_volume": "low",
                "animations": "off"
            }
        },
        "AI_STRUCTURE_INCREASE": {
            "trigger": "learner_profile.contains('autistic_profile') || learner_requests_structure == true",
            "action": "apply_structured_format",
            "modifiers": {
                "sequence_format": "step_by_step",
                "use_numbered_lists": True
            }
        },
        "AI_LITERAL_MODE": {
            "trigger": "learner_profile.contains('autistic_profile') || ambiguity_flag == true",
            "action": "convert_language_literal",
            "modifiers": {
                "figurative_language": "remove",
                "replace_with": "literal_equivalent"
            }
        },
        "AI_CONTENT_CHUNK": {
            "trigger": "learner_profile.contains('adhd_profile') || long_content_detected == true",
            "action": "chunk_content",
            "modifiers": {
                "chunk_length_seconds": 90,
                "max_chunk_length_words": 120
            }
        },
        "AI_MICRO_GOALS": {
            "trigger": "attention_drop_detected == true || learner_profile.contains('adhd_profile')",
            "action": "create_micro_goals",
            "modifiers": {
                "goal_unit": "small",
                "reward_on_completion": True
            }
        },
        "AI_TTS_ON": {
            "trigger": "reading_load_high == true || learner_profile.contains('dyslexic_profile')",
            "action": "enable_text_to_speech",
            "modifiers": {
                "voice": "calm",
                "speed": "slow"
            }
        },
        "AI_CRA_SEQUENCE": {
            "trigger": "math_abstraction_difficulty == true || learner_profile.contains('dyscalculia_profile')",
            "action": "apply_CRA_sequence",
            "modifiers": {
                "sequence": ["concrete", "representational", "abstract"]
            }
        }
    }

    def handle(self, *args, **options):
        """
        Load neuro rules into the database using update_or_create.
        """
        created_count = 0
        updated_count = 0
        
        for rule_name, rule_data in self.AI_RULES_DATA.items():
            # Extract trigger for condition field
            condition = rule_data.get("trigger", "")
            
            # Use the whole rule_data as action_payload (includes trigger, action, modifiers)
            action_payload = rule_data
            
            # Use update_or_create to either create or update the rule
            rule, created = AdaptiveRule.objects.update_or_create(
                name=rule_name,
                defaults={
                    'condition': condition,
                    'action_payload': action_payload,
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created rule: {rule_name}'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Updated existing rule: {rule_name}'
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nNeuro rules loading complete: {created_count} created, {updated_count} updated.'
            )
        )

