from src.base.models import Employee, Camera, Violation, Frame
from rest_framework import serializers

class EmployeeSeializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['last_frame'] = FrameSerializer(instance=Frame.objects.filter(camera_id=data['id']).order_by('dttm').last()).data

        return data

class FrameSerializer(serializers.ModelSerializer):
    camera_code = serializers.CharField(required=False, write_only=True)
    camera_name = serializers.CharField(source='camera.name')
    class Meta:
        model = Frame
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('camera_code') and not attrs.get('camera_id'):
            code = attrs.get('camera_code')
            camera = Camera.objects.filter(code=code).first()
            if not camera:
                raise serializers.ValidationError(f'Camera with code {code} doesn\'t exist')
            attrs['camera_id'] = camera.id
        return attrs

class ViolationSerializer(serializers.ModelSerializer):
    employee = EmployeeSeializer()
    frame = FrameSerializer()
    class Meta:
        model = Violation
        fields = '__all__'

class ChartSerializer(serializers.Serializer):
    dt_from = serializers.DateField()
    dt_to = serializers.DateField()
