from django.shortcuts import render
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

from api.pipeline_executor.pipeline_prepare import ConfigValidator

# Create your views here.
def home(request):
    cv = ConfigValidator()
    cv.download_files("test_sftp_src ==> test_sftp_dest")
    return render(request, 'api/index.html')

# class PipelinePrepare(APIView):

#     def get(self, request):
#         pass

#     def post(self, request):
