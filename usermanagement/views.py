import operator
from functools import reduce
from datetime import datetime

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models.query_utils import Q
from django.db.models import Count

from usermanagement.serializers import (UserProfileSerializer, InterviewSlotSerializer, 
                                        InterviewerSerializer, CandidateSerializer)
from usermanagement.CustomMessages import CustomMessages
from usermanagement.models import InterviewerProfile, CandidateProfile, InterviewSlot
from usermanagement.utils import convert_to_slots

msg_ob = CustomMessages()

class RegisterInterviewer(generics.CreateAPIView):
    """
    Creates the auth_user and Interviewer
    params:
        1.first_name 2.last_name 3.email 4.phone_number 5.password
    """
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_ob = serializer.save()
            InterviewerProfile.objects.create(user=user_ob, phone_number=request.data.get('phone_number'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCandidate(generics.CreateAPIView):
    """
    Creates the auth_user and Candidate
    params:
        1.first_name 2.last_name 3.email 4.phone_number 5.password
    """
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_ob = serializer.save()
            CandidateProfile.objects.create(user=user_ob, phone_number=request.data.get('phone_number'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Candidate or Interviewer login
    params - email or phone_number and password
    """

    def post(self, *args, **kwargs):
        try:
            username = self.request.data['username']
            password = self.request.data['password']
        except:
            return Response({'msg': msg_ob.invalid_parameters}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            try:
                user_ob = User.objects.get(username=username)
                user_auth = authenticate(username=username, password=password)
                if user_auth:
                    token, created = Token.objects.get_or_create(user=user_ob)
                    return Response({'token': token.key}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'msg': msg_ob.incorrect_pass_username}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'msg': msg_ob.something_went_wrong}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=username).exists():
            try:
                user_ob = User.objects.get(email=username)
                user_auth = authenticate(username=user_ob.username, password=password)
                if user_auth:
                    token, created = Token.objects.get_or_create(user=user_ob)
                    return Response({'token': token.key}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'msg': msg_ob.incorrect_pass_username}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'msg': msg_ob.something_went_wrong}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': msg_ob.login_failed}, status=status.HTTP_400_BAD_REQUEST)


class InterviewerList(generics.ListAPIView):
    """
    Interviewer List
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = InterviewerSerializer
    queryset = InterviewerProfile.objects.filter(is_active=True)


class CandidateList(generics.ListAPIView):
    """
    Candidate List
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CandidateSerializer
    queryset = CandidateProfile.objects.filter(is_active=True)


class CreateSlot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slot_list = request.data.get('slot')
        if InterviewerProfile.objects.filter(user=request.user).exists():
            try:
                user_obj = InterviewerProfile.objects.get(user=request.user)
            except:
                return Response({"msg":msg_ob.invalid_user}, status=status.HTTP_400_BAD_REQUEST)
            interviewer = user_obj.id
            candidate = None
        else:
            try:
                user_obj = CandidateProfile.objects.get(user=request.user)
            except:
                return Response({"msg":msg_ob.invalid_user}, status=status.HTTP_400_BAD_REQUEST)
            interviewer = None 
            candidate = user_obj.id
        request.data['interviewer'] = interviewer
        request.data['candidate'] = candidate
        for _ in slot_list:
            try:
                date_time_obj = datetime.strptime(_, '%Y-%m-%d %H:%M:%S.%f')
            except:
                return Response({'msg': msg_ob.invalid_date}, status=status.HTTP_400_BAD_REQUEST)
            if (interviewer and InterviewSlot.objects.filter(interviewer__id=interviewer, slot=date_time_obj, is_active=True).exists()) or (candidate and InterviewSlot.objects.filter(candidate__id=candidate, slot=date_time_obj, is_active=True).exists()):
                continue
            request.data['slot'] = _
            serializer = InterviewSlotSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class GetAvailability(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = InterviewSlotSerializer

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.GET.get('cid')
        interviewer_id = self.request.GET.get('iid')
        try:
            interviewer = InterviewerProfile.objects.get(id=interviewer_id)
        except:
            return Response({"response": msg_ob.invalid_interviewer}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidate = CandidateProfile.objects.get(id=candidate_id)
        except:
            return Response({"response": msg_ob.invalid_candidate}, status=status.HTTP_400_BAD_REQUEST)
        candidate_id = self.request.GET.get('cid')
        interviewer_id = self.request.GET.get('iid')
        filter_list = []
        filter_list.append(Q(interviewer=interviewer) | Q(candidate=candidate))
        query_set = InterviewSlot.objects.filter(reduce(operator.and_, filter_list)).values('slot').annotate(slot_count=Count('slot')).filter(slot_count__gt=1)
        response = convert_to_slots(query_set)
        return Response({"response": response}, status=status.HTTP_200_OK)