from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from team.models import TeamMember

@receiver(post_save, sender=Profile)
def manage_team_members(sender, instance, **kwargs):
    """Automatically add or remove users from TeamMember when approved."""
    if instance.is_team_member:
        # Create or update TeamMember
        TeamMember.objects.update_or_create(
            matric_number=instance.matric_number,
            defaults={
                "full_name": f"{instance.user.first_name} {instance.user.last_name}",
                "department": instance.department,
                "project_role": "Member",
                "email": instance.user.email,
                "phone": instance.phone,
            },
        )
    else:
        # Remove from TeamMember if they exist
        TeamMember.objects.filter(matric_number=instance.matric_number).delete()
