from rest_framework import generics
from .models import Topic, Comment
from .serializers import TopicSerializer, CommentSerializer

class TopicListAPI(generics.ListAPIView):
    queryset = Topic.objects.all().order_by('-created_at')
    serializer_class = TopicSerializer

class TopicDetailAPI(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'slug'

class CommentListAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Comment.objects.filter(topic__slug=slug, is_approved=True)
