from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EngagementMetric, SensoryLog, AdaptiveRule


@receiver(post_save, sender=SensoryLog)
def check_sensory_triggers(sender, instance, created, **kwargs):
    """
    Signal handler for SensoryLog post_save.
    Checks for sensory-related triggers and applies adaptive rules.
    """
    if not created:
        return  # Only process new log entries
    
    user = instance.user
    
    # Check for sensory overload trigger - AI_SENSORY_REDUCE
    if instance.sensory_overload_flag:
        rule = AdaptiveRule.objects.filter(
            name='AI_SENSORY_REDUCE',
            is_active=True
        ).first()
        
        if rule:
            print(f"⚡ TRIGGER DETECTED: {rule.name} applied for User {user.email}")


@receiver(post_save, sender=EngagementMetric)
def check_engagement_triggers(sender, instance, created, **kwargs):
    """
    Signal handler for EngagementMetric post_save.
    Checks for engagement-related triggers and applies adaptive rules.
    """
    if not created:
        return  # Only process new metric entries
    
    user = instance.user
    
    # Check for attention drop detected - AI_MICRO_GOALS
    # Trigger: attention_drop_detected == true (high idle ratio or low completion rate)
    attention_drop_detected = instance.idle_ratio > 0.5 or instance.completion_rate < 30.0
    if attention_drop_detected:
        rule = AdaptiveRule.objects.filter(
            name='AI_MICRO_GOALS',
            is_active=True
        ).first()
        
        if rule:
            print(f"⚡ TRIGGER DETECTED: {rule.name} applied for User {user.email}")
    
    # Check for long content detected - AI_CONTENT_CHUNK
    # Trigger: long_content_detected == true (high time on task indicates long content)
    long_content_detected = instance.time_on_task > 10.0
    if long_content_detected:
        rule = AdaptiveRule.objects.filter(
            name='AI_CONTENT_CHUNK',
            is_active=True
        ).first()
        
        if rule:
            print(f"⚡ TRIGGER DETECTED: {rule.name} applied for User {user.email}")

