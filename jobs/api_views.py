from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Job, Application, SavedJob
from .serializers import JobSerializer, ApplicationSerializer, SavedJobSerializer
from .recommender import get_recommendations_for_user, get_trending_skills

class JobListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        domain = request.GET.get('domain', '')
        location = request.GET.get('location', '')

        jobs = Job.objects.filter(is_active=True)

        if query:
            query = query.strip()
            jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(company_name__icontains=query) |
                Q(description__icontains=query) |
                Q(skills_required__icontains=query)
            )
        if domain:
            jobs = jobs.filter(domain__icontains=domain.strip())
        if location:
            jobs = jobs.filter(location__icontains=location.strip())

        jobs = jobs.order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class JobDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk, is_active=True)
        serializer = JobSerializer(job)
        return Response(serializer.data)


class JobSaveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Verify candidate privilege
        if not request.user.is_candidate:
            return Response({'error': 'Only candidates can save jobs.'}, status=status.HTTP_403_FORBIDDEN)

        job = get_object_or_404(Job, pk=pk, is_active=True)
        saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)

        if not created:
            # Already saved, so toggle: delete it (unsave)
            saved_job.delete()
            return Response({'saved': False, 'message': 'Job unsaved successfully.'}, status=status.HTTP_200_OK)

        return Response({'saved': True, 'message': 'Job saved successfully.'}, status=status.HTTP_201_CREATED)


class JobApplyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Verify candidate privilege
        if not request.user.is_candidate:
            return Response({'error': 'Only candidates can apply for jobs.'}, status=status.HTTP_403_FORBIDDEN)

        job = get_object_or_404(Job, pk=pk, is_active=True)
        cover_letter = request.data.get('cover_letter', '')

        # Check if already applied
        if Application.objects.filter(user=request.user, job=job).exists():
            return Response({'error': 'You have already applied for this job.'}, status=status.HTTP_400_BAD_REQUEST)

        application = Application.objects.create(
            user=request.user,
            job=job,
            cover_letter=cover_letter
        )
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecommendationsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_candidate:
            return Response({'error': 'Only candidates receive personalized recommendations.'}, status=status.HTTP_403_FORBIDDEN)

        recommended_jobs = get_recommendations_for_user(request.user)
        serializer = JobSerializer(recommended_jobs, many=True)
        return Response(serializer.data)


class TrendingSkillsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = get_trending_skills()
        return Response({'skills': skills})
