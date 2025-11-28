from django.core.management.base import BaseCommand
from assistants.models import AI_Persona


class Command(BaseCommand):
    help = 'Initialize AI personas (DANI and LUCAS) if they do not exist'

    def handle(self, *args, **options):
        """
        Create DANI and LUCAS AI personas if they don't already exist.
        """
        # Define the personas to create
        personas_data = [
            {
                'name': 'LUCAS',
                'full_name': 'Learning Uniquely, Connecting All Strengths',
                'system_prompt': 'You are LUCAS, an AI assistant focused on learning uniquely and connecting all strengths. You help users discover their unique learning styles and connect their individual strengths to create effective learning strategies.'
            },
            {
                'name': 'DANI',
                'full_name': 'Discover, Adapt, Nurture & Inspire',
                'system_prompt': 'You are DANI, an AI assistant dedicated to discovering individual needs, adapting to different learning styles, nurturing growth, and inspiring learners. You provide personalized support and encouragement.'
            }
        ]
        
        created_count = 0
        existing_count = 0
        
        for persona_data in personas_data:
            persona, created = AI_Persona.objects.get_or_create(
                name=persona_data['name'],
                defaults={
                    'full_name': persona_data['full_name'],
                    'system_prompt': persona_data['system_prompt']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {persona.name} - {persona.full_name}'
                    )
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'{persona.name} already exists. Skipping creation.'
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nInitialization complete: {created_count} created, {existing_count} already existed.'
            )
        )

