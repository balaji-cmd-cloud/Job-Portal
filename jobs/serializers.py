from rest_framework import serializers
from .models import Job, Application, SavedJob

class JobSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'domain', 'location', 
            'description', 'skills_required', 'skills_list', 
            'salary_range', 'job_type', 'experience_required', 'created_at'
        ]

    def get_skills_list(self, obj):
        return obj.get_skills_list()


class ApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'user', 'user_email', 'job', 'job_details', 'applied_at', 'cover_letter', 'status']
        read_only_fields = ['user', 'applied_at', 'status']


class SavedJobSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'job_details', 'saved_at']
        read_only_fields = ['user', 'saved_at']
