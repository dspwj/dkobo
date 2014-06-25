from rest_framework import viewsets
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from models import SurveyDraft, SurveyPreview
from serializers import ListSurveyDraftSerializer, DetailSurveyDraftSerializer
from django.shortcuts import render_to_response, HttpResponse, get_object_or_404


class SurveyAssetViewset(viewsets.ModelViewSet):
    model = SurveyDraft
    serializer_class = ListSurveyDraftSerializer
    exclude_asset_type = False

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous():
            raise PermissionDenied
        queryset = SurveyDraft.objects.filter(user=user)
        if self.exclude_asset_type:
            queryset = queryset.exclude(asset_type=None)
        else:
            queryset = queryset.filter(asset_type=None)
        return queryset.order_by('-date_modified')

    def create(self, request):
        user = self.request.user
        if user.is_anonymous():
            raise PermissionDenied
        contents = request.DATA
        survey_draft = request.user.survey_drafts.create(**contents)
        return Response(ListSurveyDraftSerializer(survey_draft).data)

    def retrieve(self, request, pk=None):
        user = request.user
        queryset = SurveyDraft.objects.filter(user=user)
        survey_draft = get_object_or_404(queryset, pk=pk)
        return Response(DetailSurveyDraftSerializer(survey_draft).data)

    @action(methods=['DELETE'])
    def delete_survey_draft(self, request, pk=None):
        draft = self.get_object()
        draft.delete()


class LibraryAssetViewset(SurveyAssetViewset):
    exclude_asset_type = True
    serializer_class = DetailSurveyDraftSerializer


class SurveyDraftViewSet(SurveyAssetViewset):
    exclude_asset_type = False
