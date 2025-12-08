from django.core.management.base import BaseCommand
from adaptive_engine.models import AdaptiveRule


class Command(BaseCommand):
    help = 'Load neuro rules into the database'

    # Define the AI rules data - Complete library of neuro rules
    AI_RULES_DATA = {
        "AI_SENSORY_REDUCE": {
            "trigger": "learner_profile.contains('autistic_profile') || sensory_overload_detected == true",
            "action": "reduce_sensory_input",
            "modifiers": {"visual_contrast": "neutral", "audio_volume": "low", "animations": "off"}
        },
        "AI_STRUCTURE_INCREASE": {
            "trigger": "learner_profile.contains('autistic_profile') || learner_requests_structure == true",
            "action": "apply_structured_format",
            "modifiers": {"sequence_format": "step_by_step", "use_numbered_lists": True}
        },
        "AI_LITERAL_MODE": {
            "trigger": "learner_profile.contains('autistic_profile') || ambiguity_flag == true",
            "action": "convert_language_literal",
            "modifiers": {"figurative_language": "remove", "replace_with": "literal_equivalent"}
        },
        "AI_INTEREST_LINKING": {
            "trigger": "learner_profile.contains('autistic_profile') || learner_interest_tag_active == true",
            "action": "embed_interest_into_instruction",
            "modifiers": {"interest_reference_frequency": "high", "use_case_examples": "interest_based"}
        },
        "AI_TRANSITION_WARNING_90_60_30": {
            "trigger": "transition_event_approaching == true",
            "action": "send_transition_warnings",
            "modifiers": {"timestamps": [90, 60, 30], "tone": "neutral_reassuring"}
        },
        "AI_VISUAL_SUPPORT_ON": {
            "trigger": "visual_support_needed == true || learner_profile.contains('autistic_profile')",
            "action": "add_visual_support",
            "modifiers": {"include_icons": True, "include_diagrams": True, "include_flowcharts": True}
        },
        "AI_CONTENT_CHUNK": {
            "trigger": "learner_profile.contains('adhd_profile') || long_content_detected == true",
            "action": "chunk_content",
            "modifiers": {"chunk_length_seconds": 90, "max_chunk_length_words": 120}
        },
        "AI_MICRO_GOALS": {
            "trigger": "attention_drop_detected == true || learner_profile.contains('adhd_profile')",
            "action": "create_micro_goals",
            "modifiers": {"goal_unit": "small", "reward_on_completion": True}
        },
        "AI_SHORT_FEEDBACK_INTERVAL": {
            "trigger": "adhd_feedback_needed == true",
            "action": "increase_feedback_frequency",
            "modifiers": {"interval_seconds": 30, "feedback_type": "encouraging_microfeedback"}
        },
        "AI_ENERGY_BREAK_REMINDER": {
            "trigger": "learner_profile.contains('adhd_profile') || fidgeting_detected == true",
            "action": "prompt_energy_break",
            "modifiers": {"break_length_seconds": 60, "frequency_minutes": 10}
        },
        "AI_REWARD_TOKEN_MODE": {
            "trigger": "motivation_needed == true",
            "action": "enable_token_rewards",
            "modifiers": {"token_frequency": "task_completion_based", "exchange_store_enabled": True}
        },
        "AI_EXECT_FUNCTION_SCAFFOLD": {
            "trigger": "working_memory_load_high == true",
            "action": "add_executive_function_supports",
            "modifiers": {"checklists": True, "timers": True, "stepwise_tasks": True}
        },
        "AI_TTS_ON": {
            "trigger": "reading_load_high == true || learner_profile.contains('dyslexic_profile')",
            "action": "enable_text_to_speech",
            "modifiers": {"voice": "calm", "speed": "slow"}
        },
        "AI_DYSLEXIA_FONT_MODE": {
            "trigger": "dyslexia_support_needed == true",
            "action": "convert_to_dyslexia_font",
            "modifiers": {"font_type": "OpenDyslexic", "line_spacing": "1.5x", "word_spacing": "wide"}
        },
        "AI_VISUAL_ANCHORING": {
            "trigger": "complex_text_detected == true",
            "action": "add_visual_anchors",
            "modifiers": {"icons": True, "color_coding": True, "semantic_maps": True}
        },
        "AI_SLOW_READING_PACE": {
            "trigger": "reading_fluency_low == true",
            "action": "reduce_reading_pace",
            "modifiers": {"pause_after_sentences": True}
        },
        "AI_ERROR_TOLERANT_SPELLING": {
            "trigger": "spelling_errors_repeated == true",
            "action": "tolerate_spelling_variants",
            "modifiers": {"penalty": "none", "autocorrect": "gentle"}
        },
        "AI_CRA_SEQUENCE": {
            "trigger": "math_abstraction_difficulty == true || learner_profile.contains('dyscalculia_profile')",
            "action": "apply_CRA_sequence",
            "modifiers": {"sequence": ["concrete", "representational", "abstract"]}
        },
        "AI_VISUAL_MATH_MODE": {
            "trigger": "numeracy_support_needed == true",
            "action": "add_visual_math_models",
            "modifiers": {"number_lines": True, "manipulatives": True, "diagrams": True}
        },
        "AI_NO_TIMER": {
            "trigger": "math_timer_anxiety_detected == true",
            "action": "disable_timers",
            "modifiers": {"remove_deadlines": True}
        },
        "AI_REAL_WORLD_CONTEXT": {
            "trigger": "abstract_math_confusion == true",
            "action": "convert_to_real_world_context",
            "modifiers": {"context_type": "daily_life"}
        },
        "AI_ERROR_GENTLE_RETRY": {
            "trigger": "math_error_rate_high == true",
            "action": "offer_gentle_retry",
            "modifiers": {"tone": "supportive"}
        },
        "AI_SPEECH_TO_TEXT": {
            "trigger": "fine_motor_load_high == true || learner_profile.contains('dyspraxia_profile')",
            "action": "enable_speech_to_text",
            "modifiers": {"voice_detection": "sensitive"}
        },
        "AI_SEQUENCING_ASSIST": {
            "trigger": "task_sequence_confusion == true",
            "action": "provide_step_prompts",
            "modifiers": {"steps": "minimal_clear"}
        },
        "AI_BIG_BUTTON_UI": {
            "trigger": "precision_motor_difficulty == true",
            "action": "increase_button_size",
            "modifiers": {"button_padding": "large"}
        },
        "AI_LOW_MOTOR_DEMAND_MODE": {
            "trigger": "writing_fatigue_detected == true",
            "action": "reduce_motor_demands",
            "modifiers": {"drag_drop": "off"}
        },
        "AI_CAPTIONS_ON": {
            "trigger": "audio_processing_support_needed == true",
            "action": "enable_captions",
            "modifiers": {"accuracy": "high"}
        },
        "AI_SLOW_AUDIO": {
            "trigger": "audio_speed_comprehension_low == true",
            "action": "reduce_audio_speed",
            "modifiers": {"speed": "0.8x"}
        },
        "AI_VISUAL_PAIRING": {
            "trigger": "audio_only_instruction_detected == true",
            "action": "pair_audio_with_visuals",
            "modifiers": {"visual_type": "diagram_or_icon"}
        },
        "AI_NO_BACKGROUND_AUDIO": {
            "trigger": "noise_sensitivity_detected == true",
            "action": "remove_background_audio"
        },
        "AI_ACCELERATE_WHEN_READY": {
            "trigger": "mastery_detected == true",
            "action": "increase_pacing",
            "modifiers": {"unlock_next_level": True}
        },
        "AI_DEPTH_MODE": {
            "trigger": "advanced_interest_detected == true",
            "action": "add_deep_learning_extensions"
        },
        "AI_PASSION_PROJECT_LINKING": {
            "trigger": "special_interest_detected == true",
            "action": "link_tasks_to_interest"
        },
        "AI_CHOICE_BOOST": {
            "trigger": "autonomy_needed == true",
            "action": "increase_choice_options"
        },
        "AI_LOW_PRESSURE_MODE": {
            "trigger": "anxiety_detected == true",
            "action": "lower_stakes",
            "modifiers": {"remove_time_limits": True, "reduce_required_items": True}
        },
        "AI_PREDICTABLE_PATH": {
            "trigger": "uncertainty_detected == true",
            "action": "increase_predictability"
        },
        "AI_ANXIETY_REASSURANCE": {
            "trigger": "stress_signals_detected == true",
            "action": "deliver_reassurance"
        },
        "AI_GENTLE_CHALLENGE": {
            "trigger": "learner_ready_for_progress == true",
            "action": "increase_challenge_gradually"
        },
        "AI_SENSORY_LOW_STIM": {
            "trigger": "overstimulation_detected == true",
            "action": "reduce_stimulation"
        },
        "AI_SENSORY_SEEK_MODE": {
            "trigger": "understimulation_detected == true",
            "action": "increase_stimulation"
        },
        "AI_ANIMATION_TOGGLE": {
            "trigger": "animation_sensitivity_flag == true",
            "action": "toggle_animations"
        },
        "AI_KINESTHETIC_PROMPTS": {
            "trigger": "movement_need_detected == true",
            "action": "add_movement_prompts"
        },
        "AI_STEPWISE_TASK_MODE": {
            "trigger": "executive_function_challenge_detected == true",
            "action": "create_stepwise_task_flow"
        },
        "AI_CHECKLIST_BUILDER": {
            "trigger": "task_complexity_high == true",
            "action": "build_checklist"
        },
        "AI_INITIATION_PROMPT": {
            "trigger": "task_initiation_delay_detected == true",
            "action": "send_start_prompt"
        },
        "AI_TIMER_SUPPORT": {
            "trigger": "time_management_support_needed == true",
            "action": "provide_timers"
        },
        "AI_DEADLINE_BREAKDOWN": {
            "trigger": "deadline_overwhelm_detected == true",
            "action": "break_deadline_into_subtasks"
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

