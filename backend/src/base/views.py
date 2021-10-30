from datetime import timedelta
from django.db.models import DateTimeField, Count, F, DateField
from django.db.models.functions import TruncHour, TruncDate
import pandas as pd
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_auth.views import UserDetailsView
from src.base.filters import ViolationFilterSet
from src.base.models import Employee, Camera, Violation, Frame
from src.base.serializers import ChartSerializer, EmployeeSeializer, CameraSerializer, UserSerializer, ViolationSerializer, FrameSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSeializer

    @action(detail=False, methods=['get'])
    def stats(self, request):

        return Response(
            {
                'count': Employee.objects.count(),
            }
        )


class CameraViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Camera.objects.all().select_related('work_shop')
    serializer_class = CameraSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):

        return Response(
            {
                'count': Camera.objects.count(),
            }
        )


class ViolationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Violation.objects.all().select_related('employee', 'frame__camera', 'frame__camera__work_shop').order_by('-frame__dttm')
    serializer_class = ViolationSerializer
    filterset_class = ViolationFilterSet

    @action(detail=False, methods=['get'])
    def chart(self, request):
        data = ChartSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        dt_from = data['dt_from']
        dt_to = data['dt_to']
        violations = Violation.objects.filter(frame__dttm__date__gte=dt_from, frame__dttm__date__lte=dt_to)
        count = violations.count()
        freq = '1d'
        if dt_from == dt_to:
            freq = '1h'
            violations = violations.annotate(
                dttm_g=TruncHour('frame__dttm', output_field=DateTimeField()),
            )
        else:
            violations = violations.annotate(
                dttm_g=TruncDate('frame__dttm', output_field=DateField()),
            )
        data = list(
            violations.values('dttm_g').annotate(
                y=Count('*'),
                x=F('dttm_g'),
            ).order_by('x').values(
                'y',
                'x',
            )
        )
        if dt_from == dt_to:
            dt_to += timedelta(1)
        dttms = pd.date_range(dt_from, dt_to, freq=freq)
        if freq == '1d':
            dttms = dttms.date
        df = pd.DataFrame(data=dttms, columns=['x'])
        df.set_index('x', inplace=True)

        df = df.merge(pd.DataFrame(data=data, columns=['x', 'y']).set_index('x'), how='left', on='x')

        data = df.reset_index().fillna(0).to_dict('records')

        return Response(
            {
                'count': count,
                'data': data,
            }
        )


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer


class UserView(UserDetailsView):
    serializer_class = UserSerializer
